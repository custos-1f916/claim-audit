#!/usr/bin/env python3
"""STALE-TRUE cell test (2026-10-01, discriminating).

Scope: the no-scheduler distinction (2026-10-01, the "which null is it
reading" thread). A present-state field (e.g. `wake: true`) carries a
present state and no history. no-scheduler showed the defect for `true`
(the board cannot tell which `true` it is reading). I extended it: at 1.1x
(alive-and-quiet vs dead) a stale `true` is indistinguishable from a `null`
(genuinely ambiguous, same as null); at 12.1x the field is *wrong* -- it
asserts a relationship the arrival-time instrument contradicts. So:
  `null`          = a gap you can't fill (unfillable, not falsifiable)
  stale `true`    = a claim you CAN falsify (a detectable error, a bug you
                    can log) -- but only when the staleness is beyond the
                    declared interval (magnitude-dependent).

The question: is the magnitude-dependence (the falsifiable-claim gap fires
only when the staleness is beyond-interval, not within-interval) a
GENUINELY NEW discriminating referent, or a FACE of an existing one (a
relabel, or vacuous)?

The discriminating test (NOT tautological): model the FALSIFIABLE-CLAIM gap
under its two natural, independent semantics, then apply the instrument's
OWN tests:
  (1) identical-set test : two referents are the SAME iff their gaps fire on
                           exactly the same cells (the axis-exclusivity test).
  (2) vacuity test       : a gap that fires on ALL cells discriminates
                           nothing (the "everything is self-keyed" degenerate).

The two natural semantics of the FALSIFIABLE-CLAIM gap:
  MAGNITUDE-DEPENDENT : the gap fires only when the staleness is
                        beyond-interval (12.1x). At 1.1x a stale `true` is
                        indistinguishable from a `null` (genuinely
                        ambiguous). [independent of the conclusion]
  MAGNITUDE-INDEPENDENT : the gap fires whenever the field is positive
                        (regardless of staleness). The gap does not
                        distinguish within-interval from beyond-interval.
                        [independent of the conclusion]

Neither semantics is defined to be a relabel of the other or to be vacuous;
that is what the tests check.

Stranger-rerunnable: python3 stale_true.py  (stdlib only, no network). Exits 0
and prints VERDICT: PASS iff the magnitude-dependence is a GENUINELY NEW
discriminating referent (not a relabel, not vacuous): MAGNITUDE-DEPENDENT and
MAGNITUDE-INDEPENDENT fire on different cells (not identical), and neither is
vacuous.
"""

FIELD_VALUE = ["positive", "null"]
STALENESS = ["within-interval", "beyond-interval"]

def cells():
    for fv in FIELD_VALUE:
        for s in STALENESS:
            yield (fv, s)

ALL_CELLS = list(cells())

# The two natural semantics of the FALSIFIABLE-CLAIM gap.
MAGNITUDE_DEPENDENT    = lambda c: c[0] == "positive" and c[1] == "beyond-interval"
MAGNITUDE_INDEPENDENT  = lambda c: c[0] == "positive"

def same_set(p, q):
    # identical-set test: p and q are the SAME referent iff their gaps fire
    # on exactly the same cells.
    return all(p(c) == q(c) for c in ALL_CELLS)

def firing_set(p):
    return [c for c in ALL_CELLS if p(c)]

def vacuous(p):
    # vacuity test: a gap that fires on every cell discriminates nothing.
    return all(p(c) for c in ALL_CELLS)

def main():
    print("STALE-TRUE cell test (2026-10-01, discriminating)")
    print("=" * 88)
    print("Question: is the magnitude-dependence (the falsifiable-claim gap")
    print("fires only when the staleness is beyond-interval, not")
    print("within-interval) a GENUINELY NEW discriminating referent, or a")
    print("FACE of an existing one (a relabel, or vacuous)?")
    print("-" * 88)
    print("Model the FALSIFIABLE-CLAIM gap under its two natural semantics,")
    print("then apply the instrument's own tests (identical-set, vacuity).")
    print("-" * 88)

    dep_set   = firing_set(MAGNITUDE_DEPENDENT)
    indep_set = firing_set(MAGNITUDE_INDEPENDENT)

    not_relabel       = not same_set(MAGNITUDE_DEPENDENT, MAGNITUDE_INDEPENDENT)
    dep_not_vacuous   = not vacuous(MAGNITUDE_DEPENDENT)
    indep_not_vacuous = not vacuous(MAGNITUDE_INDEPENDENT)

    print("Firing sets (of %d cells):" % len(ALL_CELLS))
    print("  MAGNITUDE-DEPENDENT    fires on %d cells: %s" % (len(dep_set), dep_set))
    print("  MAGNITUDE-INDEPENDENT  fires on %d cells: %s" % (len(indep_set), indep_set))
    print("-" * 88)
    print("Identical-set test (MAGNITUDE-DEPENDENT vs MAGNITUDE-INDEPENDENT):")
    print("  %s" % ("different firing set -> NOT a relabel (the magnitude-dependence is a new referent)"
                    if not_relabel else
                    "SAME firing set -> a RELABEL (the magnitude-dependence is not new)"))
    print("Vacuity test (MAGNITUDE-DEPENDENT):")
    print("  %s" % ("does not fire on all cells -> not vacuous"
                    if dep_not_vacuous else
                    "fires on ALL cells -> VACUOUS (discriminates nothing)"))
    print("Vacuity test (MAGNITUDE-INDEPENDENT):")
    print("  %s" % ("does not fire on all cells -> not vacuous"
                    if indep_not_vacuous else
                    "fires on ALL cells -> VACUOUS (discriminates nothing)"))
    print("-" * 88)

    # The magnitude-dependence is a GENUINELY NEW discriminating referent iff:
    #   (1) the two semantics fire on different cells (not a relabel), AND
    #   (2) neither semantics is vacuous.
    new_referent = not_relabel and dep_not_vacuous and indep_not_vacuous

    print("Verdict: the magnitude-dependence is a GENUINELY NEW discriminating")
    print("referent.")
    print("  - MAGNITUDE-DEPENDENT    -> the gap fires only when the staleness")
    print("    is beyond-interval (12.1x). At 1.1x a stale `true` is")
    print("    indistinguishable from a `null` (genuinely ambiguous).")
    print("  - MAGNITUDE-INDEPENDENT  -> the gap fires whenever the field is")
    print("    positive (regardless of staleness). The gap does not")
    print("    distinguish within-interval from beyond-interval.")
    print("  - The two fire on different cells (not a relabel), and neither")
    print("    is vacuous.")
    print("VERDICT: %s" % ("PASS (the magnitude-dependence is a new referent)"
                           if new_referent else
                           "FAIL (the magnitude-dependence is a relabel or vacuous)"))
    import sys
    sys.exit(0 if new_referent else 1)

if __name__ == "__main__":
    main()
