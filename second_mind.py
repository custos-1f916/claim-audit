#!/usr/bin/env python3
"""Second-mind label-derivation pass over the fact->axis conceptual class.

The calibration battery (calibration.py / calibration_boundary.py) is
independent of check IMPLEMENTATION (truth comes from raw rows) but NOT of
check DEFINITION: the mapping from a mechanical fact to an axis NAME is
authored by the same mind as the check. A taxonomy co-error (check + label
both wrong in the same direction) keeps the battery GREEN.

This pass re-derives, for each primary empirical axis, the RAW MECHANICAL
FACT by an independent code path (a different test where possible: strict
monotonicity vs the check's spearman>=0.9, set-difference vs the check's
subset test, etc.). Each second_* function uses ONLY the raw rows (spec);
none of them calls a claim_audit check. claim_audit.audit() is read only to
obtain the check's own vote, so a fact-extraction bug in the check is caught
and the fact->name judgment is surfaced as an inspectable artifact.

Three votes per (specimen, axis):
  check  = does claim_audit.audit flag this axis
  truth  = is this axis in the stored specimen label
  second = does my independent fact re-derivation fire

Because the battery baseline is GREEN, check==truth on every cell; the cells
where second != check(==truth) are exactly the co-wrongs the battery
structurally cannot see (the check and the label agree, but an independent
route to the fact disagrees).

Honest limit: this pass is still authored by the same mind, so it is a
within-taxonomy second derivation, not a full independent mind. It catches
fact-extraction co-wrongs and surfaces the name judgments; it does NOT fully
close the taxonomy co-error (that needs a genuinely different mind reading the
artifact, or marking the class self-keyed).
"""
import calibration
import claim_audit

SPECS = calibration.SPECIMENS


def _on(spec):
    return [r for r in spec.get("rows", []) if r.get("mechanism_on")]

def _nul(spec):
    return [r for r in spec.get("rows", []) if (not r.get("mechanism_on")) or r.get("is_null")]


def second_self_keyed(spec):
    rows = [r for r in spec.get("rows", []) if r.get("knob") is not None]
    if len(rows) < 2:
        return False, "N/A (fewer than 2 knob readings)"
    pairs = sorted(((r["knob"], r["metric"]) for r in rows), key=lambda t: t[0])
    diffs = [b[1] - a[1] for a, b in zip(pairs, pairs[1:])]
    if all(d > 0 for d in diffs):
        mono = "strictly increasing"
    elif all(d < 0 for d in diffs):
        mono = "strictly decreasing"
    else:
        return False, "metric not monotone in knob (diffs %s)" % diffs
    kind = spec.get("knob_kind")
    note = "knob_kind=%s" % kind if kind else "knob_kind undeclared"
    return True, "metric %s in knob %s; %s" % (mono, [p[0] for p in pairs], note)


def second_null_reaches(spec):
    on, nul = _on(spec), _nul(spec)
    if not on or not nul:
        return False, "N/A (no null rows)"
    h = max(r["metric"] for r in on); n = max(r["metric"] for r in nul)
    if h > n:
        return False, "mechanism %g > null %g" % (h, n)
    return True, "null %g >= mechanism %g" % (n, h)


def second_confounded(spec):
    if spec.get("type") != "ablation":
        return False, "N/A (not an ablation)"
    lever = spec.get("mechanism_lever")
    on, nul = _on(spec), _nul(spec)
    if not on or not nul:
        return False, "N/A (no matched rows)"
    def comps(r): return set(r.get("substrate", []))
    best = max(on, key=lambda r: r["metric"])
    for nrow in nul:
        if (comps(best) - comps(nrow)) <= {lever}:
            return False, "a null drops only the lever %r; substrate held" % lever
    bn = max(nul, key=lambda r: r["metric"])
    extra = sorted((comps(best) - comps(bn)) - {lever})
    return True, "no null holds the substrate; best null drops %s beyond the lever %r" % (extra, lever)


def second_wrong_axis(spec):
    rows = [r for r in spec.get("rows", []) if r.get("mechanism_axis") is not None]
    if len(rows) < 2:
        return False, "N/A (no mechanism-axis readings)"
    on_ax = [r["mechanism_axis"] for r in rows if r.get("mechanism_on")]
    nul_ax = [r["mechanism_axis"] for r in rows if (not r.get("mechanism_on")) or r.get("is_null")]
    if on_ax and nul_ax:
        if max(on_ax) > max(nul_ax):
            return False, "mechanism beats null on its own axis"
        return True, "mechanism at/below null on its own axis (%g <= %g)" % (max(on_ax), max(nul_ax))
    return False, "N/A (no matched axis readings)"


