#!/usr/bin/env python3
"""The fix's false-negative is witness-local, not baseline-dependent.

calibration_fix_confound.py (ARM 4) showed the fix (diff post-blind vs
baseline failures) reads a calibrated single-witness check UNCALIBRATED on a
RED baseline when its only witness is already failing for an unrelated reason.
It labeled the false-negative "baseline-dependent."

This probe sharpens the label. The false-negative is not caused by the baseline
being RED per se; it is caused by the RED being on the check's own witness. Two
RED baselines that the "baseline-dependent" label treats identically are handled
differently by the fix:

  ARM 4 (reproduce fix-confound): RED baseline, the red IS the check's witness.
        Blinding C causes no NEW failure (the witness was already failing).
        fix: UNCALIBRATED  -> FALSE-NEGATIVE.
  ARM 5 (new): RED baseline, the red is an UNRELATED green specimen; the check's
        witness stays GREEN.
        Blinding C makes the green witness NEWLY fail.
        fix: CALIBRATED    -> CORRECT.

The contrast is the result: the fix is correct on a RED baseline whenever the
check's witness is green, and fails only when the witness itself is the red.
The false-negative is witness-local (a single-witness check whose sole witness
is the red), not baseline-dependent (any red baseline). A multi-witness check is
immune: even if one witness is red, a green witness still newly fails under the
blind, so the fix reads it CALIBRATED.

Deterministic; the battery is GREEN (124/124) before and after each arm's
mutation/restore cycle.
"""
import claim_audit
import calibration

CHECKS = claim_audit.CHECKS
SPECS = calibration.SPECIMENS

def run_battery():
    out = []
    for s in SPECS:
        a = claim_audit.audit(s)
        out.append((s["name"], set(a["flags"]) == set(s["truth"])))
    return out

def baseline_fails():
    return [nm for nm, ok in run_battery() if not ok]

def blind_check(idx):
    name, fn = CHECKS[idx]
    def blind(spec):
        return True, "", "BLIND (witness-local probe: %s forced pass)" % name
    CHECKS[idx] = (name, blind)
    def restore():
        CHECKS[idx] = (name, fn)
    return restore

def classify_fix(idx):
    base = set(baseline_fails())
    restore = blind_check(idx)
    try:
        fails = [nm for nm, ok in run_battery() if not ok]
    finally:
        restore()
    new = [nm for nm in fails if nm not in base]
    return ("CALIBRATED" if new else "UNCALIBRATED"), new

def find_single_witness():
    for i, (name, fn) in enumerate(CHECKS):
        witnesses = []
        for s in SPECS:
            a = claim_audit.audit(s)
            if not a["checks"].get(name, {}).get("pass", True):
                witnesses.append(s)
        if len(witnesses) != 1:
            continue
        w = witnesses[0]
        if "NO-EMPIRICAL-CONTENT" in w["truth"]:
            continue
        if len(w["truth"]) != 1:
            continue
        if w["truth"][0] != name:
            continue
        return i, w
    return None, None

def find_unrelated_green():
    """A green specimen (truth == [], audit flags == []) — automatically distinct
    from the witness, whose truth is a single flag, not []."""
    for s in SPECS:
        if s["truth"] != []:
            continue
        if set(claim_audit.audit(s)["flags"]) != set(s["truth"]):
            continue
        return s
    return None

def main():
    print("=== baseline (GREEN expected) ===")
    bf = baseline_fails()
    print("baseline: %d/%d match (%s)" % (len(SPECS)-len(bf), len(SPECS),
          "GREEN" if not bf else "RED"))
    assert not bf, "expected a GREEN baseline"

    ci, cw = find_single_witness()
    assert ci is not None, "no clean single-witness check found"
    victim = find_unrelated_green()
    assert victim is not None and victim["name"] != cw["name"], \
        "need an unrelated green victim distinct from the witness"
    print("single-witness check: %s (idx %d), witness: %s" % (CHECKS[ci][0], ci, cw["name"]))
    print("unrelated green victim: %s" % victim["name"])

    # ARM 4 (reproduce): RED baseline, red = the witness
    print()
    print("=== ARM 4: RED baseline, red IS the witness (reproduce fix-confound) ===")
    cw_backup = cw["truth"]
    cw["truth"] = ["GHOST-FLAG"]
    assert baseline_fails() == [cw["name"]], "RED baseline should be exactly the witness"
    f4, nf4 = classify_fix(ci)
    cw["truth"] = cw_backup
    print("fix: %s (FALSE-NEGATIVE: new_fails=%s; the witness is the red, so the blind causes no new failure)" % (f4, nf4))
    assert f4 == "UNCALIBRATED" and nf4 == []

    # ARM 5 (new): RED baseline, red = unrelated green victim, witness stays green
    print()
    print("=== ARM 5: RED baseline, red is UNRELATED (witness stays GREEN) ===")
    v_backup = victim["truth"]
    victim["truth"] = ["GHOST-FLAG"]
    assert baseline_fails() == [victim["name"]], "RED baseline should be exactly the unrelated victim"
    f5, nf5 = classify_fix(ci)
    victim["truth"] = v_backup
    print("fix: %s (CORRECT: new_fails=%s; the green witness newly fails under the blind)" % (f5, nf5))
    assert f5 == "CALIBRATED" and nf5 == [cw["name"]]

    # sanity: baseline restored to GREEN
    assert not baseline_fails(), "baseline should be GREEN after the arms"

    print()
    print("=== RESULT ===")
    print("The fix's false-negative is WITNESS-LOCAL, not baseline-dependent:")
    print("  ARM 4 (red = the witness):  fix reads UNCALIBRATED (false-negative)")
    print("  ARM 5 (red = unrelated):    fix reads CALIBRATED (correct)")
    print("The fix is correct on a RED baseline whenever the check's witness is")
    print("green; it fails only when the witness itself is the red. The label")
    print('"baseline-dependent false-negative" (fix-confound) is too coarse: the')
    print("false-negative requires a single-witness check whose sole witness is")
    print("the red. A multi-witness check is immune (a green witness still newly")
    print("fails under the blind). The GREEN-baseline precondition is load-bearing")
    print("for the NAIVE rule; for the FIX it is the witness's greenness that")
    print("matters, not the baseline's.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
