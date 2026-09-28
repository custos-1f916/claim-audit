# claim-audit

A 43-axis falsification instrument for empirical claims in ML/AI papers
(and other headline claims with data). Given a claim's raw numbers as a
spec, it checks the claim against 43 axes (self-keyed, wrong-axis,
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

Runs the 129 specimens in `specimens.py` (126 real — papers from the
2026-09-15..22 audit run plus schema-boundary cells plus the live 1f916.ai
seal/ack floor — plus 3 constructed battery witnesses for TEMPORAL-ONSET,
REFERENCE-MIX, and PLATFORM-CERTIFIED; see COHERENCE.md) and prints
`ALL SPECIMENS MATCH` (exit 0) when every specimen's fired flags equal
its recorded `expected` set. `results.txt` is a fresh run of this
battery from this copy of the code.

## Files

  claim_audit.py   the instrument (43 checks + CLI), stdlib only
  calibration.py   the 78-specimen discriminating calibration
  calibration_boundary.py  the self-calibration probe (per-check mutation)
  calibration_confound.py  the RED-baseline confound (dead check reads CALIBRATED)
  calibration_bandaid.py   the baseline-integrity fix (band-aid, not removal)
  specimens.py     129 specimens (126 real + 3 battery witnesses) with expected flag sets
  results.txt      fresh battery run from this copy
  publicity_saturation.py  the PUBLICITY saturation test (certification subset -> one variable)

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
calibration: for each of the 43 checks, blind it (force always-pass) and
re-run the battery. If the battery stays GREEN, no specimen's
independently-derived ground truth requires that check to fire, so the check
could silently break and `calibration.py` would still print DISCRIMINATES.

Current state (2026-09-27): 43/43 checks are calibrated (each caught by
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
