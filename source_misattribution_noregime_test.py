#!/usr/bin/env python3
"""SOURCE-MISATTRIBUTION no-rows regime regression test (2026-10-03).

The gap this locks in: SOURCE-MISATTRIBUTION (34th axis) is a QUALITATIVE
headline-layer axis -- its check function reads ONLY `source_attribution` and
`load_bearing` (two declared string fields: which component the headline
credits as the source of the effect, and which component actually produces
it). No rows, no metric, no null. Its own N/A condition is "fields not
declared," not "no data rows." But it was ABSENT from the NO-EMPIRICAL-CONTENT
regime list, so on a pure headline claim with no data rows -- exactly the
BBC Spain-housing snap-election seed (the headline credits the HOUSING CRISIS
as the cause of a snap election, but the load-bearing lever is the JUNTS
COALITION FRACTURE; the defeat is measured, the snap election is a forecast)
-- the axis came back N/A, while its sibling THESIS-OUTRUNS-EVIDENCE (52nd,
which IS in the regime list) fired. The axis that is supposed to catch the
"the named cause is not the actual cause" seam was blind to it in the regime
where that seam actually lives.

FIX: SOURCE-MISATTRIBUTION is now in the NO-EMPIRICAL-CONTENT regime tuple
(claim_audit.py, the `if _no_empirical(spec)` branch), so the pure
headline-cause-misattribution case is no longer gated on data rows.

The existing SOURCE-MISATTRIBUTION witnesses (SICC 2609.26076, ChainUQ
2609.26060 fire + pass cells) all build specs WITH rows, so they never hit
the no-rows regime -- that is why the gap was not caught. This test grounds
the fix against the ACTUAL instrument (claim_audit.audit) on the no-rows
regime.

Cells:
  A: no rows, source_attribution="housing crisis", load_bearing="Junts
     coalition fracture" -> FIRES (the Spain shape: the credited cause is not
      the load-bearing lever)
  B: no rows, source_attribution == load_bearing -> SILENT (the pass cell:
     the credited cause IS the load-bearing lever; proves the axis is not a
     vacuous relabel of NO-EMPIRICAL-CONTENT, which fires on BOTH A and B)
  C: no rows, source_attribution undeclared -> N/A (schema-boundary: the
     headline does not declare which component it credits; the axis does not
     fire on absence)
  D: no rows, source_attribution != load_bearing AND thesis_endpoint not in
     measured_endpoints, headline_states_as_fact -> FIRES x2 (orthogonality:
     SOURCE-MISATTRIBUTION AND THESIS-OUTRUNS-EVIDENCE both fire independently
     -- the named cause is the wrong component AND the endpoint is a forecast;
     the axes are cause-attribution x endpoint-measurement, not a relabel)
  E: WITH rows, source_attribution != load_bearing -> FIRES (regression guard:
     the empirical branch is unchanged; the original discriminating cell still
     fires exactly as before)

A and B differ ONLY in source_attribution (crisis vs fracture) on the no-rows
regime: that is the discriminating variable. B being silent (while
NO-EMPIRICAL-CONTENT fires on both) is what makes the axis a genuine
discriminating referent rather than a relabel of the regime flag.
"""
import claim_audit as ca

def flags(spec):
    return set(ca.audit(spec)["flags"])

def sm_state(spec):
    return ca.audit(spec)["checks"]["SOURCE-MISATTRIBUTION"]

def toe_state(spec):
    return ca.audit(spec)["checks"]["THESIS-OUTRUNS-EVIDENCE"]

ok = True
def check(label, got, want):
    global ok
    good = (got == want)
    ok = ok and good
    print("%s %s (got %r, want %r)" % ("PASS" if good else "FAIL", label, got, want))

# A: the Spain shape -- no rows, credited cause != load-bearing lever.
A = dict(
    name="BBC Spain-housing snap-election headline (no-rows)",
    source_attribution="housing crisis",
    load_bearing="Junts coalition fracture",
)
check("A: SOURCE-MISATTRIBUTION fires (no-rows, crisis != fracture)",
      "SOURCE-MISATTRIBUTION" in flags(A), True)
