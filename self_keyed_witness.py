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

LEVEL: the instrument's verdict carries a first-class `level` field
(claim_audit.py, audit()). A REGIME verdict (NO-EMPIRICAL-CONTENT) is a
different KIND of verdict from an AXIS verdict: it says the empirical axes
do not apply to this spec-type cell, not that a specific axis fires or
passes. Comparing an axis-level name (PASS/FIRE) against a REGIME-level
verdict is therefore a LEVEL mismatch, not an axis-level disagreement. The
witness reads `level` directly instead of string-parsing the verdict --
the string parse was the last self-keyed artifact in the witness (a regex
catching 'fires' in its own sibling-cell prose).

DECOMPOSITION: a name->PASS / verdict->flawed mismatch decomposes by
mechanism:
  - REGIME-VS-AXIS (level == REGIME): the verdict is a regime flag, the name
    is an axis-level conclusion. Different levels. The genuine self-keyed
    signature -- precisely located, one direction (name->PASS), zero reverse.
  - BASE-CELL (level == AXIS, scoped refinement fired): the name's "pass
    cell" describes the BASE flat-check cell (BEATS-NULL-PASS); the verdict
    is a scoped refinement (TEMPORAL-ONSET, OUTCOME-ONSET, ...) that "can
    only flag in the BEATS-NULL-PASS cell". Same level; the instrument is
    correct; the name describes the base cell, not the refinement's
    conclusion.
  - CROSS-AXIS (level == AXIS, non-scoped flag): the name is about one axis
    (FIDELITY silent); the verdict is a different axis. Same level; the
    instrument is correct; the name names the wrong axis.

REGIME COUNTERFACTUAL: the REGIME-VS-AXIS signature is now TYPED. For every
REGIME-level cell, strip the NO-EMPIRICAL-CONTENT flag and re-derive the
verdict. If the counterfactual is clean (no other flag), the regime was the
SOLE cause of "flawed" -- the unconditional regime flag alone made a
self-constructed PASS cell read as flawed; that is the self-keying. If a
genuine axis co-fires (the counterfactual still flags), the regime is
GENUINE: it is not the sole cause, an independent axis fired on its own.
Cell 98 (OPT-IN-CENSUS) is the control: REGIME-level, CO-FIRED, name=FIRE --
it is not even a mismatch, which is what a genuine regime looks like.

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

SCOPED = {"TEMPORAL-ONSET","OUTCOME-ONSET","SUBGROUP-ONSET","DOSE-ONSET",
          "TIER-ONSET","SPLIT-ONSET","METRIC-ONSET","DOSE-RESPONSE",
          "TEMPORAL-SPIKE","OUTCOME-SPIKE","SUBGROUP-SPIKE","DOSE-SPIKE",
          "TIER-SPIKE","SPLIT-SPIKE","METRIC-SPIKE"}

def classify_mismatch(name, verdict, level):
    """Classify a name->PASS / verdict->flawed mismatch by mechanism.

    LEVEL is read from the instrument's first-class field, not string-parsed.
    """
    if level == "REGIME":
        return "REGIME-VS-AXIS"
    v = verdict.split(",")[0].strip()
    if v in SCOPED:
        return "BASE-CELL"
    return "CROSS-AXIS"

def regime_counterfactual(a):
    """Strip the NO-EMPIRICAL-CONTENT flag and re-derive the verdict.

    Returns (cf_flags, cf_verdict, sole_cause). sole_cause is True when the
    regime was the ONLY flag -- i.e. removing it makes the verdict clean.
    That is the self-keyed signature: the unconditional regime flag alone
    made the cell read as flawed. False means a genuine axis co-fired, so
    the regime is not the sole cause and is genuine.
    """
    cf_flags = [f for f in a["flags"] if f != "NO-EMPIRICAL-CONTENT"]
    cf_verdict = "DISCRIMINATES" if not cf_flags else ", ".join(cf_flags)
    return cf_flags, cf_verdict, (not cf_flags)

