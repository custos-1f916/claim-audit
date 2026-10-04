#!/usr/bin/env python3
"""VACUOUS-RATIO witness: does the instrument flag a MISSING denominator,
or silently certify a ratio whose denominator it never saw?

Four Ledgers (arXiv 2609.15015) names the failure mode: "an empty detector
output is an observed outcome, not a missing row." This witness checks whether
claim_audit's VACUOUS-RATIO guard covers the ABSENT-support case, not just the
declared support=0 case.

Findings (2026-10-04):
  Case A (support=0 declared)  -> verdict VACUOUS-RATIO, flagged. CORRECT.
  Case B (support field absent)-> verdict DISCRIMINATES, zero flags,
                                  BEATS-NULL fires "mechanism 1 > null 0.5".
                                  The absent denominator is treated as a
                                  missing row, not an observed outcome.

The instrument emits `na` only when support is DECLARED as 0. When the support
field is absent, _headline_support returns None, the VACUOUS-RATIO guard does
not fire, and the ratio is certified. That is the self-keyed gap in the
instrument itself: the denominator it needs to see is exactly the one it does
not see (the deciding metric is the one the emitter cannot see).

Zero imports beyond claim_audit. Deterministic. Selftest at the bottom.
"""
import json
import sys

sys.path.insert(0, ".")
import claim_audit as ca


def _case_a():
    """Mechanism headline row declares support=0 (empty denominator)."""
    return {
        "name": "zero-support headline (witness A)",
        "type": "regime-sweep",
        "mechanism": "m", "metric": "accuracy",
        "stated_headline": 1.0,
        "rows": [
            {"label": "mech headline", "mechanism_on": True, "metric": 1.0, "support": 0},
            {"label": "null", "mechanism_on": False, "is_null": True, "metric": 0.5},
        ],
    }


def _case_b():
    """Mechanism headline row has NO support field (absent denominator)."""
    return {
        "name": "no-support-field headline (witness B)",
        "type": "regime-sweep",
        "mechanism": "m", "metric": "accuracy",
        "stated_headline": 1.0,
        "rows": [
            {"label": "mech headline", "mechanism_on": True, "metric": 1.0},
            {"label": "null", "mechanism_on": False, "is_null": True, "metric": 0.5},
        ],
    }


def run():
    out = {}
    for tag, spec in (("A", _case_a()), ("B", _case_b())):
        res = ca.audit(spec)
        out[tag] = {
            "headline_support": ca._headline_support(spec),
            "verdict": res["verdict"],
            "flags": res["flags"],
            "noise_floor": res["checks"]["NOISE-FLOOR"],
            "beats_null": res["checks"]["BEATS-NULL"],
        }
    return out


def selftest():
    out = run()
    a, b = out["A"], out["B"]
    # Case A: the declared-zero case is caught.
    assert a["headline_support"] == 0, a
    assert a["verdict"] == "VACUOUS-RATIO", a
    assert "VACUOUS-RATIO" in a["flags"], a
    assert a["noise_floor"]["detail"].startswith("N/A (VACUOUS-RATIO"), a
    # Case B: the absent case is NOT caught -- the gap.
    assert b["headline_support"] is None, b
    assert b["verdict"] == "DISCRIMINATES", b
    assert b["flags"] == [], b
    assert b["beats_null"]["pass"] is True, b
    assert "1 > null 0.5" in b["beats_null"]["detail"], b
    return out


def main():
    out = selftest()
    print(json.dumps(out, indent=2))
    print()
    print("SELFTEST PASS: declared support=0 is flagged (VACUOUS-RATIO);")
    print("absent support is NOT flagged (DISCRIMINATES, BEATS-NULL fires).")
    print("The instrument certifies a ratio whose denominator it never saw.")


if __name__ == "__main__":
    main()
