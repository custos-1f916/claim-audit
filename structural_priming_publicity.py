#!/usr/bin/env python3
"""STRUCTURAL-PRIMING vs the PUBLICITY saturation variable (2026-10-01, discriminating).

Scope: the load-bearing open question left by the 62nd-axis commit (02588ea).
STRUCTURAL-PRIMING is a face of the SELF-KEYED family, and the SELF-KEYED family
is exactly the certification subset that the PUBLICITY saturation test
(publicity_saturation.py, 2026-09-28) collapsed into a single stranger-rerunnable
variable: is the verification data public, so a stranger can independently
verify? WITNESS-RESIDENCE (61st) is the axis-level embodiment of that PUBLICITY
variable (CUSTODIAN-RECOVERABLE vs PUBLICLY-REPRODUCIBLE).

The question: does STRUCTURAL-PRIMING SURVIVE the PUBLICITY collapse, or is it a
RELABEL of the PUBLICITY variable (i.e. does it fire exactly when the witness is
custodian-resident / stranger-unverifiable)?

The cell space (two independent dimensions, 4 cells):
  priming_position in {lead, non_lead} : is the expected value in the mandatory
                                         lead the reading procedure requires?
                                         [the STRUCTURAL-PRIMING gap]
  witness_residence in {public, custodian} : is the witness publicly reproducible
                                         (a stranger CAN verify) or custodian-
                                         resident (a stranger CANNOT)?
                                         [the PUBLICITY / WITNESS-RESIDENCE variable]

The (lead, public) discriminating cell: the document leads with its own key
(STRUCTURAL-PRIMING fires) but the witness is publicly reproducible (WITNESS-
RESIDENCE does NOT fire). A stranger CAN reproduce the witness, yet the reader
is still primed by the document's structure -- so the priming is a STRUCTURE
gap, not a PUBLICITY/verifiability gap. The (non_lead, custodian) cell is the
mirror: the witness is custodian-resident (WITNESS-RESIDENCE fires) but the
expected value is NOT in the lead (STRUCTURAL-PRIMING does NOT fire). If the
axes were a relabel, SP would fire exactly when WR fires (identical firing
set); the two exclusive cells prove they are orthogonal (position x residence).
"""

import claim_audit as C

# The 2x2 cell space: (priming_position, witness_residence)
CELLS = [
    ("lead", "public"),
    ("lead", "custodian"),
    ("non_lead", "public"),
    ("non_lead", "custodian"),
]

# Abstract predicates over the cell space (independent of the instrument's
# implementation): each axis is a function of exactly one dimension.
def GAP_STRUCTURAL_PRIMING(position, residence):
    # the priming is about the LEAD, independent of the residence
    return position == "lead"

def GAP_WITNESS_RESIDENCE(position, residence):
    # the residence (the PUBLICITY variable) is about CUSTODIAN-ness,
    # independent of the position
    return residence == "custodian"

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
# The spec carries data rows so it takes the EMPIRICAL path of audit(), which
# runs every check (STRUCTURAL-PRIMING and WITNESS-RESIDENCE are both in CHECKS
# but NOT in the NO-EMPIRICAL-CONTENT allow-list, so a no-rows spec would N/A
# both and the test would be vacuous). falsifier_witness_address is held
# DISTINCT from claim_channel_address on every cell so WITNESS-ADDRESS does not
# fire and cannot confound the SP x WR comparison.
def spec_for(position, residence):
    spec = {
        "type": "cross-model",
        "mechanism": "transcription of continuity block",
        "metric": "reader-neutrality delta (higher better)",
        "rows": [
            {"mechanism_on": True, "metric": 0.70},
            {"mechanism_on": False, "is_null": True, "metric": 0.00},
        ],
        "claim_channel_address": "exchange_ledger",
        "falsifier_witness_address": "audit_log",  # distinct: WITNESS-ADDRESS does not fire
        "witness_residence": residence,            # public or custodian
    }
    if position is not None:
        spec["priming_position"] = position
    return spec

def instrument_flags(position, residence):
    return set(C.audit(spec_for(position, residence))["flags"])

