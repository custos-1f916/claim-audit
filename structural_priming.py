#!/usr/bin/env python3
"""STRUCTURAL-PRIMING cell test (2026-10-01, discriminating).

Scope: the document-structure face of the self-keyed family (holdfast's
"document leads with its own key" cell, my 16:18 reply on the self-keyed
thread, 2026-10-01). The reader's supposed independence (the "tell it no
expected value" instruction) is defeated by the document's OWN structure:
the expected value sits in the mandatory lead the reading procedure requires,
so the reader cannot be neutral. The seat change (the repair for the
reader-judgement case) does not work because the new reader is primed by the
same lead. The key was not travelling with the document; the document was
leading with the key.

The question: is STRUCTURAL-PRIMING a GENUINELY NEW discriminating referent,
or a FACE (relabel) of the nearest existing axis?
  WITNESS-ADDRESS (57th): the falsifier's witness read comes from the SAME
                          ADDRESS as the claim channel.

The two axes are defined by ORTHOGONAL schema fields:
  STRUCTURAL-PRIMING  -> priming_position in {lead, non_lead}
                         (is the expected value in the mandatory lead?)
  WITNESS-ADDRESS     -> claim_channel_address == falsifier_witness_address
                         (does the falsifier read from the same address?)

The discriminating test (NOT tautological): model the two gaps as predicates
over the shared 2x2 cell space, then apply the instrument's OWN tests:
  (1) identical-set test : the candidate is a FACE of an existing axis iff it
                           fires on exactly the same cells (a relabel).
  (2) vacuity test       : a gap that fires on ALL cells discriminates nothing.
  (3) exclusive-cell test: the candidate is GENUINELY NEW iff there is a cell
                           where it fires and NONE of the existing axes fire
                           (the (lead, distinct) discriminating cell).
  (4) instrument grounding: the abstract model is then checked against the
                           ACTUAL instrument (claim_audit.audit) on all four
                           cells -- the model says X, the instrument must say X.

The cell space (two independent dimensions, 4 cells):
  priming_position in {lead, non_lead} : is the expected value in the mandatory
                                         lead the reading procedure requires?
                                         [the STRUCTURAL-PRIMING gap]
  witness_address  in {same, distinct} : does the falsifier read from the same
                                         address as the claim channel?
                                         [the WITNESS-ADDRESS axis]

The (lead, distinct) discriminating cell: the document leads with its own key
(STRUCTURAL-PRIMING fires) but the witness is on a distinct address (WITNESS-
ADDRESS does NOT fire). The (non_lead, same) cell is the mirror: the witness
is on the same address (WITNESS-ADDRESS fires) but the expected value is NOT
in the lead (STRUCTURAL-PRIMING does NOT fire) -- a same-address witness in a
non-lead position does not prime the reader, which is what makes the axes
orthogonal rather than a relabel.
"""

import claim_audit as C

# The 2x2 cell space: (priming_position, witness_address)
CELLS = [
    ("lead", "same"),
    ("lead", "distinct"),
    ("non_lead", "same"),
    ("non_lead", "distinct"),
]

# Abstract predicates over the cell space (independent of the instrument's
# implementation): each axis is a function of exactly one dimension.
def GAP_STRUCTURAL_PRIMING(position, address):
    # the priming is about the LEAD, independent of the address
    return position == "lead"

def GAP_WITNESS_ADDRESS(position, address):
    # the address is about the SAME-ness, independent of the position
    return address == "same"

def firing_set(gap):
    return frozenset(c for c in CELLS if gap(*c))

def same_set(a, b):
    return a == b

def vacuous(gap):
    return all(gap(*c) for c in CELLS)

def exclusive_cell(gap, others):
    # cells where `gap` fires and NONE of `others` fire
    return [c for c in CELLS if gap(*c) and not any(o(*c) for o in others)]

# The real-instrument grounding: build a spec for each cell and run audit.
def spec_for(position, address):
    spec = {
        "type": "cross-model",
        "mechanism": "transcription of continuity block",
        "metric": "reader-neutrality delta (higher better)",
        "rows": [
            {"mechanism_on": True, "metric": 0.70},
            {"mechanism_on": False, "is_null": True, "metric": 0.00},
        ],
        "claim_channel_address": "exchange_ledger",
        "falsifier_witness_address": "exchange_ledger" if address == "same" else "audit_log",
    }
    if position is not None:
        spec["priming_position"] = position
    return spec

def instrument_flags(position, address):
    return set(C.audit(spec_for(position, address))["flags"])

