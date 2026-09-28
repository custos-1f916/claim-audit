#!/usr/bin/env python3
"""Co-firing / redundancy analysis across the claim-audit axes (refined)."""
import json
from collections import defaultdict
import claim_audit
import specimens

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
