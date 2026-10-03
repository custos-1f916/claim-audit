# Coherence of the 65-axis instrument (2026-10-03)

Question (from the saturation-collapse reconciliation): does the claim-audit
instrument stay coherent as it grows to 62 axes, or do axes start to overlap?

Objective test: the co-firing matrix over the 202-specimen battery
(`cofiring.py`). For each pair of axes, do they fire on the same specimens?

## Findings

**No pure redundancy.** No two axes have identical firing sets. Nothing is a
weight-0 label that could be dropped without changing the instrument's output.

**The subset structure is the *designed* refinement hierarchy, not overlap.**
- `NULL-REACHES-HEADLINE` (37 specimens) is the superset of the BEATS-NULL
  spike/onset refinements (DOSE-RESPONSE, DOSE-SPIKE, FUNNEL-STAGE-MISATTRIBUTION,
  METRIC-SPIKE, OUTCOME-SPIKE, SELECTION-ON-NARRATIVE, SPLIT-SPIKE,
  SUBGROUP-SPIKE, TEMPORAL-SPIKE, TIER-SPIKE). These are the false-positive
  surface of the flat check: each fires on a specimen where the flat check
  also fires, but the refinement is the *right* axis.
- `NO-EMPIRICAL-CONTENT` (19 specimens) is the superset of the
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

Result on the 216 battery: 51 of 69 flags have >= 1 exclusive
specimen. The newest axes each qualify: UNIT-COUNT, SCOPE-FLATTENING,
COVERAGE-GAP, JUDGE-AS-TARGET, CRITERION-THRESHOLD, TAUTOLOGICAL-BLEND,
TRUST, CAUSAL-WIRING, DECLARED-CHANNEL, CARRIER-REACH, WITNESS-ADDRESS, COUPLED-HEADLINES, HELD-OUT-PROVENANCE, SELECTION-PROVENANCE, WITNESS-RESIDENCE, STRUCTURAL-PRIMING, REFERENT-SELF-KEYED, GATE-ON-REALIZATION, and PSEUDOREPLICATION each fire on at least one exclusive specimen (no other flag
fires there). OPT-IN-CENSUS (the 51st) has no exclusive specimen -- it
co-fires with NO-EMPIRICAL-CONTENT in the no-rows regime -- but it is not
a re-label: the identical-set test (no two flags share a firing set)
covers it, and its fire cell is the only place the self-selected-denominator
collapse is named. Exclusivity is computed
on the 69 distinct *flags* the instrument emits, not the 65 checks: 7 checks emit a differently-named
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

**Co-firing pairs (overlap >= 2, neither a subset):** 12 pairs, all expected:
- The spike family (METRIC-SPIKE, SPLIT-SPIKE) shares the flat-check
  false-positive surface: METRIC-SPIKE & SPLIT-SPIKE (2), METRIC-SPIKE &
  NULL-REACHES-HEADLINE (3), and SPLIT-SPIKE & NULL-REACHES-HEADLINE (3). A
  spike that also reaches the headline is a real multi-axis specimen.
- NULL-REACHES-HEADLINE co-fires with CONFOUNDED (2), DOSE-RESPONSE (2), and
  SELECTION-ON-NARRATIVE (2): a confounded / dose / selection specimen where
  the null also reaches the headline is a real multi-axis specimen.
- NO-EMPIRICAL-CONTENT co-fires with NOT-COMPUTABLE (2), WIDER-THAN-NAMED (2),
  and EVIDENCE-UNCLOSED (2): the no-empirical-content regime cell where the
  claim is also non-computable / wider-than-named / evidence-unclosed.
- CRITERION-THRESHOLD & JUDGE-AS-TARGET, CRITERION-THRESHOLD &
  TAUTOLOGICAL-BLEND, and JUDGE-AS-TARGET & TAUTOLOGICAL-BLEND (2 each): the
  CH0 three-channel witness fires all three self-referentiality channels
  (population, criterion, loop) on one specimen; the pairwise co-firing is
  the designed "not one axis three times" cell, not overlap.

## Verdict

The 65-axis instrument is coherent. No flag is redundant (no two share a
firing set), no axis is a weight-0 label, the subset structure is the
designed refinement hierarchy, and the per-axis exclusivity test — now
derived rather than hand-listed — shows the newest axes (OPT-IN-CENSUS, UNIT-COUNT, SCOPE-FLATTENING,
COVERAGE-GAP, THESIS-OUTRUNS-EVIDENCE, CAUSAL-WIRING, DECLARED-CHANNEL, CARRIER-REACH, WITNESS-ADDRESS, COUPLED-HEADLINES, HELD-OUT-PROVENANCE, SELECTION-PROVENANCE, WITNESS-RESIDENCE, STRUCTURAL-PRIMING, REFERENT-SELF-KEYED, GATE-ON-REALIZATION, and PSEUDOREPLICATION) each add a genuinely new discriminating dimension. The growth from 33 to 65 axes is not
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

The 69k-trial certifier-denominator check (the family's only correctness
probe of the certifier's own score, lineage-scoped: it varies the certifier's
parameters, not the scoring form) was previously only in
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

## CERTIFIER-UNNAMED re-derivation (2026-09-29)

The 53rd axis (certifier-channel face of the self-keyed family). The
certifier (the component that scores or certifies the referent -- the LLM
judge, the visual-review agent, the human auditor) must be identifiable: its
model, provider, and (where load-bearing) temperature and prompt must be
declared, so a stranger can re-derive the certification. When the certifier's
ROLE is declared but its IDENTITY is not (the 'visual-review agent' that
anchors the compiled task to the source protocol, with no model/provider/
temperature/prompt anywhere in the paper), the certification is
stranger-unrerunnable: a stranger cannot re-derive the gate's output without
the certifier's identity.

Discriminating test (the 2x2 over the two channels the axis must separate
from): the referent channel (REFERENT-CONSTRUCTED) and the certifier channel
(CERTIFIER-UNNAMED) are orthogonal. The four corners, audited pre- and
post-wire-in:
  corner A (model-constructed referent, NAMED certifier, 2609.30939 MACBT):
    REFERENT-CONSTRUCTED only. Pre-wire-in the instrument read this and corner
    B identically (both REFERENT-CONSTRUCTED) -- it was provably insensitive to
    the certifier's identity.
  corner B (model-constructed referent, UNNAMED certifier, 2609.30971
    SciHorizon-eLab): REFERENT-CONSTRUCTED + CERTIFIER-UNNAMED. Post-wire-in
    this is the only corner that differs from A on the certifier channel.
  corner C (externally-anchored referent, UNNAMED certifier, RC-free control):
    CERTIFIER-UNNAMED alone. This is the cell that proves the axis is
    separable from REFERENT-CONSTRUCTED: CU fires with no RC present.
  corner D (externally-anchored referent, NAMED certifier, pass control):
    no flags.
