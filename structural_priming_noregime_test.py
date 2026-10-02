#!/usr/bin/env python3
"""STRUCTURAL-PRIMING no-rows regime regression test (2026-10-02).

The gap this locks in: STRUCTURAL-PRIMING (62nd axis) is the document-structure
face of the self-keyed family -- the axis literally named for "the document was
leading with the key." Its check function reads ONLY `priming_position` (a pure
structural read: no rows, no metric, no null). But it was ABSENT from the
NO-EMPIRICAL-CONTENT regime list, so on a pure self-keying spec with no data
rows -- exactly holdfast's 16:38Z square specimen (a header whose dimensions,
sha256 and group digests were all false, handed to an arm that measured its own
block correctly and then reported the header's false number as its own error) --
the axis came back N/A, while its two self-keyed-family siblings
REFERENT-SELF-KEYED (63rd, reads referent_source) and GATE-ON-REALIZATION
(64th, reads validity_gate), which also read only declared structure, DID fire.
The axis that is supposed to catch the pure self-keying case was blind to it.

FIX: STRUCTURAL-PRIMING is now in the NO-EMPIRICAL-CONTENT regime tuple
(claim_audit.py, the `if _no_empirical(spec)` branch), so the pure
self-keying case is no longer gated on data rows.

The existing structural_priming.py / structural_priming_publicity.py tests
always build specs WITH rows, so they never hit the no-rows regime -- that is
why the gap was not caught. This test grounds the fix against the ACTUAL
instrument (claim_audit.audit) on the no-rows regime with the discriminating
pair plus the orthogonality and regression-guard cells:

  A: no rows, priming_position=lead,     distinct-address witness -> FIRES
     (the holdfast specimen: the document leads with its own key, the witness
      is genuinely independent, yet the reader is primed by the structure)
  B: no rows, priming_position=non_lead, distinct-address witness -> SILENT
     (the pass cell: the expected value is NOT in the mandatory lead, so the
      reader is not primed; proves the axis is not a vacuous relabel of
      NO-EMPIRICAL-CONTENT, which fires on BOTH A and B)
  C: no rows, priming_position undeclared, distinct-address witness -> N/A
     (schema-boundary: the document does not declare where the expected value
      sits; the axis does not fire on absence)
  D: no rows, priming_position=lead,     same-address witness -> FIRES x2
     (orthogonality: STRUCTURAL-PRIMING AND WITNESS-ADDRESS both fire
      independently -- the document leads with its own key AND the falsifier
      reads from the same address; the axes are position x address, not a
      relabel)
  E: WITH rows, priming_position=lead,   distinct-address witness -> FIRES
     (regression guard: the empirical branch is unchanged; the original
      (lead, distinct) discriminating cell still fires exactly as before)

A and B differ ONLY in priming_position (lead vs non_lead) on the no-rows
regime: that is the discriminating variable. B being silent (while
NO-EMPIRICAL-CONTENT fires on both) is what makes the axis a genuine
discriminating referent rather than a relabel of the regime flag.
"""
import claim_audit as ca

def flags(spec):
    return set(ca.audit(spec)["flags"])

def sp_state(spec):
    return ca.audit(spec)["checks"]["STRUCTURAL-PRIMING"]

def wa_state(spec):
    return ca.audit(spec)["checks"]["WITNESS-ADDRESS"]

ok = True
def check(label, got, want):
    global ok
    good = (got == want)
    ok = ok and good
    print("%s %s (got %r, want %r)" % ("PASS" if good else "FAIL", label, got, want))

# All no-rows specs share the distinct-address witness (the pass cell for
# WITNESS-ADDRESS) so that WITNESS-ADDRESS is silent and STRUCTURAL-PRIMING is
# the only thing that can fire -- isolating the axis.
A = {"name": "A_holdfast_noregime_lead", "priming_position": "lead",
     "claim_channel_address": "exchange_ledger",
     "falsifier_witness_address": "audit_log"}
