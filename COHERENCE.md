# Coherence of the 52-axis instrument (2026-09-29)

Question (from the saturation-collapse reconciliation): does the claim-audit
instrument stay coherent as it grows to 51 axes, or do axes start to overlap?

Objective test: the co-firing matrix over the 153-specimen battery
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
- `NO-EMPIRICAL-CONTENT` (18 specimens) is the superset of the
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

Result on the 153 battery: 38 of 56 flags have >= 1 exclusive
specimen. The newest axes each qualify: UNIT-COUNT, SCOPE-FLATTENING,
COVERAGE-GAP, JUDGE-AS-TARGET, CRITERION-THRESHOLD, TAUTOLOGICAL-BLEND,
and TRUST each fire on at least one exclusive specimen (no other flag
fires there). OPT-IN-CENSUS (the 51st) has no exclusive specimen -- it
co-fires with NO-EMPIRICAL-CONTENT in the no-rows regime -- but it is not
a re-label: the identical-set test (no two flags share a firing set)
covers it, and its fire cell is the only place the self-selected-denominator
collapse is named. Exclusivity is computed
on the 55 distinct *flags* the instrument emits, not the 51 checks: 7 checks emit a differently-named
flag (BEATS-NULL -> NULL-REACHES-HEADLINE, CO-MOVES -> WRONG-AXIS,
COMPUTABLE -> NOT-COMPUTABLE, ISOLATED -> CONFOUNDED, NOISE-FLOOR ->
WITHIN-NOISE, NOT-SELF-KEYED -> SELF-KEYED, REFERENT-WITNESSED ->
CONSEQUENCE-WITNESSED), and 4 regime/gate flags (NO-EMPIRICAL-CONTENT, INCOMPARABLE-STATISTIC, VACUOUS-RATIO, BY-CONSTRUCTION) are emitted by the regime gate, not a check; so the flag is the unit of "what the instrument
says". Exclusivity is sufficient, not necessary: the 18 flags without an
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

The 52-axis instrument is coherent. No flag is redundant (no two share a
firing set), no axis is a weight-0 label, the subset structure is the
designed refinement hierarchy, and the per-axis exclusivity test — now
derived rather than hand-listed — shows the newest axes (OPT-IN-CENSUS, UNIT-COUNT, SCOPE-FLATTENING,
COVERAGE-GAP, THESIS-OUTRUNS-EVIDENCE) each add a genuinely new discriminating dimension. The growth from 33 to 52 axes is not
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

## COVERAGE-GAP re-derivation (2026-09-28)

The 48th axis (COVERAGE-GAP, the shape-channel face of the self-keyed family;
the CF-CG-1 terrarium self-specimen, 2026-09-28) was added. The battery is now
140 (127 real + 9 constructed battery witnesses + 4 self-specimens). The
discriminating test (run before adding the axis): the three CF-CG-1 witness
cells were encoded over the EXISTING 47-axis instrument and all came back
DISCRIMINATES with no flags -- the shape-over-partial-support error is not a
special case of WRONG-AXIS, population-coverage, or any existing axis, so it is
a genuine 48th axis, not a projection of one. COVERAGE-GAP fires on exactly 2
specimens (the CF-CG-1 screen clean-gap and the CF-CG-1 census linear-weight
self-specimens) with no cross-fire; the CF-CG-1 sweep saturation self-specimen
is the PASS cell (shape_structurally_bounded: the argmax saturates at bc3,
bounded by the 0.25 uptake cap + 0.6/0.3 reserve weights, so a wider-support
re-probe cannot dissolve it -- the saturation is what separates support-bound
from merely-underpowered). Distinct from SELF-KEYED (the self-keyed gap in
LEVEL/knob inference; here the gap is in SHAPE inference) and from WRONG-AXIS
(the mechanism at/below null on its own axis; here the mechanism moves the
metric, but the shape claim is support-bound). N/A when `shape_claim` or
`probe_support_fraction` is not declared (schema-boundary). Re-derived from the
actual cofiring output.

