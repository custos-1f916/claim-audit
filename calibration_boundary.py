#!/usr/bin/env python3
"""Calibration-boundary probe for the claim-audit instrument (self-keyed gap,
applied to the instrument's OWN calibration battery).

Open question (with verdigris, 2026-09-24): can the instrument SURFACE its own
calibration boundary, rather than just locking it as regression witnesses?

Method: per-check mutation. For each of the N checks in claim_audit.CHECKS,
blind it (force it to always-pass) and re-run the calibration battery. If the
battery stays GREEN, the battery cannot catch that check breaking -> the check
is UNCALIBRATED (no discriminating specimen). If the battery goes RED, the
check is CALIBRATED (some specimen's independently-derived ground truth
requires it to fire).

Because the battery's baseline is GREEN (no cross-fire), "never fires on the
battery" and "uncalibrated" coincide: every check that fires does so on a
specimen whose truth set includes its flag, so blinding it breaks the match.

The boundary (the uncalibrated set) is a PROPERTY, not a defect: it is the
exact set of axes the battery is silent on. Exit 0 always; the report is the
point.
"""
import claim_audit
import calibration

SPECS = calibration.SPECIMENS
CHECKS = claim_audit.CHECKS
N = len(CHECKS)


def run_battery():
    """Return [(spec_name, matched)] using the battery's own match rule
    (fired set == independently-derived truth set)."""
    out = []
    for s in SPECS:
        a = claim_audit.audit(s)
        out.append((s["name"], set(a["flags"]) == set(s["truth"])))
    return out


def main():
    base = run_battery()
    base_fail = sum(1 for _, ok in base if not ok)
    print("baseline: %d/%d specimens match (battery %s)" %
          (sum(1 for _, ok in base if ok), len(base),
           "GREEN" if base_fail == 0 else "RED"))
    if base_fail:
        print("NOTE: baseline is RED; the boundary below is still computed, but")
        print("      'caught' is confounded by pre-existing failures.")

    # Which checks fire on at least one baseline specimen (exercised set).
    exercised = set()
    for s in SPECS:
        a = claim_audit.audit(s)
        for cname, res in a["checks"].items():
            if not res["pass"]:
                exercised.add(cname)

    caught, uncaught = [], []
    for i, (name, fn) in enumerate(CHECKS):
        def blind(spec, _n=name):
            return True, "", "BLIND (boundary probe: %s forced pass)" % _n
        orig = CHECKS[i]
        CHECKS[i] = (name, blind)
        try:
            res = run_battery()
        finally:
            CHECKS[i] = orig
        fails = [nm for nm, ok in res if not ok]
        (caught if fails else uncaught).append((name, fails))

    print()
    print("=== per-check mutation (blind = check forced always-pass) ===")
    for name, fails in caught:
        print("CALIBRATED %-32s -> %d specimen(s) fail: %s"
              % (name, len(fails), ", ".join(fails)))
    for name, fails in uncaught:
        ex = "fires-on-battery" if name in exercised else "never-fires"
        print("UNCALIBRATED %-32s -> battery stays green (%s)" % (name, ex))

    print()
    print("SUMMARY: %d/%d checks calibrated; %d uncalibrated (the calibration boundary)"
          % (len(caught), N, len(uncaught)))
    print("The battery is GREEN but only discriminates the calibrated set;")
    print("every uncalibrated check could silently break and the battery would")
    print("still print DISCRIMINATES. Closing the boundary = adding one")
    print("discriminating specimen per uncalibrated axis (or retiring the axis).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
