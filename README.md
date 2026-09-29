# claim-audit

A 55-axis falsification instrument for empirical claims in ML/AI papers
(and other headline claims with data). Given a claim's raw numbers as a
spec, it checks the claim against 55 axes (self-keyed, wrong-axis,
selection-bias, confounded, within-noise, lossy-projection,
aggregation-reversal, referent-witnessed, temporal/dose/outcome/subgroup
onset-and-spike, funnel-stage-misattribution, selection-on-narrative,
annotator-self-keyed, scope-of-independence, reference-mix, unwitnessed-receipt, unwitnessed-root, source-misattribution, wider-than-named, self-falsifying, primary-basis-reversal, window-present-tense, evidence-unclosed, fidelity, witness-population-selection, source-replication, opt-in-census, thesis-outruns-evidence, ...) and
returns the fired flags with a per-check detail line.

The point is not "does the claim sound plausible" but "does the claim's
own data support the specific number it headlines, on the specific axis
the mechanism is supposed to act on, without the gap being explained by
the measurement itself?"

## Requirements

Python 3.8+ standard library only. No dependencies, no network.

## Quick start (stranger-rerunnable)

```
python3 calibration.py
```

Exits 0 and prints `VERDICT: instrument DISCRIMINATES` if and only if all
three properties hold on the 82 calibration specimens:

  (a) silent-on-robust   : robust claims fire NO flag
  (b) fire-on-flawed     : flawed claims fire the expected axis
  (c) right-axis-strict  : fired set == expected set (no cross-fire, no miss)

Ground truth for each calibration specimen is derived by direct
arithmetic on the raw numbers (see `truth_reason` per specimen), not by
running the instrument. That is what makes the calibration a
discriminating test rather than a self-check: a broken instrument can
still agree with itself, but it cannot stay silent on the robust set
while routing each known flaw to the right axis.

## Auditing your own claim

```
python3 claim_audit.py --spec spec.json
```

Spec shape (one claim):

```json
{
  "name": "my claim",
  "type": "ablation",
  "mechanism_lever": "cm",
  "rows": [
    {"label": "mechanism", "mechanism_on": true, "substrate": ["cm", "base"], "metric": 0.22},
    {"label": "null", "mechanism_on": false, "is_null": true, "substrate": ["base"], "metric": 0.05}
  ]
}
```

Row fields the instrument reads (all optional; a missing field makes the
dependent axis N/A rather than guessing): `label`, `mechanism_on`,
`is_null`, `substrate`, `metric`, `ci` (95% CI), `mechanism_axis`
(metric on the axis the mechanism is supposed to act on), `knob`,
`claim_outcome`, `claim_subgroup`, `claim_dose`, `claim_scope`,
`dose`, `tier`, `split`, `temporal_order`, `annotator`, `reference_mix`.

Output: JSON with `checks` (per-axis pass/flag + detail), `flags`
(fired axes), `verdict`, `boundary` (schema-boundary notes where an
undeclared field makes a refinement N/A), `contested`.

## The battery

```
python3 claim_audit.py
```

Runs the 169 specimens in `specimens.py` (130 real — papers from the
2026-09-15..22 audit run plus schema-boundary cells plus the live 1f916.ai
seal/ack floor — plus 39 constructed/self-specimen discriminating cells: the
original 11 battery witnesses for TEMPORAL-ONSET, REFERENCE-MIX,
PLATFORM-CERTIFIED, TRUST, TAUTOLOGICAL-BLEND, CRITERION-THRESHOLD,
JUDGE-AS-TARGET, and the four three-channel independence witnesses (CH0-CH3),
plus the CF-CG-1 self-specimens and the SCOPE-FLATTENING / UNIT-COUNT /
OPT-IN-CENSUS / THESIS-OUTRUNS-EVIDENCE / CERTIFIER-UNNAMED / CAUSAL-WIRING fire+pass cells; see COHERENCE.md) and prints
`ALL SPECIMENS MATCH` (exit 0) when every specimen's fired flags equal
its recorded `expected` set. `results.txt` is a fresh run of this
battery from this copy of the code.

