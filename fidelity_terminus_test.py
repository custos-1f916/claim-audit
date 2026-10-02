#!/usr/bin/env python3
"""Two-terminus discriminating test, CORRECTED (witness-cell criterion).

The original two-terminus test (trust_cell.py, 2026-09-28) used a WEAK
criterion:
    C is genuinely new iff C's gap is not implied by EITHER single terminus.
This is too weak: a disjunction of the two termini (e.g., secret OR lossy) is
not implied by either single terminus, so it passes both arms and is called
"genuinely new" -- but it is just the union of the two known faces, not a new
referent. The original test only ever ran PUBLICITY / LOSSINESS / TRUST, so
the weakness never bit; it bites the moment a disjunction is a candidate.

The CORRECT criterion (the witness-cell test):
    C is genuinely new iff there exists a cell where ALL previously-established
    termini's gaps are False but C's gap is True.
Equivalently: C's gap is NOT a subset of the union of the known termini's
gaps -- C adds at least one cell to the gap that no known terminus covers.

Previously-established termini (before ACT-FIDELITY / REFERENT-SELF-KEYED were
minted on 2026-10-02):
    PUBLICITY  (3ddd51b0): gap = (state = secret)
    LOSSINESS  (2e9551e5): gap = (function = lossy)
    TRUST      (2b32b4d4): gap = (writer = untrusted)   [first genuinely-new
                                                         third axis, 2026-09-28]
Union of known gaps = (secret OR lossy OR untrusted). The only cell where all
known gaps are False is (public, lossless, trusted).

The two NEWEST axes (minted 2026-10-02) are run through this test:
    ACT-FIDELITY        (138fec0): the gap is (emitted AND (secret OR lossy))
                                   -- the emitted log is a record of the
                                   reasoning state; the writer controls its
                                   openness and lossiness.
    REFERENT-SELF-KEYED (46f7dbe, 63rd axis): the gap is
                                   (self-declared AND (secret OR lossy))
                                   -- the referent_value is a record of the
                                   reasoning state; the writer controls its
                                   openness and lossiness.

Both gaps are SUBSETS of (secret OR lossy), so they add no cell beyond the
union of PUBLICITY + LOSSINESS. Neither is genuinely new: both are faces of
the what-is-recorded terminus (the writer's control over the lossy function
state->record) + the PUBLICITY terminus (the writer's control over the state's
openness), applied to the reasoning state.

The distinction (channel vs terminus): the MECHANISM (channel) of
REFERENT-SELF-KEYED (the writer declaring the referent_value) is genuinely new
-- it is a different kind of act than choosing a lossy function. But the GAP
(terminus) is NOT new -- it is covered by PUBLICITY + LOSSINESS. The README's
claim "genuinely new self-keyed referent" is about the channel (mechanism),
not the terminus (gap).
"""
import sys

# Cell: (state, function, writer) where
#   state    in {public, secret}
#   function in {lossless, lossy}
#   writer   in {trusted, untrusted}
# Plus the two new-axis fields:
#   emitted          in {emitted, not-emitted}   (ACT-FIDELITY)
#   referent_source  in {self-declared, externally-witnessed}  (REFERENT-SELF-KEYED)

def all_cells():
    cells = []
    for state in ["public", "secret"]:
        for function in ["lossless", "lossy"]:
            for writer in ["trusted", "untrusted"]:
                for emitted in ["emitted", "not-emitted"]:
                    for referent_source in ["self-declared", "externally-witnessed"]:
                        cells.append({"state": state, "function": function,
                                      "writer": writer, "emitted": emitted,
                                      "referent_source": referent_source})
    return cells

# Gap predicates: True = the self-keyed gap is PRESENT (stranger cannot verify).
GAPS = {
    "PUBLICITY":  lambda c: c["state"] == "secret",
    "LOSSINESS":  lambda c: c["function"] == "lossy",
    "TRUST":      lambda c: c["writer"] == "untrusted",
    # ACT-FIDELITY: the gap is present iff the log was emitted AND the
    # reasoning state is either secret or lossy (the writer controls the
    # openness and lossiness of the emitted log).
    "ACT-FIDELITY": lambda c: c["emitted"] == "emitted"
                              and (c["state"] == "secret" or c["function"] == "lossy"),
    # REFERENT-SELF-KEYED: the gap is present iff the referent_value is
    # self-declared AND the reasoning state is either secret or lossy.
    "REFERENT-SELF-KEYED": lambda c: c["referent_source"] == "self-declared"
                              and (c["state"] == "secret" or c["function"] == "lossy"),
}

def witness_cell(candidate, known_names):
    """Return a cell where all known termini's gaps are False but candidate's
    gap is True, or None if no such cell exists."""
    for c in all_cells():
        known_all_false = all(not GAPS[k](c) for k in known_names)
        if known_all_false and GAPS[candidate](c):
            return c
    return None

def main():
    print("Two-terminus discriminating test, CORRECTED (witness-cell criterion)")
    print("=" * 92)
    print("C is GENUINELY NEW iff some cell exists where ALL previously-")
    print("established termini's gaps are False but C's gap is True (C adds a")
    print("cell no known terminus covers). Previously-established termini:")
    print("  PUBLICITY, LOSSINESS, TRUST")
    print("  union of known gaps = secret OR lossy OR untrusted")
    print("  only cell where all known gaps are False: (public, lossless, trusted)")
    print("-" * 92)
    print("%-20s %-30s %s" % ("candidate", "witness cell", "genuinely new"))
    print("-" * 92)
    results = {}
    for name in ["TRUST", "ACT-FIDELITY", "REFERENT-SELF-KEYED"]:
        known = ["PUBLICITY", "LOSSINESS"] if name == "TRUST" else \
                ["PUBLICITY", "LOSSINESS", "TRUST"]
        wc = witness_cell(name, known)
        gn = wc is not None
        results[name] = gn
        print("%-20s %-30s %s" % (name, str(wc), "YES" if gn else "no"))
    print("-" * 92)
    # Robustness: the verdict for the two new candidates is the same with or
    # without TRUST in the known set (their gap never involves trust).
    wc_no_trust_af = witness_cell("ACT-FIDELITY", ["PUBLICITY", "LOSSINESS"])
    print("Robustness: ACT-FIDELITY witness cell without TRUST in known set:")
    print("  %s  (same verdict: %s)" %
          (str(wc_no_trust_af), "not genuinely new" if wc_no_trust_af is None else "genuinely new"))
    print("-" * 92)
    ok = (results["TRUST"]
          and not results["ACT-FIDELITY"]
          and not results["REFERENT-SELF-KEYED"])
    print("CONSOLIDATION: ACT-FIDELITY and REFERENT-SELF-KEYED are NOT genuinely")
    print("  new TERMINI -- their gap (emitted/self-declared AND (secret OR lossy))")
    print("  is a subset of the union of the two known termini re-applied to the")
    print("  reasoning state; they add no cell beyond PUBLICITY + LOSSINESS.")
    print("  TRUST remains the only genuinely-new third terminus (witness cell")
    print("  (public, lossless, untrusted)). The 63rd axis and the ACT-FIDELITY")
    print("  seam are new CHANNELS (mechanisms) but NOT new TERMINI (gaps).")
    print("  RESULT: %s" % ("HOLD" if ok else "FAIL"))
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