check("A: NO-EMPIRICAL-CONTENT fires (the no-rows regime)",
      "NO-EMPIRICAL-CONTENT" in flags(A), True)

# B: pass cell -- no rows, credited cause == load-bearing lever.
B = dict(
    name="Spain control (no-rows, correct attribution)",
    source_attribution="Junts coalition fracture",
    load_bearing="Junts coalition fracture",
)
check("B: SOURCE-MISATTRIBUTION silent (no-rows, credited == load-bearing)",
      "SOURCE-MISATTRIBUTION" in flags(B), False)
check("B: NO-EMPIRICAL-CONTENT fires (the no-rows regime)",
      "NO-EMPIRICAL-CONTENT" in flags(B), True)
check("B: SOURCE-MISATTRIBUTION detail is the pass cell",
      "matches the load-bearing variable" in sm_state(B)["detail"], True)

# C: schema-boundary -- no rows, source_attribution undeclared.
C = dict(
    name="Spain schema-boundary (no-rows, no source declared)",
    load_bearing="Junts coalition fracture",
)
check("C: SOURCE-MISATTRIBUTION N/A (no-rows, source_attribution undeclared)",
      sm_state(C)["pass"], True)
check("C: SOURCE-MISATTRIBUTION not in flags",
      "SOURCE-MISATTRIBUTION" in flags(C), False)

# D: orthogonality -- SOURCE-MISATTRIBUTION AND THESIS-OUTRUNS-EVIDENCE both fire.
D = dict(
    name="Spain full (no-rows, cause-misattributed + forecast endpoint)",
    source_attribution="housing crisis",
    load_bearing="Junts coalition fracture",
    thesis_endpoint="snap election",
    measured_endpoints=["housing decree-law defeated in Congress"],
    headline_states_as_fact=True,
)
check("D: SOURCE-MISATTRIBUTION fires (no-rows, crisis != fracture)",
      "SOURCE-MISATTRIBUTION" in flags(D), True)
check("D: THESIS-OUTRUNS-EVIDENCE fires (no-rows, endpoint is a forecast)",
      "THESIS-OUTRUNS-EVIDENCE" in flags(D), True)
check("D: the axes are orthogonal (both fire independently on the same spec)",
      ("SOURCE-MISATTRIBUTION" in flags(D)) and ("THESIS-OUTRUNS-EVIDENCE" in flags(D)), True)

# E: regression guard -- the empirical branch is unchanged; the original
# (crisis, fracture) discriminating cell still fires exactly as before.
E = dict(
    name="Spain empirical (WITH rows, crisis != fracture)",
    source_attribution="housing crisis",
    load_bearing="Junts coalition fracture",
    rows=[{"mechanism_on": True, "metric": 1.0},
          {"mechanism_on": False, "is_null": True, "metric": 0.5}],
)
check("E: SOURCE-MISATTRIBUTION fires (WITH rows, crisis != fracture)",
      "SOURCE-MISATTRIBUTION" in flags(E), True)
check("E: NO-EMPIRICAL-CONTENT silent (the empirical regime)",
      "NO-EMPIRICAL-CONTENT" in flags(E), False)

print()
if ok:
    print("ALL CHECKS PASSED: SOURCE-MISATTRIBUTION now fires on the no-rows")
    print("regime (the pure headline-cause-misattribution case, the Spain")
    print("seed), is silent on a correct attribution, is N/A on an undeclared")
    print("source, is orthogonal to THESIS-OUTRUNS-EVIDENCE, and the empirical")
    print("branch is unchanged. The axis that is supposed to catch the")
    print("'named cause is not the actual cause' seam is no longer blind to it.")
    raise SystemExit(0)
else:
    print("SOME CHECKS FAILED")
    raise SystemExit(1)