## Files

  claim_audit.py   the instrument (55 checks + CLI), stdlib only
  calibration.py   the 106-specimen discriminating calibration
  calibration_boundary.py  the self-calibration probe (per-check mutation)
  calibration_confound.py  the RED-baseline confound (dead check reads CALIBRATED)
  calibration_bandaid.py   the baseline-integrity fix (band-aid, not removal)
  specimens.py     169 specimens (130 real + 39 constructed/self-specimen) with expected flag sets
  results.txt      fresh battery run from this copy
  publicity_saturation.py  the PUBLICITY saturation test (certification subset -> one variable)
  question_selection.py  terminus candidate: query-selection collapses into what-is-recorded
  schema_selection.py    terminus candidate: the carrier's own schema collapses into what-is-recorded
  vouching.py            terminus candidate: vouching for another writer's record collapses into what-is-recorded
  frame.py               terminus candidate: frame-of-reference collapses into what-is-recorded
  trust_cell.py          the two-terminus discriminating test; TRUST is the first genuinely-new self-keyed referent
  certifier_denominator.py  the 69k-trial certifier-denominator check (Case A mine / A' stranger / B certifier-dependent D)
  certifier_denominator.results.txt  the recorded result (a stranger re-run diffs against it byte-for-byte)

## The PUBLICITY saturation test (certification subset)

```
python3 publicity_saturation.py
```

The 43 axes split into two families: the empirical axes (does the claim's own
data support the headline?) and the certification axes (can a stranger
independently verify the witness?). This probe tests the consolidation claim
that the certification axes are projections of a single variable -- PUBLICITY
(is the verification data a public artifact or a private secret?) -- the same
structure as the 59-axis saturation test that collapsed distinct axes into one
instrument. It parameterizes the certification structure across 6 cells
(secret/public x platform/citizen/third-party seats) and checks three
properties:

  (a) publicity-determined      : the ground-truth stranger-verifiability
                                  verdict is seat-invariant (public vs private)
  (b) instrument-label-dependent: PLATFORM-CERTIFIED fires only for
                                  platform-secret (misses citizen-secret and
                                  third-party-secret)
  (c) narrow-face               : so the 43rd axis is a narrow face of the
                                  broader PUBLICITY variable, not the variable
                                  itself (weight-1 instrument = the PUBLICITY
                                  verdict; the axis label is weight-0)

Verdict (2026-09-28): the collapse is REAL, scoped to the certification
subset; the empirical axes are a different family, out of scope. Anchored by
the two live witnesses (server seal = private/unverifiable; anchored Merkle
root = public/verifiable).


## The what-is-recorded terminus (self-keyed family closure)

The self-keyed gap is an AGGREGATION gap, not a data gap: it is real only when
the raw state is unavailable to the stranger. That framing left an open
question -- is there a NEW self-keyed referent whose mechanism is not
what-is-recorded? Four candidates were named and each was tested as a
stranger-rerunnable script (stdlib only, `python3 <script>.py`, exits 0 with
`VERDICT: PASS`):

  question_selection.py  which-fact-is-asked (query selection)
  schema_selection.py    the carrier's own schema
  vouching.py            the writer choosing which OTHER writer's record to vouch for
  frame.py               the writer choosing which frame of reference the record is asserted in

```
python3 question_selection.py && python3 schema_selection.py \
  && python3 vouching.py && python3 frame.py
```

Verdict (2026-09-28): ALL FOUR collapse into the SAME channel -- the writer
choosing WHAT IS RECORDED (a lossy function state->record; the stranger sees
the record and cannot recover the state). Query-selection is a strict
superset of the aggregation pick-space on the same function-selection channel
(a generalization, not a new referent); the carrier's schema controls what is
recorded (the aggregation gap); vouching is a composition of lossy functions
(11,264 consistent worlds unrecoverable to a stranger); the frame is a
bijection on the content value (a relabel, not a new referent).

STRUCTURAL LESSON: the "next referent" candidates that keep getting named
(temporal, query-selection, schema-selection, vouching, frame) are all
projections of ONE act -- the writer choosing what is recorded. The
self-keyed family is closed to extension by relabeling. The only legitimate
return is a different family, or a genuinely new self-keyed referent whose
mechanism is NOT what-is-recorded (a channel where the writer's choice is a
different kind of act).

Cross-links: the PUBLICITY saturation above (certification subset -> one
variable) is the certification family's own closure; the temporal candidate
(workspace sim `sims/consensus-vs-fidelity/temporal.py`, not part of this
repo) collapsed the same way -- the re-read schedule is observable, so the
self-keying is in the recorded values, not the schedule.

## The TRUST cell (the first genuinely-new self-keyed referent)

The two terminuses above are two faces of ONE self-keyed act -- the writer
choosing what a stranger can verify. PUBLICITY = control over channel OPENNESS
(public artifact vs private secret); what-is-recorded = control over content
LOSSINESS (which lossy function state->record). A stranger's verifiability is
bounded by the WEAKER of the two, so they are the same collapse read from two
ends (openness vs lossiness), not independent. Each pointed toward a
"genuinely new self-keyed referent" but never stated the discriminating test.
It is stated now:

  A candidate self-keyed referent C is GENUINELY NEW iff its gap survives BOTH
    (a) full publicity   -- the raw state is made public
    (b) losslessness     -- the function is made identity
  If C's gap vanishes under (a), C is a face of the PUBLICITY terminus (its
  self-keyedness is just OPENNESS). If it vanishes under (b), C is a face of
  the what-is-recorded terminus (its self-keyedness is just LOSSINESS).

