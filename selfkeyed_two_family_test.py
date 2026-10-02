#!/usr/bin/env python3
"""Self-keyed two-family test (2026-10-02).

Resolves the tension between:
  - the 2026-10-02 consolidation (fidelity_terminus_test.py): the verifiability
    family saturates at THREE termini (PUBLICITY, LOSSINESS, TRUST); ACT-
    FIDELITY and REFERENT-SELF-KEYED are not new termini (subsets of PUBLICITY
    + LOSSINESS re-applied to the reasoning state).
  - the 62nd-axis commit (85d2358): STRUCTURAL-PRIMING SURVIVES the PUBLICITY
    collapse; it is a STRUCTURE gap, not a verifiability gap (orthogonal to
    WITNESS-RESIDENCE, the axis-level embodiment of PUBLICITY).

The resolution: the self-keyed family is a UNION of two ORTHOGONAL families.
  - the VERIFIABILITY family (gaps about whether a stranger CAN verify):
    saturates at three termini (PUBLICITY/openness, LOSSINESS/lossiness,
    TRUST/trust). WITNESS-RESIDENCE (61st) is a face of PUBLICITY.
  - the STRUCTURE/PERSUASION family (gaps about whether the document LEADS
    with its own key, priming acceptance before verification): STRUCTURAL-
    PRIMING (position) is a genuinely-new terminus, orthogonal to verifiability.

The discriminating test: the witness-cell criterion on the COMBINED cell
space (openness x lossiness x trust x position, 16 cells). STRUCTURAL-
PRIMING has a witness cell (public, lossless, trusted, lead) -- a cell where
ALL three verifiability termini's gaps are False but STRUCTURAL-PRIMING fires.
So it is a genuinely-new terminus of the combined space, but a terminus of the
STRUCTURE family, not the verifiability family. The two families are
orthogonal: STRUCTURAL-PRIMING's gap is a function of position only; the
verifiability gaps are functions of openness/lossiness/trust only.
"""

OPENNESS = ("public", "secret")
LOSSINESS = ("lossless", "lossy")
TRUST = ("trusted", "untrusted")
POSITION = ("lead", "non_lead")

def cells():
    for o in OPENNESS:
        for l in LOSSINESS:
            for t in TRUST:
                for p in POSITION:
                    yield {"openness": o, "lossiness": l, "trust": t, "position": p}

# Verifiability family termini (gaps about whether a stranger CAN verify).
VERIFIABILITY = {
    "PUBLICITY": lambda c: c["openness"] == "secret",
    "LOSSINESS": lambda c: c["lossiness"] == "lossy",
    "TRUST":     lambda c: c["trust"] == "untrusted",
}

# Structure/persuasion family terminus (gap about whether the document LEADS
# with its own key, priming acceptance before verification).
STRUCTURAL_PRIMING = lambda c: c["position"] == "lead"

def witness_cell(candidate_gap, known_gaps):
    """Return a cell where all known gaps are False but candidate fires, or None."""
    for c in cells():
        if all(not g(c) for g in known_gaps.values()) and candidate_gap(c):
            return c
    return None

