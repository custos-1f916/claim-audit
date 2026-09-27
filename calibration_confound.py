#!/usr/bin/env python3
"""Demonstrate the calibration-boundary probe's RED-baseline confound.

calibration_boundary.py classifies each check as CALIBRATED or UNCALIBRATED by
blinding it (force always-pass) and checking whether the battery stays GREEN.
That split is only valid under a GREEN baseline: the probe does NOT diff the
post-blind failures against the baseline failures, so a single pre-existing
failing specimen makes EVERY check (including a dead one that fires on no
specimen) look CALIBRATED.

This script demonstrates that confound empirically with two arms that differ
only in the baseline:

  ARM 1  GREEN baseline (clean battery):
         inject a DEAD check (always passes, fires on no specimen), blind it.
         Battery stays green  -> dead check classified UNCALIBRATED (correct).

  ARM 2  RED baseline (one clean specimen's truth set corrupted with a ghost
         flag the audit never fires): same dead check, same blind.
         The victim specimen fails regardless of the blind ->
         dead check classified CALIBRATED (confounded).

The dead check is identical in both arms; only the baseline differs.
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

def classify_dead_check():
    """Append the dead check, blind it, re-run the battery, classify."""
    CHECKS.append(DEAD)
    i = len(CHECKS) - 1
    def blind(spec):
        return True, "", "BLIND"
    orig = CHECKS[i]
    CHECKS[i] = (DEAD_NAME, blind)
    try:
        res = run_battery()
    finally:
        CHECKS[i] = orig
        CHECKS.pop()
    fails = [nm for nm, ok in res if not ok]
    cls = "CALIBRATED" if fails else "UNCALIBRATED"
    return fails, cls

# --- ARM 1: GREEN baseline ---
print("=== ARM 1: GREEN baseline ===")
base = run_battery()
bf = sum(1 for _, ok in base if not ok)
print("baseline: %d/%d match (%s)" % (len(base)-bf, len(base),
      "GREEN" if bf == 0 else "RED"))
fails, cls = classify_dead_check()
print("dead check -> %s (fails=%s)" % (cls, fails if fails else "none"))

# --- ARM 2: RED baseline ---
print()
print("=== ARM 2: RED baseline (corrupt one clean specimen) ===")
victim = next(s for s in SPECS if not s["truth"])
backup = victim["truth"]
victim["truth"] = ["GHOST-FLAG"]
base2 = run_battery()
bf2 = sum(1 for _, ok in base2 if not ok)
print("baseline: %d/%d match (%s) [victim: %s]" %
      (len(base2)-bf2, len(base2), "GREEN" if bf2 == 0 else "RED",
       victim["name"]))
fails2, cls2 = classify_dead_check()
print("dead check -> %s (fails=%s)" % (cls2, fails2 if fails2 else "none"))
victim["truth"] = backup

print()
print("=== RESULT ===")
print("Same dead check, only the baseline differs:")
print("  GREEN baseline -> %s  (correct: the battery is silent on a dead check)" % cls)
print("  RED baseline   -> %s  (confounded: the pre-existing failure is attributed to the blind)" % cls2)
assert cls == "UNCALIBRATED", "GREEN baseline should classify dead check UNCALIBRATED"
assert cls2 == "CALIBRATED", "RED baseline should classify dead check CALIBRATED (confound)"
assert fails2 == [victim["name"]], "RED-baseline failure should be exactly the victim"
print("CONFIRMED: the probe's CALIBRATED/UNCALIBRATED split is only valid under a GREEN baseline.")
print("The self-keyed gap is relocated, not closed: the probe's match rule + GREEN")
print("precondition is what the boundary's computation rests on, and it is not self-certifying.")
