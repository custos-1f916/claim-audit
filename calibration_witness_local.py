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
  ARM 6 (new): RED baseline on a MULTI-witness check, ONE witness is the red,
        the other stays GREEN.
        Blinding C makes the green witness NEWLY fail.
        fix: CALIBRATED    -> CORRECT (a green witness still exists).
  ARM 7 (new): RED baseline on a MULTI-witness check, ALL witnesses are the red.
        Blinding C causes no NEW failure (every witness was already failing).
        fix: UNCALIBRATED  -> FALSE-NEGATIVE (multi-witness is NOT immune).

The contrast is the result: the fix reads a check CALIBRATED iff blinding it
causes at least one NEW failure, which happens iff at least one of the check's
witnesses is GREEN on the baseline. It false-negatives iff ALL of the check's
witnesses are red. The condition is witness-count-agnostic: "single-witness"
was a conflation. A multi-witness check is immune only while a green witness
exists; all-witnesses-red multi-witness (ARM 7) reads UNCALIBRATED, so the
blanket "multi-witness is immune" claim is refuted.

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

def find_multi_witness():
    """A check with exactly TWO green witnesses (check fires AND the specimen is
    green, flags == truth). Green witnesses are the only ones that can newly fail
    under the blind, so this is the clean multi-witness case for ARM 6/7."""
    for i, (name, fn) in enumerate(CHECKS):
        witnesses = []
        for s in SPECS:
            a = claim_audit.audit(s)
            if a["checks"].get(name, {}).get("pass", True):
                continue
            if set(a["flags"]) != set(s["truth"]):
                continue
            witnesses.append(s)
        if len(witnesses) == 2:
            return i, name, witnesses
    return None, None, None

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

    # ARM 6 + ARM 7: multi-witness check, one witness red vs all witnesses red
    mi, mname, mw = find_multi_witness()
    assert mi is not None, "no clean multi-witness check found"
    m0, m1 = mw[0], mw[1]
    print()
    print("=== ARM 6: RED baseline on %s (multi-witness), ONE witness red ===" % mname)
    m0_backup = m0["truth"]
    m0["truth"] = ["GHOST-FLAG"]
    assert baseline_fails() == [m0["name"]], "RED baseline should be exactly the one witness"
    f6, nf6 = classify_fix(mi)
    m0["truth"] = m0_backup
    print("fix: %s (CORRECT: new_fails=%s; the other witness stays green and newly fails)" % (f6, nf6))
    assert f6 == "CALIBRATED" and nf6 == [m1["name"]]

    print()
    print("=== ARM 7: RED baseline on %s (multi-witness), ALL witnesses red ===" % mname)
    m0_backup, m1_backup = m0["truth"], m1["truth"]
    m0["truth"] = ["GHOST-FLAG"]
    m1["truth"] = ["GHOST-FLAG"]
    assert sorted(baseline_fails()) == sorted([m0["name"], m1["name"]]), \
        "RED baseline should be exactly both witnesses"
    f7, nf7 = classify_fix(mi)
    m0["truth"] = m0_backup
    m1["truth"] = m1_backup
    print("fix: %s (FALSE-NEGATIVE: new_fails=%s; every witness was already failing)" % (f7, nf7))
    assert f7 == "UNCALIBRATED" and nf7 == []

    # sanity: baseline restored to GREEN
    assert not baseline_fails(), "baseline should be GREEN after the arms"

    print()
    print("=== RESULT ===")
    print("The fix's false-negative is ALL-WITNESSES-RED, not baseline- or")
    print("witness-count-dependent:")
    print("  ARM 4 (single witness, red):            UNCALIBRATED (false-negative)")
    print("  ARM 5 (single witness, green):          CALIBRATED (correct)")
    print("  ARM 6 (multi witness, one red):         CALIBRATED (correct)")
    print("  ARM 7 (multi witness, all red):         UNCALIBRATED (false-negative)")
    print("The fix reads a check CALIBRATED iff blinding it causes a NEW failure,")
    print("which happens iff at least one witness is GREEN on the baseline; it")
    print("false-negatives iff ALL witnesses are red. The condition is")
    print("witness-count-agnostic: 'single-witness' was a conflation, and the")
    print("blanket 'multi-witness is immune' claim is refuted by ARM 7. The")
    print("GREEN-baseline precondition is load-bearing for the NAIVE rule; for the")
    print("FIX it is the greenness of at least one witness that matters.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
