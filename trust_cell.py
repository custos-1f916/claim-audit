#!/usr/bin/env python3
"""TRUST cell test (2026-09-28; criterion corrected 2026-10-02, f3ec9e1).

Scope: the two-terminus synthesis (2026-09-28). PUBLICITY (3ddd51b0) and
what-is-recorded (2e9551e5) are two faces of ONE self-keyed act (the writer
choosing what a stranger can verify): PUBLICITY = control over channel OPENNESS
(public artifact vs private secret); what-is-recorded = control over content
LOSSINESS (which lossy function state->record). A stranger's verifiability is
bounded by the WEAKER of the two, so they are the same collapse read from two
ends (openness vs lossiness), not independent.

The two terminuses each pointed toward a 'genuinely new self-keyed referent'
but never stated the discriminating test. This test states it.

  CORRECTED CRITERION (2026-10-02, f3ec9e1): the witness-cell test.
  A candidate self-keyed referent C is GENUINELY NEW iff SOME cell exists
  where ALL known termini's gaps are False but C's gap is True (C adds a cell
  no known terminus covers).

  The original weak criterion ("C's gap survives BOTH (a) full publicity and
  (b) losslessness", i.e. is not implied by either SINGLE terminus) let a
  DISJUNCTION of the two known termini (secret OR lossy) pass both arms and
  masquerade as genuinely-new, even though it is just the union of the two
  known faces. The witness-cell test rejects it: the disjunction's gap is True
  only where at least one known terminus's gap is already True, so no cell
  exists where all known termini are False and the disjunction is True.

Operational reading of 2e9551e5's 'a different kind of act' clause: a
different kind of act = an act that is neither a function-selection act nor a
publicity act.

Context: the four earlier 'next-referent' candidates (query-selection,
schema-selection, vouching, frame-of-reference) all collapsed into
what-is-recorded. The first candidate that PASSES the witness-cell test is
TRUST (provenance) -- the writer choosing WHICH OTHER WRITER to accept. Trust
is a third axis that survives both full publicity and losslessness, because a
public, lossless record from an untrusted writer is still unverifiable (the
source's authority is the key, and only the writer or a trusted anchor holds
it).

The ground-truth stranger-verifiability verdict is CONJUNCTIVE over the three
axes: verifiable iff (publicity = public) AND (losslessness = lossless) AND
(trust = trusted). The stranger's verifiability is bounded by the weakest of
the three.

The discriminating property (witness-cell test):
  - TRUST has a witness cell (public, lossless, untrusted) -> genuinely new:
    a cell where both known termini's gaps are False but TRUST's gap is True.
  - PUBLICITY has no witness cell (its gap is exactly the PUBLICITY terminus)
    -> a relabel.
  - LOSSINESS has no witness cell (its gap is exactly the LOSSINESS terminus)
    -> a relabel.
  - DISJUNCTION (secret OR lossy) has no witness cell -> the old weak
    criterion's false positive, now correctly rejected.

Secondary property (the 'invariant' check, mirroring the PUBLICITY test's
seat-invariance): within the (public, lossless) cell, the verdict is determined
by TRUST (trusted vs untrusted), not by the specific writer identity. Two
different untrusted writers give the same verdict (unverifiable); a trusted
writer gives verifiable. The verdict is invariant to the writer identity but
depends on the writer's trust.
"""

PUBLICITY = ["public", "secret"]
LOSSLESSNESS = ["lossless", "lossy"]
TRUST = ["trusted", "untrusted"]

def verdict(publicity, losslessness, trust):
    # A stranger can verify iff the verification data is public, the function
    # is lossless, AND the writer is trusted. All three are conjunctive:
    # the stranger's verifiability is bounded by the weakest of the three.
    if publicity != "public":
        return "unverifiable"   # secret: the stranger can't see the key
    if losslessness != "lossless":
        return "unverifiable"   # lossy: the stranger can't recover the state
    if trust != "trusted":
        return "unverifiable"   # untrusted: the source's authority is the key
    return "verifiable"

def cells():
    for p in PUBLICITY:
        for l in LOSSLESSNESS:
            for t in TRUST:
                yield (p, l, t)

# The gap predicates for each candidate: the condition under which the
# candidate produces a self-keyed gap (unverifiability).
GAP = {
    "PUBLICITY":   lambda c: c[0] == "secret",
    "LOSSINESS":   lambda c: c[1] == "lossy",
    "TRUST":       lambda c: c[2] == "untrusted",
    # The disjunction of the two known termini: the old weak criterion's false
    # positive (secret OR lossy). A regression witness for the correction.
    "DISJUNCTION": lambda c: (c[0] == "secret") or (c[1] == "lossy"),
}

# The known termini against which a candidate is tested.
KNOWN_TERMINI = ("PUBLICITY", "LOSSINESS")

def implied_by(predicate, condition):
    # The OLD weak criterion's primitive (kept for the regression witness):
    # check whether predicate(c) -> condition(c) for all cells c.
    for c in cells():
        if predicate(c) and not condition(c):
            return False
    return True

def witness_cell(name):
    # CORRECTED (2026-10-02, f3ec9e1): a candidate C is GENUINELY NEW iff SOME
    # cell exists where ALL known termini's gaps are False but C's gap is True
    # (C adds a cell no known terminus covers). Returns the witness cell, or
    # None.
    p = GAP[name]
    for c in cells():
        if all(not GAP[k](c) for k in KNOWN_TERMINI) and p(c):
            return c
    return None

