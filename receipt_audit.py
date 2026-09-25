#!/usr/bin/env python3
"""
receipt_audit.py — does a walk's receipt carry the load-bearing axis?

A cursor-based walk (pagination over an id-ordered feed) makes a completeness
claim: "no row was lost." That claim has two axes:

  SIZE axis        (cheap): pages, rows, distinct, stopping condition.
                           Internally consistent, looks complete, but says
                           nothing about WHICH rows were delivered.
  POPULATION axis  (load-bearing): which rows were actually delivered.
                           This is what carries the check. Its absence is
                           hidden by the SIZE axis's presence.

The instrument classifies a receipt against an independently known window:

  RECORDED   the receipt lists the delivered ids (or commits to a hash of
             them). The population is explicit. No flag.
  PINNED     counts-only, but distinct == span of a known contiguous window.
             The population is forced to be exactly the window by arithmetic.
             Safe, but derived, not recorded. No flag (a note is emitted).
  SUBSET     counts-only and distinct < span. The delivered population is an
             unrecorded subset of the window: C(span, distinct) possibilities.
             The debt is unpayable. -> POPULATION-UNRECORDED
  UNBOUNDED  counts-only and no independent window is known. The population
             is entirely unrecorded. -> POPULATION-UNRECORDED
  OVERFLOW   counts-only and distinct > span. The counts do not fit the
             window. -> WINDOW-INCONSISTENT

A receipt is ADEQUATE only if the population is RECORDED or PINNED. The
discriminating case is the boundary between PINNED (distinct == span) and
SUBSET (distinct < span): a one-row-short walk flips the verdict, and a
counts-only receipt cannot pay the debt either way.
"""
import json
import sys


def audit(spec):
    """Return {'flags': [...], 'classification': str, 'notes': [...]}.

    Ground truth is independent: the verdict is arithmetic on (distinct, span),
    not a re-run of the walk. `spec` is a dict with a 'receipt' (what was
    recorded) and an optional 'window' (independent knowledge of the window).
    """
    receipt = spec.get("receipt", {}) or {}
    window = spec.get("window")
    distinct = receipt.get("distinct")
    population = receipt.get("population")
    flags = []
    notes = []

    # RECORDED: the population is explicit (a list of ids, or a hash commitment).
    if population is not None:
        if isinstance(population, list):
            if distinct is not None and len(population) != distinct:
                flags.append("RECORDED-INCONSISTENT")
                notes.append("recorded population has %d ids but receipt reports distinct=%d"
                             % (len(population), distinct))
            classification = "RECORDED"
        elif isinstance(population, dict) and "hash" in population:
            classification = "RECORDED"
            notes.append("population committed by hash (a commitment device, not the rows themselves)")
        else:
            classification = "RECORDED"
        return {"flags": flags, "classification": classification, "notes": notes}

    # counts-only from here.
    if distinct is None:
        flags.append("POPULATION-UNRECORDED")
        notes.append("no distinct count and no population: nothing to pin")
        return {"flags": flags, "classification": "UNBOUNDED", "notes": notes}

    if not window:
        flags.append("POPULATION-UNRECORDED")
        notes.append("counts-only with no independent window: population entirely unrecorded")
        return {"flags": flags, "classification": "UNBOUNDED", "notes": notes}

    # derive span from the window.
    if window.get("contiguous") and "min_id" in window and "max_id" in window:
        span = window["max_id"] - window["min_id"] + 1
    elif "distinct" in window:
        span = window["distinct"]
    else:
        flags.append("POPULATION-UNRECORDED")
        notes.append("window declared but neither contiguous(min,max) nor window.distinct given: span unknown")
        return {"flags": flags, "classification": "UNBOUNDED", "notes": notes}

    if distinct == span:
        classification = "PINNED"
        notes.append("distinct==span (%d): population forced to be exactly the window by arithmetic; safe but derived, not recorded" % distinct)
    elif distinct < span:
        classification = "SUBSET"
        flags.append("POPULATION-UNRECORDED")
        notes.append("distinct %d < span %d: delivered population is an unrecorded subset (C(%d,%d) possibilities); the debt is unpayable"
                     % (distinct, span, span, distinct))
    else:
        classification = "OVERFLOW"
        flags.append("WINDOW-INCONSISTENT")
        notes.append("distinct %d > span %d: the counts do not fit the known window" % (distinct, span))

    return {"flags": flags, "classification": classification, "notes": notes}


def main(argv):
    if len(argv) >= 2:
        with open(argv[1]) as f:
            spec = json.load(f)
        res = audit(spec)
        print("classification:", res["classification"])
        print("flags:", res["flags"])
        for n in res["notes"]:
            print("note:", n)
        return 0 if not res["flags"] else 1
    print(__doc__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
