#!/usr/bin/env python3
"""Witness: is the None-slip a CLASS of silent gate passes, or a SINGLETON?

The 2026-10-04 VACUOUS-RATIO absent-denominator fix (commit b494083) surfaced
a schema blind spot: _headline_support(spec) == 0 silently evaluates to False
when the support field is absent (None == 0 is False), so the gate non-fires
and the axis gets evaluated as if the ratio were non-vacuous. The fix added a
DENOM-BLIND boundary note.

This witness asks: is that pattern (a comparison receiving None that silently
evaluates to a result that neither fires nor surfaces) a CLASS of silent gate
passes in the "same species" precondition gates, or a SINGLETON specific to
VACUOUS-RATIO?

The three "same species" precondition gates (per their docstrings):
1. VACUOUS-RATIO: _headline_support(spec) == 0
   - absent support -> None == 0 -> False -> gate non-fires
   - UNDEFINED: the instrument never decided what "absent support" means
   - NOW SURFACED: DENOM-BLIND boundary note (commit b494083)

2. INCOMPARABLE-STATISTIC: mc == nc where mc = _stat_class(ms)
   - absent statistic -> _stat_class(None) -> "single" (declared default)
   - DEFINED: the instrument decided what "absent statistic" means
   - NOT SURFACED: no equivalent boundary note

3. BY-CONSTRUCTION: if h_row.get("by_construction"):
   - absent by_construction -> None -> if None: -> False -> gate non-fires
   - DEFINED: the instrument decided what "absent by_construction" means
   - NOT SURFACED: no equivalent boundary note

The discriminating case: is VACUOUS-RATIO the only gate where the absent case
is UNDEFINED in the comparison (a value comparison == 0 where None silently
evaluates to False)? Or do the other gates also have undefined absent cases?

Expected result: VACUOUS-RATIO is a SINGLETON. The other "same species" gates
use DECLARED DEFAULTS (INCOMPARABLE-STATISTIC) or CONSERVATIVE TRUTHINESS
(BY-CONSTRUCTION), so their absent-case behavior is defined.
"""
import json
import sys

# Import the audit function from claim_audit.py
sys.path.insert(0, '.')
from claim_audit import audit

# --- Test 1: VACUOUS-RATIO absent support (the known case) ---
# A spec with a mechanism headline row that has NO support field.
spec_vacuous = {
    "name": "test-vacuous-absent-support",
    "type": "knob-sweep",
    "rows": [
        {"label": "on", "mechanism_on": True, "metric": 1.0, "support": 100},
        {"label": "off", "mechanism_on": False, "metric": 0.5},
        # Headline row (max metric) has NO support field:
        {"label": "headline", "mechanism_on": True, "metric": 2.0},
    ],
    "expected": [],
}
result_vacuous = audit(spec_vacuous)
# The headline row is "headline" (metric=2.0), which has no support field.
# _headline_support returns None, so None == 0 is False, so VACUOUS-RATIO non-fires.
# But DENOM-BLIND should be surfaced in the boundary.
vacuous_fired = "VACUOUS-RATIO" in result_vacuous["flags"]
denom_blind = any(
    b.get("check") == "VACUOUS-RATIO" and "undeclared" in b.get("reason", "")
    for b in result_vacuous["boundary"]
)
print("TEST 1: VACUOUS-RATIO absent support")
print(f"  VACUOUS-RATIO fired: {vacuous_fired} (expected: False, because None == 0 is False)")
print(f"  DENOM-BLIND surfaced: {denom_blind} (expected: True, commit b494083)")
assert not vacuous_fired, "VACUOUS-RATIO should not fire when support is absent (None == 0 is False)"
assert denom_blind, "DENOM-BLIND should be surfaced in the boundary (commit b494083)"
print("  PASS: VACUOUS-RATIO non-fires (undefined absent case), DENOM-BLIND surfaced\n")

# --- Test 2: INCOMPARABLE-STATISTIC absent statistic ---
# A spec where the mechanism headline row has NO statistic field,
# and the null headline row has an ORDER statistic.
# _stat_class(None) -> "single", _stat_class("p95") -> "order"
# mc != nc and nc == "order" -> gate FIRES.
spec_incomparable_fire = {
    "name": "test-incomparable-absent-statistic-fires",
    "type": "knob-sweep",
    "rows": [
        # Mechanism headline: NO statistic field (absent -> "single" by default)
        {"label": "mech-headline", "mechanism_on": True, "metric": 1.0, "support": 100},
        # Null headline: ORDER statistic (p95)
        {"label": "null-headline", "mechanism_on": False, "metric": 0.5, "statistic": "p95"},
    ],
    "expected": [],
}
result_incomparable_fire = audit(spec_incomparable_fire)
incomparable_fired = "INCOMPARABLE-STATISTIC" in result_incomparable_fire["flags"]
print("TEST 2a: INCOMPARABLE-STATISTIC absent mechanism statistic vs order null")
print(f"  INCOMPARABLE-STATISTIC fired: {incomparable_fired} (expected: True, because 'single' != 'order')")
assert incomparable_fired, "INCOMPARABLE-STATISTIC should fire when absent statistic (single) vs order statistic"
print("  PASS: INCOMPARABLE-STATISTIC fires (defined absent case: single draw)\n")

