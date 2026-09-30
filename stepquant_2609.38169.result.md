# STEPQuant (arXiv 2609.38169) — claim-audit run, 2026-09-30

Spec: stepquant_2609.38169.json (type=empirical, 2 rows, expected=[] as a probe).
Command: `python3 claim_audit.py --spec stepquant_2609.38169.json`

## Verdict (after the COUPLED-HEADLINES axis, 58 checks)
- verdict: COUPLED-HEADLINES
- flags: [COUPLED-HEADLINES]
- contested: []
- The instrument now CATCHES the seam this spec was chosen to expose.

## The coupled-numbers seam (what the instrument was blind to)
The abstract headlines two numbers on two DIFFERENT axes:
1. "over 5x recurrent-state compression" — the MECHANISM'S OWN axis.
   Tautological: 32/6 = 5.33x is the bit-budget arithmetic (nominal 6-bit
   budget), not a measured outcome. The abstract does not say whether the
   5x is measured (actual GPU bytes) or nominal.
2. "reduces total serving memory by 68.7%" — the WIDER substrate axis.

The two are jointly consistent ONLY IF the recurrent state is ~86% of total
serving memory: 0.8*f = 0.687 -> f = 0.8588. The abstract never declares the
substrate composition. If state were a smaller fraction (e.g. 0.5), the 5x
state compression would yield only ~40% total reduction, not 68.7%.

## Before / after
- BEFORE (57 checks): verdict DISCRIMINATES, flags [] — the instrument was
  BLIND to the coupled-numbers seam. This spec was the discriminating case
  that motivated the new axis.
- AFTER (58 checks): verdict COUPLED-HEADLINES, flags [COUPLED-HEADLINES] —
  the seam is now named and fired. The 3-cell discriminating test
  (CH1 fire / CH2 pass / CH3 schema-N/A) was built and confirmed to
  discriminate, so the axis was minted (check_coupled_headlines in
  claim_audit.py) with calibration cells (calibration.py: CH1 fire + CH2 pass)
  and battery cells (specimens.py: CH1/CH2/CH3 + this live specimen).

## What the instrument still cannot answer
- Is the 5x measured or nominal? (not in schema — the axis fires on the
  coupling, not on the measurement basis of the mechanism number)
- The substrate composition itself (the axis requires it to be declared or
  the broader number independently measured; it does not estimate it)

## Classification (resolved)
Minted as the 58th axis: COUPLED-HEADLINES. See COHERENCE.md
"## COUPLED-HEADLINES re-derivation (2026-09-30)" and the README block
"(2026-09-30): the COUPLED-HEADLINES axis (58th) was implemented."
