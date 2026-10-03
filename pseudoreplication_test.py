#!/usr/bin/env python3
"""PSEUDOREPLICATION discriminating test (2026-10-03).

The 65th axis: a reported p-value's denominator (n) must count the
INDEPENDENT unit of the design, not a finer, non-independent sub-unit.
When the reported n counts nested sub-units (e.g. 7 structures from 3
chemotypes), the reported p is anti-conservative and the significance can
flip at the independent unit. This test grounds the axis against the REPO
instrument (claim_audit.py) with the A/B discriminating pair plus the N/A
and not-the-cause arms:

  A: correlation 0.90, reported_n=7, independent_n=3 -> FIRES
     (reported p=0.0058 < 0.05, independent p=0.287 >= 0.05: flips)
  B: correlation 0.90, reported_n=7, independent_n=7 -> SILENT
     (independent_n not < reported_n: no correction)
  C: correlation 0.90, reported_n=7, independent_n=5 -> SILENT
     (the reading at the independent unit is still significant: survives)
  D: correlation 0.50,  reported_n=7, independent_n=3 -> SILENT
     (the reported reading is not significant: no significance to lose)
  E: no reported_n / independent_n declared           -> N/A

A and B differ ONLY in independent_n (3 vs 7): the axis is what
discriminates. Live witness: arXiv 2609.36057 (Mirror-Score) -- the
headline pLDDT structure-level LOO Spearman rho=0.90 (p=0.006) is
arithmetically correct at n=7, but the 7 structures come from only 3
independent chemotypes, so at the independent unit (n=3) the result is
not significant (p=0.287).
"""
import claim_audit

def fires(spec):
    return "PSEUDOREPLICATION" in set(claim_audit.audit(spec)["flags"])

rows = [{"mechanism_on": True, "metric": 0.5},
        {"mechanism_on": False, "is_null": True, "metric": 0.2}]

A = dict(rows=rows, statistic="correlation", statistic_value=0.90,
         reported_n=7, independent_n=3)
B = dict(rows=rows, statistic="correlation", statistic_value=0.90,
         reported_n=7, independent_n=7)
C = dict(rows=rows, statistic="correlation", statistic_value=0.90,
         reported_n=7, independent_n=5)
D = dict(rows=rows, statistic="correlation", statistic_value=0.50,
         reported_n=7, independent_n=3)
E = dict(rows=rows, statistic="correlation", statistic_value=0.90)

ok = True
for label, spec, want in [
    ("A fire (correlation 0.90, n=7, independent_n=3; flips to non-significant)", A, True),
    ("B silent (correlation 0.90, n=7, independent_n=7; no correction)", B, False),
    ("C silent (correlation 0.90, n=7, independent_n=5; significance survives)", C, False),
    ("D silent (correlation 0.50, n=7, independent_n=3; reported not significant)", D, False),
    ("E N/A (no reported_n / independent_n declared)", E, False),
]:
    got = fires(spec)
    good = (got == want)
    ok = ok and good
    print("%s %s (got %r, want %r)" % ("PASS" if good else "FAIL", label, got, want))

print("ALL PASS" if ok else "SOME FAIL")
raise SystemExit(0 if ok else 1)
