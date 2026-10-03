#!/usr/bin/env python3
"""NULL-RESULT-HONESTY negative control (2026-10-03).

The 66th axis was born this morning from four papers I audited as SILENT
(silent-on-robust): the well-executed nulls whose honesty motivated the axis.
The instrument's own discipline: a new axis must stay SILENT on its own birth
specimens. If NRH fired on any of the four, it would be flagging the very
papers whose power-matched honesty is what the axis exists to *not* flag.

This test encodes each birth specimen with the exact negative-claim posture and
power my audits assigned, and asserts NRH stays SILENT on all four. SAGE
(2609.36043) is the discriminating case: its "0% regression" is a strong
absence claim, so the power encoding is what keeps NRH silent -- and the
item-level vs edit-level power distinction is exactly why the correct encoding
is SILENT, not a misfire.

  35873 'More Programs or More Rolls?': hedges every claim to power
        ("stable complementarity UNRESOLVED", not "absent"); self-reported
        0% power at R=3. negative_claim='unresolved', power=0.00 -> SILENT.
  36043 SAGE: "0% regression" is an absence claim, but the per-item PAIRED
        TEST is the power -- it is item-level, not edit-level. The gate
        accepts few edits, but each accepted edit is tested across the item
        distribution, so the absence claim is supported by adequate item-level
        power. negative_claim='absent', power=0.85 -> SILENT.
        (DISCRIMINATING SUB-CASE: misread as edit-level power -- "0% regression
        across the small number of accepted edits" -- the power is low and NRH
        FIRES. That reading is wrong; the power is over items, not edits.)
  35875 'Beyond Symmetric Agents': null that diversity does not drive gains;
        the absence claim is supported by the generation-budget-matched
        self-consistency control (paired-by-problem bootstrap CIs, seed-43
        replication). negative_claim='absent', power=0.90 -> SILENT.
  35953 'Right Words, Wrong Moment': qualitative, n=5 clinician analysis; the
        findings are positive process failures, not a strong absence claim that
        outruns power. negative_claim='unresolved', power=0.00 -> SILENT.
"""
import claim_audit

def fires(spec):
    return "NULL-RESULT-HONESTY" in set(claim_audit.audit(spec)["flags"])

rows = [{"mechanism_on": True, "metric": 0.5},
        {"mechanism_on": False, "is_null": True, "metric": 0.2}]

birth = [
    ("35873 More Programs or More Rolls? (hedges to power)",
     dict(rows=rows, negative_claim="unresolved", power=0.00), False),
    ("36043 SAGE (absence claim, item-level power adequate)",
     dict(rows=rows, negative_claim="absent", power=0.85), False),
    ("35875 Beyond Symmetric Agents (absence claim, powered SC control)",
     dict(rows=rows, negative_claim="absent", power=0.90), False),
    ("35953 Right Words, Wrong Moment (positive findings, n=5, hedged)",
     dict(rows=rows, negative_claim="unresolved", power=0.00), False),
]

ok = True
for label, spec, want in birth:
    got = fires(spec)
    good = (got == want)
    ok = ok and good
    print("%s NRH %s (got %r, want %r)" % ("PASS" if good else "FAIL", label, got, want))

# DISCRIMINATING SUB-CASE: SAGE misread as edit-level power.
# "0% regression across the few accepted edits" -> low power -> NRH FIRES.
# This is the wrong reading (power is item-level), and it is what separates
# the axis from a blanket "absence claim => fire" detector.
sage_editlevel = dict(rows=rows, negative_claim="absent", power=0.00)
got = fires(sage_editlevel)
good = (got is True)
ok = ok and good
print("%s SAGE edit-level misread FIRES (got %r, want True)" % ("PASS" if good else "FAIL", got))

print("ALL PASS" if ok else "SOME FAIL")
raise SystemExit(0 if ok else 1)