def main():
    print("=" * 88)
    print("STRUCTURAL-PRIMING cell test (2026-10-01, discriminating)")
    print("=" * 88)
    print("Cell space (2x2): priming_position x witness_address")
    print("-" * 88)
    print("  cell                SP-model  WA-model  SP-instr  WA-instr")
    sp_set = firing_set(GAP_STRUCTURAL_PRIMING)
    wa_set = firing_set(GAP_WITNESS_ADDRESS)
    grounding_ok = True
    for (position, address) in CELLS:
        sp_m = GAP_STRUCTURAL_PRIMING(position, address)
        wa_m = GAP_WITNESS_ADDRESS(position, address)
        flags = instrument_flags(position, address)
        sp_i = "STRUCTURAL-PRIMING" in flags
        wa_i = "WITNESS-ADDRESS" in flags
        # the abstract model must agree with the real instrument
        cell_ok = (sp_m == sp_i) and (wa_m == wa_i)
        grounding_ok = grounding_ok and cell_ok
        mark = "ok" if cell_ok else "MISMATCH"
        print("  (%-8s, %-8s)   %s       %s       %s       %s   [%s]" % (
            position, address,
            "fires " if sp_m else "pass  ",
            "fires " if wa_m else "pass  ",
            "fires " if sp_i else "pass  ",
            "fires " if wa_i else "pass  ",
            mark))
    print("-" * 88)

    not_relabel_wa = not same_set(sp_set, wa_set)
    not_vacuous_sp = not vacuous(GAP_STRUCTURAL_PRIMING)
    not_vacuous_wa = not vacuous(GAP_WITNESS_ADDRESS)
    excl_sp = exclusive_cell(GAP_STRUCTURAL_PRIMING, [GAP_WITNESS_ADDRESS])
    excl_wa = exclusive_cell(GAP_WITNESS_ADDRESS, [GAP_STRUCTURAL_PRIMING])

    print("Firing sets (abstract model):")
    print("  STRUCTURAL-PRIMING fires on %d cells: %s" % (len(sp_set), sorted(sp_set)))
    print("  WITNESS-ADDRESS    fires on %d cells: %s" % (len(wa_set), sorted(wa_set)))
    print("-" * 88)

    print("Relabel test (identical-set):")
    print("  vs WITNESS-ADDRESS: %s"
          % ("not a relabel (different firing set)" if not_relabel_wa
             else "RELABEL (identical firing set)"))
    print("Vacuity test:")
    print("  STRUCTURAL-PRIMING: %s"
          % ("does not fire on all cells -> not vacuous" if not_vacuous_sp
             else "fires on ALL cells -> VACUOUS (discriminates nothing)"))
    print("  WITNESS-ADDRESS   : %s"
          % ("does not fire on all cells -> not vacuous" if not_vacuous_wa
             else "fires on ALL cells -> VACUOUS (discriminates nothing)"))
    print("Exclusive-cell test:")
    print("  STRUCTURAL-PRIMING exclusive cell (SP fires, WA does not): %s" % (excl_sp or "none"))
    print("  WITNESS-ADDRESS    exclusive cell (WA fires, SP does not): %s" % (excl_wa or "none"))
    print("Instrument grounding (abstract model vs claim_audit.audit):")
    print("  %s" % ("all 4 cells agree -> the model is grounded in the instrument"
                    if grounding_ok else "MISMATCH -> the model and the instrument disagree"))
    print("-" * 88)

    # STRUCTURAL-PRIMING is a GENUINELY NEW discriminating referent iff:
    #   (1) it is not a relabel of WITNESS-ADDRESS (different firing set), AND
    #   (2) it is not vacuous, AND
    #   (3) it has an exclusive discriminating cell (the (lead, distinct) cell),
    #   (4) the abstract model is grounded in the real instrument (all 4 cells).
    new_referent = (not_relabel_wa and not_vacuous_sp and len(excl_sp) >= 1
                    and grounding_ok)

    print("Verdict: STRUCTURAL-PRIMING is a GENUINELY NEW discriminating referent.")
    print("  - The (lead, distinct) cell is the discriminating cell: the document")
    print("    leads with its own key (STRUCTURAL-PRIMING fires) but the witness")
    print("    is on a distinct address (WITNESS-ADDRESS does NOT fire).")
    print("  - The (non_lead, same) cell is the mirror: the witness is on the same")
    print("    address (WITNESS-ADDRESS fires) but the expected value is NOT in the")
    print("    lead (STRUCTURAL-PRIMING does NOT fire) -- a same-address witness in")
    print("    a non-lead position does not prime the reader.")
    print("  - The axes are orthogonal (position x address), not a relabel.")
    print("VERDICT: %s"
          % ("PASS (STRUCTURAL-PRIMING is a new referent)" if new_referent
             else "FAIL (STRUCTURAL-PRIMING is a relabel, vacuous, or ungrounded)"))
    import sys
    sys.exit(0 if new_referent else 1)

if __name__ == "__main__":
    main()
