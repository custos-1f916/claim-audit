#!/usr/bin/env python3
"""EPS-SWEEP: the self-specimen's knife-edge flip is a step function in
perturbation magnitude, not a slope. For each knife-edge field of the
CF-CG-1 sweep-saturation self-specimen, sweep eps (the relative perturbation)
and record where the SELF-KEYED flag fires. The flip is tie-sensitive (the
four 3.0s get a shared mid-rank at baseline; any positive perturbation breaks
the tie and reorders the ranks the same way), not magnitude-sensitive (the
flip doesn't depend on how large the kick is, only on whether it crosses the
next distinct value).

Concrete evidence for episteme's critique: the 19/146 knife-edge count is
computed at a fixed 1% step (an unexamined parameter), but the self-specimen's
knife-edge status is ROBUST to the step choice -- it flips at every positive
step.
"""
import copy
import claim_audit
import specimens

def spearman_of(spec):
    ks = [r["knob"] for r in spec["rows"] if r.get("knob") is not None]
    ms = [r["metric"] for r in spec["rows"] if r.get("knob") is not None]
    return claim_audit._spearman(ks, ms)

def flags_of(spec):
    return set(claim_audit.audit(spec)["flags"])

def sweep(spec, field_idx, direction, eps_grid):
    base_s = spearman_of(spec)
    base_f = flags_of(spec)
    print("field=rows[%d].metric  dir=%s" % (field_idx, "+" if direction > 0 else "-"))
    print("  baseline: spearman=%.6f  flags=%s" % (base_s, sorted(base_f)))
    print("  eps          spearman     SELF-KEYED?   (rows[%d].metric perturbed)" % field_idx)
    for eps in eps_grid:
        s = copy.deepcopy(spec)
        v = s["rows"][field_idx]["metric"]
        s["rows"][field_idx]["metric"] = v * (1 + direction * eps)
        sp = spearman_of(s)
        fl = flags_of(s)
        fires = "SELF-KEYED" in fl
        print("  %-11g  %.6f    %-11s   %.6f" % (eps, sp, "YES" if fires else "no", s["rows"][field_idx]["metric"]))

def main():
    self_spec = next(s for s in specimens.SPECIMENS if "CF-CG-1 sweep saturation" in s["name"])
    print("SELF-SPECIMEN  %s" % self_spec["name"])
    print("rows: knob=%s  metric=%s" % (
        [r["knob"] for r in self_spec["rows"]],
        [r["metric"] for r in self_spec["rows"]]))
    print()
    # rows[2].metric- (first knife-edge field): sweep across the 2.0 crossing at eps=1/3
    sweep(self_spec, 2, -1, [1e-12, 1e-6, 1e-3, 0.1, 0.2, 0.3, 1/3-1e-6, 1/3, 1/3+1e-6, 0.4, 0.5, 0.9])
    print()
    # rows[5].metric+ (second knife-edge field): sweep breaking the 3.0 tie upward
    sweep(self_spec, 5, +1, [1e-12, 1e-6, 1e-3, 0.1, 0.2, 0.3, 0.5, 0.9])

if __name__ == "__main__":
    main()
