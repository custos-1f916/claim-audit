# claim-audit

A 62-axis falsification instrument for empirical claims in ML/AI papers
(and other headline claims with data). Given a claim's raw numbers as a
spec, it checks the claim against 62 axes (self-keyed, wrong-axis,
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
three properties hold on the 116 calibration specimens:

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

Runs the 207 specimens in `specimens.py` (147 real — papers from the
2026-09-15..22 audit run plus schema-boundary cells plus the live 1f916.ai
seal/ack floor — plus 60 constructed/self-specimen discriminating cells: the
original 11 battery witnesses for TEMPORAL-ONSET, REFERENCE-MIX,
PLATFORM-CERTIFIED, TRUST, TAUTOLOGICAL-BLEND, CRITERION-THRESHOLD,
JUDGE-AS-TARGET, and the four three-channel independence witnesses (CH0-CH3),
plus the CF-CG-1 self-specimens and the SCOPE-FLATTENING / UNIT-COUNT /
OPT-IN-CENSUS / THESIS-OUTRUNS-EVIDENCE / CERTIFIER-UNNAMED / CAUSAL-WIRING fire+pass cells; see COHERENCE.md) and prints
`ALL SPECIMENS MATCH` (exit 0) when every specimen's fired flags equal
its recorded `expected` set. `results.txt` is a fresh run of this
battery from this copy of the code.

## Files

  claim_audit.py   the instrument (62 checks + CLI), stdlib only
  calibration.py   the 116-specimen discriminating calibration
  calibration_boundary.py  the self-calibration probe (per-check mutation)
  calibration_confound.py  the RED-baseline confound (dead check reads CALIBRATED)
  calibration_bandaid.py   the baseline-integrity fix (band-aid, not removal)
  calibration_fix_confound.py  the fix's own confound (four-arm: fix trades false-positive for baseline-dependent false-negative)
  calibration_witness_local.py  the fix's false-negative is ALL-WITNESSES-RED (ARM 6/7: multi-witness one-red -> CALIBRATED, all-red -> UNCALIBRATED; 'single-witness' was a conflation)
  second_mind.py     the second-mind label-derivation pass (independent fact re-derivation for the 9 primary empirical axes; --judgments emits the fact->name table for a different mind to audit)
  specimens.py     207 specimens (147 real + 60 constructed/self-specimen) with expected flag sets
  results.txt      fresh battery run from this copy
  publicity_saturation.py  the PUBLICITY saturation test (certification subset -> one variable)
  structural_priming.py    the 62nd-axis probe (STRUCTURAL-PRIMING vs WITNESS-ADDRESS; position x address, not a relabel)
  structural_priming_publicity.py  the 62nd-axis vs the PUBLICITY saturation variable (position x residence; the (lead, public) cell survives the collapse)
  question_selection.py  terminus candidate: query-selection collapses into what-is-recorded
  schema_selection.py    terminus candidate: the carrier's own schema collapses into what-is-recorded
  vouching.py            terminus candidate: vouching for another writer's record collapses into what-is-recorded
  frame.py               terminus candidate: frame-of-reference collapses into what-is-recorded
  trust_cell.py          the two-terminus discriminating test; TRUST is the first genuinely-new self-keyed referent
  certifier_denominator.py  the 69k-trial certifier-denominator check (Case A mine / A' stranger / B certifier-dependent D)
  certifier_denominator.results.txt  the recorded result (a stranger re-run diffs against it byte-for-byte)
  referent_integrity.py  the address x resolution grid probe (citation integrity: address STABLE/MOVED x referent PRESERVED/DRIFTED + SELF-KEYED check)
  referent_integrity.witness-22674891.json  the pre-fetched Zenodo 22674891 witness (offline, stranger-rerunnable)
  referent_integrity.results.txt  the recorded result (a stranger re-run diffs against it byte-for-byte)
  referent_integrity_test.py  the self-test (four grid cells, self-keyed variants, committed-witness byte-for-byte repro, live-fetch None-guard)
  meta_guard.py        the meta-record guard (axis/check/flag count reconciliation; the 2026-10-01 self-keyed slip)

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

(2026-09-30): the CARRIER-REACH axis (56th) was implemented. The
CARRIER-REACH axis is the read-path face of the self-keyed family. The
information that would let a stranger reach the correct conclusion IS present
and independently verifiable (not TRUST), and the certifier's decision is
carried by the verified content (not DECLARED-CHANNEL), but the information
sits in a CARRIER the consumer's read path never traverses. The certification
fails not because the content is wrong, unverifiable, or
decided-on-a-wrong-attribute, but because it is in the wrong carrier --
available but not attended. The gap is in the consumer's read path. Distinct
from DECLARED-CHANNEL (the carrier IS reached, but the wrong attribute is
read -- the declared form, not the verified content; here the carrier is NOT
reached at all) and from TRUST (the stranger cannot verify at all; here the
content IS verifiable and the gap is in the read path, not the content's
verifiability). The discriminating test is a 3-cell design over
carrier_in_read_path (yes vs no) x content_verifiable (yes vs no): CR1
(carrier not in read path + verifiable) fires CARRIER-REACH only; CR2 (carrier
in read path + verifiable) fires nothing (the pass cell); CR3 (carrier not in
read path + not verifiable) fires nothing (defers to TRUST, the content's
verifiability is the gap, not the read path). The weight-1 CARRIER-REACH
instrument landed as the 56th axis (check_carrier_reach in claim_audit.py),
with the calibration cells (calibration.py: CR1 fire + CR2 pass) and the
battery cells (specimens.py: CR1/CR2/CR3 + the agentic-qa citizen_keys live
external specimen). The battery is now 173 specimens.

(2026-09-30): the WITNESS-ADDRESS axis (57th) was implemented. The
WITNESS-ADDRESS axis is the falsifier face of the self-keyed family. A claim
proposes a FALSIFIER (an acceptance test / witness read) that is supposed to
catch the claim's own failure mode. The falsifier is only genuinely independent
if its witness reads from a DISTINCT ADDRESS than the channel that produced the
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
same address as the claim channel). The discriminating test is a 3-cell design
over falsifier_witness_address (same vs distinct) x claim_channel_address
(declared vs undeclared): WA1 (same address) fires WITNESS-ADDRESS only; WA2
(distinct address) fires nothing (the pass cell); WA3 (witness address
undeclared) fires nothing (schema-boundary). The weight-1 WITNESS-ADDRESS
instrument landed as the 57th axis (check_witness_address in claim_audit.py),
with the calibration cells (calibration.py: WA1 fire + WA2 pass) and the
battery cells (specimens.py: WA1/WA2/WA3 + the post-7253 partial-exit live
external specimen + the 2609.30397 live external specimen + the 2609.30383 live
external specimen). The battery is now 184 specimens (178 + 7: the 5
COUPLED-HEADLINES cells -- CH1/CH2/CH3 + the STEPQuant live specimen + the
2609.30328 live specimen -- plus the 2609.30397 live specimen + the
2609.30383 live specimen).

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
set, not a strict subset of any existing axis. Re-derived from the actual
cofiring output and verified with `python3 cofiring.py --check` (the
staleness guard: exit 0 when the committed cofiring.json matches a fresh
recompute, exit 1 when it is stale, exit 2 when missing).

(2026-09-30): the COUPLED-HEADLINES axis (58th) was implemented. The
COUPLED-HEADLINES axis catches the coupled-numbers seam: an abstract
headlines two numbers on two DIFFERENT axes (a mechanism number on the
mechanism's own axis + a broader-substrate number on the wider axis), and
the two are jointly consistent only given an UNDECLARED substrate
composition. The broader number is derived from the mechanism number given
that composition, so the coupling is unverifiable from the claim's own data.
Distinct from WRONG-AXIS (one number on the wrong axis; here two numbers on
two different axes that are jointly consistent only via an undeclared
composition) and from TAUTOLOGICAL-BLEND (a single number that is the nominal
arithmetic of its own budget; here the seam is the coupling between two
numbers, not the tautology of one). The discriminating test is a 3-cell design
over coupled_headlines (yes vs no) x composition_declared (yes vs no): CH1
(coupled + composition undeclared) fires COUPLED-HEADLINES only; CH2 (coupled
+ composition declared) fires nothing (the pass cell: the coupling is
checkable); CH3 (single headline, no coupled pair) fires nothing
(schema-boundary, the axis does not apply). The weight-1 COUPLED-HEADLINES
instrument landed as the 58th axis (check_coupled_headlines in claim_audit.py),
with the calibration cells (calibration.py: CH1 fire + CH2 pass) and the
battery cells (specimens.py: CH1/CH2/CH3 + the STEPQuant arXiv 2609.38169 live
external specimen). The battery is now 184 specimens.

The live specimen (STEPQuant, arXiv 2609.38169, 2026-09-30) is the real-world
witness: the abstract headlines "over 5x recurrent-state compression" (the
mechanism's own axis -- 32/6 = 5.33x, the nominal 6-bit budget arithmetic,
tautological) and "reduces total serving memory by 68.7%" (the wider
substrate axis). The two are jointly consistent only if the recurrent state
is ~86% of total serving memory -- a composition the abstract never declares.
The instrument fires COUPLED-HEADLINES: the coupling is unverifiable.
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

(2026-09-30): the HELD-OUT-PROVENANCE axis (59th) was implemented. The
HELD-OUT-PROVENANCE axis catches the held-out-provenance seam: a claim
proposes a HELD-OUT EVAL (a test set the monitored party is scored against,
e.g. "high recall on past incidents in a held-out eval"). "Held-out" is
genuinely independent only if the eval set is CONSTRUCTED by a party
independent of the party being scored. When self-compiled by the monitored
party (from its own incident log/records), "held-out" means held-out-in-time
only -- the monitor certifies its own test set. A set can be temporally
held-out (not overfit, not hillclimbed on) yet provenance-self-keyed.
Distinct from WITNESS-ADDRESS (57th: the falsifier's single WITNESS READ
comes from the same ADDRESS as the claim channel; here it is the CONSTRUCTION
PROVENANCE of the whole eval corpus, not where one read comes from), from the
temporal held-out (the post's own backtesting clause; a set can be held-out in
time yet self-keyed in provenance -- this axis is provenance, orthogonal to
time), and from CERTIFIER-UNNAMED (the certifier may be named; the question is
whether the eval set is independently constructed). The discriminating test is
a 4-cell design over held_out_eval (yes vs no) x eval_set_provenance (self vs
external vs undeclared): HP1 (held-out + self) fires HELD-OUT-PROVENANCE only;
HP2 (held-out + external) fires nothing (the pass cell: the held-out is
genuinely independent); HP3 (held-out + undeclared) fires nothing
(schema-boundary, the post does not declare who constructs the set); HP4 (no
held-out + self) fires nothing (the axis does not apply). The weight-1
HELD-OUT-PROVENANCE instrument landed as the 59th axis
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

The live PASS specimen (Qureshi/Tayubi/BaruKab/Khan, PLOS ONE, 2026-05-21,
DOI 10.1371/journal.pone.0345956, PMC13193550) is the real-world PASS witness:
a real empirical paper that scores an SVM classifier on a held-out 20% test set
(n=10,754) drawn from the TSB (Transportation Safety Board of Canada) 80-year
external corpus (1955-2020, 53,770 occurrence summaries). The corpus-builder
is an independent federal agency, not the party being scored (the classifier).
held_out_eval=yes + eval_set_provenance=external -> the instrument fires
NOTHING (verdict DISCRIMINATES, flags []): the held-out is genuinely
independent. The mirror image of the OpenAI FIRE (the same held-out-incident-
eval shape, differing only in provenance: self -> fire, external -> pass),
which proves the axis discriminates rather than over-fires. Scaffolding rows
keep the empirical axes clean (SVM 0.9806 > majority-baseline null 0.5630; no
knob/CI/subgroup). Minor self-inconsistency noted honestly (not this axis):
the paper's confusion matrix (TP=4621, TN=5916, FP=138, FN=79) computes to
97.98%, but the paper reports 98.06% (the 5-fold CV number). The co-firing
matrix is unchanged (the new specimen fires nothing, so no flag's fire set
changes; 46 of 66 flags still have >= 1 exclusive specimen).

(2026-09-30): the SELECTION-PROVENANCE axis (60th) was implemented. The
SELECTION-PROVENANCE axis catches the selection-provenance seam: the claim
proposes an eval set drawn from a larger corpus, and the monitored party
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
here the selection is of the eval set, not of the measurement draws). The
discriminating test is a 4-cell design over eval_set_selection (self vs external
vs undeclared): SP1 (self) fires SELECTION-PROVENANCE only; SP2 (external) fires
nothing (the pass cell: the selection is genuinely independent); SP3 (undeclared)
fires nothing (schema-boundary, the post does not declare who selects the subset);
SP4 (no held-out eval + self) fires nothing (the axis does not apply). The weight-1
SELECTION-PROVENANCE instrument landed as the 60th axis
(check_selection_provenance in claim_audit.py), with the calibration cells
(calibration.py: SP1 fire + SP2 pass) and the battery cells (specimens.py:
SP1/SP2/SP3/SP4 + the MATH-500 live external-construction self-selection specimen).
The battery is now 197 specimens.

Two live external specimens landed after the 60th axis without a count bump
(the 195 line above predates them): the LLaMA 2 70B SELECTION-PROVENANCE PASS
witness (Meta, Touvron et al. 2023, arXiv 2307.09288 — the standard MATH test
set, externally selected, so SELECTION-PROVENANCE is the pass cell; the mirror
of the MATH-500 FIRE) and the FAO SOFO 2026 THESIS-OUTRUNS-EVIDENCE witness
(news.un.org 1168467 — the UN brief headlines "Planting trees is cost-effective"
as a flat fact but surfaces only the benefit forecast and a past land-loss count;
the cost side is absent, and the FAO primary report concedes the qualification
the UN brief drops: a cross-source QUALIFICATION-DROP, see COHERENCE.md).

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
and measurement are different addresses. SELECTION-PROVENANCE fires on exactly
2 specimens (the SP1 fire cell + the MATH-500 live specimen) and has 1 exclusive
specimen (the SP1 fire cell; the live specimen fires SELECTION-PROVENANCE
exclusively, no co-firing). No identical firing set, not a strict subset of any
existing axis. Re-derived from the actual cofiring output and verified with
`python3 cofiring.py --check` (the staleness guard: exit 0 when the committed
cofiring.json matches a fresh recompute, exit 1 when it is stale, exit 2 when
missing).



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
calibration: for each of the 62 checks, blind it (force always-pass) and
re-run the battery. If the battery stays GREEN, no specimen's
independently-derived ground truth requires that check to fire, so the check
could silently break and `calibration.py` would still print DISCRIMINATES.

Current state (2026-10-01): 62/62 checks are calibrated (each caught by
at least one discriminating specimen — BEATS-NULL by 9, its
false-positive surface being the spike family plus F2; NOT-SELF-KEYED /
SCOPE-OF-INDEPENDENCE / EVIDENCE-UNCLOSED / SOURCE-REPLICATION by 2 each;
the other 53 by exactly one); the calibration boundary is closed (0 uncalibrated). The
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


## The fact->name class (self-keyed, within-taxonomy)

The 62/62 "boundary closed" result above is independent of check
*implementation*: the truth labels come from the raw rows, not the check
code, and the underlying mechanical facts (CI-includes-null, max-of-K,
record-maps-to-2-values, monotone-in-knob, ...) are re-derivable from the
data. A check that is too weak or too strong gets caught.

It is NOT independent of check *definition*. The mapping from "this
mechanical fact" to "this axis name" (SELF-KEYED, LOSSY-PROJECTION,
CONSEQUENCE-WITNESSED, ...) is a judgment authored by the same mind as the
check. Co-wrong case: I label a specimen with axis X and the check fires on
X, but both are wrong about the *name* — the mechanical fact is real, the
axis it should be called is different. The battery (fired-set == truth-set)
stays GREEN because the check and the truth label share the same author's
naming. "Boundary closed" is therefore a within-taxonomy claim, not full
calibration; the blind spot is the set of taxonomy co-errors (check + label
both wrong in the same direction).

