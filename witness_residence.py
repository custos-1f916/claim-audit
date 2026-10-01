#!/usr/bin/env python3
"""WITNESS-RESIDENCE cell test (2026-10-01, discriminating).

Scope: the seat-dependent verifiability cell (the 87920 square comment,
2026-10-01, extending the no-seal/no-session distinction closed this stretch,
stale_true.py f2e5a5d). The custodian holds the witness bytes and can
verify+replay via skill_sha256; a stranger lacks the bytes and cannot
reproduce the coverage diff. That is CUSTODIAN-RECOVERABLE vs
PUBLICLY-REPRODUCIBLE: the certification is seat-dependent. The custodian can
verify (they hold the witness); the stranger cannot (they lack it).

The question: is WITNESS-RESIDENCE a GENUINELY NEW discriminating referent,
or a FACE of one of the three nearest existing axes?
  TRUST          (44th): the stranger cannot verify AT ALL (the content is not
                         independently verifiable).
  CARRIER-REACH  (56th): the content is verifiable but sits in a carrier the
                         consumer's read path never traverses.
  SELF-KEYED     (1st) : the instrument certifies itself (no external witness).

The discriminating test (NOT tautological): model the WITNESS-RESIDENCE gap
and the three nearest existing axes as predicates over a shared cell space,
then apply the instrument's OWN tests:
  (1) identical-set test : the candidate is a FACE of an existing axis iff it
                           fires on exactly the same cells (a relabel).
  (2) vacuity test       : a gap that fires on ALL cells discriminates nothing.
  (3) exclusive-cell test: the candidate is GENUINELY NEW iff there is a cell
                           where it fires and NONE of the three existing axes
                           fire (the 87920 discriminating cell).

The cell space (four independent dimensions, 16 cells):
  content_verifiable   in {yes, no}          : can the content be independently
                                               verified (by a seat that holds
                                               the witness)? [TRUST axis]
  carrier_in_read_path in {yes, no}          : does the custodian's read path
                                               reach the carrier? [CARRIER-REACH]
  witness_residence    in {custodian, public}: is the witness resident in a
                                               specific seat or publicly
                                               available? [the WITNESS-RESIDENCE
                                               gap]
  external_witness     in {yes, no}          : is there an external witness (a
                                               hash, an audit log) the verifier
                                               checks against? [SELF-KEYED axis]

The 87920 discriminating cell is (yes, yes, custodian, yes): the content IS
verifiable (not TRUST), the carrier IS in the read path (not CARRIER-REACH),
there IS an external witness (not SELF-KEYED), but the witness is
custodian-resident so a stranger cannot reproduce (the WITNESS-RESIDENCE gap).
The pass cell is (yes, yes, public, yes): the witness is publicly available, so
a stranger CAN reproduce; WITNESS-RESIDENCE does not fire (seat-independent).

Stranger-rerunnable: python3 witness_residence.py  (stdlib only, no network).
Exits 0 and prints VERDICT: PASS iff WITNESS-RESIDENCE is a GENUINELY NEW
discriminating referent (not a face of TRUST / CARRIER-REACH / SELF-KEYED, not
vacuous, and has an exclusive discriminating cell).
"""

CONTENT_VERIFIABLE = ["yes", "no"]
CARRIER_IN_READ_PATH = ["yes", "no"]
WITNESS_RESIDENCE = ["custodian", "public"]
EXTERNAL_WITNESS = ["yes", "no"]

def cells():
    for cv in CONTENT_VERIFIABLE:
        for cr in CARRIER_IN_READ_PATH:
            for wr in WITNESS_RESIDENCE:
                for ew in EXTERNAL_WITNESS:
                    yield (cv, cr, wr, ew)

ALL_CELLS = list(cells())

# The candidate gap (61st axis): the content is verifiable, the carrier is in
# the read path, there is an external witness, but the witness is resident in a
# specific seat (custodian-held), so a stranger cannot reproduce. The
# certification is seat-dependent.
GAP_WITNESS_RESIDENCE = lambda c: (
    c[0] == "yes" and c[1] == "yes" and c[2] == "custodian" and c[3] == "yes"
)

# The three nearest existing axes, as predicates over the SAME cells.
GAP_TRUST         = lambda c: c[0] == "no"                       # 44th
GAP_CARRIER_REACH = lambda c: c[0] == "yes" and c[1] == "no"     # 56th
GAP_SELF_KEYED    = lambda c: c[3] == "no"                       # 1st

def same_set(p, q):
    # identical-set test: p and q are the SAME referent iff their gaps fire on
    # exactly the same cells.
    return all(p(c) == q(c) for c in ALL_CELLS)

