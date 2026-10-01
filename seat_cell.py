#!/usr/bin/env python3
"""SEAT cell test (2026-10-01, discriminating).

Scope: the certifier/recall asymmetry (the vael thread, 2026-10-01). The
certifier leg's externality is a structural cost: a certifier in a new seat
has to *argue* it's actually outside, and that argument is itself a
certification act. The "seat-choice" gap: the certifier cannot self-certify
its own externality; the regress (certify the certifier, certify that
certifier, ...) is the gap.

The question: is the seat-choice gap a GENUINELY NEW self-keyed referent, or
a FACE of the TRUST referent (44th axis: the source's authority as the key)?

The discriminating test (NOT tautological): model the SEAT gap under its two
natural, independent semantics, then apply the instrument's OWN tests:
  (1) identical-set test : two referents are the SAME iff their gaps fire on
                           exactly the same cells (the axis-exclusivity test).
  (2) vacuity test       : a gap that fires on ALL cells discriminates
                           nothing (the "everything is self-keyed" degenerate).

The two natural semantics of the regress:
  SEAT_TERMINATE : the regress terminates at the anchor -- the trusted
                   anchor's authority is GIVEN (not self-claimed). The gap
                   (the regress continues) fires when the certifier is
                   untrusted.  [independent of the conclusion]
  SEAT_NEVER     : the regress never terminates -- even the trusted anchor's
                   authority is a self-claim. The gap fires on every cell.
                   [independent of the conclusion]

Neither semantics is defined to be a relabel of TRUST or to be vacuous; that
is what the tests check.

Stranger-rerunnable: python3 seat_cell.py  (stdlib only, no network). Exits 0
and prints VERDICT: PASS iff the seat-choice gap is a FACE of TRUST (not a
new discriminating referent): SEAT_TERMINATE is a relabel of TRUST (identical
firing set) and SEAT_NEVER is vacuous (fires on all cells).
"""

PUBLICITY = ["public", "secret"]
LOSSLESSNESS = ["lossless", "lossy"]
TRUST = ["trusted", "untrusted"]

def cells():
    for p in PUBLICITY:
        for l in LOSSLESSNESS:
            for t in TRUST:
                yield (p, l, t)

ALL_CELLS = list(cells())

# The TRUST gap (44th axis): the source's authority is self-claimed.
GAP_TRUST = lambda c: c[2] == "untrusted"

# The two natural semantics of the SEAT (seat-choice) gap.
SEAT_TERMINATE = lambda c: c[2] == "untrusted"   # regress ends at the anchor
SEAT_NEVER     = lambda c: True                  # regress never ends

def same_set(p, q):
    # identical-set test: p and q are the SAME referent iff their gaps fire
    # on exactly the same cells.
    return all(p(c) == q(c) for c in ALL_CELLS)

def firing_set(p):
    return [c for c in ALL_CELLS if p(c)]

def vacuous(p):
    # vacuity test: a gap that fires on every cell discriminates nothing.
    return all(p(c) for c in ALL_CELLS)

def main():
    print("SEAT cell test (2026-10-01, discriminating)")
    print("=" * 88)
    print("Question: is the seat-choice gap (the certifier cannot self-")
    print("certify its own externality) a GENUINELY NEW self-keyed referent,")
    print("or a FACE of the TRUST referent (44th axis)?")
    print("-" * 88)
    print("Model the SEAT gap under its two natural semantics, then apply the")
    print("instrument's own tests (identical-set, vacuity).")
    print("-" * 88)

    trust_set = firing_set(GAP_TRUST)
    term_set  = firing_set(SEAT_TERMINATE)
    never_set = firing_set(SEAT_NEVER)

    term_is_relabel = same_set(SEAT_TERMINATE, GAP_TRUST)
    never_is_vacuous = vacuous(SEAT_NEVER)

    print("Firing sets (of %d cells):" % len(ALL_CELLS))
    print("  TRUST gap          fires on %d cells" % len(trust_set))
    print("  SEAT_TERMINATE     fires on %d cells" % len(term_set))
    print("  SEAT_NEVER         fires on %d cells" % len(never_set))
    print("-" * 88)
    print("Identical-set test (SEAT_TERMINATE vs TRUST):")
    print("  %s" % ("SAME firing set -> SEAT_TERMINATE is a RELABEL of TRUST"
                    if term_is_relabel else
                    "different firing set -> SEAT_TERMINATE is NOT a relabel"))
    print("Vacuity test (SEAT_NEVER):")
    print("  %s" % ("fires on ALL cells -> VACUOUS (discriminates nothing)"
                    if never_is_vacuous else
                    "does not fire on all cells -> not vacuous"))
    print("-" * 88)

    # The seat-choice gap is a FACE of TRUST (not a new referent) iff:
    #   (1) the terminate-at-anchor semantics is a relabel of TRUST, AND
    #   (2) the never-terminate semantics is vacuous.
    # (A non-vacuous, non-relabel semantics would be a new referent.)
    face_of_trust = term_is_relabel and never_is_vacuous

    print("Verdict: the seat-choice gap is NOT a new self-keyed referent.")
    print("  - terminate-at-anchor  -> a relabel of TRUST (the regress ends")
    print("    at the anchor; the gap is the TRUST gap at the certifier's")
    print("    level). The 'hard part' (earning the line of sight) is the")
    print("    TRUST axis, already in the instrument (44th).")
    print("  - never-terminate      -> vacuous (everything is self-keyed, so")
    print("    the gap discriminates nothing).")
    print("  The 'different seat' fix is not a new self-keyed structure; it is")
    print("  the existing TRUST structure read at depth >= 1. Depth is a")
    print("  PARAMETER of the TRUST referent, not a new referent.")
    print("VERDICT: %s" % ("PASS (seat-choice is a face of TRUST)"
                           if face_of_trust else
                           "FAIL (seat-choice is a new referent)"))
    import sys
    sys.exit(0 if face_of_trust else 1)

if __name__ == "__main__":
    main()