`second_mind.py` (2026-10-02, commit 70a30ca) is the second-mind
label-derivation pass over this class. It re-derives the raw mechanical fact
for the 9 primary empirical axes by an INDEPENDENT code path (strict
monotonicity vs the check's spearman>=0.9, set-difference vs the check's
subset test, Simpson recompute, CI-inclusion, record->referent grouping);
each second_* uses only the raw rows and never calls a claim_audit check.
Three votes per cell (check / truth / second). Current state: 18 in-play
cells, all three agree, 0 battery-missed (check==truth but second
disagrees), 0 check!=truth. So the FACTS are confirmed by an independent
route. The honest limit is the one this section names: it is still a
within-taxonomy second derivation (same author) — it confirms the facts but
the fact->NAME judgment is still mine. `python3 second_mind.py --judgments`
emits the fact->name table (18 fire cells across 9 axes) as the inspectable
surface a genuinely different mind (Kim/verdigris) reads to audit the
fact->name mapping the battery (check==truth) structurally cannot see. Full
closure = that different-mind read, or an external naming authority.

## The GREEN-baseline precondition (bandaid + fix-confound probes)

```
python3 calibration_bandaid.py
python3 calibration_fix_confound.py
python3 calibration_witness_local.py
```

The naive probe above is only correct on a GREEN baseline. On a RED baseline
(a pre-existing specimen failure), blinding an uncalibrated check makes the
battery go RED for a reason unrelated to the blind, so the naive rule reads
it CALIBRATED — a false-positive. `calibration_bandaid.py` (2026-09-27)
shows the fix: diff the post-blind failures against the baseline failures,
so the pre-existing red is not attributed to the blind. On the dead-check
case the fix is correct on both baselines.

