#!/usr/bin/env python3
"""Self-keyed witness: does my own primary-axis conclusion match my own flag?

The self-keyed gap: the certifier's own conclusion about the primary axis
("PASS CELL" -> robust, "FIRE CELL" -> flawed) is decoupled from the
instrument's verdict. If the cell's own name says the primary axis passes
but the verdict is flawed (or vice versa), the verdict is decoupled from its
own reasoning -- the self-keyed signature.

CLASSIFIER: read the primary-axis conclusion from the cell's NAME label
(PASS CELL / FIRE CELL / N/A / mirror / schema-boundary), NOT from the
free-form truth_reason prose. The prose is a long design explanation that
mentions sibling fire cells ("byte-identical to the fire cell except ...")
and negations ("so nothing fires"); a naive `fires` regex catches those and
inflates the count. The name is the cell's own primary-axis conclusion.

DECOMPOSITION: a name->PASS / verdict->flawed mismatch is NOT uniformly
self-keyed. It decomposes by mechanism:
  - REGIME-VS-AXIS: the verdict is a regime flag (NO-EMPIRICAL-CONTENT)
    inserted unconditionally (claim_audit.py:2703) for spec-type cells, but
    the name is an axis-level conclusion ("pass cell" / "N/A mirror"). The
    instrument's verdict is decoupled from the axis-level conclusion: the
    genuine self-keyed signature.
  - BASE-CELL: the name's "pass cell" describes the BASE flat-check cell
    (BEATS-NULL-PASS); the verdict is a scoped refinement (TEMPORAL-ONSET,
    OUTCOME-ONSET, ...) that "can only flag in the BEATS-NULL-PASS cell"
    (claim_audit.py:17). The instrument is correct; the name describes the
    base cell, not the refinement's conclusion.
  - CROSS-AXIS: the name is about one axis (FIDELITY silent); the verdict is
    a different axis (SCOPE-OF-INDEPENDENCE). The instrument is correct; the
    name names the wrong axis.

This is a witness test: it checks whether the certifier's own conclusion
matches the certifier's own verdict. It does NOT check whether the verdict is
correct (independent verification is the stranger's job).
"""
import json, re, sys
from collections import Counter

def load(path):
    return {r["id"]: r for r in json.load(open(path))}

def name_label(name):
    n = name.lower()
    if re.search(r"\bfire\b", n):
        return "FIRE"
    if re.search(r"pass cell|pass\b|n/a|schema-boundary|mirror", n):
        return "PASS"
    return "?"

REGIME = {"NO-EMPIRICAL-CONTENT"}
SCOPED = {"TEMPORAL-ONSET","OUTCOME-ONSET","SUBGROUP-ONSET","DOSE-ONSET",
          "TIER-ONSET","SPLIT-ONSET","METRIC-ONSET","DOSE-RESPONSE",
          "TEMPORAL-SPIKE","OUTCOME-SPIKE","SUBGROUP-SPIKE","DOSE-SPIKE",
          "TIER-SPIKE","SPLIT-SPIKE","METRIC-SPIKE"}

def classify_mismatch(name, verdict):
    """Classify a name->PASS / verdict->flawed mismatch by mechanism."""
    v = verdict.split(",")[0].strip()
    if v in REGIME:
        return "REGIME-VS-AXIS"
    if v in SCOPED:
        return "BASE-CELL"
    return "CROSS-AXIS"

def main():
    truth = load(sys.argv[1] if len(sys.argv) > 1 else "gt_rederivation/truth_2026-10-03.json")
    # The verdict is instrument-derived; re-derive it from the raw facts.
    sys.path.insert(0, ".")
    import claim_audit as CA
    raw = load(sys.argv[2] if len(sys.argv) > 2 else "gt_rederivation/raw_2026-10-03.json")

    c = Counter()
    mismatches = []
    for cid in sorted(truth):
        r = truth[cid]
        L = name_label(r.get("name", ""))
        verdict = CA.audit(raw[cid])["verdict"]
        flawed = verdict != "DISCRIMINATES"
        c[(L, flawed)] += 1
        if L == "PASS" and flawed:
            mech = classify_mismatch(r.get("name",""), verdict)
            mismatches.append((cid, mech, verdict.split(",")[0].strip(), r.get("name","")))
        elif L == "FIRE" and not flawed:
            mismatches.append((cid, "FIRE->robust", verdict, r.get("name","")))

    labeled = sum(n for (L, _), n in c.items() if L != "?")
    print(f"Self-keyed witness (name-label + mechanism): {len(mismatches)}/{labeled} labeled cells mismatch")
    for (L, fl), n in sorted(c.items()):
        print(f"  {L:5s} flawed={str(fl):5s} {n}")
    print(f"  (real-paper cells with no constructed label: {c[('?', True)] + c[('?', False)]})")
    print("\nMismatches by mechanism:")
    mc = Counter(m for _, m, _, _ in mismatches)
    for m, n in mc.most_common():
        print(f"  {m:16s} {n}")
    for cid, mech, v, name in mismatches:
        print(f"  [{cid:3d}] {mech:16s} {v:24s} {name[:44]}")

if __name__ == "__main__":
    main()
