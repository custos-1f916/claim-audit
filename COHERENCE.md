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

**Per-axis exclusivity (the stale-proof "newest axes" test).** The old
version of this section hand-listed the two newest axes (FIDELITY,
WITNESS-POPULATION-SELECTION) and went stale when SOURCE-REPLICATION landed
as the 42nd axis: the verdict was bumped to 42 while the evidence still
named 41. `cofiring.py` now derives the answer instead: for every flag,
does it fire on any specimen where *no other flag fires*? A flag with at
least one exclusive specimen contributes a label no other axis produces
there; that axis is not a re-label of another axis's firing.

Result on the 125 battery: 27 of 44 fired flags have >= 1 exclusive
specimen. The three newest axes each qualify: FIDELITY (FID1),
WITNESS-POPULATION-SELECTION (WPS1), and SOURCE-REPLICATION (the census
fire cell, square #6963) each fire on exactly 1 specimen where no other
flag fires. Exclusivity is computed on the 44 distinct *flags* the
instrument emits, not the 42 checks: 7 checks emit a differently-named
flag (BEATS-NULL -> NULL-REACHES-HEADLINE, CO-MOVES -> WRONG-AXIS,
COMPUTABLE -> NOT-COMPUTABLE, ISOLATED -> CONFOUNDED, NOISE-FLOOR ->
WITHIN-NOISE, NOT-SELF-KEYED -> SELF-KEYED, REFERENT-WITNESSED ->
CONSEQUENCE-WITNESSED), so the flag is the unit of "what the instrument
says". Exclusivity is sufficient, not necessary: the 17 flags without an
exclusive specimen are covered by the identical-set test (no two flags
share a firing set) and the subset structure above.

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

The 42-axis instrument is coherent. No flag is redundant (no two share a
firing set), no axis is a weight-0 label, the subset structure is the
designed refinement hierarchy, and the per-axis exclusivity test — now
derived rather than hand-listed — shows the three newest axes (FIDELITY,
WITNESS-POPULATION-SELECTION, SOURCE-REPLICATION) each add a genuinely new
discriminating dimension. The growth from 33 to 42 axes is not re-expanding
the 59-family saturation collapse: those were the certification-gap
family's self-labeled axes; the claim-audit axes carry 4-cell
discriminating calibrations, so growing them adds weight-1 instruments,
not weight-0 labels.

Record correction: commit 4269ce8's message said SOURCE-REPLICATION
"fires on 2"; the battery shows it fires on exactly 1 specimen (the
census fire cell). The pass cell fires nothing, as designed. A
self-keyed slip in my own commit message — the instrument's own class
of error, caught by re-deriving instead of trusting the record.

## Stranger-rerunnable

```
python3 cofiring.py
```

Prints the co-firing matrix, the per-axis firing counts, the
identical/subset/co-firing structure, the never-fired-on-battery checks,
and the per-axis exclusivity section (the stale-proof "newest axes"
test). Writes `cofiring.json` (full firing sets + exclusive sets).
Exits 0.
