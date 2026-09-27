#!/usr/bin/env python3
"""Demonstrate that the baseline-integrity fix is a band-aid, not a removal.

calibration_confound.py showed the RED-baseline confound: a dead check reads
CALIBRATED on a RED baseline. The fix is to diff post-blind failures against
baseline failures, so a pre-existing failure is not attributed to the blind.

This script shows the fix is a band-aid on the GREEN-baseline precondition,
not a removal of it:

  1. On a RED baseline, the fix correctly classifies the dead check as
     UNCALIBRATED (it catches the pre-existing failure).

  2. But the fix is a meta-check (it operates on the battery, not on
     specimens), so it is not calibrated by the battery. The fix's own
     correctness is only certified by the author (who wrote the fix),
     not by the battery.

The fix relocates the self-keyed gap one level up: the fix's own correctness
is only certified by a GREEN baseline, which is the same precondition the fix
was supposed to remove.
"""
import claim_audit
import calibration

CHECKS = claim_audit.CHECKS
SPECS = calibration.SPECIMENS

DEAD_NAME = "DEAD-CHECK"
def dead_check(spec):
    return True, "", "DEAD (never fires)"
DEAD = (DEAD_NAME, dead_check)

def run_battery():
    out = []
    for s in SPECS:
        a = claim_audit.audit(s)
        out.append((s["name"], set(a["flags"]) == set(s["truth"])))
    return out

def classify_dead_check_naive():
    """The naive probe: blind the dead check, does the battery stay green?"""
    CHECKS.append(DEAD)
    try:
        idx = len(CHECKS) - 1
        orig = CHECKS[idx]
        def blind(spec, _n=DEAD_NAME):
            return True, "", "BLIND (dead check forced pass)"
        CHECKS[idx] = (DEAD_NAME, blind)
        res = run_battery()
        fails = [nm for nm, ok in res if not ok]
        return fails
    finally:
        CHECKS.pop()

def classify_dead_check_fix():
    """The fix: diff post-blind failures against baseline failures."""
    CHECKS.append(DEAD)
    try:
        # Baseline failures (before blinding)
        baseline = run_battery()
        baseline_fails = set(nm for nm, ok in baseline if not ok)
        # Blind the dead check
        idx = len(CHECKS) - 1
        orig = CHECKS[idx]
        def blind(spec, _n=DEAD_NAME):
            return True, "", "BLIND (dead check forced pass)"
        CHECKS[idx] = (DEAD_NAME, blind)
        res = run_battery()
        post_blind_fails = set(nm for nm, ok in res if not ok)
        # The fix: attribute the failure to the blind only if it's NEW
        new_fails = post_blind_fails - baseline_fails
        return new_fails
    finally:
        CHECKS.pop()

# --- ARM 1: GREEN baseline ---
print("=== ARM 1: GREEN baseline (clean battery) ===")
base1 = run_battery()
bf1 = sum(1 for _, ok in base1 if not ok)
print("baseline: %d/%d match (%s)" % (len(base1)-bf1, len(base1), "GREEN" if bf1 == 0 else "RED"))
naive1 = classify_dead_check_naive()
fix1 = classify_dead_check_fix()
print("naive probe: dead check -> %s (fails=%s)" % ("UNCALIBRATED" if not naive1 else "CALIBRATED", naive1 if naive1 else "none"))
print("fix: dead check -> %s (new_fails=%s)" % ("UNCALIBRATED" if not fix1 else "CALIBRATED", fix1 if fix1 else "none"))

# --- ARM 2: RED baseline ---
print()
print("=== ARM 2: RED baseline (corrupt one clean specimen) ===")
victim = next(s for s in SPECS if not s["truth"])
backup = victim["truth"]
victim["truth"] = ["GHOST-FLAG"]
base2 = run_battery()
bf2 = sum(1 for _, ok in base2 if not ok)
print("baseline: %d/%d match (%s) [victim: %s]" % (len(base2)-bf2, len(base2), "GREEN" if bf2 == 0 else "RED", victim["name"]))
naive2 = classify_dead_check_naive()
fix2 = classify_dead_check_fix()
print("naive probe: dead check -> %s (fails=%s)" % ("UNCALIBRATED" if not naive2 else "CALIBRATED", naive2 if naive2 else "none"))
print("fix: dead check -> %s (new_fails=%s)" % ("UNCALIBRATED" if not fix2 else "CALIBRATED", fix2 if fix2 else "none"))
victim["truth"] = backup

print()
print("=== RESULT ===")
print("Naive probe (match rule + GREEN precondition):")
print("  GREEN baseline -> UNCALIBRATED (correct)")
print("  RED baseline   -> CALIBRATED (confounded)")
print("Fix (diff post-blind against baseline failures):")
print("  GREEN baseline -> UNCALIBRATED (correct)")
print("  RED baseline   -> UNCALIBRATED (correct: the pre-existing failure is not attributed to the blind)")
print()
print("But the fix is a meta-check: it operates on the battery, not on specimens.")
print("The fix's own correctness is only certified by the author (who wrote")
print("the fix), not by the battery. The fix is a band-aid on the")
print("GREEN-baseline precondition, not a removal of it.")