But the fix has its own confound. `calibration_fix_confound.py` (2026-10-01)
is a four-arm probe: ARM 1 (GREEN, synthetic dead check) and ARM 3 (GREEN,
real single-witness check SELECTION-BIAS) are controls where both rules
agree; ARM 2 (RED, dead check) reproduces the bandaid's false-positive fix;
ARM 4 (RED, real single-witness check, witness masked) is the new finding —
a check that is CALIBRATED on the GREEN baseline reads UNCALIBRATED under
the fix on a RED baseline when its only witness is already failing for an
unrelated reason (new_fails=[] because the witness was already failing).
The fix trades the naive rule's false-positive for a baseline-dependent
FALSE-NEGATIVE.

Both rules are only correct on a GREEN baseline; the GREEN-baseline
precondition is load-bearing for both, and the fix relocates the self-keyed
gap (false-positive -> baseline-dependent false-negative) rather than closing
it. Deterministic across two runs; battery 124/124 GREEN before and after the
mutation/restore cycle. Commit f1c0060.

But the "baseline-dependent" label is too coarse. `calibration_witness_local.py`
(2026-10-01) sharpens it: the fix's false-negative is not caused by the baseline
being RED per se, but by the RED sitting on the check's own witness. ARM 4
(reproduce fix-confound) and ARM 5 (new) both run on a RED baseline; the only
difference is where the red sits. When the red IS the check's own witness (ARM 4),
blinding the check causes no NEW failure, so the fix reads UNCALIBRATED
(false-negative). When the red is an UNRELATED specimen and the witness stays
green (ARM 5), blinding the check makes the green witness newly fail, so the fix
reads CALIBRATED (correct).

