#!/usr/bin/env python3
"""ACT-FIDELITY SEAM discriminating test (2026-10-02).

The 09:26 seam: the emission mechanism (a1031af7, mechanism b =
witness-requires-emission, 'in principle closeable') joins the FIDELITY axis
at the closing act. The emission test (sims/claim-audit/emission_selfkeyed_test.py)
proved mechanism b is invisible to the 31-check SIMS instrument (no FIDELITY
axis; pathway_log_emitted read by no check; toggle boundary-constant 23==23).

But 'in principle closeable' was never made precise: WHAT closes it, and what
structure does the closing have? This test grounds the seam against the REPO
instrument (claim_audit.py), which HAS the FIDELITY axis (40th). The
discriminating question:

  Does emission (pathway_log_emitted=True) close the self-keyed gap, or does it
  relocate it to the FIDELITY of the emitted artifact (does the written log
  byte-match the reasoning actually performed)?

Predicted structure (the seam made precise):
  - FIDELITY reads referent_value/reading, NOT pathway_log_emitted. So the
    emission toggle is boundary-constant for FIDELITY: declaring the log
    emitted does not, by itself, make FIDELITY fire or pass. Emission alone
    does not close the gap.
  - The gap becomes closeable only when the emitted artifact is declared as a
    FIDELITY referent pair. Written log byte-matches reasoning performed ->
    FIDELITY passes (faithful copy; the closing act is complete). They differ
    -> FIDELITY fires (distorted copy; emission relocated the self-keyed gap
    from the pathway to the fidelity of the artifact).
"""
import sys
import claim_audit as ca

ok = True
def check(label, got, want):
    global ok
    good = (got == want)
    ok = ok and good
    print("%s %s (got %r, want %r)" % ("PASS" if good else "FAIL", label, got, want))

# The four arms differ only in the emission declaration and the FIDELITY
# referent pair. pathway_log_emitted is the emission toggle; referent_value is
# the reasoning actually performed; reading is the written log.
E0   = {"name": "E0",  "pathway_log_emitted": False}
E1   = {"name": "E1",  "pathway_log_emitted": True}
E1_F = {"name": "E1-F", "pathway_log_emitted": True,
        "referent_value": "differential: ruled out A, B; chose X on finding F",
        "reading":        "differential: ruled out A, B; chose X on finding F"}
E1_D = {"name": "E1-D", "pathway_log_emitted": True,
        "referent_value": "differential: ruled out A, B; chose X on finding F",
        "reading":        "differential: ruled out A; chose X on finding F"}

r0 = ca.check_fidelity(E0)
r1 = ca.check_fidelity(E1)
rf = ca.check_fidelity(E1_F)
rd = ca.check_fidelity(E1_D)

print("E0  (not emitted, no pair):   FIDELITY pass=%s detail=%r" % (r0[0], r0[2]))
print("E1  (emitted, no pair):       FIDELITY pass=%s detail=%r" % (r1[0], r1[2]))
print("E1-F(emitted, faithful copy): FIDELITY pass=%s detail=%r" % (rf[0], rf[2]))
print("E1-D(emitted, distorted copy):FIDELITY pass=%s detail=%r" % (rd[0], rd[2]))
print()

# The seam made precise:
check("E0 FIDELITY N/A (pass=True) when the log is not emitted and no pair declared", r0[0], True)
check("E1 FIDELITY N/A (pass=True) when the log is emitted but no pair declared", r1[0], True)
check("emission toggle is boundary-constant for FIDELITY (E0 and E1 give the identical result)", (r0[0], r0[2]) == (r1[0], r1[2]), True)
check("E1-F FIDELITY passes (faithful copy: the written log byte-matches the reasoning performed)", rf[0], True)
check("E1-D FIDELITY fires (pass=False, flag=FIDELITY): the written log omits a ruled-out differential", (rd[0], rd[1]), (False, "FIDELITY"))

print()
if ok:
    print("ACT-FIDELITY SEAM PROVEN against the repo instrument: FIDELITY reads referent_value/reading, not pathway_log_emitted. Emission alone is boundary-constant (blind) and does not close the self-keyed gap; the gap relocates to the FIDELITY of the emitted artifact. The closing act is emission + a faithful copy: a faithful written log passes FIDELITY, a distorted one fires it.")
    sys.exit(0)
else:
    print("ACT-FIDELITY SEAM NOT PROVEN: see FAIL lines above.")
    sys.exit(1)