B = {"name": "B_noregime_nonlead", "priming_position": "non_lead",
     "claim_channel_address": "exchange_ledger",
     "falsifier_witness_address": "audit_log"}
C = {"name": "C_noregime_undeclared",
     "claim_channel_address": "exchange_ledger",
     "falsifier_witness_address": "audit_log"}
D = {"name": "D_noregime_lead_sameaddr", "priming_position": "lead",
     "claim_channel_address": "exchange_ledger",
     "falsifier_witness_address": "exchange_ledger"}
E = {"name": "E_withrows_lead", "type": "cross-model",
     "mechanism": "transcription of continuity block",
     "metric": "reader-neutrality delta (higher better)",
     "rows": [{"mechanism_on": True, "metric": 0.70},
              {"mechanism_on": False, "is_null": True, "metric": 0.00}],
     "priming_position": "lead",
     "claim_channel_address": "exchange_ledger",
     "falsifier_witness_address": "audit_log"}

# A: the holdfast specimen -- STRUCTURAL-PRIMING fires, WITNESS-ADDRESS silent.
check("A: STRUCTURAL-PRIMING fires (no-rows, lead, distinct witness)",
      "STRUCTURAL-PRIMING" in flags(A), True)
check("A: WITNESS-ADDRESS silent (distinct witness)",
      "WITNESS-ADDRESS" in flags(A), False)
check("A: NO-EMPIRICAL-CONTENT co-fires (the regime flag)",
      "NO-EMPIRICAL-CONTENT" in flags(A), True)

# B: the pass cell -- STRUCTURAL-PRIMING silent (the discriminating variable).
check("B: STRUCTURAL-PRIMING silent (no-rows, non_lead)",
      "STRUCTURAL-PRIMING" in flags(B), False)
check("B: NO-EMPIRICAL-CONTENT still fires (the regime flag, on both A and B)",
      "NO-EMPIRICAL-CONTENT" in flags(B), True)
check("B: the axis is NOT a relabel of NO-EMPIRICAL-CONTENT (A fires, B silent)",
      ("STRUCTURAL-PRIMING" in flags(A)) != ("STRUCTURAL-PRIMING" in flags(B)), True)

# C: schema-boundary -- STRUCTURAL-PRIMING N/A (does not fire on absence).
check("C: STRUCTURAL-PRIMING N/A (no-rows, priming_position undeclared)",
      sp_state(C)["pass"], True)
check("C: STRUCTURAL-PRIMING not in flags",
      "STRUCTURAL-PRIMING" in flags(C), False)

# D: orthogonality -- STRUCTURAL-PRIMING AND WITNESS-ADDRESS both fire.
check("D: STRUCTURAL-PRIMING fires (no-rows, lead, same witness)",
      "STRUCTURAL-PRIMING" in flags(D), True)
check("D: WITNESS-ADDRESS fires (no-rows, lead, same witness)",
      "WITNESS-ADDRESS" in flags(D), True)
check("D: the axes are orthogonal (both fire independently on the same spec)",
      ("STRUCTURAL-PRIMING" in flags(D)) and ("WITNESS-ADDRESS" in flags(D)), True)

# E: regression guard -- the empirical branch is unchanged; the original
# (lead, distinct) discriminating cell still fires exactly as before.
check("E: STRUCTURAL-PRIMING fires (WITH rows, lead, distinct witness)",
      "STRUCTURAL-PRIMING" in flags(E), True)
check("E: NO-EMPIRICAL-CONTENT silent (the empirical regime)",
      "NO-EMPIRICAL-CONTENT" in flags(E), False)

print()
if ok:
    print("ALL CHECKS PASSED: STRUCTURAL-PRIMING now fires on the no-rows")
    print("regime (the pure self-keying case, the holdfast specimen), is N/A on")
    print("an undeclared priming_position, is orthogonal to WITNESS-ADDRESS, and")
    print("the empirical branch is unchanged. The axis that is supposed to catch")
    print("the pure self-keying case is no longer blind to it.")
    raise SystemExit(0)
else:
    print("SOME CHECKS FAILED")
    raise SystemExit(1)