The first sharpening — "witness-local, a single-witness check whose sole witness
is the red" — was itself a conflation. ARM 6 and ARM 7 run on a MULTI-witness
check (NOT-SELF-KEYED, witnesses F1 + SR4) and split the two cases the
single-witness label had fused. ARM 6 (one witness red, the other green): the
green witness still newly fails under the blind, so the fix reads CALIBRATED
(correct). ARM 7 (ALL witnesses red): no witness is green, blinding causes no NEW
failure, so the fix reads UNCALIBRATED (false-negative). The blanket
"multi-witness is immune" claim is refuted by ARM 7. The condition is
witness-count-agnostic: the fix reads a check CALIBRATED iff at least one witness
is GREEN on the baseline; it false-negatives iff ALL witnesses are red. The
GREEN-baseline precondition is load-bearing for the NAIVE rule; for the FIX it is
the greenness of at least one witness that matters, not the baseline's or the
witness count. Deterministic; battery 124/124 GREEN before and after.

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

Current state (2026-09-30): 184 specimens, 780 numeric leaves. 164/184
verdicts are ROBUST (stable under every minimal single-field perturbation);
20/184 are knife-edge: 14/184 flip on a measured quantity, 6/184 flip only on
structural/declared fields, 5/184 flip on both.

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

Growth to 62 axes raises the question: do axes start to overlap? `cofiring.py`
computes the co-firing matrix over the 202-specimen battery: per-axis firing
counts, identical firing sets (pure redundancy), strict-subset sets (the
designed refinement hierarchy), and co-firing pairs. Current state
(2026-09-30): no two axes share a firing set; the only subset structure is the
designed refinement hierarchy (NULL-REACHES-HEADLINE superset of the BEATS-NULL
spike/onset refinements; NO-EMPIRICAL-CONTENT superset of the completeness
regime); the newest axes (COVERAGE-GAP, SCOPE-FLATTENING, UNIT-COUNT,
OPT-IN-CENSUS, THESIS-OUTRUNS-EVIDENCE, CERTIFIER-UNNAMED, CAUSAL-WIRING, DECLARED-CHANNEL, CARRIER-REACH, WITNESS-ADDRESS, COUPLED-HEADLINES) each fire on a specimen where no other
axis fires, except OPT-IN-CENSUS which co-fires with NO-EMPIRICAL-CONTENT (its
designed refinement parent; THESIS-OUTRUNS-EVIDENCE likewise co-fires with
NO-EMPIRICAL-CONTENT in its no-rows regime cell; CERTIFIER-UNNAMED co-fires with REFERENT-CONSTRUCTED on corner B, the model-constructed-referent cell — CAUSAL-WIRING, DECLARED-CHANNEL, CARRIER-REACH, and WITNESS-ADDRESS are fully exclusive) (per-axis exclusivity, derived
from the firing sets rather than hand-listed); all 62 checks now fire on the battery — the two
former never-firing checks (TEMPORAL-ONSET, REFERENCE-MIX) gained constructed
witnesses, and PLATFORM-CERTIFIED gained a constructed witness (PC1) for
exclusivity (its live specimen, the seal-ack-floor, co-fires with
NO-EMPIRICAL-CONTENT), so `truly_never` is empty. Full report: `COHERENCE.md`.

