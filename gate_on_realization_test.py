#!/usr/bin/env python3
"""GATE-ON-REALIZATION discriminating test (2026-10-02).

The 64th axis: a sampling receipt's VALIDITY GATE must be the structural
design-consistency check (declared_fraction == rule_inclusion probability,
exact, no realized n), not a realized-size plausibility band. This test
grounds the axis against the REPO instrument (claim_audit.py) with the A/B
discriminating pair plus the N/A arms:

  A: gate=realized_size_band, design holds, n=0 (tail, band rejects) -> FIRES
  B: gate=realized_size_band, design holds, n=3 (mean, band passes)  -> SILENT
  C: gate=design_consistency,   design holds, n=0 (correct gate)     -> SILENT
  D: gate=realized_size_band, design does NOT hold (0.05!=0.06), n=0 -> SILENT
     (the structural gate legitimately fails; the conflation is not the cause)
  E: no sampling design (no declared_fraction)                        -> N/A

A and B differ ONLY in realized_n (0 vs 3): the axis is what discriminates.
"""
import claim_audit

def fires(spec):
    return "GATE-ON-REALIZATION" in set(claim_audit.audit(spec)["flags"])

rows = [{"mechanism_on": True, "metric": 0.5},
        {"mechanism_on": False, "is_null": True, "metric": 0.2}]

A = dict(rows=rows, declared_fraction=0.06, rule_probability=0.06,
         population_N=50, realized_n=0, validity_gate="realized_size_band",
         gate_band_sd=1.0)
B = dict(rows=rows, declared_fraction=0.06, rule_probability=0.06,
         population_N=50, realized_n=3, validity_gate="realized_size_band",
         gate_band_sd=1.0)
C = dict(rows=rows, declared_fraction=0.06, rule_probability=0.06,
         population_N=50, realized_n=0, validity_gate="design_consistency")
D = dict(rows=rows, declared_fraction=0.05, rule_probability=0.06,
         population_N=50, realized_n=0, validity_gate="realized_size_band",
         gate_band_sd=1.0)
E = dict(rows=rows, population_N=50, realized_n=0,
         validity_gate="realized_size_band", gate_band_sd=1.0)

ok = True
for label, spec, want in [
    ("A fire (realized gate, design holds, n=0 tail)", A, True),
    ("B silent (realized gate, design holds, n=3 mean)", B, False),
    ("C silent (structural gate, the correct gate)", C, False),
    ("D silent (design does NOT hold; structural failure)", D, False),
    ("E N/A (no sampling design declared)", E, False),
]:
    got = fires(spec)
    good = (got == want)
    ok = ok and good
    print("%s %s (got %r, want %r)" % ("PASS" if good else "FAIL", label, got, want))

print("ALL PASS" if ok else "SOME FAIL")
raise SystemExit(0 if ok else 1)