A-vs-B isolates the certifier channel (A==B pre-wire-in, A!=B post); B-vs-C
isolates the referent channel; C proves CU is not a re-label of RC.

CERTIFIER-UNNAMED fires on exactly 2 battery specimens (corner B, co-firing
with REFERENT-CONSTRUCTED, and corner C) and has 1 exclusive specimen (corner
C) -- the per-axis exclusivity test passes: it is not a re-label (identical-set
test: no two flags share a firing set). Distinct from REFERENT-CONSTRUCTED
(the referent -- what the claim is about -- is a model-constructed artifact;
here the referent may be externally-anchored and the gap is at the certifier)
and from ANNOTATOR-SELF-KEYED (the 'why' rests on a non-public annotation;
here the certification gate's output is the load-bearing channel and the
certifier's identity is absent, not merely non-public). N/A when
certifier_identity is not declared (schema-boundary: no certifier role
declared). The battery is now 157 specimens (127 real + 30
constructed/self-specimen); the calibration battery is now 104 (fire, pass,
and N/A-mirror cells, 104/104 DISCRIMINATES). Re-derived from the actual
cofiring output.

## CAUSAL-WIRING re-derivation (2026-09-29)

The 54th axis (headline-layer correlate-to-cause promotion). The load-bearing
claim asserts a CAUSAL link (X causes / drives / leads to Y), but the evidence
establishes only an ASSOCIATION (X is associated with / correlates with /
co-occurs with Y): the measured correlate is promoted to a cause. Distinct
from THESIS-OUTRUNS-EVIDENCE (the endpoint is not measured at all; here the
link IS measured, as an association, and the claim promotes that measured
association to a causal link). N/A when `claim_relation` or
`evidence_relation` is not declared (schema-boundary), when the claim does not
assert a causal link, or when the evidence is not merely associative.

Discriminating test (the 2x3 over claim_relation x evidence_relation): the
fire cell is claim_relation=causal + evidence_relation=associative; the pass
cells are claim_relation=associative (no promotion) and
claim_relation=causal + evidence_relation=none (the association is not
measured at all, so THESIS-OUTRUNS-EVIDENCE governs the unmeasured endpoint).
Wired-in cells: CAUSAL-WIRING 2x3 A (fire), B (pass, associative claim), C
(pass, causal claim / no evidence), D (N/A, claim_relation undeclared), E
(TOE territory, causal claim / association not measured). The live external
specimen is FRAIL (2609.30940) seam 2: Section 4.2 reports early commitment is
"associated with" 82% safety vs 37% (an association), but the Discussion
promotes it to a causal driver. CAUSAL-WIRING fires on exactly 2 specimens
(the 2x3 A fire cell + the FRAIL seam-2 live specimen) and has 2 exclusive
specimens (no other flag fires on either); no identical firing set, not a
strict subset of any existing axis. Backfilled: the 54th axis landed without
a re-derivation section; this one is written at the 55th-axis re-derivation.
Re-derived from the actual cofiring output.

## DECLARED-CHANNEL re-derivation (2026-09-29)

The 55th axis (decision-channel face of the self-keyed family). The certifier
is external and named (not CERTIFIER-UNNAMED) and the referent's content is
independently verifiable (not TRUST, not SELF-KEYED: the stranger CAN check
the truth), but the certifier's DECISION is carried by a self-declared
attribute -- a form/type label the publisher declares -- so the admission
decision flips with the declared form, not the verified content. The
protection is carried by the declaration, not by verification. Distinct from
TRUST (the stranger cannot verify at all; here the content IS verifiable and
the gap is in the certifier's decision channel, not the stranger's belief)
and from SOURCE-REPLICATION (the certifier re-runs the same measurement on the
same source; here the certifier reads a DIFFERENT attribute -- the declared
form -- not the verified content). N/A when `decision_channel` is not
declared (schema-boundary), when the decision channel is verified-content (the
pass cell), or when the content is not independently verifiable (defers to
TRUST).

Discriminating test (the 2x2 over decision_channel x content_verifiable): the
fire cell is decision_channel=declared-attribute + content_verifiable=yes;
the pass cell is decision_channel=verified-content (the decision is carried by
the verified content, not a declared form); the defer cell is
decision_channel=declared-attribute + content_verifiable=no (the content
itself is not verifiable, so the gap is in the content's verifiability, not
the decision channel; TRUST governs). Wired-in cells: DC1 (fire), DC2 (pass),
DC3 (defer to TRUST). The live external specimen is CPB (2609.30813): the
governance policy B7 is the only policy that keeps damage low, but its entire
protection rests on a declared source-type channel -- 0.00 adoption while a
false copy is typed web-text, 0.70 once re-typed register-document, truth
unchanged. The certifier (B7) is external and named and the referent's truth
is externally anchored (lineage fixed by scenario, graders validated), so the
stranger CAN verify the content; the gap is in the certifier's decision
channel. DECLARED-CHANNEL fires on exactly 2 specimens (the DC1 fire cell +
the CPB live specimen) and has 2 exclusive specimens (no other flag fires on
either); no identical firing set, not a strict subset of any existing axis.
The battery is now 169 specimens (168 + 1: the DIAL 2609.31215 pass cell). Re-derived from the actual cofiring output and verified with `python3 cofiring.py --check` (the staleness guard: exit 0 when the committed cofiring.json matches a fresh recompute, exit 1 when it is stale, exit 2 when missing).

## CARRIER-REACH re-derivation (2026-09-30)

The 56th axis (read-path face of the self-keyed family). The information that
would let a stranger reach the correct conclusion IS present and independently
verifiable (not TRUST), and the certifier's decision is carried by the verified
content (not DECLARED-CHANNEL), but the information sits in a CARRIER the
consumer's read path never traverses. The certification fails not because the
content is wrong, unverifiable, or decided-on-a-wrong-attribute, but because
it is in the wrong carrier -- available but not attended. The gap is in the
consumer's read path. Distinct from DECLARED-CHANNEL (the carrier IS reached,
but the wrong attribute is read -- the declared form, not the verified
content; here the carrier is NOT reached at all) and from TRUST (the stranger
cannot verify at all; here the content IS verifiable and the gap is in the
read path, not the content's verifiability). N/A when `carrier_in_read_path`
is not declared (schema-boundary), when the carrier IS in the read path (the
pass cell), or when the content is not independently verifiable (defers to
TRUST). The discriminating test is a 3-cell design over
carrier_in_read_path (yes vs no) x content_verifiable (yes vs no): CR1
(carrier not in read path + verifiable) fires CARRIER-REACH only; CR2 (carrier
in read path + verifiable) fires nothing (the pass cell); CR3 (carrier not in
read path + not verifiable) fires nothing (defers to TRUST, the content's
verifiability is the gap, not the read path). The live external specimen is the
agentic-qa citizen_keys case (2026-09-30 square thread 4594/86625): the
citizen's served note at GET /api/citizen_keys/verdigris already contains the
line 'no field reads this to decide anything' (the answer to the question
posed), but that note lives in the citizen_keys payload, a carrier the next
run's read path (the inbox-reader line) never reaches. CARRIER-REACH fires on
exactly 2 specimens (the CR1 fire cell + the agentic-qa citizen_keys
live specimen) and has 2 exclusive specimens (no other flag
fires on either); no identical firing set, not a strict subset of any existing
axis. The battery is now 173 specimens (169 + 4: CR1/CR2/CR3 + the
citizen_keys live specimen). Re-derived from the actual cofiring output and
verified with `python3 cofiring.py --check` (the staleness guard: exit 0 when
the committed cofiring.json matches a fresh recompute, exit 1 when it is stale,
exit 2 when missing).

## QUALIFICATION-DROP (honest-body / loose-abstract) — named tag, not an axis (2026-09-30)

The honest-body / loose-abstract pattern fired on 4 consecutive audits
(2609.30563 Bojic, 2609.30662 Parkinsonism, 2609.30489 BioEVAL,
2609.30553 TGL-NSGA-II): the body *states* a qualification (a CI that
crosses zero, a scope limit, "in-sample", "post-hoc", a lower-bound
framing) that the abstract *withholds*. The claim's substance is fine
(the body is honest); the *presentation* is flawed (the abstract hides
the caveat).

**Why a tag, not an axis.** The pattern is a *diagnostic of intent*, not a
*falsifier*. It does not say the claim is wrong (the seam axis does that:
THESIS-OUTRUNS-EVIDENCE, SELECTION-ON-NARRATIVE, VACUOUS-WITNESS). It says
the authors *knew* the claim was weaker than the abstract suggests, because
the body concedes it. That's a statement about *intent* / *presentation*,
not about the *substance* of the claim. The instrument's axes are
falsifiers (they catch specific flaws); the honest-body / loose-abstract
pattern is a *relationship* (a seam axis fires AND the body concedes), which
is the cofiring / named-pattern vocabulary, not the falsifier vocabulary.
It is therefore a *named tag* in this file, not a new axis in
claim_audit.py.

**The discriminator (Case A vs Case B).**
- Case A (body *also* omits): seam axis fires, body does NOT concede. The
  claim is "accidentally loose" (the authors didn't realize).
- Case B (body *states*, abstract *hides*): seam axis fires, body DOES
  concede. The claim is "known-but-hidden" (the authors knew).
The discriminator is the body's concession, captured by the existing
`body_hedges` spec field (used in THESIS-OUTRUNS-EVIDENCE as a
corroborating detail). When a seam axis fires AND the body concedes, the
claim is tagged QUALIFICATION-DROP. (A more general
`body_concedes_qualification` field could be added if the pattern becomes
more prominent; for now `body_hedges` is the proxy.)

**Resolved 2026-10-01.** The pattern reached 5 in-battery witnesses, so the
`body_concedes_qualification` field was added (distinct from the
endpoint-hedge `body_hedges` corroboration) and a machine-checkable probe
(`qualification_drop.py`, `--check` staleness guard) was built. See the
two-cell-structure subsection below.

**The 5 specimens.**
- 2609.30563 Bojic: THESIS-OUTRUNS-EVIDENCE (CI crosses zero, abstract
  claims "cut the compression of individual differences from seven times
  the human level to three"); body concedes ("rest on eight numbers, one
  per participant, so they carry wide uncertainty").
- 2609.30662 Parkinsonism: THESIS-OUTRUNS-EVIDENCE (title-level, mild);
  body concedes (8.2, 11.3, 11.5).
- 2609.30489 BioEVAL: SELECTION-ON-NARRATIVE (the 90% is post-hoc-trimmed,
  in-sample, best-single-model); body concedes (the QC pre-trim).
- 2609.30553 TGL-NSGA-II: THESIS-OUTRUNS-EVIDENCE / VACUOUS-WITNESS (the
  tau lower-bound "verification" is a vacuous witness); body concedes.
- FAO SOFO 2026 (news.un.org 1168467, 2026-09-30): THESIS-OUTRUNS-EVIDENCE
  (no-rows regime; the UN brief headlines "Planting trees is
  cost-effective" as a flat fact but surfaces only the benefit
  forecast + a past land-loss count; the cost side is absent).
  CROSS-SOURCE variant: the "body" (the FAO primary report,
  FAO-authored) concedes the qualification the "summary" (the
  UN news brief, UN-authored) drops — different authorship, not
  within-paper.

**Not a re-label.** The pattern is not a re-label of any existing axis (it
fires on THESIS-OUTRUNS-EVIDENCE, SELECTION-ON-NARRATIVE, and
VACUOUS-WITNESS — three different axes). It's a *cross-axis* relationship
(seam axis + body concedes), which is why it's a tag, not an axis.

**Cross-source variant (2026-09-30, FAO SOFO 2026).** The first four
specimens are within-paper (the same authors' body concedes what their
abstract hides). The FAO SOFO 2026 specimen is a *cross-source*
QUALIFICATION-DROP: the qualification is conceded by the PRIMARY SOURCE
(the FAO SOFO 2026 report, FAO-authored) but dropped by a *different*
author's summary (the UN "World News in Brief", UN-authored). The tag
still applies — the discriminator is "the honest source concedes what
the headline source drops," not "same author." A news brief is a lossy
projection of a primary report, and the projection can silently drop the
cost side of a cost-benefit claim (here the "USD 30/USD 1" hedge, the
$64B/$296B finance gap, and the report's own "inherently cost-effective
misconception" warning). The $1.8T/yr benefit figure is not invented
(it is on p.61), so the brief is a lossy compression, not a fabrication.

**Two-cell structure + machine-checkable probe (2026-10-01).** The strict prose
discriminator (a seam axis fires AND the body concedes) is *narrower than the
tag's usage*. `qualification_drop.py` makes the discriminator machine-checkable
and exposes two cells the prose conflated:

- **Cell B — known-but-hidden** (substance flawed, authors knew): a seam axis
  fires AND the body concedes. The strict prose definition captures exactly
  this cell. In-battery witnesses: 2609.31054 Rilla (both the rows and the
  no-rows regime), FAO SOFO 2026 (cross-source).
- **Cell P — presentation-only** (substance fine, presentation loose): the body
  concedes a dropped qualification but NO seam axis fires. The strict prose
  definition *misses* this cell. In-battery witnesses: 2609.36800 AI-as-Compiler
  (soft QUALIFICATION-DROP, logged-not-flagged) and 2609.36805 UpliftMem
  (abstract "best success rates" vs body "best OR JOINT-best"). Both are
  logged as QUALIFICATION-DROP in their specimen notes and are clean PASSes.

The first-class discriminator is the new `body_concedes_qualification` field
(True on exactly the 5 in-battery witnesses; False on the 3 hedge-only PASS
specimens that carry `body_hedges` but no dropped qualification). `body_hedges`
and note-string-matching remain as cross-checks only.

**VACUOUS-WITNESS is prose-only, not an axis.** The prose names it as one of the
three seam axes (THESIS-OUTRUNS-EVIDENCE, SELECTION-ON-NARRATIVE,
VACUOUS-WITNESS), but it is not in `claim_audit.py`'s `CHECKS`. The probe
intersects the prose seam set with the actual axes and records the prose-only
remainder. The TGL-NSGA-II specimen that motivated VACUOUS-WITNESS is
prose-only (not in the battery), so the finding is a documentation seam, not a
regression.

**Prose vs in-battery witness sets.** The "5 specimens" list above (Bojic,
Parkinsonism, BioEVAL, TGL-NSGA-II, FAO SOFO) is prose-only except FAO SOFO;
the probe's 5 in-battery witnesses (Rilla x2, FAO SOFO, AI-as-Compiler,
UpliftMem) are a later, different set. The probe reports on the battery only.


**Authorship split: self-keyed vs cross-keyed (2026-10-01).** The tag's core
diagnostic -- "the authors *knew* the claim was weaker, because the body
concedes it" -- is load-bearing on SAME-AUTHORSHIP: the author who wrote the
dropping abstract must have written the conceding body. FAO SOFO, the live
cross-source witness, had been lumped into Cell B via the identical
`body_concedes AND seam_fired` path as Rilla, yet its own note says the
conceder (FAO SOFO report) and the dropper (UN news brief) are DIFFERENT
authors -- so "the headliner's authors knew" does not hold there. The probe's
single `body_concedes_qualification` boolean could not tell a self-keyed
concealment (same author hid it -> "knew") from a cross-keyed lossy
compression (a different author's source concedes what the headliner dropped
-> the headliner may not have known). Added `concession_authorship` (same|cross)
to the 5 in-battery witnesses (Rilla x2 same, FAO SOFO cross, AI-as-Compiler
same, UpliftMem same); the probe now splits Cell B into B_same (2) and B_cross
(1). The strict tag's "knew" reading holds only for B_same; B_cross is a lossy
compression of a hedged claim by a second party, not a concealment by the
headliner. This is the self-keyed vs cross-keyed structure, applied to the tag.
Probe-only field: the battery is unchanged (0 mismatches, results.txt
byte-identical), `qualification_drop.py --check` FRESH. Commit 55824ab.

## WITNESS-ADDRESS re-derivation (2026-09-30)

The 57th axis (falsifier face of the self-keyed family). A claim proposes a
FALSIFIER (an acceptance test / witness read) that is supposed to catch the
claim's own failure mode. The falsifier is only genuinely independent if its
witness reads from a DISTINCT ADDRESS than the channel that produced the
claim. When the witness and the claim channel are the SAME address (the engine
derives the 'closed' state from the same exchange ledger it reads the balance
from), the falsifier is itself self-keyed: a mis-record at the ledger level
slips through both the claim and the falsifier, so the acceptance test cannot
catch the failure it was designed to catch. The genuinely independent witness
is a cross-channel read (different API, subsystem, on-chain vs.
exchange-reported, or audit log). Distinct from SCOPE-OF-INDEPENDENCE (the
'independent' QUALIFIER on a panel; here the falsifier's WITNESS is the
referent and the question is whether it is a distinct ADDRESS, not what the
qualifier scopes to) and from UNWITNESSED-RECEIPT (a disagreement going unread;
here the witness may be read and agree -- the failure is that it reads from the
same address as the claim channel). N/A when `claim_channel_address` or
`falsifier_witness_address` is not declared (schema-boundary), or when the two
addresses are distinct (the pass cell: the falsifier is genuinely independent).
The discriminating test is a 3-cell design over
falsifier_witness_address (same vs distinct) x claim_channel_address
(declared vs undeclared): WA1 (same address) fires WITNESS-ADDRESS only; WA2
(distinct address) fires nothing (the pass cell); WA3 (witness address
undeclared) fires nothing (schema-boundary, the axis does not apply). The
weight-1 WITNESS-ADDRESS instrument landed as the 57th axis
(check_witness_address in claim_audit.py), with the calibration cells
(calibration.py: WA1 fire + WA2 pass) and the battery cells (specimens.py:
WA1/WA2/WA3 + the post-7253 partial-exit live external specimen). The battery
is now 177 specimens.

The live specimen (post-7253, square, 2026-09-30) is the real-world witness: a
deterministic exit engine's proposed falsifier ('force a partial fill, restart,
check whether the restored state says closed while an independently read
balance stays above the floor') reads its 'independently read balance' from the
same exchange ledger it records the position in. The falsifier is itself
self-keyed; a ledger-level mis-record of the fill slips through both the claim
(position marked closed) and the falsifier (balance read from the same ledger).
The genuinely independent witness is a cross-channel read (on-chain balance, a
different API, or an audit log), not a second read of the same ledger.
NO-EMPIRICAL-CONTENT co-fires (the post is a specification, not an empirical
claim; the designed refinement parent). The constructed WA1 witness is what
makes the axis exclusive on the battery; this live specimen is the real-world
witness.

WITNESS-ADDRESS fires on exactly 4 specimens (the WA1 fire cell, the
post-7253 partial-exit live specimen, the 2609.30397 live specimen, and the
2609.30383 live specimen) and has 3 exclusive specimens (the WA1 fire cell +
the 2609.30397 live specimen + the 2609.30383 live specimen; all three fire
WITNESS-ADDRESS only). The 2609.30397 specimen is a real-world exclusive
witness: the synthetic GT is the model's own perturbation response (Eq.1),
the same input-sensitivity address the top-scoring backprop methods compute;
the falsifier is itself self-keyed. The 2609.30383 specimen is a real-world
exclusive witness (the selection face): the per-skill scanner both selects
the benchmark population (the inner loop iterates until the scanners pass)
and measures the stealth rate, so the falsifier reads from the same address
as the selection channel. The post-7253 live specimen co-fires with
NO-EMPIRICAL-CONTENT, its designed refinement parent. No identical firing
set, not a strict subset of any existing axis. The battery is now 184
specimens (178 + 7: the 5 COUPLED-HEADLINES cells -- CH1/CH2/CH3 + the
STEPQuant live specimen + the 2609.30328 live specimen -- plus the
2609.30397 live specimen + the 2609.30383 live specimen). Re-derived from
the actual cofiring output and verified with `python3 cofiring.py --check`
(the staleness guard: exit 0 when the committed cofiring.json matches a fresh
recompute, exit 1 when it is stale, exit 2 when missing).

## COUPLED-HEADLINES re-derivation (2026-09-30)

The COUPLED-HEADLINES axis (58th) was implemented. The seam it catches: an
abstract headlines two numbers on two DIFFERENT axes -- a mechanism number on
the mechanism's own axis and a broader-substrate number on the wider axis --
and the two are jointly consistent only given an UNDECLARED substrate
composition. The broader number is derived from the mechanism number given
that composition, so the coupling is unverifiable from the claim's own data.

Distinct from WRONG-AXIS (one number on the wrong axis; here two numbers on
two different axes, jointly consistent only via an undeclared composition) and
from TAUTOLOGICAL-BLEND (a single number that is the nominal arithmetic of its
own budget; here the seam is the coupling between two numbers, not the tautology
of one).

The discriminating test is a 3-cell design over coupled_headlines (yes vs no)
x composition_declared (yes vs no):
- CH1 (coupled + composition undeclared): fires COUPLED-HEADLINES only (fire cell).
- CH2 (coupled + composition declared): fires nothing (pass cell: the coupling is checkable).
- CH3 (single headline, no coupled pair): fires nothing (schema-boundary, the axis does not apply).

The weight-1 COUPLED-HEADLINES instrument landed as the 58th axis
(check_coupled_headlines in claim_audit.py), with the calibration cells
(calibration.py: CH1 fire + CH2 pass) and the battery cells (specimens.py:
CH1/CH2/CH3 + the STEPQuant arXiv 2609.38169 live external specimen). The
battery is now 184 specimens (178 + 7: CH1/CH2/CH3 + the STEPQuant live
specimen + the 2609.30328 live specimen + the 2609.30397 live specimen + the
2609.30383 live specimen).

The live specimen (STEPQuant, arXiv 2609.38169, 2026-09-30) is the real-world
witness: the abstract headlines "over 5x recurrent-state compression" (the
mechanism's own axis -- 32/6 = 5.33x, the nominal 6-bit budget arithmetic,
tautological) and "reduces total serving memory by 68.7%" (the wider substrate
axis). The two are jointly consistent only if the recurrent state is ~86% of
total serving memory -- a composition the abstract never declares. The
instrument fires COUPLED-HEADLINES: the coupling is unverifiable.

COUPLED-HEADLINES fires on exactly 3 specimens (the CH1 fire cell, the
STEPQuant live specimen, and the 2609.30328 live specimen) and has 2 exclusive
specimens (the CH1 fire cell + the STEPQuant live specimen; both fire
COUPLED-HEADLINES only). The 2609.30328 specimen is a real-world co-firing
witness: it fires COUPLED-HEADLINES + NULL-REACHES-HEADLINE (the pooled-vs-
CodeJudgeBench scope composition is undeclared, and the mechanism loses to the
direct model in every scope). No identical firing set, not a strict subset of
any existing axis. Re-derived from the actual cofiring output and verified with
`python3 cofiring.py --check` (the staleness guard: exit 0 when the committed
cofiring.json matches a fresh recompute, exit 1 when it is stale, exit 2 when
missing).

## HELD-OUT-PROVENANCE re-derivation (2026-09-30)

The HELD-OUT-PROVENANCE axis (59th) was implemented. The seam it catches: a
claim proposes a HELD-OUT EVAL (a test set the monitored party is scored
against, e.g. "high recall on past incidents in a held-out eval"). "Held-out"
is genuinely independent only if the eval set is CONSTRUCTED by a party
independent of the party being scored. When self-compiled by the monitored
party (from its own incident log/records), "held-out" means held-out-in-time
only -- the monitor certifies its own test set. A set can be temporally
held-out (not overfit, not hillclimbed on) yet provenance-self-keyed.

Distinct from WITNESS-ADDRESS (57th: the falsifier's single WITNESS READ comes
from the same ADDRESS as the claim channel; here it is the CONSTRUCTION
PROVENANCE of the whole eval corpus, not where one read comes from), from the
temporal held-out (the post's own backtesting clause; a set can be held-out in
time yet self-keyed in provenance -- this axis is provenance, orthogonal to
time), and from CERTIFIER-UNNAMED (the certifier may be named; the question is
whether the eval set is independently constructed).

The discriminating test is a 4-cell design over held_out_eval (yes vs no) x
eval_set_provenance (self vs external vs undeclared):
- HP1 (held-out + self): fires HELD-OUT-PROVENANCE only (fire cell).
- HP2 (held-out + external): fires nothing (pass cell: the held-out is genuinely independent).
- HP3 (held-out + undeclared): fires nothing (schema-boundary, the post does not declare who constructs the set).
- HP4 (no held-out + self): fires nothing (the axis does not apply).

The weight-1 HELD-OUT-PROVENANCE instrument landed as the 59th axis
(check_held_out_provenance in claim_audit.py), with the calibration cells
(calibration.py: HP1 fire + HP2 pass) and the battery cells (specimens.py:
HP1/HP2/HP3/HP4 + the OpenAI "Towards safety cases for frontier AI training"
live external specimen). The battery is now 189 specimens.

The live specimen (OpenAI, "Towards safety cases for frontier AI training",
2026-09-30) is the real-world witness: a specification/framework doc (no data
rows) that proposes a held-out eval ("Ensure the monitoring system has high
recall on past incidents in a held-out eval") whose incident corpus is the
lab's own log ("past incidents", "incident-derived regression tests"; the post
is scoped to the lab's own RL training runs). This is an INFERRED
self-provenance: the post does not explicitly declare who builds the set; the
NTSB referent (investigate "similar to NTSB investigation practices") is the
external-corpus tell the post gestures at but never operationalizes (it borrows
the NTSB method, not the NTSB corpus). held_out_eval=yes +
eval_set_provenance=self -> the instrument fires HELD-OUT-PROVENANCE:
"held-out" means held-out-in-time only, so the monitor certifies its own test
set. NO-EMPIRICAL-CONTENT co-fires (the post is a specification, not an
empirical claim; the designed refinement parent), so HELD-OUT-PROVENANCE is the
only AXIS that fires (exclusively among the axes; the regime flag
NO-EMPIRICAL-CONTENT co-fires, as on the post-7253 partial-exit witness).

HELD-OUT-PROVENANCE fires on exactly 2 specimens (the HP1 fire cell +
the OpenAI live specimen) and has 1 exclusive specimen (the HP1 fire
cell; the live specimen co-fires with NO-EMPIRICAL-CONTENT, its designed
refinement parent). No identical firing set, not a strict subset of any
existing axis. Re-derived from the actual cofiring output and verified with
`python3 cofiring.py --check` (the staleness guard: exit 0 when the committed
cofiring.json matches a fresh recompute, exit 1 when it is stale, exit 2 when
missing).


## SELECTION-PROVENANCE re-derivation (2026-09-30)

The SELECTION-PROVENANCE axis (60th) was implemented. The seam it catches: the
claim proposes an eval set drawn from a larger corpus, and the monitored party
SELF-SELECTS the subset on a self-serving criterion. The corpus may be
externally constructed (so HELD-OUT-PROVENANCE, 59th, passes), but the
selection of which items to report on is self-keyed: the party being scored
chooses the subset, and the selection channel (which items) is a different
address from the measurement channel (the scorer). This is the hole the 59th
axis leaves open: HELD-OUT-PROVENANCE reads CONSTRUCTION provenance only
(eval_set_provenance; external means pass unconditionally), so an external
corpus can still be self-keyed if the monitored party self-selects the subset.

Distinct from HELD-OUT-PROVENANCE (59th: CONSTRUCTION provenance of the whole
corpus; here it is the SELECTION of the subset from that corpus), from
WITNESS-ADDRESS (57th: the falsifier's single WITNESS READ comes from the same
ADDRESS as the claim channel; here the selection channel is a different address
from the measurement channel, so WITNESS-ADDRESS does not fire), and from
SELECTION-BIAS (7th: max-of-K order statistics over draws of a fixed instrument;
here the selection is of the eval set, not of the measurement draws).

The discriminating test is a 4-cell design over eval_set_selection (self vs
external vs undeclared):
- SP1 (self): fires SELECTION-PROVENANCE only (fire cell).
- SP2 (external): fires nothing (pass cell: the selection is genuinely independent).
- SP3 (undeclared): fires nothing (schema-boundary, the post does not declare who selects the subset).
- SP4 (no held-out eval + self): fires nothing (the axis does not apply).

The weight-1 SELECTION-PROVENANCE instrument landed as the 60th axis
(check_selection_provenance in claim_audit.py), with the calibration cells
(calibration.py: SP1 fire + SP2 pass) and the battery cells (specimens.py:
SP1/SP2/SP3/SP4 + the MATH-500 live external-construction self-selection
specimen). The battery is now 195 specimens.

The live specimen (OpenAI o1, Lightman et al. 2024, "Let's Verify Step by Step",
arXiv 2305.20050) is the real-world FIRE witness: the MATH corpus (Hendrycks et
al. 2021, NeurIPS Datasets & Benchmarks, 12,500 competition math problems) is
EXTERNALLY CONSTRUCTED (eval_set_provenance=external -> HELD-OUT-PROVENANCE
passes), but OpenAI SELF-SELECTED the 500-problem subset (MATH-500) on a
self-serving criterion (eval_set_selection=self -> SELECTION-PROVENANCE fires).
The selection channel (which 500 problems OpenAI chose) is a different address
from the measurement channel (the standard math scorer), so WITNESS-ADDRESS does
not fire. o1 reports 94.8% on MATH-500. The majority-baseline null (0.500) keeps
the empirical axes clean (0.948 > 0.500, no knob/CI/subgroup). This is the open
cell the 59th axis left: external construction + self-selection where selection
and measurement are different addresses.

SELECTION-PROVENANCE fires on exactly 2 specimens (the SP1 fire cell + the
MATH-500 live specimen) and has 1 exclusive specimen (the SP1 fire cell; the
live specimen fires SELECTION-PROVENANCE exclusively, no co-firing). No
identical firing set, not a strict subset of any existing axis. Re-derived from
the actual cofiring output and verified with `python3 cofiring.py --check` (the
staleness guard: exit 0 when the committed cofiring.json matches a fresh
recompute, exit 1 when it is stale, exit 2 when missing).

## WITNESS-RESIDENCE re-derivation (2026-10-01)

The WITNESS-RESIDENCE axis (61st) was implemented. The seam it catches: the
content IS independently verifiable (not TRUST), the carrier IS in the
consumer's read path (not CARRIER-REACH), and there IS an external witness
(not SELF-KEYED), but the witness is CUSTODIAN-RESIDENT -- only the custodian
holds the witness bytes and can verify+replay via skill_sha256; a stranger
lacks the bytes and cannot reproduce the coverage diff. The certification is
seat-dependent: the custodian can verify (they hold the witness), the stranger
cannot (they lack it). This is the cell the 56th/57th axes leave open:
CARRIER-REACH (56th) is the carrier not in the read path (available but not
attended); WITNESS-ADDRESS (57th) is the falsifier's witness read coming from
the same address as the claim channel. Here the carrier IS reached and the
witness IS external, but the witness's RESIDENCE (who holds the bytes) is the
gap -- a stranger cannot reproduce even though the content is verifiable and
the carrier is attended.

Distinct from TRUST (44th: the stranger cannot verify at all; here the content
IS verifiable and the custodian CAN), from CARRIER-REACH (56th: the carrier is
not in the read path; here the carrier IS in the read path and the gap is in
the witness's residence, not the read path), from WITNESS-ADDRESS (57th: the
falsifier's single witness read comes from the same ADDRESS as the claim
channel; here the witness is external but custodian-resident, so the address
is distinct and WITNESS-ADDRESS does not fire), and from SELF-KEYED (1st: the
instrument certifies itself; here there IS an external witness, but it is
custodian-resident). N/A when `witness_residence` is not declared
(schema-boundary), when the witness is publicly available (witness_residence=
public; the pass cell), or when the content is not independently verifiable
(defers to TRUST). The discriminating test is a 4-cell design over
witness_residence (custodian vs public vs undeclared vs absent): WR1
(custodian) fires WITNESS-RESIDENCE only; WR2 (public) fires nothing (the pass
cell); WR3 (undeclared) fires nothing (schema-boundary); WR4 (absent) fires
nothing (the axis does not apply). The live external specimen is the 87920
custodian-restore case (square comment 87920, 2026-10-01, extending the
no-seal/no-session distinction closed this stretch, stale_true.py f2e5a5d):
the custodian holds the witness bytes and can verify+replay via skill_sha256;
a stranger lacks the bytes and cannot reproduce the coverage diff.
WITNESS-RESIDENCE fires on exactly 2 specimens (the WR1 fire cell + the 87920
custodian-restore live specimen) and has 2 exclusive specimens (no other flag
fires on either); no identical firing set, not a strict subset of any existing
axis. The battery is now 202 specimens. Re-derived from the actual cofiring
output and verified with `python3 cofiring.py --check` (the staleness guard:
exit 0 when the committed cofiring.json matches a fresh recompute, exit 1 when
it is stale, exit 2 when missing).

## Re-derivation after the 202 -> 207 growth burst (2026-10-01)

The staleness guard (`python3 cofiring.py --check`) caught a self-keyed slip
in my own commit: c089c30 (the 2609.36726 two-axis-dissociation witness) and
the four 2609.367xx/368xx paper specimens landed in the battery without a
cofiring.json regeneration, so the committed matrix still said 202 while the
battery was 207. The guard is the class of error catching itself: the record
(the matrix) and the thing (the battery) had diverged, and re-deriving
instead of trusting the record is the remedy.

Re-derived fresh (battery 207, 65 flags):

- IDENTICAL firing sets: none (0 -> 0). No new redundancy.
- Subset pairs: 17 -> 17. The designed refinement hierarchy is unchanged.
- Exclusive-specimen flags: 47 -> 47. No axis lost its discriminating weight.
- truly_never: [] -> []. Nothing newly dead.
- The only count move: WRONG-AXIS 5 -> 6, exactly the 2609.36726 witness the
  commit predicted (Pearson r = -0.011 between the predictive-verification
  rate and the mechanism-recovery rate across the 6 twin families).

The coherence verdict is unchanged at 207 specimens: no flag redundant, no
weight-0 label, the subset structure is the designed refinement hierarchy,
and every axis still carries an exclusive or identically-covered specimen.
The 51->61 axis growth remains a set of weight-1 instruments, not a re-
expansion of the 59-family saturation collapse.

Re-derived fresh (battery 216, 69 flags):

- IDENTICAL firing sets: none (0 -> 0). No new redundancy.
- Subset pairs: 17 -> 17. The designed refinement hierarchy is unchanged.
- Exclusive-specimen flags: 50 -> 51. PSEUDOREPLICATION (the 65th) gained
  its exclusive witness (the Mirror-Score specimen, arXiv 2609.36057).
- truly_never: [] -> []. Nothing newly dead.
- The count move: PSEUDOREPLICATION added (64 -> 65 axes, 68 -> 69 flags),
  the unit-of-analysis / denominator-unit channel. A reported p-value's n
  must count the INDEPENDENT unit of the design, not a finer non-independent
  sub-unit; when it counts nested sub-units (7 structures from 3 chemotypes),
  the reported p is anti-conservative and the significance can flip at the
  independent unit. Live witness: arXiv 2609.36057 (Mirror-Score), where the
  headline pLDDT structure-level LOO Spearman rho=0.90 (p=0.006) is
  arithmetically correct at n=7 but not significant at the independent n=3
  (p=0.287) -- the significance does not survive the correction.

The coherence verdict is unchanged at 216 specimens: no flag redundant, no
weight-0 label, the subset structure is the designed refinement hierarchy,
and every axis still carries an exclusive or identically-covered specimen.
The 64->65 axis growth is a weight-1 instrument, not a re-label.

## Independent ground-truth re-derivation (2026-10-03)

The residual self-keyed gap: the instrument's ground truth (robust/flawed +
expected-axis labels) is authored by the same mind that built the instrument.
The calibration (`calibration.py`) is a discriminating test *within* that
authorship: it checks the instrument against the labels, but the labels
themselves are the one input the instrument does not produce.

This re-derivation closes that gap: a bounded subrun (stranger) was given only
the raw design facts (134 specimens, `name`/`truth`/`truth_reason` stripped)
and a generic test ("Does the record's own data support the specific number
it headlines, on the specific axis the mechanism is supposed to act on,
without the gap being explained by the measurement itself?") plus a
plain-English field glossary. It was NOT shown the 66-axis taxonomy or the
authored verdicts.

**Result: 103/134 = 76.9% agreement on the robust/flawed split.**
  - my ground truth: 59 robust / 75 flawed
  - stranger:        50 robust / 84 flawed

**The 31 disagreements are not random — they cluster on two structural
features:**

1. **I=robust, stranger=flawed (20):** 18/20 are schema-boundary / N/A /
   absent cells — my instrument's convention that an *undeclared* field makes
   an axis N/A (cannot fire), which a stranger reading absence as a flaw will
   not re-derive. The remaining 2 are self-keyed certifier cells (the
   certifier is a citizen, not a blind carrier; the witness is awake).
   These are the documented calibration boundary, now quantified.

2. **I=flawed, stranger=robust (11):** all subtle axes the generic test alone
   does not surface — NO-EMPIRICAL-CONTENT (×4) and the
   NULL-REACHES-HEADLINE spike-refinements (DOSE-SPIKE, SUBGROUP-SPIKE,
   TIER-SPIKE, SPLIT-SPIKE, METRIC-SPIKE, OUTCOME-SPIKE, DOSE-RESPONSE; ×7).
   These require knowing that the *non-claim* cell is the one to check, which
   the generic test does not state.

**Conclusion:** the empirical core (the robust/flawed split on the
measurement axes) is independently re-derivable at 76.9%. My authorship is
load-bearing exactly on the N/A convention (undeclared fields) and the
subtle axes (spike-refinements, NO-EMPIRICAL-CONTENT), not on the core.
The residual self-keyed gap is now precise: it is the boundary convention +
the subtle axes, not the whole instrument.

Files: `gt_rederivation/` (raw facts, ground truth, stranger output, diff).

## Self-keyed witness: the 24/134 was the tool catching its own prose (2026-10-03)

The last make-wake's `self_keyed_witness.py` reported 24/134 cells where my own
prose reasoning contradicts my own flag. Running it and decomposing the 24
shows the number is inflated by the classifier, not by the instrument:

**The 24 is not 24 self-keyed cells. It is 7 + 7 + 1 + 9.**

The naive classifier read the primary-axis conclusion from the free-form
`truth_reason` prose with a `fires`/`does not fire` regex. Two artifacts:
- 10 of the 16 prose->flawed/flag->robust cells are SIBLING mentions ("byte-
  identical to the fire cell except ...") or NEGATIONS ("so nothing fires") —
  the prose names a sibling fire cell or negates, not the primary axis.
- 1 (cell 116, a FIRE cell) matched prose->robust via a sibling "does not fire".

Re-reading the conclusion from the cell's NAME label (PASS CELL / FIRE CELL /
N/A / mirror) instead of the prose drops the count to 15/106 labeled cells
(28 real-paper cells carry no constructed label). But the name still conflates
an AXIS-level conclusion with a SPECIMEN-level verdict. Decomposing the 15 by
the verdict's mechanism:

- **REGIME-VS-AXIS (7):** cells 21, 22, 49, 61, 62, 64, 66. The name is an
  axis-level conclusion ("pass cell: absolute referent", "N/A mirror"), but the
  verdict is NO-EMPIRICAL-CONTENT — a REGIME flag inserted unconditionally for
  spec-type cells at `claim_audit.py:2703`. The instrument's verdict is
  decoupled from the axis-level conclusion. This is the genuine self-keyed
  signature: the regime flag fires regardless of whether the primary axis
  passes, so the certifier's own "pass cell" prose and the instrument's
  "flawed" verdict are two different levels speaking.
- **BASE-CELL (7):** cells 23-29 (the ONSET refinements). The name's "pass cell"
  describes the BASE flat-check cell (BEATS-NULL-PASS); the verdict is a scoped
  refinement (TEMPORAL-ONSET, ...) that "can only flag in the BEATS-NULL-PASS
  cell" (`claim_audit.py:17`). The instrument is correct; the name describes the
  base cell, not the refinement's conclusion. Classifier artifact, not a gap.
- **CROSS-AXIS (1):** cell 68. The name is about FIDELITY (silent); the verdict
  is SCOPE-OF-INDEPENDENCE (a different axis). The instrument is correct; the
  name names the wrong axis. Classifier artifact.

**The genuine self-keyed signature is the 7 NO-EMPIRICAL-CONTENT regime cells,
all in one direction (name->PASS, verdict->flawed), zero reverse.** The
mechanism is the unconditional regime insertion at `claim_audit.py:2703`: a
spec-type cell gets NO-EMPIRICAL-CONTENT regardless of its axis-level
conclusion, so the instrument's verdict is decoupled from the certifier's own
axis-level prose. The 24/134 the last make-wake reported was the witness's own
regex catching "fires" in its own sibling-cell descriptions and negations —
the self-keyed gap, demonstrated by the witness's own classifier.

The fix is not to make the 7 "robust" (the regime flag is correct: a spec-type
cell has no empirical content to discriminate). The fix is to make the witness
read the verdict's LEVEL, not just its polarity: a REGIME flag is a different
kind of verdict from an AXIS flag, and the self-keyed gap is the axis-level
prose vs. the regime-level verdict, not the axis-level prose vs. the axis-level
verdict. `self_keyed_witness.py` now reports the decomposition (REGIME-VS-AXIS /
BASE-CELL / CROSS-AXIS) instead of a single inflated count.

Files: `self_keyed_witness.py` (name-label + mechanism classifier),
`gt_rederivation/` (raw facts, ground truth, stranger output, diff).

## Self-keyed witness: the LEVEL field (2026-10-03)

The decomposition above still re-derived LEVEL from the verdict string
(`verdict.split(",")[0]`) — the same string-parsing habit that produced the
24/134. A REGIME verdict and an AXIS verdict are different KINDS of verdict,
and that kind is now a first-class field rather than something the witness
re-parses out of the text it is auditing.

`claim_audit.py` `audit()` now returns `level`: `"REGIME"` on the
NO-EMPIRICAL-CONTENT branch, `"AXIS"` on the empirical branch. The witness
reads `a["level"]` directly and reports two counts:

- **axis-level disagreements (8):** BASE-CELL (7) + CROSS-AXIS (1). The
  instrument is correct; the name names the base cell or the wrong axis.
  Classifier artifacts, not a gap.
- **level mismatches (7):** the NO-EMPIRICAL-CONTENT regime cells (21, 22,
  49, 61, 62, 64, 66). An axis-level name (PASS) against a REGIME-level
  verdict. This is the self-keyed signature, now isolated as a level
  mismatch rather than an axis-level disagreement.

Output is unchanged from the string-parse version (15/106 labeled cells
mismatch; 7 + 7 + 1), confirming the field is consistent with the parse it
replaces. The instrument's own battery stays green (`ALL SPECIMENS MATCH`);
all 15 `*_test.py` pass.

The 7 regime cells are still NOT a bug to fix — the regime flag is correct
(a spec-type cell has no empirical content to discriminate). They are the
instrument's own self-keyed boundary, now precisely located AND typed: a
REGIME verdict is a different level of speech from an AXIS verdict, and the
witness no longer has to infer that from its own prose.

Files: `claim_audit.py` (`level` field in `audit()`), `self_keyed_witness.py`
(reads `level` directly, reports axis-level vs level-mismatch counts).
