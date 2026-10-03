#!/usr/bin/env python3
"""REGIME-PARTITION completeness test (2026-10-03).

The gap this locks in: the NO-EMPIRICAL-CONTENT regime used to be an inline
hidden constant inside audit() -- a 32-name tuple hand-maintained against the
66-axis CHECKS list, with the empirical-only set IMPLICIT (every axis not
whitelisted). The 2026-10-03 SOURCE-MISATTRIBUTION drift was exactly this
surface: a regime-relevant axis silently missing from the tuple, so it came
back N/A in the regime where its seam actually lives, with no test forcing the
notice.

The fix promoted the partition to two named spec-level constants:
  NO_EMPIRICAL_AXES  -- axes that run their real check on a pure
                        specification (no data rows / type 'specification')
  EMPIRICAL_AXES     -- axes that need the (mechanism, metric, null) triple
                        and are forced to the blanket N/A in the no-empirical
                        branch of audit()

This test witnesses the partition two ways:

  (1) STATIC -- the constants form an exact partition of the CHECKS names:
      disjoint, complete, no stale names. An axis added to CHECKS without a
      regime assignment to EITHER constant fails completeness (the forward
      teeth: the 67th axis cannot silently default to a regime).

  (2) BEHAVIORAL -- the named sets agree with audit()'s ACTUAL branch
      routing. In the no-empirical branch, an axis is routed to the blanket
      N/A ("N/A (NO-EMPIRICAL-CONTENT: no data rows; ...)") iff it is NOT in
      NO_EMPIRICAL_AXES. So on a no-rows spec, every EMPIRICAL_AXES axis must
      show that exact blanket string and every NO_EMPIRICAL_AXES axis must NOT.
      This is the marker that the constants are not just a count but the set
      audit() really branches on.
"""
import claim_audit as ca

BLANKET = "N/A (NO-EMPIRICAL-CONTENT: no data rows; the empirical axis does not apply)"

ok = True
def check(label, got, want):
    global ok
    good = (got == want)
    ok = ok and good
    print("%s %s (got %r, want %r)" % ("PASS" if good else "FAIL", label, got, want))

# ground truth: the registry
checks = [n for (n, _f) in ca.CHECKS]
check_names = set(checks)

# (1a) disjoint
check("disjoint: NO_EMPIRICAL & EMPIRICAL == empty",
      ca.NO_EMPIRICAL_AXES & ca.EMPIRICAL_AXES, set())

# (1b) no stale names (each constant is a subset of the registry)
check("no stale: NO_EMPIRICAL_AXES subset of CHECKS",
      ca.NO_EMPIRICAL_AXES - check_names, set())
check("no stale: EMPIRICAL_AXES subset of CHECKS",
      ca.EMPIRICAL_AXES - check_names, set())

# (1c) complete -- the forward teeth: every axis assigned to exactly one
check("complete: union of both sets == CHECKS names (no unassigned axis)",
      ca.NO_EMPIRICAL_AXES | ca.EMPIRICAL_AXES, check_names)

# (1d) no axis double-assigned (redundant with disjoint but stated per-axis)
check("no double-assignment: counts sum to the registry size",
      len(ca.NO_EMPIRICAL_AXES) + len(ca.EMPIRICAL_AXES), len(check_names))

# (2) behavioral routing witness on a no-rows spec.
# A minimal pure specification: no rows, no evidence walk, no declared fields
# that would trip any specific axis. The routing marker is the blanket N/A
# string, which the no-empirical branch writes for every axis NOT in
# NO_EMPIRICAL_AXES.
spec = dict(name="regime-partition routing witness (no-rows)")
res = ca.audit(spec)["checks"]
routed_blanket = {n for n, c in res.items() if c["detail"] == BLANKET}
check("behavioral: exactly the EMPIRICAL_AXES axes show the blanket N/A",
      routed_blanket, ca.EMPIRICAL_AXES)
check("behavioral: no NO_EMPIRICAL_AXES axis is routed to the blanket N/A",
      routed_blanket & ca.NO_EMPIRICAL_AXES, set())

print()
if ok:
    print("ALL CHECKS PASSED: the regime partition is an exact, disjoint,")
    print("complete assignment of all %d axes, and the named sets agree with" % len(check_names))
    print("audit()'s actual branch routing (the blanket-N/A marker). A new")
    print("axis added to CHECKS without a regime assignment now fails here.")
    raise SystemExit(0)
else:
    print("SOME CHECKS FAILED")
    raise SystemExit(1)
