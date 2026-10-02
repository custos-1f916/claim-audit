"""
WRONG-AXIS 'tie -> wrong-axis' regression witness.

The second-mind audit (run 4ad5e24f) flagged WRONG-AXIS as the remaining
WEAK axis: its fact is a tie (0 <= 0), the weakest CO-MOVES failure, which
under-determines the stronger "wrong-axis" label.

This witness isolates the tie assumption as the sole load-bearing variable:
a W-triple differing ONLY in the mechanism-axis value (tie vs below vs above).

  W-tie   : mechanism_axis = 0.0, null_axis = 0.0 (tie). The check fires
            WRONG-AXIS (mode a: at/below null). The tie is a legitimate
            part of the WRONG-AXIS pattern: the mechanism's own axis is at
            the null (0), so the mechanism is not doing anything on its own
            axis. The headline is on a different axis. So the mechanism is
            on the wrong axis.
  W-below : mechanism_axis = -0.1, null_axis = 0.0 (below). The check fires
            WRONG-AXIS (mode a: at/below null). Correct: the mechanism is
            BELOW the null on its own axis.
  W-above : mechanism_axis = 0.1, null_axis = 0.0 (above). The check does
            NOT fire WRONG-AXIS (the mechanism beats the null on its own
            axis). Correct: the mechanism is doing something on its own
            axis.

The tie is a legitimate part of the WRONG-AXIS pattern. The check fires
WRONG-AXIS on the tie case (correct). The below case also fires WRONG-AXIS
(correct). The above case does NOT fire WRONG-AXIS (correct).

Run: python3 wrong_axis_witness_test.py   (exit 0 = the regression holds)
"""
import sys
import claim_audit as ca

ok = True

def check(label, got, want):
    global ok
    good = got == want
    if not good:
        ok = False
    print('  [%s] %s -> got %r, want %r' % ('ok' if good else 'MISMATCH', label, got, want))

# W-tie: mechanism_axis = 0.0, null_axis = 0.0 (tie)
w_tie = {
    "spec": "W-tie",
    "rows": [
        {"label": "mechanism", "mechanism_on": True, "metric": 1.0, "mechanism_axis": 0.0},
        {"label": "null", "mechanism_on": False, "is_null": True, "metric": 0.0, "mechanism_axis": 0.0},
    ],
}

# W-below: mechanism_axis = -0.1, null_axis = 0.0 (below)
w_below = {
    "spec": "W-below",
    "rows": [
        {"label": "mechanism", "mechanism_on": True, "metric": 1.0, "mechanism_axis": -0.1},
        {"label": "null", "mechanism_on": False, "is_null": True, "metric": 0.0, "mechanism_axis": 0.0},
    ],
}

# W-above: mechanism_axis = 0.1, null_axis = 0.0 (above)
w_above = {
    "spec": "W-above",
    "rows": [
        {"label": "mechanism", "mechanism_on": True, "metric": 1.0, "mechanism_axis": 0.1},
        {"label": "null", "mechanism_on": False, "is_null": True, "metric": 0.0, "mechanism_axis": 0.0},
    ],
}

# Run the check on all three
tie_res = ca.check_co_moves(w_tie)
below_res = ca.check_co_moves(w_below)
above_res = ca.check_co_moves(w_above)

print("W-tie:   %s" % (tie_res,))
print("W-below: %s" % (below_res,))
print("W-above: %s" % (above_res,))

# The tie is a legitimate part of the WRONG-AXIS pattern. The check fires
# WRONG-AXIS on the tie case (correct). The below case also fires WRONG-AXIS
# (correct). The above case does NOT fire WRONG-AXIS (correct).
check("W-tie fires WRONG-AXIS (the tie is a legitimate part of the pattern)", tie_res[1], "WRONG-AXIS")
check("W-below fires WRONG-AXIS (correct)", below_res[1], "WRONG-AXIS")
check("W-above does NOT fire WRONG-AXIS (the mechanism beats the null)", above_res[1], "")

sys.exit(0 if ok else 1)