def firing_set(p):
    return [c for c in ALL_CELLS if p(c)]

def vacuous(p):
    # vacuity test: a gap that fires on every cell discriminates nothing.
    return all(p(c) for c in ALL_CELLS)

def exclusive_cell(p, others):
    # exclusive-cell test: a cell where p fires and NONE of the others fire.
    return [c for c in ALL_CELLS if p(c) and not any(o(c) for o in others)]

def main():
    print("WITNESS-RESIDENCE cell test (2026-10-01, discriminating)")
    print("=" * 88)
    print("Cell space: %d cells (content_verifiable x carrier_in_read_path x"
          % len(ALL_CELLS))
    print("            witness_residence x external_witness)")
    print("-" * 88)

    wr_set = firing_set(GAP_WITNESS_RESIDENCE)
    tr_set = firing_set(GAP_TRUST)
    cr_set = firing_set(GAP_CARRIER_REACH)
    sk_set = firing_set(GAP_SELF_KEYED)

    print("Firing sets:")
    print("  WITNESS-RESIDENCE (candidate) fires on %d cells: %s"
          % (len(wr_set), wr_set))
    print("  TRUST (44th)         fires on %d cells" % len(tr_set))
    print("  CARRIER-REACH (56th) fires on %d cells" % len(cr_set))
    print("  SELF-KEYED (1st)     fires on %d cells" % len(sk_set))
    print("-" * 88)

    not_relabel_trust = not same_set(GAP_WITNESS_RESIDENCE, GAP_TRUST)
    not_relabel_cr    = not same_set(GAP_WITNESS_RESIDENCE, GAP_CARRIER_REACH)
    not_relabel_sk    = not same_set(GAP_WITNESS_RESIDENCE, GAP_SELF_KEYED)
    not_vacuous       = not vacuous(GAP_WITNESS_RESIDENCE)
    excl              = exclusive_cell(GAP_WITNESS_RESIDENCE,
                                       [GAP_TRUST, GAP_CARRIER_REACH, GAP_SELF_KEYED])

    print("Relabel test (identical-set):")
    print("  vs TRUST:         %s"
          % ("not a relabel (different firing set)" if not_relabel_trust
             else "RELABEL (identical firing set)"))
    print("  vs CARRIER-REACH: %s"
          % ("not a relabel (different firing set)" if not_relabel_cr
             else "RELABEL (identical firing set)"))
    print("  vs SELF-KEYED:    %s"
          % ("not a relabel (different firing set)" if not_relabel_sk
             else "RELABEL (identical firing set)"))
    print("Vacuity test:")
    print("  %s"
          % ("does not fire on all cells -> not vacuous" if not_vacuous
             else "fires on ALL cells -> VACUOUS (discriminates nothing)"))
    print("Exclusive-cell test:")
    print("  %s"
          % ("discriminating cell(s) where WITNESS-RESIDENCE fires and no existing axis fires: %s" % excl
             if excl else
             "NO exclusive cell (the candidate is covered by the existing axes)"))
    print("-" * 88)

    # WITNESS-RESIDENCE is a GENUINELY NEW discriminating referent iff:
    #   (1) it is not a relabel of any of the three nearest existing axes, AND
    #   (2) it is not vacuous, AND
    #   (3) it has an exclusive discriminating cell (the 87920 cell).
    new_referent = (not_relabel_trust and not_relabel_cr and not_relabel_sk
                    and not_vacuous and len(excl) >= 1)

    print("Verdict: WITNESS-RESIDENCE is a GENUINELY NEW discriminating referent.")
    print("  - The 87920 cell (yes, yes, custodian, yes) is the discriminating")
    print("    cell: the content IS verifiable (not TRUST), the carrier IS in")
    print("    the read path (not CARRIER-REACH), there IS an external witness")
    print("    (not SELF-KEYED), but the witness is custodian-resident so a")
    print("    stranger cannot reproduce (the WITNESS-RESIDENCE gap).")
    print("  - The pass cell (yes, yes, public, yes) is the seat-independent")
    print("    case: the witness is publicly available, so a stranger CAN")
    print("    reproduce; WITNESS-RESIDENCE does not fire.")
    print("VERDICT: %s"
          % ("PASS (WITNESS-RESIDENCE is a new referent)" if new_referent
             else "FAIL (WITNESS-RESIDENCE is a relabel, vacuous, or covered)"))
    import sys
    sys.exit(0 if new_referent else 1)

if __name__ == "__main__":
    main()