`trust_cell.py` (stdlib only, `python3 trust_cell.py`, exits 0 with
`VERDICT:`) runs the test over three candidates -- PUBLICITY, LOSSINESS, and
TRUST (the writer choosing WHICH OTHER WRITER to accept; the source's
authority as the key) -- against a ground-truth stranger-verifiability verdict
that is conjunctive over the three axes (a stranger can verify iff the state
is public AND the function is lossless AND the writer is trusted):

```
python3 trust_cell.py
```

Verdict (2026-09-28): TRUST is the FIRST GENUINELY NEW self-keyed referent.
The (public, lossless, untrusted) cell is still unverifiable -- the gap
survives both arms -- while the (public, lossless, trusted) control is
verifiable. PUBLICITY and LOSSINESS each fail their own arm (relabels: faces
of the two terminuses). The invariant check confirms the verdict is
writer-identity-invariant within the (public, lossless) cell and depends only
on the trust flag. The forward move is the weight-1 TRUST instrument
(stranger-rerunnable: "is the writer trusted?"), of which provenance is a
face. The self-keyed family is no longer closed: it has a third axis
(source authority) that is conjunctive with openness and lossiness.

(2026-09-28): the forward move was implemented. The weight-1 TRUST instrument
landed as the 44th axis (check_trust in claim_audit.py), with the T1-T4
calibration cells (calibration.py) and the TW1 battery witness (specimens.py).
The battery is now 130 specimens (126 real + 4 constructed battery witnesses).

(2026-09-28): the TAUTOLOGICAL-BLEND axis (45th) was implemented. The
construction-channel face of the self-keyed family (the SignTrace
decomposition, 2026-09-28): fires when the headline metric's population
includes a construction-guaranteed subset -- the system's own setup
guarantees the result for that metric -- and the guaranteed component is
not separated from the measured in the headline number. The guarantee is
METRIC-SPECIFIC: the construction guarantees the pool metric (target in
top-K), not the rank metrics (Hit@1/Hit@9). Distinct from
SELECTION-ON-NARRATIVE (the headline is over a narrative-selected subset;
here the headline is over the full population, and the preselection is a
construction fact about a subset of it) and from REFERENT-CONSTRUCTED
(the query side is constructed in the system's own style; here the
construction is on the setup side: the targets are preselected into the
pool). The weight-1 TAUTOLOGICAL-BLEND instrument landed as the 45th axis
(check_tautological_blend in claim_audit.py), with the TB1-TB3 calibration
cells (calibration.py) and the TW2 battery witness (specimens.py). The
battery is now 131 specimens (126 real + 5 constructed battery witnesses).

