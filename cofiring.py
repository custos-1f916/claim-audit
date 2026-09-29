#!/usr/bin/env python3
"""Co-firing / redundancy analysis across the claim-audit axes (refined).

Run as `python3 cofiring.py` to recompute and rewrite cofiring.json.
Run as `python3 cofiring.py --check` to verify the committed cofiring.json is
not stale (it matches a fresh recompute) without rewriting it: exit 0 fresh,
exit 1 stale, exit 2 missing. This makes the COHERENCE.md claim "re-derived
from the actual cofiring output" machine-checkable rather than asserted."""
import json
from collections import defaultdict
import claim_audit
import specimens
import sys


specs = specimens.SPECIMENS
N = len(specs)
print("battery size: %d specimens" % N)

fired = []
for s in specs:
    fired.append(set(claim_audit.audit(s)["flags"]))

check2flag = {}
for name, fn in claim_audit.CHECKS:
    flag = None
    for s in specs:
        try:
            ok, fl, _ = fn(s)
        except Exception:
            continue
        if not ok:
            flag = fl
            break
    check2flag[name] = flag

fired_flags = set()
for fl in fired:
    fired_flags |= fl
truly_never = [n for n, _ in claim_audit.CHECKS if check2flag[n] is None]
print("\n=== checks whose flag NEVER fires on the battery (weight-0 on this data) ===")
for n in truly_never:
    print("  %s" % n)

axis_specs = defaultdict(set)
for i, fl in enumerate(fired):
    for ax in fl:
        axis_specs[ax].add(i)

print("\n=== per-flag firing counts (fired on N of %d) ===" % N)
for ax, s in sorted(axis_specs.items(), key=lambda kv: (-len(kv[1]), kv[0])):
    print("    %3d  %s" % (len(s), ax))

by_set = defaultdict(set)
for ax, s in axis_specs.items():
    by_set[frozenset(s)].add(ax)
print("\n=== IDENTICAL firing sets (pure redundancy) ===")
found = False
for s, axes in by_set.items():
    if len(axes) > 1:
        found = True
        print("  %s  (on %d specimens)" % (sorted(axes), len(s)))
if not found:
    print("  (none)")

names = sorted(axis_specs.keys())
subs = []
for i, a in enumerate(names):
    for b in names[i+1:]:
        sa, sb = axis_specs[a], axis_specs[b]
        if sa and sb and sa < sb:
            subs.append((a, b, len(sa), len(sb)))
        elif sa and sb and sb < sa:
            subs.append((b, a, len(sb), len(sa)))
if "--check" in sys.argv[1:]:
    # Staleness guard: does the committed cofiring.json match a fresh recompute?
    # This is what makes the COHERENCE.md "re-derived from the actual cofiring
    # output" claim machine-checkable: a stranger runs this, not the prose.
    import os
    if not os.path.exists("cofiring.json"):
        print("cofiring.json missing (run `python3 cofiring.py` to generate it)")
        sys.exit(2)
    committed = json.load(open("cofiring.json"))
    stale = []
    if committed.get("battery") != N:
        stale.append("battery: committed %s != fresh %d" % (committed.get("battery"), N))
    c_counts = committed.get("counts", {})
    for ax in sorted(set(c_counts) | set(axis_specs)):
        c = c_counts.get(ax, 0)
        f = len(axis_specs.get(ax, set()))
        if c != f:
            stale.append("count %s: committed %d != fresh %d" % (ax, c, f))
    c_subs = committed.get("subsets")
    # JSON round-trips tuples as lists; normalize both sides before comparing.
    norm = lambda x: sorted(tuple(t) for t in (x or []))
    if norm(c_subs) != norm(subs):
        stale.append("strict-subset structure: committed %d pairs != fresh %d" % (
            len(c_subs) if c_subs is not None else -1, len(subs)))
    if stale:
        print("cofiring.json is STALE (committed file does not match a fresh recompute):")
        for s in stale:
            print("  - " + s)
        print("run `python3 cofiring.py` to regenerate, then re-run --check")
        sys.exit(1)
    print("cofiring.json is FRESH (matches a fresh recompute: battery %d, %d flags, %d subset pairs)" % (
        N, len(axis_specs), len(subs)))
    sys.exit(0)

print("\n=== STRICT-SUBSET firing sets (refinement candidates) ===")
if not subs:
    print("  (none)")
for small, big, ns, nb in subs:
    print("  %s  <  %s   (%d < %d specimens)" % (small, big, ns, nb))

cf2, cf1 = [], []
for i, a in enumerate(names):
    for b in names[i+1:]:
        sa, sb = axis_specs[a], axis_specs[b]
        inter = sa & sb
        if len(inter) >= 2:
            cf2.append((len(inter), a, b))
        elif len(inter) == 1:
            cf1.append((a, b, sorted(inter)[0]))
cf2.sort(reverse=True)
print("\n=== CO-FIRING pairs ===")
print("  overlap >= 2: %d pairs" % len(cf2))
for n, a, b in cf2:
    print("    %d  %s & %s" % (n, a, b))
print("  overlap == 1 (single-specimen): %d pairs" % len(cf1))
for a, b, idx in cf1:
    print("    %s & %s  (specimen %d: %s)" % (a, b, idx, specs[idx]["name"]))

print("\n=== per-axis exclusivity (fires where NO other axis fires) ===")
# Stale-proof replacement for the hand-maintained "newest axes" list:
# derived from the full firing sets, so a new axis needs no edit here.
# An axis with >= 1 exclusive specimen contributes a flag no other axis
# produces there; it is not a re-label of another axis's firing.
exclusive = {}
for ax in names:
    s = axis_specs.get(ax, set())
    ex = sorted(i for i in s if all(i not in axis_specs.get(o, set()) for o in names if o != ax))
    exclusive[ax] = ex
    print("  %s: fires %d, exclusive %d%s" % (
        ax, len(s), len(ex),
        (" [%s]" % ", ".join(specs[i]["name"] for i in ex)) if ex else ""))

out = {
    "battery": N,
    "check2flag": check2flag,
    "truly_never": truly_never,
    "counts": {ax: len(s) for ax, s in axis_specs.items()},
    "firing_sets": {ax: sorted(s) for ax, s in axis_specs.items()},
    "identical": {str(sorted(v)): sorted(v) for k, v in by_set.items() if len(v) > 1},
    "exclusive": exclusive,
    "subsets": subs,
    "cofire_ge2": cf2,
    "cofire_eq1": cf1,
}
with open("cofiring.json", "w") as f:
    json.dump(out, f, indent=2, sort_keys=True)
print("\nwrote cofiring.json")