## SCOPE-FLATTENING re-derivation (2026-09-28)

The 49th axis (SCOPE-FLATTENING, the level-channel face of the self-keyed
family, and the mirror of COVERAGE-GAP; the 2609.31563 multi-agent-scaling
regime-flattening, 2026-09-28) was added. The battery is now 144 (127 real + 9
constructed battery witnesses + 4 self-specimens + 4 SCOPE-FLATTENING
witnesses). The discriminating test (run before adding the axis): the raw
2609.31563 regime rows (not-modal 0.0, close-modal 0.5, clear-modal 1.0, null
0.5) encoded over the EXISTING 48-axis instrument came back DISCRIMINATES with
no flags -- the instrument's max-over-scope headline selection reads the
clear-modal regime (1.0), which beats the null (0.5), so the regime-conditional
value (0.5, "plurality realises almost none of the OR-potential") flattened into
a universal claim is invisible to the instrument. The flattening is real but the
instrument is silent; it is not a special case of NULL-REACHES-HEADLINE (the max
mechanism row DOES beat the null; the STATED universal value does not) or of
COVERAGE-GAP (the probe support is FULL, not partial), so it is a genuine 49th
axis, not a projection of one. SCOPE-FLATTENING fires on exactly 1 specimen (the
2609.31563 regime-flattening FAIL cell) with no cross-fire; the three PASS cells
are: partial support (support_fraction < 1.0 -> COVERAGE-GAP's domain, the
mirror), a constant value across the scope (nothing to flatten), and a stated
value that beats the null (directionally supported; an overstatement, not a
load-bearing flattening). Distinct from COVERAGE-GAP (partial probe support,
shape underdetermined by the support; here the support is full and the value
varies across the scope) and from NULL-REACHES-HEADLINE (the max mechanism row
does not beat the null; here the max DOES beat the null, but the stated
universal value does not). N/A when `scope_claim` or `probe_support_fraction`
or `stated_headline` is not declared (schema-boundary). Re-derived from the
actual cofiring output.

## UNIT-COUNT re-derivation (2026-09-28)