(2026-09-28): the CRITERION-THRESHOLD (46th) and JUDGE-AS-TARGET (47th)
axes were implemented. These are the criterion-channel and loop-channel
faces of the self-keyed family, completing the three-channel decomposition
pinned from the SignTrace/SlideLab/Spotify streak (2026-09-28).
CRITERION-THRESHOLD (check_criterion_threshold in claim_audit.py) fires when
a detector claims to catch a failure, the catch verdict is computed on the
detector's OWN metric, and the detection threshold (the delta that counts as
'caught') is not disclosed -- the detector is its own criterion (the
SlideLab/ConfArena threshold-undisclosed seam). JUDGE-AS-TARGET
(check_judge_as_target in claim_audit.py) fires when the judge emits the
labels AND the agent optimizes toward those same labels -- the measure is the
optimization target, so the loop closes on the judge (the Spotify
self-improvement-loop seam). Each landed with its calibration cells (CT1-CT3,
JT1-JT3 in calibration.py) and battery witness (TW3, TW4 in specimens.py).

The three-channel independence test (the falsifiable prediction from the
consolidation thought, 2026-09-28): the four CH0-CH3 witnesses (specimens.py)
build a specimen with all three channels open (CH0), then close exactly ONE
channel in each of CH1 (population), CH2 (criterion), CH3 (loop). The
prediction: closing one channel silences only that axis and the other two
still fire. Result: CONFIRMED. Each axis fires on exactly 4 specimens (its
own TW + CH0 + the two CH specimens where that channel stays open), and each
pair co-fires on exactly 2 (CH0 + the CH specimen where both channels are
open). Closing one channel does NOT silence the other two -- the three
channels are independent, not one axis three times. The battery is now 137
specimens (126 real + 11 constructed battery witnesses).

(2026-09-29): the THESIS-OUTRUNS-EVIDENCE axis (52nd) was implemented.
The headline-layer face of the scope family (arXiv 2609.31054, Rilla et al.,
"Cheap, open agents make LLM pollution harder to mitigate", the arXiv feed
seed): the title states a present-tense causal fact about the endpoint
(mitigation difficulty), but the evidence measures only the premises
(deployment cost, survey competitiveness, per-check failure profile, SED) —
the endpoint is a forecast, not a measurement. Fires when the thesis endpoint
is not in the measured set AND the headline states it as a present-tense fact;
the body hedge ("may have removed this barrier", "FUTURE pollution") is
corroborating, not the discriminator (it is present in the properly-scoped
control too). Distinct from SCOPE-FLATTENING (a measured value varies across
regimes and is stated universal — the endpoint IS measured) and from
FUNNEL-STAGE-MISATTRIBUTION (the named stage is inside the measured pipeline;
here the endpoint is downstream of it). The weight-1 THESIS-OUTRUNS-EVIDENCE
instrument landed as the 52nd axis (check_thesis_outruns_evidence in
claim_audit.py), with the T1-T2 calibration cells (calibration.py) and the
battery cells (specimens.py: the Rilla fire cell, the 2609.31563
measured-endpoint reverse control, the properly-scoped-headline pass cell,
and the no-rows regime cell). The battery is now 153 specimens (126 real +
27 constructed/self-specimen).

(2026-09-29): the CERTIFIER-UNNAMED axis (53rd) was implemented. The
certification-gate face of the self-keyed family (arXiv 2609.30971,
SciHorizon-eLab, the agentic protocol-to-task compiler, the arXiv feed seed):
the paper's certification gate is anchored only to a protocol channel whose
identity is never declared — the certifier is unnamed, so the 'certified'
verdict has no external anchor to check against. The discriminating test is a
2x2 over referent_provenance (model-constructed vs externally-anchored) x
certifier_identity (named vs unnamed): corner B (model-constructed referent +
unnamed certifier, the SciHorizon-eLab shape) fires CERTIFIER-UNNAMED only;
corner A (MACBT: model-constructed referent + NAMED GPT-4 judge) fires
REFERENT-CONSTRUCTED only — the named certifier is exactly what keeps
CERTIFIER-UNNAMED from firing; corner D (external referent + named certifier)
fires neither; corner C (external + unnamed) fires CERTIFIER-UNNAMED only.
The weight-1 CERTIFIER-UNNAMED instrument landed as the 53rd axis
(check_certifier_unnamed in claim_audit.py; schema field certifier_identity,
N/A when undeclared, fires on 'unnamed'), with the 2x2 calibration cells
(calibration.py) and the battery cells (specimens.py: the four 2x2 corners).
The battery is now 157 specimens (127 real + 30 constructed/self-specimen).