def second_within_noise(spec):
    on, nul = _on(spec), _nul(spec)
    if not on or not nul:
        return False, "N/A (no null rows)"
    h_row = max(on, key=lambda r: r["metric"]); h = h_row["metric"]
    n = max(r["metric"] for r in nul)
    if not (h > n):
        return False, "N/A (no point beat)"
    ci = h_row.get("ci")
    if ci is None:
        se = h_row.get("se")
        if se is None:
            return False, "N/A (no CI/SE)"
        lo = h - 1.96 * se
    else:
        lo = ci[0]
    if n >= lo:
        return True, "null %g inside mechanism CI (lo %g)" % (n, lo)
    return False, "null %g outside CI (lo %g)" % (n, lo)


def second_consequence(spec):
    ref = spec.get("referent"); wo = spec.get("witness_observes")
    if ref is None or wo is None:
        return False, "N/A (referent or witness not declared)"
    def norm(s): return " ".join(str(s).lower().split())
    refn = norm(ref)
    for w in wo:
        if norm(w) == refn:
            return False, "witness observes the referent directly"
    return True, "witness observes only consequences (%s), never the referent %r" % (wo, ref)


def second_lossy(spec):
    by = {}
    for r in spec.get("rows", []):
        if r.get("record") is None or r.get("referent_value") is None:
            continue
        rec = tuple(r["record"]) if isinstance(r["record"], (list, tuple)) else r["record"]
        by.setdefault(rec, set()).add(r["referent_value"])
    multi = {rec: vals for rec, vals in by.items() if len(vals) > 1}
    if not multi:
        return False, "N/A (no record maps to >1 referent value)"
    return True, "record(s) %s map to >1 referent value: %s" % (list(multi.keys()), multi)


def second_selection_bias(spec):
    rows = spec.get("rows", [])
    draws = [r for r in rows if r.get("draw") is not None or r.get("statistic") == "max"]
    if len(draws) < 2:
        return False, "N/A (fewer than 2 draws)"
    knobs = [r["knob"] for r in draws if r.get("knob") is not None]
    fixed = (len(set(knobs)) <= 1) if knobs else False
    if not fixed:
        return False, "knob varies across draws %s -> not a fixed instrument" % sorted(set(knobs))
    hmax = max(r["metric"] for r in draws)
    allmax = max(r["metric"] for r in rows)
    if allmax != hmax:
        return False, "headline is not the max of the draws"
    return True, "headline %g is the max of %d independent draws of a fixed instrument (knob %s)" % (hmax, len(draws), sorted(set(knobs)))


def second_agg_reversal(spec):
    rows = spec.get("rows", [])
    by = {}
    for r in rows:
        if r.get("subgroup") is None or r.get("n") is None:
            continue
        by.setdefault(r["subgroup"], []).append(r)
    dirs = {}
    for sg, rs in by.items():
        m = [r["metric"] for r in rs if r.get("mechanism_on")]
        n = [r["metric"] for r in rs if (not r.get("mechanism_on")) or r.get("is_null")]
        if not m or not n:
            continue
        dirs[sg] = 1 if max(m) > max(n) else (-1 if max(n) > max(m) else 0)
    if len(dirs) < 2:
        return False, "N/A (fewer than 2 subgroups with both readings)"
    if any(v == 0 for v in dirs.values()):
        return False, "a subgroup is a tie (no unanimous direction)"
    if max(dirs.values()) != min(dirs.values()):
        return False, "within-subgroup directions not unanimous (%s)" % dirs
    pm = sum(r["metric"] * r["n"] for r in rows if r.get("mechanism_on"))
    pn = sum(r["metric"] * r["n"] for r in rows if (not r.get("mechanism_on")) or r.get("is_null"))
    nm = sum(r["n"] for r in rows if r.get("mechanism_on"))
    nn = sum(r["n"] for r in rows if (not r.get("mechanism_on")) or r.get("is_null"))
    if nm == 0 or nn == 0:
        return False, "N/A (no pooled weight)"
    pooled_dir = 1 if pm / nm > pn / nn else (-1 if pn / nn > pm / nm else 0)
    if pooled_dir == max(dirs.values()):
        return False, "pooled agrees with within-subgroup (no reversal)"
    return True, "within-subgroup unanimous %s but pooled reverses to %d (Simpson)" % (dirs, pooled_dir)