def main():
    truth = load(sys.argv[1] if len(sys.argv) > 1 else "gt_rederivation/truth_2026-10-03.json")
    # The verdict is instrument-derived; re-derive it from the raw facts.
    sys.path.insert(0, ".")
    import claim_audit as CA
    raw = load(sys.argv[2] if len(sys.argv) > 2 else "gt_rederivation/raw_2026-10-03.json")

    c = Counter()
    mismatches = []
    regime_cells = []
    for cid in sorted(truth):
        r = truth[cid]
        L = name_label(r.get("name", ""))
        a = CA.audit(raw[cid])
        verdict = a["verdict"]
        level = a["level"]
        flawed = verdict != "DISCRIMINATES"
        c[(L, flawed)] += 1
        if L == "PASS" and flawed:
            mech = classify_mismatch(r.get("name",""), verdict, level)
            mismatches.append((cid, mech, level, verdict.split(",")[0].strip(), r.get("name","")))
        elif L == "FIRE" and not flawed:
            mismatches.append((cid, "FIRE->robust", level, verdict, r.get("name","")))
        if level == "REGIME":
            cf_flags, cf_verdict, sole = regime_counterfactual(a)
            regime_cells.append((cid, sole, cf_flags, L, r.get("name","")))

    labeled = sum(n for (L, _), n in c.items() if L != "?")
    print(f"Self-keyed witness (name-label + level + mechanism): {len(mismatches)}/{labeled} labeled cells mismatch")
    for (L, fl), n in sorted(c.items()):
        print(f"  {L:5s} flawed={str(fl):5s} {n}")
    print(f"  (real-paper cells with no constructed label: {c[('?', True)] + c[('?', False)]})")
    print("\nMismatches by mechanism:")
    mc = Counter(m for _, m, _, _, _ in mismatches)
    for m, n in mc.most_common():
        print(f"  {m:16s} {n}")
    axis_level = sum(n for m, n in mc.items() if m != "REGIME-VS-AXIS")
    regime_level = mc.get("REGIME-VS-AXIS", 0)
    print(f"\n  axis-level disagreements (BASE-CELL + CROSS-AXIS + FIRE->robust): {axis_level}")
    print(f"  level mismatches (axis-name vs REGIME-verdict, the self-keyed signature): {regime_level}")
    print("\nCells:")
    for cid, mech, level, v, name in mismatches:
        print(f"  [{cid:3d}] {mech:16s} level={level:6s} {v:24s} {name[:40]}")

    # REGIME COUNTERFACTUAL: type the REGIME-VS-AXIS signature. For every
    # REGIME-level cell, strip the NO-EMPIRICAL-CONTENT flag and ask whether
    # the verdict is still flawed. SOLE-CAUSE -> the regime alone made it
    # flawed (the self-keyed signature). CO-FIRED -> a genuine axis fired
    # too (the regime is genuine, not the sole cause).
    print("\nRegime counterfactual (strip NO-EMPIRICAL-CONTENT; is it still flawed?):")
    sole = [x for x in regime_cells if x[1]]
    cofired = [x for x in regime_cells if not x[1]]
    for cid, s, cf, L, name in regime_cells:
        tag = "SOLE-CAUSE (self-keyed)" if s else "CO-FIRED (genuine)"
        print(f"  [{cid:3d}] {tag:26s} cf_flags={cf!r:24s} name={L:4s} {name[:40]}")
    print(f"\n  SOLE-CAUSE (regime alone made a cell flawed; the self-keyed signature): {len(sole)}")
    for cid, s, cf, L, name in sole:
        print(f"    [{cid:3d}] {name[:55]}")
    print(f"  CO-FIRED (a genuine axis fired; the regime is genuine): {len(cofired)}")
    for cid, s, cf, L, name in cofired:
        print(f"    [{cid:3d}] {cf!r:24s} {name[:45]}")

if __name__ == "__main__":
    main()
