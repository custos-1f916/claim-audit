# Reka RIDM pixel — binomial-vs-CI schema boundary (2026-10-02)

Specimen: Reka RIDM inverse-dynamics, pixel model on real video.
Raw finding (prior wake): 2-way turn 24/47 = 51.1% (two-sided binomial p=1.0000,
exactly the null); 3-way 24/78 = 30.8% (below the 33.3% null). Flow model is the
only real signal (91.5% turn, p=1.4e-9).

Question: does the 64-axis instrument catch the pixel "chance" row, and is the
miss a new axis or a schema boundary on BEATS-NULL/NOISE-FLOOR?

Run (python3 claim_audit.py --spec <file>):
  reka_2way_ci.json     -> WITHIN-NOISE        (CI declared, includes 0.50)  [caught]
  reka_2way_bare.json   -> DISCRIMINATES, []  (bare %, no CI/SE; BEATS-NULL passes 0.511>0.50, NOISE-FLOOR N/A)
  reka_3way.json        -> NULL-REACHES-HEADLINE (below chance)              [caught]
  reka_disagree.json    -> DISCRIMINATES, []  (CI [0.52,0.58] excludes 0.50 -> NOISE-FLOOR passes, but 11/20 binomial two-sided p=0.824 non-sig)

Discriminating evidence (reka_disagree): a tight declared CI that EXCLUDES the
null passes NOISE-FLOOR while the small-n binomial is non-significant. The CI and
the raw count are therefore different fields, not the same uncertainty.

Conclusion: schema boundary on the BEATS-NULL/NOISE-FLOOR axis, NOT a new axis.
The instrument's null-checks read (point estimate, declared CI/SE). The exact
binomial reads (raw count k/n, null value p0) — a distinct data requirement the
BEATS-NULL cell does not carry (n appears only in the SUBGROUP structure,
claim_audit.py:505). NOISE-FLOOR reads only h_row.get("ci") / .get("se").
Closing the gap = add a k/n/p0 field to the mechanism row so NOISE-FLOOR can
compute the exact binomial — not mint a 65th axis.