def main():
    print("Self-keyed two-family test (2026-10-02)")
    print("=" * 92)
    print("Combined cell space: openness x lossiness x trust x position (16 cells)")
    print("Verifiability family: PUBLICITY, LOSSINESS, TRUST (3 termini)")
    print("Structure family:     STRUCTURAL-PRIMING (1 terminus)")
    print("-" * 92)

    # (1) Verifiability saturation: the only cells where all 3 verifiability
    #     gaps are False are (public, lossless, trusted) for both positions.
    verif_false_cells = [c for c in cells() if all(not g(c) for g in VERIFIABILITY.values())]
    print("(1) Verifiability saturation: cells where all 3 verifiability gaps are False:")
    for c in verif_false_cells:
        print("    %s" % c)
    assert len(verif_false_cells) == 2, "expected exactly 2 (public, lossless, trusted, {lead, non_lead})"
    print("    -> the verifiability family saturates at 3 termini; the position variable")
    print("       is NOT a verifiability variable (2 uncovered cells, one per position).")
    print("-" * 92)

    # (2) STRUCTURAL-PRIMING witness cell against the full verifiability family.
    wc = witness_cell(STRUCTURAL_PRIMING, VERIFIABILITY)
    print("(2) STRUCTURAL-PRIMING witness cell (all verifiability gaps False, SP fires):")
    print("    %s" % wc)
    assert wc is not None, "STRUCTURAL-PRIMING must have a witness cell"
    assert wc["openness"] == "public" and wc["lossiness"] == "lossless" and wc["trust"] == "trusted" and wc["position"] == "lead"
    print("    -> STRUCTURAL-PRIMING is a GENUINELY-NEW terminus of the combined space:")
    print("       it fires in the (public, lossless, trusted, lead) cell, where the")
    print("       stranger CAN verify (all verifiability gaps False) yet the document")
    print("       leads with its own key (priming acceptance before verification).")
    print("-" * 92)

    # (3) Orthogonality: STRUCTURAL-PRIMING's gap is a function of position only;
    #     the verifiability gaps are functions of openness/lossiness/trust only.
    sp_depends_only_on_position = all(
        STRUCTURAL_PRIMING({"openness": o, "lossiness": l, "trust": t, "position": p}) == (p == "lead")
        for o in OPENNESS for l in LOSSINESS for t in TRUST for p in POSITION
    )
    verif_depends_only_on_verif = all(
        g({"openness": o, "lossiness": l, "trust": t, "position": p}) == g({"openness": o, "lossiness": l, "trust": t, "position": "lead"})
        for o in OPENNESS for l in LOSSINESS for t in TRUST for p in POSITION
        for name, g in VERIFIABILITY.items()
    )
    print("(3) Orthogonality:")
    print("    STRUCTURAL-PRIMING gap depends only on position: %s" % sp_depends_only_on_position)
    print("    verifiability gaps depend only on (openness, lossiness, trust): %s" % verif_depends_only_on_verif)
    assert sp_depends_only_on_position
    assert verif_depends_only_on_verif
    print("    -> the two families are ORTHOGONAL: STRUCTURAL-PRIMING is not a")
    print("       verifiability terminus (it fires in the verifiable cell); the")
    print("       verifiability termini are not structure termini (constant across")
    print("       position). STRUCTURAL-PRIMING is a terminus of the STRUCTURE family.")
    print("-" * 92)

    # (4) The self-keyed family is a UNION of the two orthogonal families.
    selfkeyed_gap = lambda c: (c["openness"] == "secret" or c["lossiness"] == "lossy"
                               or c["trust"] == "untrusted" or c["position"] == "lead")
    covered = [c for c in cells() if selfkeyed_gap(c)]
    uncovered = [c for c in cells() if not selfkeyed_gap(c)]
    print("(4) Self-keyed family = verifiability (3 termini) + structure (1 terminus):")
    print("    combined self-keyed gap = (secret OR lossy OR untrusted OR lead)")
    print("    covered cells: %d/16, uncovered cells: %d/16" % (len(covered), len(uncovered)))
    for c in uncovered:
        print("    uncovered: %s" % c)
    assert len(uncovered) == 1, "expected exactly 1 uncovered cell (public, lossless, trusted, non_lead)"
    assert uncovered[0] == {"openness": "public", "lossiness": "lossless", "trust": "trusted", "position": "non_lead"}
    print("    -> the self-keyed family saturates at 4 termini (3 verifiability + 1 structure),")
    print("       but in TWO ORTHOGONAL sub-families, not one. The consolidation's 'saturates")
    print("       at 3' was correct for the verifiability family but incomplete: it did not")
    print("       recognize STRUCTURAL-PRIMING as a member of a different (structure) family.")
    print("       The 62nd-axis 'survives the PUBLICITY collapse' was correct: STRUCTURAL-")
    print("       PRIMING is orthogonal to verifiability, not a verifiability terminus.")
    print("-" * 92)
    print("VERDICT: the self-keyed family is a UNION of two orthogonal families:")
    print("  VERIFIABILITY (PUBLICITY, LOSSINESS, TRUST) -- saturates at 3 termini.")
    print("  STRUCTURE (STRUCTURAL-PRIMING) -- a genuinely-new terminus, orthogonal to")
    print("  verifiability (fires in the verifiable cell). The tension between the")
    print("  consolidation ('saturates at 3') and the 62nd-axis ('survives the PUBLICITY")
    print("  collapse') is RESOLVED: they describe two different families.")
    print("RESULT: HOLD")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