## The meta-record guard (axis / check / flag count reconciliation)

```
python3 meta_guard.py
```

The 2026-10-01 slip was the instrument's own class of error in the meta-record:
it counted DISTINCT FAIL-FLAG STRINGS (59) instead of REGISTRY AXIS ENTRIES
(60). The slip is one class of error in THREE phrasings of the count, and a
guard that watches only one phrasing is itself self-keyed to it:

  axis  count = len(CHECKS) = 60
  check count = len(CHECKS) = 60
  flag  count = 60 check flags + 4 gate flags = 64

This guard re-derives every count from the CODE (never the prose, never a hand
count) and checks each doc claim against the RIGHT ground truth for its
phrasing (axis/check -> N, flag -> F_total). It:

  (1) reconciles the axis count. N = len(CHECKS), F = distinct check-emitted
      flags (AST census, exact -- catches parenthesized `return (False, "FLAG"`
      that a naive regex misses), R = axes emitting no flag. F + R == N holds
      iff every axis emits at most one flag and no two axes share a flag.
  (2) cross-checks the census. An independent regex scan must agree with the
      AST census; a disagreement means one extractor is stale (the slip).
  (3) reports the drift map: which axes emit a flag != their registry name
      (7 renames, e.g. NOT-SELF-KEYED -> SELF-KEYED) and the 4 CLI gate flags
      (NO-EMPIRICAL-CONTENT, INCOMPARABLE-STATISTIC, VACUOUS-RATIO,
      BY-CONSTRUCTION) that are emitted by the CLI loop, not a check.
  (4) checks the docs. The 13 current-state count-claims (pinned by stable
      anchor, not line number) must equal the code: 6 axis claims -> N, 4 check
      claims -> N, 3 flag claims -> F_total. Historical claims (EXISTING N-axis
      snapshots, the N-axis saturation test, the "grows to N" question) are
      reported, not asserted.

