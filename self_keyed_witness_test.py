#!/usr/bin/env python3
"""SELF-KEYED "undeclared -> lever" regression witness (2026-10-02, post-fix).

The second-mind audit (second_mind_audit_2026-10-02.md) flagged the
SELF-KEYED mapping as the load-bearing co-error candidate: the check's
data-inference fallback treated an UNDECLARED knob_kind as the mechanism's
own lever (fires SELF-KEYED on monotone data). If the knob is actually a
workload axis (batch size, etc.) that just was not declared, the check fired
when the honest label is N/A. The battery (check==truth) could not see this:
the author's naming (SELF-KEYED) agreed with the check's wrong firing, so the
battery stayed green while both were wrong. The second_mind route also fired
on both cells (it re-derives the monotonicity FACT but ignores knob_kind), so
the co-error was invisible to all three votes (check, truth, second).

FIX: the data-inference fallback is now conservative. An UNDECLARED knob_kind
is reported N/A (schema-boundary), not inferred as a lever. SELF-KEYED now
requires a positive knob_kind=lever declaration. The 5 genuine-lever
specimens in the battery carry that declaration, so the battery stays green
via declaration, not inference.

This witness is now a REGRESSION test: it locks in the fixed behavior so the
co-error cannot come back. It uses a TRIPLE of specimens with byte-identical
raw data differing only in the knob_kind declaration. The knob varies across
rows and the metric is strictly monotone in the knob (the SELF-KEYED pattern).
The knob is a workload axis (batch size), established by the W-workload cell.

  W-undeclared : knob_kind absent. The check is N/A (the fix). Correct: the
                 honest label is N/A (the knob is a workload axis).
  W-workload   : knob_kind=workload. The check is N/A. Correct.
  W-lever      : knob_kind=lever. The check fires SELF-KEYED. Correct: this
                 is the positive case (the knob IS the mechanism's own lever).

The co-error is now CLOSED: the check no longer infers the knob's role from
the data, so the author's naming can no longer agree with a wrong firing. If
the author wrongly names W-undeclared SELF-KEYED, the check says N/A, so
check != truth and the battery would catch the mismatch.

The second_mind route still re-derives the monotonicity FACT on all three
cells (the fact is real), but the NAME is now determined by the declaration,
not inference. So the second route confirms the fact; the declaration
determines the name.

Run: python3 self_keyed_witness_test.py   (exit 0 = the regression holds)
"""
import sys
import claim_audit as ca
import second_mind as sm

ok = True

def check(label, got, want):
    global ok
    good = got == want
    if not good:
        ok = False
    print('  [%s] %s -> got %r, want %r' % ('ok' if good else 'MISMATCH', label, got, want))

# Byte-identical raw data: the knob varies, the metric is strictly monotone
# in the knob (the SELF-KEYED pattern). The knob is a workload axis
# (batch size), established by the W-workload cell's declaration.
rows = [
    {"mechanism_on": True, "knob": 0.90, "metric": 0.50},
    {"mechanism_on": True, "knob": 0.95, "metric": 0.60},
    {"mechanism_on": True, "knob": 0.99, "metric": 0.80},
]
w_undeclared = {"name": "W-undeclared", "rows": rows}
w_workload   = {"name": "W-workload",   "rows": rows, "knob_kind": "workload"}
w_lever      = {"name": "W-lever",      "rows": rows, "knob_kind": "lever"}

# The raw data is byte-identical; only the knob_kind declaration differs.
assert w_undeclared["rows"] == w_workload["rows"] == w_lever["rows"], "the triple must share identical raw data"

print('== (1) the check verdict is now declaration-driven (the fix) ==')
ok_u, flag_u, det_u = ca.check_not_self_keyed(w_undeclared)
ok_w, flag_w, det_w = ca.check_not_self_keyed(w_workload)
ok_l, flag_l, det_l = ca.check_not_self_keyed(w_lever)
check('W-undeclared is N/A (the fix: no inference from the data)', flag_u, '')
check('W-workload is N/A (knob_kind=workload)', flag_w, '')
check('W-lever fires SELF-KEYED (knob_kind=lever, the positive case)', flag_l, 'SELF-KEYED')

print('== (2) the honest label for W-undeclared (N/A) now matches the check ==')
# The knob is a workload axis (batch size), established by the identical
# W-workload cell. So the honest label for W-undeclared is N/A, not
# SELF-KEYED. After the fix, the check's verdict (N/A) matches the honest
# label (N/A). The co-error is closed.
honest_label = []  # N/A: no SELF-KEYED flag
check('the check is now correct on W-undeclared (verdict == honest label)',
      (flag_u != '') == (honest_label != []), True)

print('== (3) the co-error is closed: a wrong author naming is now catchable ==')
# Before the fix, the author's naming (SELF-KEYED) agreed with the check's
# wrong firing (SELF-KEYED), so the battery stayed green. After the fix, the
# check says N/A on W-undeclared. If the author wrongly names it SELF-KEYED,
# the check (N/A) != the author's naming (SELF-KEYED), so the battery would
# catch the mismatch. The co-error (check==truth, both wrong) is no longer
# possible.
author_naming_wrong = ['SELF-KEYED']  # the author's WRONG naming
check_fires = flag_u != ''
truth_fires = author_naming_wrong != []
check('a wrong author naming (SELF-KEYED) now disagrees with the check (N/A)',
      check_fires != truth_fires, True)

print('== (4) the second_mind route still re-derives the monotonicity fact ==')
# The second route re-derives the monotonicity FACT (it is real on all three
# cells), but the NAME is now determined by the declaration, not inference.
# So the second route confirms the fact; the declaration determines the name.
sec_u_fired, sec_u_fact = sm.second_self_keyed(w_undeclared)
sec_w_fired, sec_w_fact = sm.second_self_keyed(w_workload)
sec_l_fired, sec_l_fact = sm.second_self_keyed(w_lever)
check('second re-derives the monotonicity fact on W-undeclared', sec_u_fired, True)
check('second re-derives the monotonicity fact on W-workload', sec_w_fired, True)
check('second re-derives the monotonicity fact on W-lever', sec_l_fired, True)
check('the fact is real on all three cells (the name is declaration-driven)',
      sec_u_fired == sec_w_fired == sec_l_fired, True)

print()
if ok:
    print('RESULT: the SELF-KEYED "undeclared -> lever" regression holds.')
    print('  The check is now declaration-driven: undeclared -> N/A, lever -> SELF-KEYED.')
    print('  The co-error (check==truth, both wrong, battery green) is closed.')
    print('  The second_mind route confirms the fact; the declaration determines the name.')
    sys.exit(0)
print('RESULT: the SELF-KEYED "undeclared -> lever" regression FAILED.')
sys.exit(1)
