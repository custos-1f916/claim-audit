# Coherence of the 42-axis instrument (2026-09-27)

Question (from the saturation-collapse reconciliation): does the claim-audit
instrument stay coherent as it grows to 42 axes, or do axes start to overlap?

Objective test: the co-firing matrix over the 125-specimen battery
(`cofiring.py`). For each pair of axes, do they fire on the same specimens?

## Findings

**No pure redundancy.** No two axes have identical firing sets. Nothing is a
weight-0 label that could be dropped without changing the instrument's output.

**The subset structure is the *designed* refinement hierarchy, not overlap.**
- `NULL-REACHES-HEADLINE` (36 specimens) is the superset of the BEATS-NULL
  spike/onset refinements (DOSE-RESPONSE, DOSE-SPIKE, FUNNEL-STAGE-MISATTRIBUTION,
  METRIC-SPIKE, OUTCOME-SPIKE, SELECTION-ON-NARRATIVE, SPLIT-SPIKE,
  SUBGROUP-SPIKE, TEMPORAL-SPIKE, TIER-SPIKE). These are the false-positive
  surface of the flat check: each fires on a specimen where the flat check
  also fires, but the refinement is the *right* axis.
- `NO-EMPIRICAL-CONTENT` (14 specimens) is the superset of the
  completeness/regime axes (EVIDENCE-UNCLOSED, NOT-COMPUTABLE,
  UNWITNESSED-RECEIPT, UNWITNESSED-ROOT, WIDER-THAN-NAMED,
  WINDOW-PRESENT-TENSE). Same design: the regime gate short-circuits the
  completeness predicate, so these fire on a subset of the no-empirical-content
  specimens.

Subsets are the structure, not the defect. A refinement that fires on a strict
subset of its parent is doing its job: it catches the cases the parent catches
*and* distinguishes them.

**The two newest axes discriminate cleanly.** FIDELITY and
WITNESS-POPULATION-SELECTION each fire on exactly 1 specimen where *no other
axis fires* (FID1, WPS1). They add a genuinely new dimension; they do not
re-fire an existing axis on a new specimen.

**Two checks never fire on the 125 battery: TEMPORAL-ONSET and REFERENCE-MIX.**
This is the one thing to investigate. "Never fires on the battery" is a proxy,
not the weight-0 test. The real test (per COARSER-MERGE) is: does the axis have
a *discriminating calibration*? Both do:
- TEMPORAL-ONSET: T1 (fire cell) in `calibration.py`.
- REFERENCE-MIX: RM1 (fire) + RM2 (pass) in `calibration.py`.
`calibration.py` passes 78/78 and `calibration_boundary.py` reports 42/42
checks calibrated. So both are weight-1 instruments the 125 battery doesn't
trigger, not weight-0 labels. The battery is not the calibration; the
calibration is the calibration.

**Co-firing pairs (overlap >= 2, neither a subset):** only 2, both expected:
- METRIC-SPIKE & SPLIT-SPIKE (2 specimens): the spike family shares the
  false-positive surface of the flat check; co-firing on a specimen where both
  a metric-spike and a split-spike are present is correct.
- CONFOUNDED & NULL-REACHES-HEADLINE (2 specimens): a confounded ablation where
  the null also reaches the headline is a real, multi-axis specimen.

## Verdict

The 42-axis instrument is coherent. No axis is redundant, no axis is a weight-0
label, the subset structure is the designed refinement hierarchy, and the two
newest axes each add a genuinely new discriminating dimension. The growth from
33 to 42 axes is not re-expanding the 59-family saturation collapse: those were
the certification-gap family's self-labeled axes; the claim-audit axes carry
4-cell discriminating calibrations, so growing them adds weight-1 instruments,
not weight-0 labels.

## Stranger-rerunnable

```
python3 cofiring.py
```

Prints the co-firing matrix, the per-axis firing counts, the identical/subset/
co-firing structure, and the never-fired-on-battery checks. Writes `cofiring.json`
(full firing sets). Exits 0.
