#!/usr/bin/env python3
"""STEP-SWEEP for the knife-edge probe (answers: is the knife-edge set a
property of the battery or of the step knob?).

Re-runs knife_edge's per-specimen probe at several step configurations and
reports how the knife-edge SPECIMEN SET moves. Reuses knife_edge's own
leaf-walk / path / audit machinery so the only variable is the step.
Deterministic (claim_audit has no randomness).

Step configs (relative step for continuous fields, integer step for counts):
  0.1% rel, +-1 counts
  0.5% rel, +-1 counts
  1.0% rel, +-1 counts   (the published baseline)
  2.0% rel, +-1 counts   (disentangle: continuous knob only)
  2.0% rel, +-2 counts   (the directed-ask config)
  5.0% rel, +-2 counts

Run:  python3 knife_edge_step_sweep.py
"""
import copy
import claim_audit
import specimens
import knife_edge


def flags_of(spec):
    return set(claim_audit.audit(spec)["flags"])


def run(rel, count_step):
    """Return the set of specimen names that are knife-edge at this step."""
    knife = set()
    for s in specimens.SPECIMENS:
        base = flags_of(s)
        for path, val in knife_edge.numeric_leaves(s):
            is_int = isinstance(val, int) and not isinstance(val, bool)
            step = count_step if is_int else max(abs(val) * rel, 1e-9)
            tokens = knife_edge._split_path(path)
            for direction in (+1, -1):
                if direction < 0 and is_int and val <= 0:
                    continue
                newval = val + direction * step
                if isinstance(newval, int) and newval < 0:
                    continue
                pert = copy.deepcopy(s)
                knife_edge._set_at(pert, tokens, newval)
                if flags_of(pert) != base:
                    knife.add(s["name"])
                    break
    return knife


CONFIGS = [
    ("0.1% rel, +-1 counts", 0.001, 1),
    ("0.5% rel, +-1 counts", 0.005, 1),
    ("1.0% rel, +-1 counts", 0.010, 1),   # baseline
    ("2.0% rel, +-1 counts", 0.020, 1),   # disentangle (continuous knob only)
    ("2.0% rel, +-2 counts", 0.020, 2),   # directed-ask config
    ("5.0% rel, +-2 counts", 0.050, 2),
]


def main():
    N = len(specimens.SPECIMENS)
    labels = [c[0] for c in CONFIGS]
    sets = {lab: run(rel, cs) for lab, rel, cs in CONFIGS}
    print("KNIFE-EDGE STEP-SWEEP  (N=%d specimens)" % N)
    print("rel step for continuous fields; integer step for counts")
    print()
    print("=== knife-edge specimen count by config ===")
    for lab in labels:
        print("  %-22s  %d/%d" % (lab, len(sets[lab]), N))
    print()
    print("=== pairwise overlap (jaccard) ===")
    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            a, b = sets[labels[i]], sets[labels[j]]
            inter, union = a & b, a | b
            jac = len(inter) / len(union) if union else 1.0
            print("  %-22s & %-22s  inter=%d union=%d jac=%.3f"
                  % (labels[i], labels[j], len(inter), len(union), jac))
    print()
    core = set.intersection(*sets.values())
    print("=== core (knife-edge at EVERY step config): %d ===" % len(core))
    for n in sorted(core):
        print("    " + n)
    print()
    self_name = next((s["name"] for s in specimens.SPECIMENS
                      if "CF-CG-1 sweep saturation" in s["name"]), None)
    if self_name:
        print("=== self-specimen (CF-CG-1 sweep saturation) ===")
        for lab in labels:
            print("  %-22s  %s" % (lab, "knife-edge" if self_name in sets[lab] else "robust"))
        print()
    print("=== per-config knife-edge sets (full) ===")
    for lab in labels:
        print("--- %s (%d) ---" % (lab, len(sets[lab])))
        for n in sorted(sets[lab]):
            print("    " + n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