(2026-09-29): the CAUSAL-WIRING axis (54th) was implemented. The
measurement-layer face of the overclaim family (arXiv 2609.30940, FRAIL,
'Financial Fragility in Societies of LLM Agents', the arXiv feed seed): the
evidence measures an association (early commitment is 'associated with' an 82%
vs 37% outcome gap) and the Discussion promotes it to a cause — the measured
correlate is promoted to a cause (the 'associated with' -> 'causes'
promotion). The empirical layer passes (on 1.0 > off 0.2, lever isolated), so
the only flag is the causal-wiring promotion. Distinct from
THESIS-OUTRUNS-EVIDENCE (the endpoint is not measured at all; here the link
IS measured, as an association, and the claim promotes it) and from
SCOPE-FLATTENING (a measured value varies across regimes and is stated
universal). The discriminating test is a 2x3 over claim_relation (causal vs
associative) x evidence_relation (causal vs associative) plus a TOE-territory
control: corner A (claim asserts causal, evidence measures only association)
fires CAUSAL-WIRING only; corner B (claim asserts causal, evidence measures
causal) fires nothing (the causal control); corners C/D (claim asserts
associative) fire nothing (the scoping/clean controls); corner E (TOE
territory) isolates the endpoint-not-measured regime. The weight-1
CAUSAL-WIRING instrument landed as the 54th axis (check_causal_wiring in
claim_audit.py), with the 2x3 calibration cells (calibration.py) and the
battery cells (specimens.py: the 2x3 A-E grid plus the FRAIL seam-2 fire cell,
the early-commitment promotion). The battery is now 164 specimens (128 real +
36 constructed/self-specimen).

(2026-09-29): the DECLARED-CHANNEL axis (55th) was implemented. The
decision-channel face of the self-keyed family (arXiv 2609.30813, CPB,
'A Benchmark and Diagnostic Study of Epistemic Admission in Shared Agent
Memory', the arXiv feed seed): the certifier is external and named (not
CERTIFIER-UNNAMED) and the referent's content is independently verifiable
(not TRUST, not SELF-KEYED: the stranger CAN check the truth), but the
certifier's DECISION is carried by a self-declared attribute -- a form/type
label the publisher declares -- so the admission decision flips with the
declared form, not the verified content. The protection is carried by the
declaration, not by verification. Distinct from TRUST (the stranger cannot
verify at all; here the content IS verifiable and the gap is in the
certifier's decision channel, not the stranger's belief) and from
SOURCE-REPLICATION (the certifier re-runs the same measurement on the same
source; here the certifier reads a DIFFERENT attribute -- the declared form
-- not the verified content). The discriminating test is a 2x2 over
decision_channel (declared-attribute vs verified-content) x
content_verifiable (yes vs no): DC1 (declared-attribute + verifiable) fires
DECLARED-CHANNEL only; DC2 (verified-content + verifiable) fires nothing
(the pass cell); DC3 (declared-attribute + not verifiable) fires nothing
(defers to TRUST, the content's verifiability is the gap, not the decision
channel). The weight-1 DECLARED-CHANNEL instrument landed as the 55th axis
(check_declared_channel in claim_audit.py), with the 2x2 calibration cells
(calibration.py: DC1 fire + DC2 pass) and the battery cells (specimens.py:
DC1/DC2/DC3 + the CPB live external specimen). The battery is now 168
specimens (129 real + 39 constructed/self-specimen).

## Lineage

Built 2026-09-15..22 as a workspace instrument for tearing apart
arXiv headlines and square-thread claims. Shipped as a public repo
2026-09-24 because the instrument's own three properties were only
checkable by its author: the certifier's self-claims were self-keyed.
The calibration is the fix — a stranger can clone this repo and verify
the instrument discriminates without trusting its author.

## The calibration boundary (self-calibration probe)

```
python3 calibration_boundary.py
```

The battery being GREEN is not the same as the battery being COMPLETE.
This probe answers the self-keyed question applied to the instrument's own
calibration: for each of the 55 checks, blind it (force always-pass) and
re-run the battery. If the battery stays GREEN, no specimen's
independently-derived ground truth requires that check to fire, so the check
could silently break and `calibration.py` would still print DISCRIMINATES.

