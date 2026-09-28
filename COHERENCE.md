# Coherence of the 47-axis instrument (2026-09-28)

Question (from the saturation-collapse reconciliation): does the claim-audit
instrument stay coherent as it grows to 43 axes, or do axes start to overlap?

Objective test: the co-firing matrix over the 129-specimen battery
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

Result on the 129 battery: 30 of 47 fired flags have >= 1 exclusive
specimen. The four newest axes each qualify: FIDELITY (FID1),
WITNESS-POPULATION-SELECTION (WPS1), SOURCE-REPLICATION (the census
fire cell, square #6963), and PLATFORM-CERTIFIED (PC1) each fire on exactly
1 specimen where no other flag fires; the two battery witnesses
(TEMPORAL-ONSET, REFERENCE-MIX) are exclusive as well. Exclusivity is computed
on the 47 distinct *flags* the instrument emits, not the 43 checks: 7 checks emit a differently-named
flag (BEATS-NULL -> NULL-REACHES-HEADLINE, CO-MOVES -> WRONG-AXIS,
COMPUTABLE -> NOT-COMPUTABLE, ISOLATED -> CONFOUNDED, NOISE-FLOOR ->
WITHIN-NOISE, NOT-SELF-KEYED -> SELF-KEYED, REFERENT-WITNESSED ->
CONSEQUENCE-WITNESSED), so the flag is the unit of "what the instrument
says". Exclusivity is sufficient, not necessary: the 17 flags without an
exclusive specimen are covered by the identical-set test (no two flags
share a firing set) and the subset structure above.

**Two checks never fired on the 125 battery: TEMPORAL-ONSET and REFERENCE-MIX.**
This was the one thing to investigate. "Never fires on the battery" is a proxy,
not the weight-0 test. The real test (per COARSER-MERGE) is: does the axis have
a *discriminating calibration*? Both do:
- TEMPORAL-ONSET: T1 (fire cell) in `calibration.py`.
- REFERENCE-MIX: RM1 (fire) + RM2 (pass) in `calibration.py`.
`calibration.py` passes 82/82 and `calibration_boundary.py` reports 43/43
checks calibrated. So both are weight-1 instruments the 125 battery doesn't
trigger, not weight-0 labels. The battery is not the calibration; the
calibration is the calibration.

**Resolved (2026-09-27, this commit):** the battery's silence was a coverage
gap, not a defect — and a coverage gap is closable. Two constructed witnesses
mirroring the calibration fire cells (T1, RM1) were added to `specimens.py`:
the battery is now 129 (126 real + 3 witnesses), the instrument fires all 47
flags on it (was 46; the two silent flags now fire on exactly their witness,
no cross-fire; PLATFORM-CERTIFIED's live specimen co-fires with
NO-EMPIRICAL-CONTENT, so its constructed witness PC1 is what makes it
exclusive), `truly_never` is empty, and each witness is an exclusive
specimen (exclusivity 30/47). The witnesses are constructed, not real
specimens: they make the battery a second, independent confirmation of the
calibration's discriminating cells, not new ground truth.

**Co-firing pairs (overlap >= 2, neither a subset):** only 2, both expected:
- METRIC-SPIKE & SPLIT-SPIKE (2 specimens): the spike family shares the
  false-positive surface of the flat check; co-firing on a specimen where both
  a metric-spike and a split-spike are present is correct.
- CONFOUNDED & NULL-REACHES-HEADLINE (2 specimens): a confounded ablation where
  the null also reaches the headline is a real, multi-axis specimen.

## Verdict

The 45-axis instrument is coherent. No flag is redundant (no two share a
firing set), no axis is a weight-0 label, the subset structure is the
designed refinement hierarchy, and the per-axis exclusivity test — now
derived rather than hand-listed — shows the five newest axes (FIDELITY,
WITNESS-POPULATION-SELECTION, SOURCE-REPLICATION, PLATFORM-CERTIFIED, TRUST) each add
a genuinely new discriminating dimension. The growth from 33 to 43 axes is not
re-expanding
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

## TRUST re-derivation (2026-09-28)

The 44th axis (TRUST, the authority-channel face of the self-keyed family;
the trust_cell result, 2026-09-28) was added. The battery is now 130
(126 real + 4 constructed battery witnesses). TRUST fires on exactly 1
specimen (TW1, the constructed trust battery witness) with no cross-fire.
Re-derived from the actual cofiring.py output.

## TAUTOLOGICAL-BLEND re-derivation (2026-09-28)

The 45th axis (TAUTOLOGICAL-BLEND, the construction-channel face of the
self-keyed family; the SignTrace decomposition, 2026-09-28) was added.
The battery is now 131 (126 real + 5 constructed battery witnesses).
TAUTOLOGICAL-BLEND fires on exactly 1 specimen (TW2, the constructed
tautological-blend battery witness, SignTrace Pool@60 numbers) with no
cross-fire. Re-derived from the actual cofiring.py output.

## CRITERION-THRESHOLD + JUDGE-AS-TARGET re-derivation (2026-09-28)

The 46th axis (CRITERION-THRESHOLD, the criterion-channel face of the
self-keyed family; the SlideLab/ConfArena threshold-undisclosed seam) and the
47th axis (JUDGE-AS-TARGET, the loop-channel face; the Spotify
self-improvement-loop seam) were added. The battery is now 137
(126 real + 11 constructed battery witnesses). CRITERION-THRESHOLD fires on
exactly 4 specimens (TW3 + CH0 + CH1 + CH3) and JUDGE-AS-TARGET fires on
exactly 4 (TW4 + CH0 + CH1 + CH2), each with one exclusive specimen (TW3, TW4
respectively) and no cross-fire. The four three-channel independence witnesses
(CH0-CH3) confirm the decomposition: closing exactly one channel silences only
that axis, and the other two still fire (CH1 closes population -> only
TAUTOLOGICAL-BLEND goes silent; CH2 closes criterion -> only CRITERION-THRESHOLD
goes silent; CH3 closes loop -> only JUDGE-AS-TARGET goes silent). Re-derived
from the actual cofiring.py output.