def main():
    sp_set = firing_set(GAP_STRUCTURAL_PRIMING)
    wr_set = firing_set(GAP_WITNESS_RESIDENCE)

    print("STRUCTURAL-PRIMING vs the PUBLICITY variable (WITNESS-RESIDENCE)")
    print("=" * 88)
    print("Cell space: priming_position {lead, non_lead} x witness_residence")
    print("           {public, custodian}  --  the PUBLICITY saturation variable")
    print("-" * 88)
    print("%-12s %-12s | %-10s %-10s | %-10s %-10s | %s" %
          ("position", "residence", "SP model", "WR model",
           "SP instr", "WR instr", "ground"))
    grounding_ok = True
    for (position, residence) in CELLS:
        sp_m = GAP_STRUCTURAL_PRIMING(position, residence)
        wr_m = GAP_WITNESS_RESIDENCE(position, residence)
        flags = instrument_flags(position, residence)
        sp_i = "STRUCTURAL-PRIMING" in flags
        wr_i = "WITNESS-RESIDENCE" in flags
        # the abstract model must agree with the real instrument
        cell_ok = (sp_m == sp_i) and (wr_m == wr_i)
        grounding_ok = grounding_ok and cell_ok
        mark = "ok" if cell_ok else "MISMATCH"
        print("%-12s %-12s | %-10s %-10s | %-10s %-10s | %s" % (
            position, residence,
            "fires " if sp_m else "pass  ",
            "fires " if wr_m else "pass  ",
            "fires " if sp_i else "pass  ",
            "fires " if wr_i else "pass  ",
            mark))
    print("-" * 88)

    not_relabel_wr = not same_set(sp_set, wr_set)
    not_vacuous_sp = not vacuous(GAP_STRUCTURAL_PRIMING)
    not_vacuous_wr = not vacuous(GAP_WITNESS_RESIDENCE)
    excl_sp = exclusive_cell(GAP_STRUCTURAL_PRIMING, [GAP_WITNESS_RESIDENCE])
    excl_wr = exclusive_cell(GAP_WITNESS_RESIDENCE, [GAP_STRUCTURAL_PRIMING])

    print("Firing sets (abstract model):")
    print("  STRUCTURAL-PRIMING fires on %d cells: %s" % (len(sp_set), sorted(sp_set)))
    print("  WITNESS-RESIDENCE  fires on %d cells: %s" % (len(wr_set), sorted(wr_set)))
    print("-" * 88)

    print("Relabel test (identical-set) vs the PUBLICITY variable:")
    print("  STRUCTURAL-PRIMING vs WITNESS-RESIDENCE: %s"
          % ("not a relabel (different firing set)" if not_relabel_wr
             else "RELABEL (identical firing set -> SP collapses into PUBLICITY)"))
    print("Vacuity test:")
    print("  STRUCTURAL-PRIMING: %s"
          % ("does not fire on all cells -> not vacuous" if not_vacuous_sp
             else "fires on ALL cells -> VACUOUS (discriminates nothing)"))
    print("  WITNESS-RESIDENCE : %s"
          % ("does not fire on all cells -> not vacuous" if not_vacuous_wr
             else "fires on ALL cells -> VACUOUS (discriminates nothing)"))
    print("Exclusive-cell test:")
    print("  STRUCTURAL-PRIMING exclusive cell (SP fires, WR does not): %s" % (excl_sp or "none"))
    print("    -> the (lead, public) cell: the witness is publicly reproducible")
    print("       (a stranger CAN verify) yet the reader is still primed by the")
    print("       document's structure: a STRUCTURE gap, not a PUBLICITY gap")
    print("  WITNESS-RESIDENCE  exclusive cell (WR fires, SP does not): %s" % (excl_wr or "none"))
    print("    -> the (non_lead, custodian) cell: the witness is custodian-")
    print("       resident (a stranger CANNOT verify) but the expected value is")
    print("       NOT in the lead: the reader is not primed by the structure")
    print("Instrument grounding (abstract model vs claim_audit.audit):")
    print("  %s" % ("all 4 cells agree -> the model is grounded in the instrument"
                    if grounding_ok else "MISMATCH -> the model and the instrument disagree"))
    print("-" * 88)

    # STRUCTURAL-PRIMING SURVIVES the PUBLICITY collapse (is a genuinely new
    # discriminating referent, not a relabel of the PUBLICITY variable) iff:
    #   (1) it is not a relabel of WITNESS-RESIDENCE (different firing set), AND
    #   (2) it is not vacuous, AND
    #   (3) it has an exclusive discriminating cell (the (lead, public) cell),
    #   (4) the abstract model is grounded in the real instrument (all 4 cells).
    survives = (not_relabel_wr and not_vacuous_sp and len(excl_sp) >= 1
                and grounding_ok)

    print("Verdict: does STRUCTURAL-PRIMING survive the PUBLICITY collapse?")
    print("  - The (lead, public) cell is the discriminating cell: the witness is")
    print("    publicly reproducible (WITNESS-RESIDENCE does NOT fire) but the")
    print("    document leads with its own key (STRUCTURAL-PRIMING fires). A")
    print("    stranger CAN verify the witness, yet the reader is still primed by")
    print("    the document's structure -- the priming is a STRUCTURE gap, not a")
    print("    PUBLICITY/verifiability gap.")
    print("  - The axes are orthogonal (position x residence), not a relabel.")
    print("VERDICT: %s"
          % ("PASS (STRUCTURAL-PRIMING survives the PUBLICITY collapse; new referent)"
             if survives
             else "FAIL (STRUCTURAL-PRIMING collapses into the PUBLICITY variable)"))
    import sys
    sys.exit(0 if survives else 1)

if __name__ == "__main__":
    main()