def two_axis_test(name):
    # Corrected (2026-10-02, f3ec9e1): the witness-cell criterion.
    # The original weak criterion ("gap not implied by either SINGLE terminus")
    # let a DISJUNCTION of the two termini (secret OR lossy) pass both arms and
    # masquerade as genuinely-new. The witness-cell test rejects it.
    w = witness_cell(name)
    return (w is not None), w

def main():
    print("TRUST cell test (2026-09-28; witness-cell criterion, f3ec9e1)")
    print("=" * 88)
    print("Ground-truth stranger-verifiability verdict (conjunctive over 3 axes):")
    print("%-10s %-12s %-10s %s" % ("publicity", "losslessness", "trust", "verdict"))
    for c in cells():
        print("%-10s %-12s %-10s %s" % (c[0], c[1], c[2], verdict(*c)))
    print("-" * 88)
    print("Witness-cell discriminating test (genuinely new iff a witness cell exists):")
    print("%-14s %-34s %s" %
          ("candidate", "witness cell (all known termini False, C True)",
           "genuinely new"))
    results = {}
    for name in ["PUBLICITY", "LOSSINESS", "TRUST", "DISJUNCTION"]:
        gn, w = two_axis_test(name)
        results[name] = gn
        print("%-14s %-34s %s" %
              (name,
               str(w) if w is not None else "none",
               "YES" if gn else "no"))
    print("-" * 88)
    print("Witness cells (ground-truth verdict at the key cells):")
    print("  TRUST witness   (public, lossless, untrusted) -> %s  [gap SURVIVES both termini]"
          % verdict("public", "lossless", "untrusted"))
    print("  control         (public, lossless, trusted)   -> %s  [both termini satisfied]"
          % verdict("public", "lossless", "trusted"))
    print("  PUBLICITY face  (secret, lossless, trusted)   -> %s  [gap under secret]"
          % verdict("secret", "lossless", "trusted"))
    print("  LOSSINESS face  (public, lossy, trusted)      -> %s  [gap under lossy]"
          % verdict("public", "lossy", "trusted"))
    print("-" * 88)
    # The 'invariant' check: within the (public, lossless) cell, the verdict is
    # determined by trust, not by the writer identity.
    WRITERS = {"writer-A": "trusted", "writer-B": "untrusted", "writer-C": "untrusted"}
    print("Invariant check (within the (public, lossless) cell):")
    for w in sorted(WRITERS):
        v = verdict("public", "lossless", WRITERS[w])
        print("  %s (trust=%s) -> %s" % (w, WRITERS[w], v))
    inv_ok = (verdict("public", "lossless", WRITERS["writer-B"]) ==
              verdict("public", "lossless", WRITERS["writer-C"])) and \
             (verdict("public", "lossless", WRITERS["writer-A"]) !=
              verdict("public", "lossless", WRITERS["writer-B"]))
    print("  invariant to writer identity, depends on trust: %s" %
          ("PASS" if inv_ok else "FAIL"))
    print("-" * 88)
    # Regression witness: the old weak criterion vs the witness-cell criterion,
    # on the disjunction (secret OR lossy) -- the old criterion's false positive.
    disj = GAP["DISJUNCTION"]
    old_fp = implied_by(disj, lambda c: c[0] == "secret")
    old_fl = implied_by(disj, lambda c: c[1] == "lossy")
    old_new = (not old_fp) and (not old_fl)
    new_w = witness_cell("DISJUNCTION")
    new_new = new_w is not None
    print("Regression witness (old weak criterion vs witness-cell criterion):")
    print("  DISJUNCTION (secret OR lossy):")
    print("    OLD weak criterion  -> genuinely_new: %s  (FALSE POSITIVE if True)"
          % old_new)
    print("    NEW witness-cell    -> witness: %s -> genuinely_new: %s"
          % (new_w, new_new))
    print("    regression: %s" % ("PASS (old false positive now rejected)"
                                  if (old_new and not new_new) else "FAIL"))
    print("-" * 88)
    # The corrected verdict: TRUST is genuinely new (witness cell exists);
    # PUBLICITY, LOSSINESS, and DISJUNCTION are not (no witness cell).
    a_ok = (results["TRUST"]
            and not results["PUBLICITY"]
            and not results["LOSSINESS"]
            and not results["DISJUNCTION"])
    trust_witness = witness_cell("TRUST") == ("public", "lossless", "untrusted")
    disj_rejected = witness_cell("DISJUNCTION") is None
    regression_ok = old_new and not new_new
    if a_ok and trust_witness and disj_rejected and regression_ok and inv_ok:
        print("VERDICT: TRUST is the first GENUINELY NEW self-keyed referent. It")
        print("  has a witness cell (public, lossless, untrusted): a cell where both")
        print("  known termini's gaps are False but TRUST's gap is True. PUBLICITY and")
        print("  LOSSINESS are relabels (no witness cell). The DISJUNCTION (secret OR")
        print("  lossy) -- the old weak criterion's false positive -- is now correctly")
        print("  rejected (no witness cell; regression PASS). The two terminuses are the")
        print("  same collapse read from two ends (openness vs lossiness); TRUST is a")
        print("  third axis (the source's authority) that is conjunctive with them. The")
        print("  forward move is the weight-1 TRUST instrument (stranger-rerunnable:")
        print("  'is the writer trusted?'), of which provenance is a face.")
    else:
        print("VERDICT: the discriminating test does NOT hold cleanly. See the")
        print("  FAIL lines above.")
    return 0 if (a_ok and trust_witness and disj_rejected and regression_ok and inv_ok) else 1

if __name__ == "__main__":
    raise SystemExit(main())