Current state (2026-09-29): 55/55 checks are calibrated (each caught by
at least one discriminating specimen — BEATS-NULL by 9, its
false-positive surface being the spike family plus F2; NOT-SELF-KEYED /
SCOPE-OF-INDEPENDENCE / EVIDENCE-UNCLOSED / SOURCE-REPLICATION by 2 each;
the other 50 by exactly one); the calibration boundary is closed (0 uncalibrated). The
last 8 were closed with one discriminating fire+pass cell per axis
(AR/RC/F/SN/AK/C/SI/RM pairs, ground truth by direct arithmetic): each
fire cell fires exactly its target axis, each pass cell fires nothing,
and the pair differs only on the field the axis reads. The final 5
(COVERAGE-GAP, SCOPE-FLATTENING, UNIT-COUNT, OPT-IN-CENSUS,
CERTIFIER-UNNAMED) were closed
2026-09-29 by porting their discriminating fire cells from specimens.py into
calibration.py (the calibration battery), so the boundary probe now sees them.
Because the baseline battery is green, "never fires" and
"uncatchable" coincide: the uncalibrated set is exactly the calibration
boundary, surfaced as a computed property instead of locked as regression
witnesses. Closing the boundary = one discriminating specimen per
uncalibrated axis (or retiring the axis). The probe always exits 0; the
report is the point.

## Knife-edge probe (verdict ruggedness — the near-miss rows)

```
python3 knife_edge.py
```

Dual of `calibration_boundary.py`. That probe asks, per CHECK, "can the
battery catch this check breaking?" (per-check mutation). This probe asks,
per SPECIMEN, "how far is this verdict from the decision boundary?" (per-field
perturbation): for each numeric leaf in each specimen, perturb it by one
minimal step (+1/-1 for integer counts, +/-1% for continuous values) and
re-audit. If the fired-flag set changes, the verdict is KNIFE-EDGE on that
field — the paper's audit verdict is one rounding error from a different
verdict. A near-miss is a normal row, not a confession; a stable verdict is
logged too. Exit 0 always; the report is the point.

Flips are tagged by field class, because a knife-edge on a MEASURED quantity
(measurement noise — the true near-miss) is a different near-miss from one on
a STRUCTURAL set-size (support, check_count, cursor_runs — a different
dataset) or a DECLARED parameter (knob, threshold, stated_headline — the
claim's own exact value). The classes are not mutually exclusive per specimen.

Current state (2026-09-29): 168 specimens, 736 numeric leaves. 148/168
verdicts are ROBUST (stable under every minimal single-field perturbation);
20/168 are knife-edge: 14/168 flip on a measured quantity, 6/168 flip only on
structural/declared fields, 5/168 flip on both.

The load-bearing finding is the self-specimen: CF-CG-1 sweep saturation (the
PASS-cell self-specimen, expected flags = []) sits one 1% relative perturbation
(EPS=0.01) from SELF-KEYED. Its metric plateau is 0, 2, 3, 3, 3, 3 — the
four-way tie at 3.0 keeps the knob-metric spearman at 0.8452, just under the
0.9 threshold, so the instrument reads "not self-keyed". A 1% nudge on the
first or last plateau row (the edges) breaks the four-way tie, pushing spearman
to 0.9411 — over the 0.9 threshold — so the verdict flips to SELF-KEYED, the
instrument's own theme, on its own specimen. (A 1% nudge on a middle plateau
row creates a local inversion and does not flip.) The "clean" verdict rests
entirely on the plateau being exactly flat.

The probe also caught its own seam on first run: the report's "the other N"
count parsed as `A | B | C - D` = `A | B | (C - D)`, so it printed a number
that did not reconcile with the total (13 + 10 != 19) — a precedence slip of
exactly the kind the instrument hunts for, in the instrument's own report.
Fixed; the class sets now reconcile (19 = 13 measured + 6 only-structural/
declared, 4 overlap both).

## Coherence check (axis overlap / redundancy)

```
python3 cofiring.py
```

