# claim-audit

A 38-axis falsification instrument for empirical claims in ML/AI papers
(and other headline claims with data). Given a claim's raw numbers as a
spec, it checks the claim against 38 axes (self-keyed, wrong-axis,
selection-bias, confounded, within-noise, lossy-projection,
aggregation-reversal, referent-witnessed, temporal/dose/outcome/subgroup
onset-and-spike, funnel-stage-misattribution, selection-on-narrative,
annotator-self-keyed, scope-of-independence, reference-mix, unwitnessed-receipt, unwitnessed-root, source-misattribution, wider-than-named, self-falsifying, primary-basis-reversal, window-present-tense, ...) and
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
three properties hold on the 57 calibration specimens:

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

Runs the 107 real specimens in `specimens.py` (papers from the
2026-09-15..22 audit run plus schema-boundary cells) and prints
`ALL SPECIMENS MATCH` (exit 0) when every specimen's fired flags equal
its recorded `expected` set. `results.txt` is a fresh run of this
battery from this copy of the code.

## Files

  claim_audit.py   the instrument (36 checks + CLI), stdlib only
  calibration.py   the 57-specimen discriminating calibration
  calibration_boundary.py  the self-calibration probe (per-check mutation)
  specimens.py     107 real specimens with expected flag sets
  results.txt      fresh battery run from this copy

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
calibration: for each of the 36 checks, blind it (force always-pass) and
re-run the battery. If the battery stays GREEN, no specimen's
independently-derived ground truth requires that check to fire, so the check
could silently break and `calibration.py` would still print DISCRIMINATES.

Current state (2026-09-25): 36/36 checks are calibrated (each caught by
at least one discriminating specimen — BEATS-NULL by 9, its
false-positive surface being the spike family plus F2, the other 35 by
exactly one); the calibration boundary is closed (0 uncalibrated). The
last 8 were closed with one discriminating fire+pass cell per axis
(AR/RC/F/SN/AK/C/SI/RM pairs, ground truth by direct arithmetic): each
fire cell fires exactly its target axis, each pass cell fires nothing,
and the pair differs only on the field the axis reads. Because the baseline battery is green, "never fires" and
"uncatchable" coincide: the uncalibrated set is exactly the calibration
boundary, surfaced as a computed property instead of locked as regression
witnesses. Closing the boundary = one discriminating specimen per
uncalibrated axis (or retiring the axis). The probe always exits 0; the
report is the point.

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
