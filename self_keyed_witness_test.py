#!/usr/bin/env python3
"""SELF-KEYED "undeclared -> lever" discriminating witness (2026-10-02).

The second-mind audit (second_mind_audit_2026-10-02.md) flagged the
SELF-KEYED mapping as the load-bearing co-error candidate: the check's
data-inference fallback treats an UNDECLARED knob_kind as the mechanism's
own lever (fires SELF-KEYED on monotone data). If the knob is actually a
workload axis (batch size, etc.) that just was not declared, the check fires
when the honest label is N/A. The battery (check==truth) can see this only if
the truth label encodes the HONEST answer, not the same assumption.

This witness isolates the assumption as the sole load-bearing variable: a
PAIR of specimens with byte-identical raw data differing only in the
knob_kind declaration. The knob varies across rows and the metric is strictly
monotone in the knob (the SELF-KEYED pattern). The knob is a workload axis
(batch size), established by the W-workload cell's declaration.

  W-undeclared : knob_kind absent. The check fires SELF-KEYED (data-inference
                 fallback: knob varies -> lever). But the honest label is N/A
                 (the knob is a workload axis) -> the check is WRONG.
  W-workload   : knob_kind=workload. The check is N/A. Correct.

The co-error: if the author's naming for W-undeclared is SELF-KEYED (the
check's verdict), then check==truth==SELF-KEYED and the battery stays GREEN,
but both are wrong (the honest label is N/A). The second_mind route also
fires on both cells (it re-derives the monotonicity FACT but ignores
knob_kind), so the co-error is invisible to all three votes (check, truth,
second). This witness is the route that sees it.

Run: python3 self_keyed_witness_test.py   (exit 0 = the witness behaves as expected)
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

# The raw data is byte-identical; only the knob_kind declaration differs.
assert w_undeclared["rows"] == w_workload["rows"], "the pair must share identical raw data"

print('== (1) the check verdict flips on the undeclared field ==')
ok_u, flag_u, det_u = ca.check_not_self_keyed(w_undeclared)
ok_w, flag_w, det_w = ca.check_not_self_keyed(w_workload)
check('W-undeclared fires SELF-KEYED (data-inference fallback)', flag_u, 'SELF-KEYED')
check('W-workload is N/A (knob_kind=workload)', flag_w, '')
check('the verdict differs (the assumption is load-bearing)', flag_u != flag_w, True)

print('== (2) the honest label for W-undeclared is N/A (the knob is a workload axis) ==')
# The knob is a workload axis (batch size), established by the identical
# W-workload cell. So the honest label for W-undeclared is N/A, not
# SELF-KEYED. The check's verdict (SELF-KEYED) != the honest label (N/A).
honest_label = []  # N/A: no SELF-KEYED flag
check('the check is wrong on W-undeclared (verdict != honest label)',
      (flag_u != '') != (honest_label != []), True)

print('== (3) the co-error: author naming == check, both wrong, battery green ==')
# If the author's naming for W-undeclared is SELF-KEYED (the check's
# verdict), then check==truth==SELF-KEYED and the battery stays GREEN, but
# both are wrong (the honest label is N/A).
author_naming = ['SELF-KEYED']  # the author's naming (the check's verdict)
check_fires = flag_u != ''
truth_fires = author_naming != []
check('check==truth (the battery stays green)', check_fires == truth_fires, True)
check('but both are wrong (the honest label is N/A)',
      (check_fires and truth_fires) and (honest_label == []), True)

print('== (4) the second_mind route also fires on both (confirms the fact, not the name) ==')
sec_u_fired, sec_u_fact = sm.second_self_keyed(w_undeclared)
sec_w_fired, sec_w_fact = sm.second_self_keyed(w_workload)
check('second fires on W-undeclared (re-derives the monotonicity fact)', sec_u_fired, True)
check('second fires on W-workload (re-derives the monotonicity fact)', sec_w_fired, True)
check('the second route is blind to the co-error (fires on both)', sec_u_fired == sec_w_fired, True)

print()
if ok:
    print('RESULT: the SELF-KEYED "undeclared -> lever" witness behaves as expected.')
    print('  The check fires SELF-KEYED on W-undeclared when the honest label is N/A.')
    print('  The co-error (author naming == check, both wrong, battery green) is real.')
    print('  The second_mind route is blind to it (confirms the fact, not the name).')
    sys.exit(0)
print('RESULT: the SELF-KEYED "undeclared -> lever" witness FAILED.')
sys.exit(1)
