#!/usr/bin/env python3
"""The fix's own confound: a baseline-dependent false-negative.

calibration_bandaid.py showed the fix (diff post-blind failures against
baseline failures) fixes the naive rule's false-positive on a RED baseline:
a dead check reads UNCALIBRATED, not CALIBRATED. It left open whether the fix
has its OWN confound.

This probe shows it does. ARM 4 constructs a RED baseline where a check C that
IS calibrated on the GREEN baseline (blinding it causes its single witness W
to newly fail) reads UNCALIBRATED under the fix, because W is already failing
for an unrelated reason (its truth is corrupted), so blinding C causes no NEW
failure.

The fix trades the naive rule's false-positive (dead check on RED) for a
baseline-dependent false-negative (calibrated check on RED with a masked
witness). Both rules are only correct on a GREEN baseline; the GREEN-baseline
precondition is load-bearing for both. The self-keyed gap is relocated
(false-positive -> false-negative), not closed.

Arms:
  ARM 1 (GREEN, synthetic dead check):
        naive UNCALIBRATED (correct), fix UNCALIBRATED (correct)
  ARM 2 (RED, synthetic dead check):
        naive CALIBRATED (false-positive), fix UNCALIBRATED (correct)
  ARM 3 (GREEN, real single-witness check):
        naive CALIBRATED (correct), fix CALIBRATED (correct)  [control]
  ARM 4 (RED, real single-witness check, witness masked):
        naive CALIBRATED (correct, wrong reason), fix UNCALIBRATED (FALSE-NEGATIVE)
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
        return True, "", "BLIND (fix-confound probe: %s forced pass)" % name
    CHECKS[idx] = (name, blind)
    def restore():
        CHECKS[idx] = (name, fn)
    return restore

def classify_naive(idx):
    restore = blind_check(idx)
    try:
        fails = [nm for nm, ok in run_battery() if not ok]
    finally:
        restore()
    return ("CALIBRATED" if fails else "UNCALIBRATED"), fails

def classify_fix(idx):
    base = set(baseline_fails())
    restore = blind_check(idx)
    try:
        fails = [nm for nm, ok in run_battery() if not ok]
    finally:
        restore()
    new = [nm for nm in fails if nm not in base]
    return ("CALIBRATED" if new else "UNCALIBRATED"), new

def add_dead_check():
    name = "DEAD-CHECK"
    def dead(spec):
        return True, "", "DEAD (never fires)"
    CHECKS.append((name, dead))
    return len(CHECKS) - 1

def find_single_witness():
    """A real check that fires on exactly one empirical specimen whose truth is
    exactly that check's flag (clean single-witness mechanics)."""
    for i, (name, fn) in enumerate(CHECKS):
        witnesses = []
        for s in SPECS:
            a = claim_audit.audit(s)
            if not a["checks"].get(name, {}).get("pass", True):
                witnesses.append(s)
        if len(witnesses) != 1:
            continue
        w = witnesses[0]
        # empirical (not NO-EMPIRICAL) and truth is exactly the single flag
        if "NO-EMPIRICAL-CONTENT" in w["truth"]:
            continue
        if len(w["truth"]) != 1:
            continue
        if w["truth"][0] != name:
            continue
        return i, w
    return None, None

def main():
    print("=== baseline (GREEN expected) ===")
    bf = baseline_fails()
    print("baseline: %d/%d match (%s)" % (len(SPECS)-len(bf), len(SPECS),
          "GREEN" if not bf else "RED"))
    assert not bf, "expected a GREEN baseline"

    di = add_dead_check()
    ci, cw = find_single_witness()
    print("synthetic dead check: %s (idx %s)" % (CHECKS[di][0], di))
    print("real single-witness check: %s (idx %s), witness: %s"
          % (CHECKS[ci][0], ci, cw["name"]))
    assert ci is not None, "no clean single-witness check found"

    # ARM 1: GREEN, dead check
    print()
    print("=== ARM 1: GREEN baseline, synthetic dead check ===")
    n1, _ = classify_naive(di)
    f1, _ = classify_fix(di)
    print("naive: %s (correct)" % n1)
    print("fix:   %s (correct)" % f1)
    assert n1 == "UNCALIBRATED" and f1 == "UNCALIBRATED"

    # ARM 2: RED, dead check (corrupt a robust specimen)
    print()
    print("=== ARM 2: RED baseline, synthetic dead check ===")
    victim = next(s for s in SPECS if not s["truth"])
    backup = victim["truth"]
    victim["truth"] = ["GHOST-FLAG"]
    assert baseline_fails() == [victim["name"]], "RED baseline should be exactly the victim"
    n2, _ = classify_naive(di)
    f2, _ = classify_fix(di)
    print("naive: %s (false-positive: the pre-existing red is attributed to the blind)" % n2)
    print("fix:   %s (correct: the pre-existing red is not attributed to the blind)" % f2)
    assert n2 == "CALIBRATED" and f2 == "UNCALIBRATED"
    victim["truth"] = backup

    # ARM 3: GREEN, real single-witness check (control: it IS calibrated)
    print()
    print("=== ARM 3: GREEN baseline, real single-witness check (control) ===")
    n3, nf3 = classify_naive(ci)
    f3, nf3b = classify_fix(ci)
    print("naive: %s (correct)" % n3)
    print("fix:   %s (correct)" % f3)
    assert n3 == "CALIBRATED" and f3 == "CALIBRATED"
    assert nf3 == [cw["name"]] and nf3b == [cw["name"]], "witness should be the only failure"

    # ARM 4: RED, real single-witness check, witness masked
    print()
    print("=== ARM 4: RED baseline, real single-witness check (witness masked) ===")
    cw_backup = cw["truth"]
    cw["truth"] = ["GHOST-FLAG"]
    assert baseline_fails() == [cw["name"]], "RED baseline should be exactly the witness"
    n4, nf4 = classify_naive(ci)
    f4, nf4b = classify_fix(ci)
    print("naive: %s (correct, wrong reason: the witness is red; fails=%s)" % (n4, nf4))
    print("fix:   %s (FALSE-NEGATIVE: new_fails=%s; the check is calibrated, but its witness is masked)" % (f4, nf4b))
    cw["truth"] = cw_backup  # restore the witness's real single-flag truth
    assert n4 == "CALIBRATED" and f4 == "UNCALIBRATED"

    # sanity: baseline restored to GREEN
    assert not baseline_fails(), "baseline should be GREEN after the arms"

    print()
    print("=== RESULT ===")
    print("The fix (diff post-blind vs baseline failures):")
    print("  fixes the naive's false-positive (ARM 2: dead check reads UNCALIBRATED)")
    print("  but is baseline-dependent (ARM 4: a check calibrated on the GREEN")
    print("  baseline reads UNCALIBRATED on a RED baseline when its only witness")
    print("  is already failing for an unrelated reason -> false-negative)")
    print("Both rules are only correct on a GREEN baseline. The fix relocates the")
    print("confound (false-positive -> baseline-dependent false-negative); it does")
    print("not remove the GREEN-baseline precondition. The self-keyed gap is")
    print("relocated, not closed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