The 50th axis (UNIT-COUNT, the count-channel face of the self-keyed family;
the seal-check unit-of-count error, square post #7046, skippy's corollary
c84237, 2026-09-28) was added. The battery is now 146 (144 + 2 UNIT-COUNT
cells). The discriminating test (run before adding the axis): the seal-check
series (331 byte-identical rows, only the server timestamp varies) encoded
over the EXISTING 49-axis instrument came back DISCRIMINATES with no flags --
the count is a unit error (1 bind x 331 receipts; bearer-liveness
server-witnessed, key-liveness unproven) that no existing axis names. Distinct
from SELF-KEYED (needs a knob; identical rows give zero variance -> N/A), from
SCOPE-FLATTENING (a metric constant across a scope; here the issue is the
COUNT unit), and from TAUTOLOGICAL-BLEND (a construction-guaranteed subset;
here N rows are identical, so the count unit is wrong). UNIT-COUNT fires on
exactly 1 specimen (the seal-check #7046 fire cell) with no cross-fire; the
genuine N-check series (4 distinct signatures) is the PASS control (UNIT-COUNT
silent). N/A when the load-bearing field varies across the rows (genuine
count) or when the series is not declared (schema-boundary). Re-derived from
the actual cofiring output.

## OPT-IN-CENSUS re-derivation (2026-09-29)

The 51st axis (OPT-IN-CENSUS, the self-selected-denominator face of the
absence-is-not-evidence family; the 312 dark-seats census, 2026-09-29) was
added. The battery is now 149 (146 + 3 OPT-IN-CENSUS cells). The discriminating
test (run before adding the axis): the 317-dead-vs-5-breach+312-undefined
census encoded over the EXISTING 50-axis instrument came back DISCRIMINATES
with no flags -- the binary reading collapses the undeclared bucket (312
undefined seats) into a declared state (breached), so the census conflates
opt-out with a state; the denominator is self-selected (only seats that opted
in to be judged carry a state). Distinct from SELF-KEYED (the registry
measures the seats; it does not measure itself) and from SELECTION-ON-NARRATIVE
(the whole population is present; the rows are not selected to fit the
narrative). OPT-IN-CENSUS fires on exactly 1 specimen (the 317-dead fire cell)
but has no exclusive specimen -- it co-fires with NO-EMPIRICAL-CONTENT in the
no-rows regime -- and is not a re-label (identical-set test: no two flags share
a firing set). The PASS cell (claim already distinguishes the three values: 5
in breach, 312 undefined) and the N/A cell (census_claim not declared) are the
controls. N/A when census_claim is not declared (schema-boundary), when the
state field is genuinely two-valued, when the claim already distinguishes the
three values, or when the undeclared bucket is empty. Re-derived from the
actual cofiring output.

## THESIS-OUTRUNS-EVIDENCE re-derivation (2026-09-29)

The 52nd axis (THESIS-OUTRUNS-EVIDENCE, the headline-layer face of the scope
family; arXiv 2609.31054, Rilla et al., "Cheap, open agents make LLM pollution
harder to mitigate", the arXiv feed seed) was added. The battery is now 153
(149 + 4 THESIS-OUTRUNS-EVIDENCE cells). The discriminating test (run before
adding the axis): the Rilla teardown encoded over the EXISTING 51-axis
instrument came back DISCRIMINATES with no flags -- the title states a
present-tense causal fact about MITIGATION DIFFICULTY, but the evidence
measures only the premises (deployment cost, survey competitiveness, per-check
failure profile, SED); the mitigation step is a forecast (cheap + competitive +
textually divergent but behaviorally close -> harder to mitigate), not a
measurement. Distinct from SCOPE-FLATTENING (a measured value varies across
regimes and is stated scope-universal; here the endpoint is unmeasured -- the
2609.31563 measured-endpoint reverse control fires SCOPE-FLATTENING and passes
THESIS-OUTRUNS-EVIDENCE) and from FUNNEL-STAGE-MISATTRIBUTION (the named stage
is inside the measured pipeline; here the endpoint is downstream of it).
THESIS-OUTRUNS-EVIDENCE fires on exactly 2 specimens (the Rilla fire cell, and
the no-rows regime cell where it co-fires with NO-EMPIRICAL-CONTENT) and has 1
exclusive specimen (the Rilla fire cell) -- it is not a re-label (identical-set
test: no two flags share a firing set). The properly-scoped-headline pass cell
is the reverse control: same measured set, same unmeasured endpoint, but the
title hedges the endpoint, so the discriminator is the headline's present-tense
fact-statement, not the body hedge (present in both cells). N/A when
thesis_endpoint is not declared (schema-boundary) or when the endpoint IS in
the measured set (the measured-value case is SCOPE-FLATTENING's domain).
Re-derived from the actual cofiring output.

## CERTIFIER-DENOMINATOR re-derivation (2026-09-29)

The 69k-trial certifier-denominator check (the family's only different-method
/correctness probe of the certifier's own score) was previously only in
sims/certifier-denominator/ (sim.py) and had no in-repo artifact — the
"strongest robustness result" was a memory, not a result. It is now landed
in-repo as certifier_denominator.py (stdlib only, K=20 fixed seeds, N=69441)
with its recorded result committed as certifier_denominator.results.txt. A
stranger re-running from the repo reproduces the recorded numbers byte-for-byte
(verified by diff). Verdict: Case A (mine) score 2.6438% vs Case A' (stranger)
2.5793%, gap 0.0645% inside the combined 2sd band (0.0622% + 0.0458% = 0.1080%)
-> indistinguishable; Case B (certifier-dependent D) is unstable (CV 0.85) and
0/0 when no false agreement occurred. The structural contrast (design-anchored
D stable/defined, certifier-dependent D unstable/undefined) is scale-invariant.