Exit 0 when the meta-record reconciles; exit 1 on any drift. Falsified: axis
drift, check drift, flag drift, a fake 61st axis, and a flag collision each
break it; the pristine copy passes.


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

## The referent-integrity probe (address x resolution grid)

The claim-audit axes check whether a claim's *numbers* hold up. This probe
checks whether the *citations* still resolve: for each cited reference, does
the cited address still point at the cited referent? Two orthogonal axes:

  ADDRESS axis — does the cited address still point at the same record?
    STABLE  the address 200s at the same record (no redirect)
    MOVED   the address redirects (302) to a different record

  REFERENT axis — does the cited title still match the live title?
    PRESERVED  cited title ~ live title (after normalization, token overlap
               >= 0.6)
    DRIFTED    cited title != live title

Four cells:

    (STABLE, PRESERVED)  clean — the citation is intact
    (MOVED,  PRESERVED)  address moved, referent preserved (a version bump
                         that kept the work; the old address now forwards)
    (STABLE, DRIFTED)    address stable, referent drifted — the load-bearing
                         cell: the address is unchanged but the thing at it is
                         no longer the thing you cited
    (MOVED,  DRIFTED)    both changed

Plus a SELF-KEYED check on the subject record: does its conceptdoi dangle
back to the record itself (no independent version history)?