Growth to 55 axes raises the question: do axes start to overlap? `cofiring.py`
computes the co-firing matrix over the 168-specimen battery: per-axis firing
counts, identical firing sets (pure redundancy), strict-subset sets (the
designed refinement hierarchy), and co-firing pairs. Current state
(2026-09-29): no two axes share a firing set; the only subset structure is the
designed refinement hierarchy (NULL-REACHES-HEADLINE superset of the BEATS-NULL
spike/onset refinements; NO-EMPIRICAL-CONTENT superset of the completeness
regime); the newest axes (COVERAGE-GAP, SCOPE-FLATTENING, UNIT-COUNT,
OPT-IN-CENSUS, THESIS-OUTRUNS-EVIDENCE, CERTIFIER-UNNAMED, CAUSAL-WIRING) each fire on a specimen where no other
axis fires, except OPT-IN-CENSUS which co-fires with NO-EMPIRICAL-CONTENT (its
designed refinement parent; THESIS-OUTRUNS-EVIDENCE likewise co-fires with
NO-EMPIRICAL-CONTENT in its no-rows regime cell; CERTIFIER-UNNAMED co-fires with REFERENT-CONSTRUCTED on corner B, the model-constructed-referent cell — CAUSAL-WIRING is fully exclusive) (per-axis exclusivity, derived
from the firing sets rather than hand-listed); all 55 checks now fire on the battery — the two
former never-firing checks (TEMPORAL-ONSET, REFERENCE-MIX) gained constructed
witnesses, and PLATFORM-CERTIFIED gained a constructed witness (PC1) for
exclusivity (its live specimen, the seal-ack-floor, co-fires with
NO-EMPIRICAL-CONTENT), so `truly_never` is empty. Full report: `COHERENCE.md`.

## Receipt axis (walk completeness)

`receipt_audit.py` + `receipt_calibration.py`: a separate instrument for
cursor-walk receipts. Classifies whether a receipt carries the POPULATION
axis (which rows were delivered) or only the SIZE axis (pages/rows/distinct/
stopping). Verdicts: RECORDED (population listed or hash-committed), PINNED
(counts-only but distinct == span of a known window), SUBSET / UNBOUNDED
(counts-only, unpayable debt -> POPULATION-UNRECORDED), OVERFLOW
(-> WINDOW-INCONSISTENT). Calibration: `python3 receipt_calibration.py`
(7 specimens, ground truth by arithmetic on (distinct, span), not by
re-running the walk). Discriminating boundary: PINNED vs SUBSET — a
one-row-short walk flips the verdict, and a counts-only receipt cannot pay
the debt either way. The window is independent input: the same receipt
against its claimed range is PINNED; against the true window it is SUBSET.

## The certifier-denominator check (the stranger's score — the correctness probe)

```
python3 certifier_denominator.py
```

The instrument's flags are audited by same-method re-runs (calibration.py,
knife_edge.py): those catch execution drift and non-determinism. They cannot
catch the certifier's own lineage bias, because that error is baked into the
certifier. This is the correctness half of the stability-vs-correctness
split, scoped to lineage: re-derive the headline score with an independent
stranger's certifier (different sensitivity s' and false-positive rate f')
and compare. The difference lives in the dimension where lineage error lives
(the certifier's parameters), so it earns independence for the lineage
question; it does not establish full method-independence, because the
scoring form (count-only X/D) is shared with Case A.

The check runs N=69441 items (the ATE headline scaled 10x down; relative bands
scale as 1/sqrt(N), the structural contrast is scale-invariant), K=20 fixed
seeds, stdlib only. Three cases:

  Case A   (mine, s=0.90 f=0.0027): D = N, design-anchored; score always defined.
  Case A'  (stranger, s=0.92 f=0.0015): same D, a stranger's certifier.
  Case B   (certifier-dependent D): D = items since the last false agreement;
           D is the certifier's own output.

Recorded result (committed as certifier_denominator.results.txt; a stranger
re-run diffs against it byte-for-byte):

  Case A  score 2.6438% (2sd 0.0622%)
  Case A' score 2.5793% (2sd 0.0458%); gap 0.0645% < combined 2sd band
          (0.0622% + 0.0458% = 0.1080%) -> indistinguishable: the score is not
          an artifact of my certifier's lineage.
  Case B  D range 6-1579 (CV 0.85), score 1.8552%, range 0.0000%-2.5000%;
          0/0 when no false agreement occurred (D undefined).

The structural contrast: a design-anchored denominator gives a stable,
always-defined score; a certifier-dependent denominator is unstable and
sometimes undefined. This is the family's only correctness probe of the
certifier's own score (lineage-scoped: it varies the certifier's parameters,
not the scoring form); the other self-checks are same-method (stability)
re-runs of the flags.
