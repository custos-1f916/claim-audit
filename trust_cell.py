#!/usr/bin/env python3
"""TRUST cell test (2026-09-28).

Scope: the two-terminus synthesis (2026-09-28). PUBLICITY (3ddd51b0) and
what-is-recorded (2e9551e5) are two faces of ONE self-keyed act (the writer
choosing what a stranger can verify): PUBLICITY = control over channel OPENNESS
(public artifact vs private secret); what-is-recorded = control over content
LOSSINESS (which lossy function state->record). A stranger's verifiability is
bounded by the WEAKER of the two, so they are the same collapse read from two
ends (openness vs lossiness), not independent.

The two terminuses each pointed toward a 'genuinely new self-keyed referent'
but never stated the discriminating test. This test states it:

  A candidate self-keyed referent C is GENUINELY NEW iff its self-keyedness
  (its gap) survives BOTH:
    (a) full publicity   : the raw state is made public   (publicity = public)
    (b) losslessness     : the function is made identity  (losslessness = lossless)

  If C's gap vanishes under (a), C is a face of the PUBLICITY terminus (its
  self-keyedness is just OPENNESS). If C's gap vanishes under (b), C is a face
  of the what-is-recorded terminus (its self-keyedness is just LOSSINESS).

Operational reading of 2e9551e5's 'a different kind of act' clause: a
different kind of act = an act that is neither a function-selection act nor a
publicity act.

Context: the four earlier 'next-referent' candidates (query-selection,
schema-selection, vouching, frame-of-reference) all collapsed into
what-is-recorded (they failed arm (b) -- their gap vanishes under
losslessness). The first candidate that PASSES this two-axis test is
TRUST (provenance) -- the writer choosing WHICH OTHER WRITER to accept. Trust
is a third axis that survives both full publicity and losslessness, because a
public, lossless record from an untrusted writer is still unverifiable (the
source's authority is the key, and only the writer or a trusted anchor holds
it).

The ground-truth stranger-verifiability verdict is CONJUNCTIVE over the three
axes: verifiable iff (publicity = public) AND (losslessness = lossless) AND
(trust = trusted). The stranger's verifiability is bounded by the weakest of
the three.

The discriminating property:
  - TRUST PASSES both arms (genuinely new): its gap survives full publicity AND
    losslessness. The witness cell is (public, lossless, untrusted) ->
    unverifiable.
  - PUBLICITY FAILS arm (a) (a relabel): its gap vanishes under full publicity.
  - LOSSINESS FAILS arm (b) (a relabel): its gap vanishes under losslessness.

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
    "PUBLICITY": lambda c: c[0] == "secret",
    "LOSSINESS": lambda c: c[1] == "lossy",
    "TRUST":     lambda c: c[2] == "untrusted",
}

def implied_by(predicate, condition):
    # Check whether predicate(c) -> condition(c) for all cells c.
    for c in cells():
        if predicate(c) and not condition(c):
            return False
    return True

def two_axis_test(name):
    # A candidate is GENUINELY NEW iff its gap survives BOTH:
    #   (a) full publicity   : the gap is NOT implied by (publicity = secret)
    #   (b) losslessness     : the gap is NOT implied by (losslessness = lossy)
    p = GAP[name]
    face_of_publicity = implied_by(p, lambda c: c[0] == "secret")
    face_of_lossiness = implied_by(p, lambda c: c[1] == "lossy")
    genuinely_new = (not face_of_publicity) and (not face_of_lossiness)
    return genuinely_new, face_of_publicity, face_of_lossiness

def main():
    print("TRUST cell test (2026-09-28) -- two-terminus discriminating test")
    print("=" * 88)
    print("Ground-truth stranger-verifiability verdict (conjunctive over 3 axes):")
    print("%-10s %-12s %-10s %s" % ("publicity", "losslessness", "trust", "verdict"))
    for c in cells():
        print("%-10s %-12s %-10s %s" % (c[0], c[1], c[2], verdict(*c)))
    print("-" * 88)
    print("Two-axis discriminating test (genuinely new iff survives BOTH arms):")
    print("%-14s %-24s %-24s %s" %
          ("candidate", "arm (a) full publicity", "arm (b) losslessness",
           "genuinely new"))
    results = {}
    for name in ["PUBLICITY", "LOSSINESS", "TRUST"]:
        gn, fp, fl = two_axis_test(name)
        results[name] = gn
        print("%-14s %-24s %-24s %s" %
              (name,
               "FAIL (face of PUBLICITY)" if fp else "PASS (gap survives)",
               "FAIL (face of LOSSINESS)" if fl else "PASS (gap survives)",
               "YES" if gn else "no"))
    print("-" * 88)
    print("Witness cells:")
    print("  TRUST witness   (public, lossless, untrusted) -> %s  [gap SURVIVES both arms]"
          % verdict("public", "lossless", "untrusted"))
    print("  control         (public, lossless, trusted)   -> %s  [both terminuses satisfied]"
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
    a_ok = (results["TRUST"] and not results["PUBLICITY"] and not results["LOSSINESS"])
    trust_witness = verdict("public", "lossless", "untrusted") == "unverifiable"
    if a_ok and trust_witness and inv_ok:
        print("VERDICT: TRUST is the first GENUINELY NEW self-keyed referent. It")
        print("  survives BOTH the publicity and losslessness terminuses (the (public,")
        print("  lossless, untrusted) cell is still unverifiable). PUBLICITY and")
        print("  LOSSINESS are relabels (faces of the two terminuses): each fails")
        print("  its own arm. The two terminuses are the same collapse read from")
        print("  two ends (openness vs lossiness); TRUST is a third axis (the")
        print("  source's authority) that is conjunctive with them. The forward")
        print("  move is the weight-1 TRUST instrument (stranger-rerunnable: 'is")
        print("  the writer trusted?'), of which provenance is a face.")
    else:
        print("VERDICT: the discriminating test does NOT hold cleanly. See the")
        print("  FAIL lines above.")
    return 0 if (a_ok and trust_witness and inv_ok) else 1

if __name__ == "__main__":
    raise SystemExit(main())