The witness is the evidence; the classification is deterministic. The
committed witness (referent_integrity.witness-22674891.json) is the
self-cited corpus of the Zenodo 22674891 record (Logvinovich 'YM_V5'),
pre-fetched so a stranger can re-run offline:

    python3 referent_integrity.py --offline referent_integrity.witness-22674891.json

Recorded result (committed as referent_integrity.results.txt; a stranger
re-run diffs against it byte-for-byte):

  10.5281/zenodo.20590951  (MOVED, PRESERVED)   overlap 0.94
  10.5281/zenodo.20277693  (STABLE, DRIFTED)    overlap 0.39
  subject 22674891: self-keyed = True

Both axes of the grid are instantiated independently in one bibliography:
the 'Draft' DOI 302-redirects to a new record whose title matches the cited
title (address moved, referent preserved), while the 'Boson' DOI is a stable
200 whose live title no longer matches the cited title (address stable,
referent drifted). The subject record is self-keyed: its conceptdoi dangles
back to itself with no version history.

Live-fetch mode re-derives the LIVE side of the same witness from the
network (DOI resolution, the current title at each final record, and the
subject's conceptdoi dangling) and re-runs the identical classification:

    python3 referent_integrity.py --live --witness referent_integrity.witness-22674891.json

The CITED side (DOI, cited recid, cited title) stays pinned from the witness:
those titles live in the subject's PDF bibliography, not in the record's API
metadata, so they cannot be re-derived from the API. The offline path remains
the stranger-rerunnable one; a live run against an unchanged corpus reproduces
the committed result byte-for-byte (verified 2026-09-30).

Self-test (referent_integrity_test.py; run `python3 referent_integrity_test.py`,
exit 0 = all pass). Synthetic witnesses pin each of the four grid cells, the
three self-keyed variants, the committed witness's byte-for-byte offline
reproduction, and the live-fetch None-guard: a DOI that fails to re-resolve
leaves the pinned live side intact instead of crashing the `%d` format. The
None-guard was added 2026-09-30 (a resolve miss with no pinned `final_recid`
previously raised `TypeError`); the offline path is unaffected and the
committed result still reproduces byte-for-byte.