AXES = [
    ("SELF-KEYED", second_self_keyed),
    ("NULL-REACHES-HEADLINE", second_null_reaches),
    ("CONFOUNDED", second_confounded),
    ("WRONG-AXIS", second_wrong_axis),
    ("WITHIN-NOISE", second_within_noise),
    ("CONSEQUENCE-WITNESSED", second_consequence),
    ("LOSSY-PROJECTION", second_lossy),
    ("SELECTION-BIAS", second_selection_bias),
    ("AGGREGATION-REVERSAL", second_agg_reversal),
]


def main():
    audit_flags = {s["name"]: set(claim_audit.audit(s)["flags"]) for s in SPECS}

    in_play = agree = 0
    missed = []      # check==truth (battery-green) but second disagrees
    other = []       # check != truth (battery would be RED on this cell)
    for s in SPECS:
        name = s["name"]; truth = set(s["truth"]); flags = audit_flags[name]
        for axis, fn in AXES:
            sf, fact = fn(s)
            cf = axis in flags; th = axis in truth
            if not (cf or th or sf):
                continue
            in_play += 1
            if cf == th == sf:
                agree += 1
            elif cf == th:
                missed.append((name, axis, cf, fact))
            else:
                other.append((name, axis, cf, th, sf, fact))

    print("=== second-mind label-derivation pass (fact->axis conceptual class) ===")
    print("axes re-derived independently : %d" % len(AXES))
    print("specimens                      : %d" % len(SPECS))
    print()
    print("in-play cells (any vote fires) : %d" % in_play)
    print("  all-three-agree              : %d" % agree)
    print("  BATTERY-MISSED (check==truth, second disagrees) : %d" % len(missed))
    print("  check!=truth (battery would be RED on this cell): %d" % len(other))
    print()
    if missed:
        print("--- BATTERY-MISSED co-wrong candidates (the check and the label agree;")
        print("    an independent route to the fact disagrees) ---")
        for name, axis, cf, fact in missed:
            print("  %-30s %-24s (check+truth fire)" % (name, axis))
            print("      second-fact: %s" % fact)
        print()
    if other:
        print("--- check!=truth (the battery itself is RED on these cells) ---")
        for name, axis, cf, th, sf, fact in other:
            print("  %-30s %-24s check=%s truth=%s second=%s" % (name, axis, cf, th, sf))
            print("      second-fact: %s" % fact)
        print()
    print("Honest limit: this pass is a within-taxonomy second derivation (same")
    print("author). It confirms the FACTS by an independent route and surfaces the")
    print("fact->name judgments; it does NOT fully close the taxonomy co-error.")
    print("Full closure = a different mind (Kim/verdigris) reading this artifact,")
    print("or marking the fact->name class self-keyed in the report.")
    return 0


def emit_judgments():
    """Emit the inspectable fact->name table: for each axis, the fact that fires
    it, the fire-cell specimens (where the independent second derivation fires),
    and the check/truth votes on those cells. This is the artifact a genuinely
    different mind (Kim/verdigris) reads to audit the fact->name mapping the
    battery (check==truth) structurally cannot see.

    Because the battery baseline is GREEN, check==truth on every cell; the cells
    where the second derivation fires but the check does not are the fact-
    extraction co-wrongs, and the cells where all three agree are the confirmed
    facts. The fact->name judgment itself remains authored by the same mind;
    this table is the surface a different mind audits."""
    audit_flags = {s["name"]: set(claim_audit.audit(s)["flags"]) for s in SPECS}
    print("=== fact->name judgments (the inspectable surface) ===")
    print("For each axis: the fact that fires it, the fire cells (where the")
    print("independent second derivation fires), and the check/truth votes.")
    print("A different mind reads this to audit the fact->name mapping the")
    print("battery (check==truth) cannot see.")
    print()
    total_fire = 0
    for axis, fn in AXES:
        fire_cells = []
        for s in SPECS:
            sf, fact = fn(s)
            if sf:
                flags = audit_flags[s["name"]]
                fire_cells.append((s["name"], axis in flags, axis in set(s["truth"]), fact))
        total_fire += len(fire_cells)
        if not fire_cells:
            print("AXIS %-26s: no fire cell (not exercised by the battery)" % axis)
            continue
        print("AXIS %-26s: %d fire cell(s)" % (axis, len(fire_cells)))
        for name, cf, th, fact in fire_cells:
            print("    %-30s check=%-5s truth=%-5s second=True" % (name, cf, th))
            print("        fact: %s" % fact)
        print()
    print("%d fire cells total across %d axes." % (total_fire, len(AXES)))
    print()
    print("The fact->name mapping above is authored by the same mind as the")
    print("checks. A different mind reading this table is the closure the")
    print("battery cannot provide (the taxonomy co-error).")
    return 0


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--judgments":
        raise SystemExit(emit_judgments())
    raise SystemExit(main())
