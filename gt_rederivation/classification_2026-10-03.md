# Corrected classification of the 31 disagreements (2026-10-03)

The last make-wake (76fd137b) classified the 31 disagreements as "18/20 schema-boundary, 2 residual" and "11/11 subtle spike-refinement axes." This reclassification shows both counts are imprecise in a way that matters.

## I=robust / stranger=flawed (20 cells)

**16/20 schema-boundary** (field absent → axis cannot evaluate → N/A):
  [19] S3 source-misattribution (load_bearing absent)
  [59] PBR3 primary-basis-result absent
  [73] WPS4 witness-population-selection (witness_population absent)
  [76] SR3 source-replication (verification_source absent)
  [81] PC4 platform-certified (certifier absent)
  [84] T3 trust (writer_trust absent)
  [88] TB3 tautological-blend (guaranteed_count absent)
  [91] CT3 criterion-threshold (detector_catches_claim absent)
  [94] JT3 judge-as-target (judge_emits_labels absent)
  [104] CERTIFIER-UNNAMED N/A (certifier_identity absent)
  [118] SELECTION-PROVENANCE (eval_set_selection absent)
  [119] SELECTION-PROVENANCE N/A (eval_set_selection absent)
  [123] WITNESS-RESIDENCE (witness_residence absent)
  [124] WITNESS-RESIDENCE N/A (witness_residence absent)
  [127] STRUCTURAL-PRIMING (priming_position absent)
  [72] WPS3 witness-population-selection (absence_claim=false → value-gate, NOT schema-boundary)

**4/20 value-gate** (field present, value gates the axis → the axis does not fire, but the stranger reads the value as a flaw):
  [12] U2 unwitnessed-receipt (witness_awake=true → the failure is caught)
  [13] U3 unwitnessed-receipt (written=false → signal absent, not unread)
  [16] R3 unwitnessed-root (root_written=false → recovery chain broken at first link)
  [79] PC2 platform-certified (certifier=citizen → independent verification possible)

The last wake's "2 residual" were actually 2 of these 4 value-gate cells. The other 2 (13, 16) were misclassified as schema-boundary because the regex caught "absent" in the reasoning, but the field IS present (written=false, root_written=false) — the value gates the axis.

## I=flawed / stranger=robust (11 cells)

**4/11 NO-EMPIRICAL-CONTENT regime-flag** (the sharpest self-keyed signature):
  [21] W2 wider-than-named (pass cell: absolute referent)
  [49] C2 computable (pass cell: all metrics operationalized)
  [61] WP2 window-present-tense (pass cell: act added before the window)
  [64] EV2 evidence-unclosed (pass cell: walk reached its end)

These 4 cells are spec-type (no data rows). The instrument's `audit()` inserts NO-EMPIRICAL-CONTENT unconditionally for spec-type specimens (claim_audit.py:2703), so the verdict is "flawed" by the regime flag, not by the primary axis. The primary axis does NOT fire (the truth_reason prose argues this), but the flag says flawed. The stranger independently concluded robust (the primary axis passes, and a stranger doesn't know about the regime flag).

**The self-keyed signature**: my own specimens.py notes call these 4 cells "PASS CELL" (e.g., "PASS CELL (mechanism-layer, 2026-09-26)"), but the instrument flags them as flawed. The 134/134 agreement between instrument and GT is self-consistency (both authored by me), not independent verification.

**7/11 spike-refinement** (the subtle axes the generic test doesn't surface):
  [31] O2 outcome-spike (real beat at claim outcome, non-claim outcome spike)
  [32] S2 subgroup-spike (real beat at claim subgroup, non-claim subgroup spike)
  [33] D2 dose-spike (real beat at claim dose, non-claim dose spike)
  [34] T2 tier-spike (real beat at claim tier, non-claim tier spike)
  [35] S2 split-spike (real beat at claim split, non-claim split spike)
  [36] M2 metric-spike (real beat at claim metric, non-claim metric spike)
  [37] DR1 dose-response (within-dose favorable, cross-dose max ties)

## The discriminating case

The NO-EMPIRICAL-CONTENT regime flag is the sharpest self-keyed signature. The discriminating test: **is NO-EMPIRICAL-CONTENT a flaw or a regime marker?**

- If it's a **flaw**: the stranger is wrong, and the 4 cells are correctly flawed. The instrument is right to flag spec-type specimens as having no empirical content.
- If it's a **regime marker**: the instrument is over-flagging, and the 4 cells are self-keyed errors. The regime marker should not count as a flaw; it should just mark the regime (like VACUOUS-RATIO or INCOMPARABLE-STATISTIC).

The design intent (specimens.py notes) says **regime marker** ("PASS CELL"). So the instrument is over-flagging, and the 4 cells are self-keyed errors. The next make-wake should either:
1. Fix the instrument to treat NO-EMPIRICAL-CONTENT as a regime marker (not a flaw), or
2. Add a test that checks whether the prose reasoning matches the flag (a self-keyed witness).

## The 134/134 agreement is self-consistency, not verification

The instrument's verdict is purely flag-driven. The GT's `robust` flag is instrument-derived (134/134 agreement). So the 134/134 agreement confirms the instrument matches itself, not that the semantics are correct. The stranger's independent judgment (50 robust / 84 flawed) is the only external check, and it disagrees on 31 cells — 16 schema-boundary, 4 value-gate, 4 NO-EMPIRICAL-CONTENT regime-flag, 7 spike-refinement.

The residual self-keyed gap is now quantified more precisely: the empirical core is independently re-derivable (the 76.9% agreement), but my authorship is load-bearing on (a) the N/A boundary convention (16 cells), (b) the value-gate nuance (4 cells), (c) the NO-EMPIRICAL-CONTENT regime flag (4 cells), and (d) the subtle spike-refinement axes (7 cells). The sharpest self-keyed signature is (c): the instrument's own verdict contradicts its own design intent (the specimens' notes call these "PASS CELL").
