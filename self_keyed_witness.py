#!/usr/bin/env python3
"""Self-keyed witness: does my own prose reasoning match my own flag?

For each specimen, the truth_reason prose argues a conclusion about the
primary axis ("does not fire" -> robust, "fires" -> flawed). The robust flag
is instrument-derived (flag-driven). If the prose argues robust but the flag
is flawed (or vice versa), the instrument's verdict is decoupled from its own
reasoning -- the self-keyed signature.

This is a witness test: it checks whether the certifier's own prose matches
the certifier's own flag. It does NOT check whether the flag is correct
(independent verification is the stranger's job).
"""
import json, re, sys

def load(path):
    return {r["id"]: r for r in json.load(open(path))}

def prose_concludes_robust(reason):
    """Prose argues the primary axis does NOT fire (-> robust)."""
    return bool(re.search(r"does not fire|does not apply|does not fire \(N", reason))

def prose_concludes_flawed(reason):
    """Prose argues the primary axis FIRES (-> flawed)."""
    # "FIRE CELL" or "fires" (not "does not fire")
    if re.search(r"FIRE CELL|fires\b|fires \(|fires N", reason):
        # exclude "does not fire"
        if not re.search(r"does not fire", reason):
            return True
    return False

def main():
    truth = load(sys.argv[1] if len(sys.argv) > 1 else "gt_rederivation/truth_2026-10-03.json")
    raw   = load(sys.argv[2] if len(sys.argv) > 2 else "gt_rederivation/raw_2026-10-03.json")

    mismatches = []
    for cid in sorted(truth):
        r = truth[cid]
        reason = r.get("truth_reason", "")
        robust = r["robust"]
        concl_robust = prose_concludes_robust(reason)
        concl_flawed = prose_concludes_flawed(reason)
        # Mismatch: prose argues robust but flag is flawed
        if concl_robust and not robust:
            mismatches.append((cid, "prose->robust, flag->flawed", r.get("name","")))
        # Mismatch: prose argues flawed but flag is robust
        elif concl_flawed and robust:
            mismatches.append((cid, "prose->flawed, flag->robust", r.get("name","")))

    print(f"Self-keyed witness: {len(mismatches)}/{len(truth)} cells have prose-reasoning/flag mismatch")
    for cid, direction, name in mismatches:
        print(f"  [{cid:3d}] {direction:28s} {name[:60]}")

if __name__ == "__main__":
    main()
