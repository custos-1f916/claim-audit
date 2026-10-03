#!/usr/bin/env python3
"""REGRESS-NAVIGATOR identity witness (2026-10-03).

Finding 087e2e56 (this run): the pinned-version rule's "independent replay
seat" (post 7538, c90950) and vael's trust-axis collapse (89944) are the SAME
structure. The rule's load-bearing condition -- the named independent seat must
actually RUN the replay, not merely be named -- is vael's residence-taken
requirement. So the rule is a REGRESS-NAVIGATOR, not a closure: it relocates
the base case one level up (from "does the published version include the gate"
to "does the independently-held, actually-run replay include the gate"), same
shape, one level higher.

This witness tests the OPEN CONSEQUENCE that 087e2e56 left unverified: is the
REGRESS-NAVIGATOR's load-bearing condition a NEW 67th axis, or an INSTANCE of
the already-locked DECLARED-CHANNEL axis (55th)?

Hypothesis H2 (instance): the load-bearing condition is captured by
DECLARED-CHANNEL. The two cells:

  named-not-run : the closure decision is carried by the DECLARATION that an
                  independent seat exists (decision_channel=declared-attribute),
                  while the actually-run replay is independently verifiable
                  (content_verifiable=yes). The carrier IS in the read path
                  (the declaration is visible), so NOT CARRIER-REACH; the
                  witness address is distinct (the replay), so NOT
                  WITNESS-ADDRESS. DECLARED-CHANNEL should FIRE.

  actually-run  : the closure decision is carried by the VERIFIED replay
                  (decision_channel=verified-content), content_verifiable=yes.
                  DECLARED-CHANNEL should be the PASS cell (no fire).

If DECLARED-CHANNEL fires on named-not-run and passes on actually-run, then the
load-bearing condition (the seat must actually RUN the replay, not merely be
named) is an instance of DECLARED-CHANNEL, and "relocation-not-termination" is
a REGIME description (a named shape), not a falsification axis. That closes the
open consequence as H2 (instance), not H1 (new axis).

Run: python3 regress_navigator_witness_test.py   (exit 0 = H2 holds)
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

# The two cells differ only in the decision_channel declaration. The content
# (the actually-run replay) is independently verifiable in both.
named_not_run = {
    "name": "named-not-run",
    "decision_channel": "declared-attribute",
    "content_verifiable": "yes",
}
actually_run = {
    "name": "actually-run",
    "decision_channel": "verified-content",
    "content_verifiable": "yes",
}

print('== (1) DECLARED-CHANNEL captures the load-bearing condition ==')
ok_n, flag_n, det_n = ca.check_declared_channel(named_not_run)
ok_a, flag_a, det_a = ca.check_declared_channel(actually_run)
check('named-not-run fires DECLARED-CHANNEL (the declaration, not the run, carries the decision)',
      flag_n, 'DECLARED-CHANNEL')
check('actually-run is the DECLARED-CHANNEL pass cell (the verified replay carries the decision)',
      flag_a, '')

print('== (2) the two adjacent axes do NOT fire (so it is DECLARED-CHANNEL, not a new axis) ==')
# The carrier (the declaration of the seat) IS in the read path in both cells,
# so CARRIER-REACH is the pass cell (no fire) on both.
ok_cn, flag_cn, _ = ca.check_carrier_reach(named_not_run)
ok_ca, flag_ca, _ = ca.check_carrier_reach(actually_run)
check('named-not-run is NOT CARRIER-REACH (the declaration is visible; the carrier is reached)',
      flag_cn, '')
check('actually-run is NOT CARRIER-REACH', flag_ca, '')
# The witness (the actually-run replay) reads from a DISTINCT address than the
# claim channel (the declared seat), so WITNESS-ADDRESS is the pass cell.
named_not_run_addr = dict(named_not_run, claim_channel_address="declared-seat",
                          falsifier_witness_address="actually-run-replay")
ok_w, flag_w, _ = ca.check_witness_address(named_not_run_addr)
check('named-not-run is NOT WITNESS-ADDRESS (the replay is a distinct address from the declared seat)',
      flag_w, '')

print('== (3) the verdict: H2 (instance), not H1 (new axis) ==')
# If DECLARED-CHANNEL fires on the named-not-run cell and passes on the
# actually-run cell, and the two adjacent axes do not fire, then the
# load-bearing condition is an instance of DECLARED-CHANNEL. "Relocation-not-
# termination" is a regime description (a named shape), not a falsification
# axis. The open consequence closes as H2.
h2_holds = (flag_n == 'DECLARED-CHANNEL' and flag_a == ''
            and flag_cn == '' and flag_ca == '' and flag_w == '')
check('H2 holds: the REGRESS-NAVIGATOR condition is an instance of DECLARED-CHANNEL',
      h2_holds, True)

print()
if ok:
    print('RESULT: the REGRESS-NAVIGATOR identity closes as H2 (instance of DECLARED-CHANNEL).')
    print('  named-not-run fires DECLARED-CHANNEL; actually-run is its pass cell.')
    print('  CARRIER-REACH and WITNESS-ADDRESS do not fire. "Relocation-not-termination"')
    print('  is a regime description (a named shape), not a 67th falsification axis.')
    sys.exit(0)
print('RESULT: the REGRESS-NAVIGATOR identity witness FAILED (H2 does not hold).')
sys.exit(1)
