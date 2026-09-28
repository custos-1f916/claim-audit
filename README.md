# claim-audit

A 44-axis falsification instrument for empirical claims in ML/AI papers
(and other headline claims with data). Given a claim's raw numbers as a
spec, it checks the claim against 44 axes (self-keyed, wrong-axis,
selection-bias, confounded, within-noise, lossy-projection,
aggregation-reversal, referent-witnessed, temporal/dose/outcome/subgroup
onset-and-spike, funnel-stage-misattribution, selection-on-narrative,
annotator-self-keyed, scope-of-independence, reference-mix, unwitnessed-receipt, unwitnessed-root, source-misattribution, wider-than-named, self-falsifying, primary-basis-reversal, window-present-tense, evidence-unclosed, fidelity, witness-population-selection, source-replication, ...) and
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

Runs the 130 specimens in `specimens.py` (126 real — papers from the
2026-09-15..22 audit run plus schema-boundary cells plus the live 1f916.ai
seal/ack floor — plus 4 constructed battery witnesses for TEMPORAL-ONSET,
REFERENCE-MIX, PLATFORM-CERTIFIED, and TRUST; see COHERENCE.md) and prints
`ALL SPECIMENS MATCH` (exit 0) when every specimen's fired flags equal
its recorded `expected` set. `results.txt` is a fresh run of this
battery from this copy of the code.

## Files

  claim_audit.py   the instrument (44 checks + CLI), stdlib only
  calibration.py   the 78-specimen discriminating calibration
  calibration_boundary.py  the self-calibration probe (per-check mutation)
  calibration_confound.py  the RED-baseline confound (dead check reads CALIBRATED)
  calibration_bandaid.py   the baseline-integrity fix (band-aid, not removal)
  specimens.py     130 specimens (126 real + 4 battery witnesses) with expected flag sets
  results.txt      fresh battery run from this copy
  publicity_saturation.py  the PUBLICITY saturation test (certification subset -> one variable)
  question_selection.py  terminus candidate: query-selection collapses into what-is-recorded
  schema_selection.py    terminus candidate: the carrier's own schema collapses into what-is-recorded
  vouching.py            terminus candidate: vouching for another writer's record collapses into what-is-recorded
  frame.py               terminus candidate: frame-of-reference collapses into what-is-recorded
  trust_cell.py          the two-terminus discriminating test; TRUST is the first genuinely-new self-keyed referent

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
calibration: for each of the 44 checks, blind it (force always-pass) and
re-run the battery. If the battery stays GREEN, no specimen's
independently-derived ground truth requires that check to fire, so the check
could silently break and `calibration.py` would still print DISCRIMINATES.

Current state (2026-09-28): 44/44 checks are calibrated (each caught by
at least one discriminating specimen — BEATS-NULL by 9, its
false-positive surface being the spike family plus F2; NOT-SELF-KEYED /
SCOPE-OF-INDEPENDENCE / EVIDENCE-UNCLOSED / SOURCE-REPLICATION by 2 each;
the other 38 by exactly one); the calibration boundary is closed (0 uncalibrated). The
last 8 were closed with one discriminating fire+pass cell per axis
(AR/RC/F/SN/AK/C/SI/RM pairs, ground truth by direct arithmetic): each
fire cell fires exactly its target axis, each pass cell fires nothing,
and the pair differs only on the field the axis reads. Because the baseline battery is green, "never fires" and
"uncatchable" coincide: the uncalibrated set is exactly the calibration
boundary, surfaced as a computed property instead of locked as regression
witnesses. Closing the boundary = one discriminating specimen per
uncalibrated axis (or retiring the axis). The probe always exits 0; the
report is the point.

## Coherence check (axis overlap / redundancy)

```
python3 cofiring.py
```

Growth to 43 axes raises the question: do axes start to overlap? `cofiring.py`
computes the co-firing matrix over the 129-specimen battery: per-axis firing
counts, identical firing sets (pure redundancy), strict-subset sets (the
designed refinement hierarchy), and co-firing pairs. Current state
(2026-09-27): no two axes share a firing set; the only subset structure is the
designed refinement hierarchy (NULL-REACHES-HEADLINE superset of the BEATS-NULL
spike/onset refinements; NO-EMPIRICAL-CONTENT superset of the completeness
regime); the newest axes (FIDELITY, WITNESS-POPULATION-SELECTION,
SOURCE-REPLICATION, PLATFORM-CERTIFIED) each fire on a specimen where no
other axis fires (per-axis exclusivity, derived from the firing sets rather
than hand-listed); all 47 emitted flags now fire on the battery — the two
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
