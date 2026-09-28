#!/usr/bin/env python3
"""Knife-edge probe: how far is each verdict from flipping?

Dual of calibration_boundary.py. That probe asks, per CHECK, "can the battery
catch this check breaking?" (per-check mutation). This probe asks, per SPECIMEN,
"how far is this verdict from the decision boundary?" (per-field perturbation).

Method: for each specimen in the battery, take its baseline verdict (the fired
flag set). Then, for each numeric leaf field, perturb it by ONE minimal step
(+1/-1 for integer counts, +/-1% for continuous values) and re-audit. If the
flag set changes, the verdict is KNIFE-EDGE on that field: the paper's audit
verdict is one rounding error from a different verdict (a near-miss). A
specimen is ROBUST if no minimal perturbation to any single field flips its
verdict.

The aggregate (fraction knife-edge) is the instrument's decision-surface
ruggedness: a high fraction means verdicts are sensitive to the measurement
noise in the input -- a self-keyed-style seam where the verdict is not robust
to the very rounding that produced the numbers. Both outcomes are normal rows:
a near-miss is logged, a stable verdict is logged. Exit 0 always; the report is
the point.
"""
import copy
import re
import claim_audit
import specimens

EPS = 0.01  # relative step for continuous fields


def numeric_leaves(obj, path=""):
    """Yield (path, value) for every numeric leaf in a nested dict/list."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from numeric_leaves(v, "%s.%s" % (path, k) if path else str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from numeric_leaves(v, "%s[%d]" % (path, i))
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        yield (path, obj)


def _split_path(path):
    tokens = []
    for part in re.split(r"\.", path):
        m = re.match(r"^([^\[\]]+)\[(\d+)\]$", part)
        if m:
            tokens.append(m.group(1))
            tokens.append(int(m.group(2)))
        else:
            tokens.append(part)
    return tokens


def _set_at(obj, tokens, newval):
    cur = obj
    for t in tokens[:-1]:
        cur = cur[t]
    cur[tokens[-1]] = newval


def step_for(value):
    if isinstance(value, int) and not isinstance(value, bool):
        return 1
    return max(abs(value) * EPS, 1e-9)


def audit_flags(spec):
    return set(claim_audit.audit(spec)["flags"])



# Field-role classifier: a knife-edge is only a "rounding-error near-miss" if it
# sits on a MEASURED quantity. A flip on a set-size (structural) or a declared
# parameter (exact, author-set) is a different near-miss and must not be counted
# as measurement noise. Heuristic on the last known token in the path.
MEASURED   = {"metric", "value", "measured_count", "referent_value",
              "probe_support_fraction", "references"}
STRUCTURAL = {"support", "check_count", "distinct_checks", "cursor_runs",
              "n", "total_count", "draw"}
DECLARED   = {"knob", "threshold", "stated_headline", "guaranteed_count",
              "mechanism_axis"}

def classify_field(path):
    last = "unclassified"
    for tok in _split_path(path):
        t = tok if isinstance(tok, str) else None
        if not t:
            continue
        if t in MEASURED:
            last = "measured"
        elif t in STRUCTURAL:
            last = "structural"
        elif t in DECLARED:
            last = "declared"
    return last

def main():
    specs = specimens.SPECIMENS
    total_leaves = 0
    knife = []      # (name, [(path, dir, old, new)])
    robust = []
    field_hits = {} # path -> number of specimens it flips

    for s in specs:
        base = audit_flags(s)
        flips = []
        for path, val in numeric_leaves(s):
            total_leaves += 1
            step = step_for(val)
            tokens = _split_path(path)
            for direction in (+1, -1):
                if direction < 0 and isinstance(val, int) and val <= 0:
                    continue
                newval = val + direction * step
                # keep counts non-negative
                if isinstance(newval, int) and newval < 0:
                    continue
                pert = copy.deepcopy(s)
                _set_at(pert, tokens, newval)
                new = audit_flags(pert)
                if new != base:
                    flips.append((path, "+" if direction > 0 else "-",
                                  sorted(base), sorted(new), classify_field(path)))
                    field_hits[path] = field_hits.get(path, 0) + 1
        if flips:
            knife.append((s["name"], flips))
        else:
            robust.append(s["name"])

    print("KNIFE-EDGE PROBE  (dual of calibration_boundary.py)")
    print("%d specimens, %d numeric leaves perturbed (one minimal step each)"
          % (len(specs), total_leaves))
    print()
    print("ROBUST (verdict stable under every minimal single-field perturbation): %d/%d"
          % (len(robust), len(specs)))
    print("KNIFE-EDGE (verdict flips under >=1 minimal perturbation): %d/%d"
          % (len(knife), len(specs)))
    print()
    by_class = {"measured": [], "structural": [], "declared": [], "unclassified": []}
    for name, flips in knife:
        for path, d, old, new, cls in flips:
            by_class[cls].append((name, path, d, old, new))

    print("=== knife-edge by field class ===")
    for cls in ("measured", "structural", "declared", "unclassified"):
        rows = by_class[cls]
        names = sorted(set(r[0] for r in rows))
        print("  %-13s %2d flips across %2d specimens" % (cls, len(rows), len(names)))
    print()
    print("=== knife-edge specimens (near-miss rows, tagged) ===")
    for name, flips in knife:
        print("[%s]" % name)
        for path, d, old, new, cls in flips:
            print("    [%s] %s%s  %s -> %s" % (cls, path, d,
                                                ",".join(old) or "(clean)",
                                                ",".join(new) or "(clean)"))
    print()
    print("=== most load-bearing fields (specimens flipped) ===")
    for path, n in sorted(field_hits.items(), key=lambda kv: -kv[1])[:15]:
        print("    %-28s %d" % (path, n))
    print()
    meas_specs = set(r[0] for r in by_class["measured"])
    struct_specs = set(r[0] for r in by_class["structural"])
    decl_specs = set(r[0] for r in by_class["declared"])
    uncl_specs = set(r[0] for r in by_class["unclassified"])
    only_struct_decl = (struct_specs | decl_specs | uncl_specs) - meas_specs
    both = meas_specs & (struct_specs | decl_specs)
    print("Ruggedness (measurement-noise only): %d/%d verdicts are one rounding"
          % (len(meas_specs), len(specs)))
    print("error from flipping on a MEASURED quantity. %d/%d flip only on"
          % (len(only_struct_decl), len(specs)))
    print("structural set-sizes or declared parameters (dataset shape / the claim's")
    print("own declared value), not measurement noise. %d/%d flip on both."
          % (len(both), len(specs)))
    print("Every knife-edge row is a logged near-miss, not a confession.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
