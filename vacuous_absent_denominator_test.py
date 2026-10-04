#!/usr/bin/env python3
"""VACUOUS-RATIO absent-denominator witness (2026-10-04).

The gap this locks in: the VACUOUS-RATIO precondition gate in audit() tests
`_headline_support(spec) == 0`, but _headline_support returns None when the
mechanism's headline row declares NO support field. `None == 0` is False, so
an ABSENT denominator silently passed: BEATS-NULL fired and the verdict was
DISCRIMINATES, while the instrument certified a ratio whose denominator it
never saw.

The fix (2026-10-04) is the calibration-boundary surface, not a new fire:
an absent denominator is a schema blind spot (the emitter did not report the
denominator), distinct from a DECLARED support of 0 (a reported empty
denominator, which fires VACUOUS-RATIO). The fix adds a VACUOUS-RATIO
schema-conditional boundary note when the headline row is present but its
support field is absent. It is additive: verdict and flags are unchanged.

Witnessed three ways:
  (1) ABSENT support  -> verdict DISCRIMINATES, no VACUOUS-RATIO flag, but a
      VACUOUS-RATIO schema-conditional boundary note IS present.
  (2) DECLARED support=0 -> verdict VACUOUS-RATIO (the fire), and NO boundary
      note (the denominator is declared, not blind).
  (3) NO mechanism row -> no VACUOUS-RATIO boundary note (nothing to be blind
      to; the no-empirical regime governs).
"""
import claim_audit as ca

ok = True
def check(label, got, want):
    global ok
    good = (got == want)
    ok = ok and good
    print("%s %s (got %r, want %r)" % ("PASS" if good else "FAIL", label, got, want))

def _spec(support):
    row = {"label": "mech headline", "mechanism_on": True, "metric": 1.0}
    if support is not None:
        row["support"] = support
    return {
        "name": "witness",
        "type": "regime-sweep",
        "mechanism": "m", "metric": "accuracy",
        "stated_headline": 1.0,
        "rows": [
            row,
            {"label": "null", "mechanism_on": False, "is_null": True, "metric": 0.5},
        ],
    }

def _vacuous_boundary(res):
    return [b for b in res.get("boundary", []) if b["check"] == "VACUOUS-RATIO"]

# (1) absent support: blind spot, not a fire
a = ca.audit(_spec(None))
check("(1) absent support: _headline_support is None", ca._headline_support(_spec(None)), None)
check("(1) absent support: verdict is DISCRIMINATES (additive, not a fire)", a["verdict"], "DISCRIMINATES")
check("(1) absent support: no VACUOUS-RATIO flag", "VACUOUS-RATIO" in a["flags"], False)
check("(1) absent support: VACUOUS-RATIO boundary note present", len(_vacuous_boundary(a)), 1)
check("(1) absent support: note is schema-conditional", _vacuous_boundary(a)[0]["note"].startswith("schema-conditional"), True)

# (2) declared support=0: the fire, not the blind spot
z = ca.audit(_spec(0))
check("(2) declared support=0: _headline_support is 0", ca._headline_support(_spec(0)), 0)
check("(2) declared support=0: verdict is VACUOUS-RATIO (the fire)", z["verdict"], "VACUOUS-RATIO")
check("(2) declared support=0: VACUOUS-RATIO flag present", "VACUOUS-RATIO" in z["flags"], True)
check("(2) declared support=0: NO VACUOUS-RATIO boundary note (declared, not blind)", len(_vacuous_boundary(z)), 0)

# (3) no mechanism row: nothing to be blind to
n = ca.audit({
    "name": "no-mech", "type": "regime-sweep",
    "mechanism": "m", "metric": "accuracy",
    "rows": [{"label": "null", "mechanism_on": False, "is_null": True, "metric": 0.5}],
})
check("(3) no mechanism row: _headline_support is None", ca._headline_support({"rows": []}), None)
check("(3) no mechanism row: NO VACUOUS-RATIO boundary note", len(_vacuous_boundary(n)), 0)

print()
print("VERDICT:", "ABSENT-DENOMINATOR FIX CONFIRMED (blind spot surfaced as a boundary note; declared-0 still fires; verdicts unchanged)" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
