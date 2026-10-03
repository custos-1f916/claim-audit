#!/usr/bin/env python3
"""NULL-RESULT-HONESTY discriminating test (2026-10-03).

The 66th axis: a well-executed NULL result is the complement of the 65
positive-claim detectors. The discriminating question for a negative claim is
'does the negative claim match the statistical power?': FIRE when a paper
asserts 'X absent' at a power that cannot separate absent from small; SILENT
when it hedges to power ('unresolved / insufficient evidence'). This test
grounds the axis against the REPO instrument (claim_audit.py) with the 2x2
discriminating grid plus the N/A arm:

  A: negative_claim='absent',     power=0.00 (low)      -> FIRES
  B: negative_claim='absent',     power=0.95 (adequate) -> SILENT
  C: negative_claim='unresolved', power=0.00 (low)      -> SILENT
  D: negative_claim='unresolved', power=0.95 (adequate) -> SILENT
  E: no negative_claim / power declared                  -> N/A (SILENT)

The 2609.35873 'More Programs or More Rolls?' witness is cell C (hedges every
claim to power, self-reported 0% power at R=3) -- the SILENT calibration
witness that motivated the axis.
"""
import claim_audit

def fires(spec):
    return "NULL-RESULT-HONESTY" in set(claim_audit.audit(spec)["flags"])

rows = [{"mechanism_on": True, "metric": 0.5},
        {"mechanism_on": False, "is_null": True, "metric": 0.2}]

A = dict(rows=rows, negative_claim="absent", power=0.00)
B = dict(rows=rows, negative_claim="absent", power=0.95)
C = dict(rows=rows, negative_claim="unresolved", power=0.00)
D = dict(rows=rows, negative_claim="unresolved", power=0.95)
E = dict(rows=rows)

ok = True
for label, spec, want in [
    ("A fire (absent claim, power 0.00 < 0.80; outruns power)", A, True),
    ("B silent (absent claim, power 0.95 >= 0.80; powered to support)", B, False),
    ("C silent (unresolved claim, power 0.00; hedged to power)", C, False),
    ("D silent (unresolved claim, power 0.95; hedged)", D, False),
    ("E N/A (no negative_claim / power declared)", E, False),
]:
    got = fires(spec)
    good = (got == want)
    ok = ok and good
    print("%s %s (got %r, want %r)" % ("PASS" if good else "FAIL", label, got, want))

print("ALL PASS" if ok else "SOME FAIL")
raise SystemExit(0 if ok else 1)
