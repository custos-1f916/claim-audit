#!/usr/bin/env python3
"""CLAIM-POLARITY framing boundary (2026-10-03, 2609.35875).

The instrument's BEATS-NULL assumes a POSITIVE claim (mechanism beats null).
A NEGATIVE-result claim (the mechanism does NOT beat the null) framed with the
rejected hypothesis as `mechanism` fires NULL-REACHES-HEADLINE as a FALSE
POSITIVE: the data (mechanism < null) SUPPORTS the negative claim, but the
polarity-blind comparison reads it as a flaw. Reframing with the WINNING
component as `mechanism` clears.

This is the claim-level analog of the metric-polarity witness (logged-not-
flagged, by design in check_beats_null). Unlike metric polarity (a scale
direction), claim polarity is a FRAMING boundary: the wrong framing produces a
false positive, the right framing audits cleanly. DECIDED (2026-10-03 make
wake): logged-not-flagged witness, mirroring metric_polarity -- NOT a narrow
gate (flag suppression). Rationale: suppressing the flag on a declared field
would change the firing set on author-declared input (a self-keyed judgment
the instrument should not make silently); the honest move is the note. No new
flag, no changed pass/fail, no change to the firing set. Not a full new
empirical axis.

Rerunnable: python3 claim_polarity_test.py  (exits 0 iff both framings behave)
"""
import json, claim_audit

# The 2609.35875 recast: MAD gains are an ensemble-sampling effect.
# Table 1 (context-corrected, 23-model pool, mean): solo 80.4, debate 84.4,
# SC-9 84.8, persona 81.9. The load-bearing negative claim: debate does NOT
# beat budget-matched sampling.

def base(name, mech, mech_label, null, null_label, extra=None):
    spec = {
        "name": name, "type": "cross-model",
        "mechanism": mech, "mechanism_lever": "the lever under test",
        "metric": "mean accuracy (%) over 4 inline-scored tasks, 23-model pool",
        "metric_polarity": "higher-is-better", "scope_claim": False,
        "stated_headline": "reported MAD gains are an ensemble-sampling effect",
        "coupled_headlines": "no", "broader_derived": "no",
        "composition_declared": "yes",
        # thesis_endpoint made LITERAL in measured_endpoints so
        # THESIS-OUTRUNS-EVIDENCE cannot confound the claim-polarity test.
        "thesis_endpoint": "debate does not beat budget-matched sampling at matched budget",
        "measured_endpoints": [
            "debate does not beat budget-matched sampling at matched budget",
            "debate 84.4 vs SC-9 84.8 mean (context-corrected); solo 80.4",
        ],
        "headline_states_as_fact": True, "body_hedges": True,
        "negative_claim": "absent", "power": 0.95, "power_threshold": 0.80,
        "rows": [
            {"label": mech_label, "mechanism_on": True, "metric": mech},
            {"label": null_label, "mechanism_on": False, "is_null": True, "metric": null},
        ],
    }
    if extra:
        spec.update(extra)
    return spec

# Framing A: rejected hypothesis (debate) as mechanism, sampling as null.
# The negative claim is SUPPORTED (84.4 < 84.8) -> NULL-REACHES-HEADLINE is a
# FALSE POSITIVE.
A = base("A: rejected-hypothesis-as-mechanism", 84.4, "debate (3x3)", 84.8,
         "SC-9 budget-matched sampling (null)",
         extra={"claim_polarity": "negative"})
# Framing B: winning component (sampling) as mechanism, solo as null.
# The positive component (sampling captures the gain over solo) is real
# (84.8 > 80.4) -> clean.
B = base("B: winner-as-mechanism", 84.8, "SC-9 budget-matched sampling", 80.4,
         "solo single-agent (baseline)")

aA = claim_audit.audit(A)
aB = claim_audit.audit(B)
print("Framing A flags:", aA["flags"])
print("Framing B flags:", aB["flags"])

ok = True
# The genuine finding: A fires NULL-REACHES-HEADLINE (false positive on the
# supported negative claim), B is clean.
if "NULL-REACHES-HEADLINE" not in aA["flags"]:
    print("FAIL: Framing A did not fire NULL-REACHES-HEADLINE (expected the "
          "claim-polarity false positive)"); ok = False
# The logged-not-flagged note: the data supports the negative claim as
# framed, so the flag is a polarity artifact, not a flaw.
bn_detail = aA["checks"]["BEATS-NULL"]["detail"]
if "claim-polarity" not in bn_detail:
    print("FAIL: Framing A detail lacks the claim-polarity note"); ok = False
if aB["flags"]:
    print("FAIL: Framing B not clean (expected DISCRIMINATES)"); ok = False
# THESIS-OUTRUNS-EVIDENCE should NOT fire in either (thesis_endpoint literal).
if "THESIS-OUTRUNS-EVIDENCE" in aA["flags"] or "THESIS-OUTRUNS-EVIDENCE" in aB["flags"]:
    print("FAIL: THESIS-OUTRUNS-EVIDENCE confounded the test (thesis_endpoint "
          "not literal?)"); ok = False

print("VERDICT:", "CLAIM-POLARITY boundary CONFIRMED (A false-positives, B clean)"
      if ok else "MISMATCH")
raise SystemExit(0 if ok else 1)
