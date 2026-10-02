#!/usr/bin/env python3
"""REFERENT-SELF-KEYED discriminating test (2026-10-02).

The act-fidelity seam (138fec0) proved that emission relocates the self-keyed
gap to the FIDELITY of the emitted artifact: the closing act is emission +
faithful copy. But the closing act itself has a self-keyed structure that the
seam test never grounded: the writer declares BOTH sides of the FIDELITY
byte-match.

  - referent_value = "the reasoning actually performed" (self-declared by the
    writer, who is the subject: the one who performed the reasoning)
  - reading = "the written log" (self-declared by the writer, the artifact)

So the certifier of the referent_value is the writer, who is also the subject.
The writer can make FIDELITY pass by setting referent_value == reading,
regardless of whether the reading faithfully represents the reasoning
performed. FIDELITY at the closing act is then a vacuous check: it certifies
the declared referent matches the reading, which is trivially satisfiable.

The discriminating question:
  Does FIDELITY at the closing act certify a faithful copy, or is it
  self-keyed in the referent_value declaration (the writer can always make it
  pass by re-labeling referent_value to match reading)?

Predicted structure (the referent-self-keyed escape):
  - The writer performed reasoning R but wrote down R' (a distorted copy).
  - Honest declaration (referent_value=R, reading=R'): FIDELITY fires (R != R').
    The distorted copy is caught.
  - Re-labeled declaration (referent_value=R', reading=R'): FIDELITY passes
    (R' == R'). The distorted copy is NOT caught.
  - The writer can make FIDELITY pass by re-labeling referent_value. FIDELITY
    at the closing act does not certify a faithful copy; it only certifies
    that the declared referent_value matches the reading, which is trivially
    satisfiable by the writer. The gap relocates to the referent_value
    declaration, which is a NEW special case of the self-keyed pattern.

Distinct from the docstring's case B (self-keyed, FAITHFUL copy -> provenance
fires, FIDELITY silent): there the copy IS faithful, so FIDELITY passing is
correct, and the self-keyed-ness is caught by the provenance axis. Here the
copy is DISTORTED, so FIDELITY passing is wrong, and no provenance axis fires
in the minimal spec (no provenance fields declared). The instrument is blind.
"""
import sys
import claim_audit as ca

ok = True
def check(label, got, want):
    global ok
    good = (got == want)
    ok = ok and good
    print("%s %s (got %r, want %r)" % ("PASS" if good else "FAIL", label, got, want))

# The writer performed reasoning R but wrote down R' (a distorted copy:
# omits the ruled-out differential B).
R  = "differential: ruled out A, B; chose X on finding F"
Rp = "differential: ruled out A; chose X on finding F"

# Case 1: honest declaration (referent_value = R, the actual reasoning).
honest = {"name": "honest", "pathway_log_emitted": True,
          "referent_value": R, "reading": Rp}
rh = ca.check_fidelity(honest)
print("honest  (referent=R,  reading=R'): FIDELITY pass=%s detail=%r" % (rh[0], rh[2]))

# Case 2: re-labeled declaration (referent_value = R', matching the reading).
relabeled = {"name": "relabeled", "pathway_log_emitted": True,
             "referent_value": Rp, "reading": Rp}
rr = ca.check_fidelity(relabeled)
print("relabel (referent=R', reading=R'): FIDELITY pass=%s detail=%r" % (rr[0], rr[2]))

print()

# The referent-self-keyed structure:
check("honest FIDELITY fires (R != R')", rh[0], False)
check("relabel FIDELITY passes (R' == R')", rr[0], True)
check("writer can make FIDELITY pass by re-labeling referent_value",
      rr[0], True)

# The vacuous-check structure: FIDELITY at the closing act certifies the
# declared referent matches the reading, which is trivially satisfiable. It
# does NOT certify a faithful copy of the reasoning performed.
check("FIDELITY is self-keyed in the referent_value declaration "
      "(honest fires, re-label passes)",
      (rh[0], rr[0]), (False, True))

print()
if ok:
    print("ALL CHECKS PASSED: the closing act is self-keyed in the referent_value")
    print("declaration. FIDELITY at the closing act does not certify a faithful")
    print("copy; it only certifies that the declared referent_value matches the")
    print("reading, which is trivially satisfiable by the writer (re-label")
    print("referent_value == reading). The gap relocates to the referent_value")
    print("declaration: a NEW special case of the self-keyed pattern that the")
    print("existing axes do not catch (the docstring's case B is caught by the")
    print("provenance axis; this case is blind to the instrument).")
    sys.exit(0)
else:
    print("SOME CHECKS FAILED")
    sys.exit(1)