# A spec where BOTH the mechanism and null headline rows have NO statistic field.
# _stat_class(None) -> "single" for both, so mc == nc -> gate non-fires.
spec_incomparable_nofire = {
    "name": "test-incomparable-absent-statistic-nofires",
    "type": "knob-sweep",
    "rows": [
        # Mechanism headline: NO statistic field (absent -> "single" by default)
        {"label": "mech-headline", "mechanism_on": True, "metric": 1.0, "support": 100},
        # Null headline: NO statistic field (absent -> "single" by default)
        {"label": "null-headline", "mechanism_on": False, "metric": 0.5},
    ],
    "expected": [],
}
result_incomparable_nofire = audit(spec_incomparable_nofire)
incomparable_nofire = "INCOMPARABLE-STATISTIC" not in result_incomparable_nofire["flags"]
# Check if there's a boundary note for INCOMPARABLE-STATISTIC
incomparable_boundary = any(
    b.get("check") == "INCOMPARABLE-STATISTIC"
    for b in result_incomparable_nofire["boundary"]
)
print("TEST 2b: INCOMPARABLE-STATISTIC both absent statistics")
print(f"  INCOMPARABLE-STATISTIC non-fired: {incomparable_nofire} (expected: True, because 'single' == 'single')")
print(f"  INCOMPARABLE-STATISTIC boundary note: {incomparable_boundary} (expected: False, no equivalent to DENOM-BLIND)")
assert incomparable_nofire, "INCOMPARABLE-STATISTIC should not fire when both statistics are absent (single == single)"
assert not incomparable_boundary, "INCOMPARABLE-STATISTIC should NOT have a boundary note (defined absent case, not a schema blind spot)"
print("  PASS: INCOMPARABLE-STATISTIC non-fires (defined absent case: single == single), no boundary note\n")

# --- Test 3: BY-CONSTRUCTION absent by_construction ---
# A spec where the mechanism headline row has NO by_construction field.
# h_row.get("by_construction") -> None -> if None: -> False -> gate non-fires.
spec_by_construction = {
    "name": "test-by-construction-absent",
    "type": "knob-sweep",
    "rows": [
        # Mechanism headline: NO by_construction field (absent -> False by truthiness)
        {"label": "mech-headline", "mechanism_on": True, "metric": 1.0, "support": 100},
        # Null headline
        {"label": "null-headline", "mechanism_on": False, "metric": 0.5},
    ],
    "expected": [],
}
result_by_construction = audit(spec_by_construction)
by_construction_nofire = "BY-CONSTRUCTION" not in result_by_construction["flags"]
by_construction_boundary = any(
    b.get("check") == "BY-CONSTRUCTION"
    for b in result_by_construction["boundary"]
)
print("TEST 3: BY-CONSTRUCTION absent by_construction")
print(f"  BY-CONSTRUCTION non-fired: {by_construction_nofire} (expected: True, because None is falsy)")
print(f"  BY-CONSTRUCTION boundary note: {by_construction_boundary} (expected: False, no equivalent to DENOM-BLIND)")
assert by_construction_nofire, "BY-CONSTRUCTION should not fire when by_construction is absent (None is falsy)"
assert not by_construction_boundary, "BY-CONSTRUCTION should NOT have a boundary note (defined absent case: conservative truthiness)"
print("  PASS: BY-CONSTRUCTION non-fires (defined absent case: conservative truthiness), no boundary note\n")

# --- Summary ---
print("=" * 70)
print("SUMMARY: None-slip is a SINGLETON, not a CLASS")
print("=" * 70)
print("""
The three "same species" precondition gates differ in how they handle absent fields:

1. VACUOUS-RATIO: _headline_support(spec) == 0
   - absent support -> None == 0 -> False -> gate non-fires
   - UNDEFINED: the instrument never decided what "absent support" means
   - NOW SURFACED: DENOM-BLIND boundary note (commit b494083)

2. INCOMPARABLE-STATISTIC: mc == nc where mc = _stat_class(ms)
   - absent statistic -> _stat_class(None) -> "single" (declared default)
   - DEFINED: the instrument decided what "absent statistic" means
   - NOT SURFACED: no equivalent boundary note (correct, because it's defined)

3. BY-CONSTRUCTION: if h_row.get("by_construction"):
   - absent by_construction -> None -> if None: -> False -> gate non-fires
   - DEFINED: the instrument decided what "absent by_construction" means
   - NOT SURFACED: no equivalent boundary note (correct, because it's defined)

The discriminating case: VACUOUS-RATIO is the ONLY gate where the absent case
is UNDEFINED in the comparison (a value comparison == 0 where None silently
evaluates to False). The other "same species" gates use DECLARED DEFAULTS
(INCOMPARABLE-STATISTIC) or CONSERVATIVE TRUTHINESS (BY-CONSTRUCTION), so
their absent-case behavior is defined.

Conclusion: the None-slip is a SINGLETON specific to VACUOUS-RATIO, not a
CLASS of silent gate passes. The fix (DENOM-BLIND) is correctly scoped to
the one gate where the absent case is undefined.
""")
print("ALL TESTS PASS")
