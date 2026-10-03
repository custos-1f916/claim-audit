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


# (3) OUTCOME witness: assignment-correctness teeth in Direction 1.
#
# The static partition (1a-1d) and the behavioral blanket-marker (2) are
# self-keyed for ASSIGNMENT CORRECTNESS: they witness that audit() routes via
# the named constant and that the two constants partition the registry, but
# neither can catch an axis sitting in the WRONG set. The discriminating
# mutation proved it: moving SOURCE-MISATTRIBUTION from NO_EMPIRICAL_AXES to
# EMPIRICAL_AXES leaves all four static checks AND the blanket-marker passing
# (routed_blanket = CHECKS - NO_EMPIRICAL_AXES = EMPIRICAL_AXES by the static
# partition, so the marker restates the partition rather than witnessing it).
#
# The OUTCOME witness closes that seam. A NO-EMPIRICAL axis mis-assigned to
# EMPIRICAL_AXES is routed to the blanket N/A on a no-rows spec, so its real
# check never runs and a spec that should FIRE comes back pass/blanket.
# Asserting the FIRE cell on a concrete spec therefore has real teeth in
# Direction 1: it fails exactly when the 2026-10-03 SOURCE-MISATTRIBUTION
# drift (a regime-relevant axis silently missing from the tuple) recurs.
#
# It is BLIND in Direction 2 (an EMPIRICAL axis wrongly in NO_EMPIRICAL_AXES):
# there the mis-routed real check runs on a spec lacking its rows and the
# observable is behaviorally invisible (row-caused N/A == blanket N/A in
# pass/flag), so no outcome assertion can catch it -- the blanket-marker (2)
# is the only witness there, and it catches the drift only by the accidental
# KeyError the mis-routed check raises. Documented, not hidden.
#
# Two independent fire cells (SOURCE-MISATTRIBUTION, the historical drift
# axis, and SELF-FALSIFYING) so the witness is not single-axis.

def _fire_cell(axis, spec):
    """Assert axis FIRES (pass=False, not the blanket N/A) on a no-rows spec."""
    r = ca.audit(spec)["checks"][axis]
    check("outcome: %s FIRES on a no-rows spec (not blanket N/A)" % axis,
          (r["pass"], r["detail"] == BLANKET), (False, False))

# SOURCE-MISATTRIBUTION: credited component != load-bearing variable.
_fire_cell("SOURCE-MISATTRIBUTION",
           dict(name="witness", source_attribution="the API layer",
                load_bearing="the model weights"))
# SELF-FALSIFYING: the paper's own limitation negates its own headline scope.
_fire_cell("SELF-FALSIFYING",
           dict(name="witness", headline_scope="universal",
                limitation_negates="universal"))

# (3b) discriminating mutation: prove the outcome witness has teeth the static
# checks and the blanket-marker lack. Move SOURCE-MISATTRIBUTION to the wrong
# set (NO_EMPIRICAL -> EMPIRICAL). The static partition stays complete and
# disjoint, and the blanket-marker still passes (routed_blanket == EMPIRICAL),
# but the fire spec is now routed to the blanket N/A: only the outcome witness
# fails. This is the exact historical drift, caught by behavior.
_orig_ne, _orig_e = ca.NO_EMPIRICAL_AXES, ca.EMPIRICAL_AXES
ca.NO_EMPIRICAL_AXES = frozenset(_orig_ne - {"SOURCE-MISATTRIBUTION"})
ca.EMPIRICAL_AXES = frozenset(_orig_e | {"SOURCE-MISATTRIBUTION"})
try:
    r = ca.audit(dict(name="witness", source_attribution="the API layer",
                      load_bearing="the model weights"))["checks"]["SOURCE-MISATTRIBUTION"]
    check("outcome mutation: drift to EMPIRICAL routes the fire spec to blanket N/A (witness catches it)",
          (r["pass"], r["detail"] == BLANKET), (True, True))
finally:
    ca.NO_EMPIRICAL_AXES, ca.EMPIRICAL_AXES = _orig_ne, _orig_e

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
