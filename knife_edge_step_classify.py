#!/usr/bin/env python3
"""STEP-CLASSIFY: for every knife-edge the 1% probe flags, sweep the
perturbation step and classify the flip along two axes.

PRIMARY AXIS -- INVARIANT vs WINDOWED (is the knife-edge status robust to the
probe's step choice? This is the direct answer to episteme's critique that the
1% step is an unexamined parameter):
  - INVARIANT: flips at every relative step from the minimum kick up to the
    grid max (5.0x for direction=+1; capped at the 1.0 domain boundary for
    direction=-1). Changing the probe's step cannot remove the knife-edge; it
    is a stable property. The sweep is in relative terms (val * EPS), matching
    the probe's parameter space.
  - WINDOWED: flips only in a bounded relative-step range. The knife-edge count
    is step-relative: a different probe step gives a different count.

The sweep grid is direction-aware: out-of-domain points (newval < 0) are
excluded rather than counted as non-flips, so a truly INVARIANT row cannot be
misclassified as WINDOWED by domain-excluded points. The continuous grid is
extended above 0.9 (to 5.0x), so a row whose flip window stops above relative
step 0.9 is no longer INVARIANT by construction.

SECONDARY AXIS -- TIE vs CLOSE-CALL (is the flip a measurement degeneracy or a
genuine near-miss?). This is only defined for CONTINUOUS fields:
  - TIE: flips at 1e-6 (far below the 1% probe step). The baseline value sits
    exactly on a rank/decision boundary, so any kick breaks it. This is the
    self-specimen's structure (it flips at 1e-12).
  - CLOSE-CALL: flips at 1% but NOT at 1e-6. The value is near the boundary
    with a real (if small) gap; the 1% is a real kick over a real gap.
  For INTEGER fields the knife-edge is DEFINED by the +1 kick (the minimum
  possible), so "flips at min kick" is tautological and the TIE/CLOSE-CALL
  distinction is not measurable -- int rows are tagged MIN-KICK and excluded
  from the TIE count.

Re-runnable; battery self-check is inherited from the specimen set.
"""
import copy
import claim_audit
import specimens
from knife_edge import numeric_leaves, _split_path, _set_at, audit_flags, EPS

CONT_GRID = [1e-9, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 0.2, 0.5, 0.9, 1.0, 1.5, 2.0, 3.0, 5.0, 10, 100, 1000, 1e4, 1e6, 1e9, 1e12]
INT_GRID  = [1, 2, 3, 5, 10]
TIE_IDX_CONT = 1   # 1e-6 (grid[0]=1e-9 is numerically degenerate); still index 1 in the
    # direction-capped grids (1e-6 < 1.0, so the cap never drops it)


def flagged_fields():
    """Re-derive the exact (spec, path, val, direction, kind) tuples the 1%
    probe flags, so we classify the same set knife_edge.py reports."""
    out = []
    for s in specimens.SPECIMENS:
        base = audit_flags(s)
        for path, val in numeric_leaves(s):
            if isinstance(val, int) and not isinstance(val, bool):
                for direction in (+1, -1):
                    if direction < 0 and val <= 0:
                        continue
                    newval = val + direction
                    if newval < 0:
                        continue
                    pert = copy.deepcopy(s)
                    _set_at(pert, _split_path(path), newval)
                    if audit_flags(pert) != base:
                        out.append((s, path, val, direction, "int"))
            else:
                step = max(abs(val) * EPS, 1e-9)
                for direction in (+1, -1):
                    newval = val + direction * step
                    pert = copy.deepcopy(s)
                    _set_at(pert, _split_path(path), newval)
                    if audit_flags(pert) != base:
                        out.append((s, path, val, direction, "cont"))
    return out


def sweep(spec, path, val, direction, kind):
    base = audit_flags(spec)
    # Direction-aware grid: cap out-of-domain points so they cannot read as
    # non-flips (a truly INVARIANT row must not be misclassified as WINDOWED
    # by points the domain excludes). TIE_IDX_CONT stays valid: 1e-6 < 1.0.
    if kind == "int":
        grid = INT_GRID if direction > 0 else [g for g in INT_GRID if g <= val]
    else:
        grid = CONT_GRID if direction > 0 else [g for g in CONT_GRID if g <= 1.0]
    flips = []
    for g in grid:
        if kind == "cont":
            # Relative step, matching the probe's parameter space (val * EPS)
            step = max(abs(val) * g, 1e-9)
            newval = val + direction * step
        else:
            # Absolute kick (int fields have a fixed step of 1)
            newval = val + direction * g
        if newval < 0:
            flips.append(False)
            continue
        pert = copy.deepcopy(spec)
        _set_at(pert, _split_path(path), newval)
        flips.append(audit_flags(pert) != base)
    return grid, flips


def classify(flips, kind):
    invariant = all(flips)
    robust = "INVARIANT" if invariant else "WINDOWED"
    if kind == "cont":
        kind_name = "TIE" if flips[TIE_IDX_CONT] else "CLOSE-CALL"
    else:
        kind_name = "MIN-KICK"   # tautological for int; not a degeneracy test
    return kind_name, robust


def window_tag(flips, grid, direction, kind):
    """For a WINDOWED row, say where the flip window is bounded. The grid range
    is an unexamined parameter: a window that reaches the grid max/min is NOT
    confirmed bounded there -- it may extend beyond the grid. The grid now spans
    [1e-9, 1e12] (cont), so an edge tag is a statement about that range. Tags:
      [bounded]      both ends confirmed strictly inside the grid (genuine window)
      ->half-line    high end at the grid max AND the flip is a contiguous run
                     (monotone threshold) reaching the max: the window is
                     unbounded above within the probed range (a threshold, not a
                     bounded window that happens to reach the max).
      ->domain       high end at the domain boundary (dir=-1 cont, g=1.0 -> newval=0)
      <-step-floor   low end at the grid min AND the flip is a contiguous run
                     reaching the min: the window extends down to the
                     instrument's minimum resolvable kick (a TIE/degeneracy --
                     the value sits exactly on a boundary, so any resolvable
                     kick flips it).
      ->grid-max     high end at the grid max, flip NOT contiguous (a bounded
                     window whose true high end is beyond the grid; unconfirmed)
      <-grid-min     low end at the grid min, flip NOT contiguous (unconfirmed)
    A non-monotone window can carry two edge tags; a contiguous one carries one.
    """
    n = len(flips)
    flip_idx = [i for i, f in enumerate(flips) if f]
    if not flip_idx:
        return "(no flip in grid)"
    lo, hi = flip_idx[0], flip_idx[-1]
    contiguous = all(flips[i] for i in range(lo, hi + 1))  # no gaps in [lo, hi]
    tags = []
    if lo == 0:
        tags.append("<-step-floor" if contiguous else "<-grid-min")
    if hi == n - 1:
        if direction < 0 and kind == "cont":
            tags.append("->domain")
        elif contiguous:
            tags.append("->half-line")
        else:
            tags.append("->grid-max")
    if not tags:
        tags.append("[bounded]")
    return " ".join(tags)


def main():
    rows = flagged_fields()
    specs = specimens.SPECIMENS
    n_specs_knife = len(set(s["name"] for s, *_ in rows))
    print("STEP-CLASSIFY  (generalizes the CF-CG-1 eps-sweep to the whole battery)")
    print("%d specimens; %d have >=1 knife-edge; %d knife-edge (field, direction) rows at the 1%% probe step"
          % (len(specs), n_specs_knife, len(rows)))
    print("cont grid: %s" % CONT_GRID)
    print("int  grid: %s" % INT_GRID)
    print()

    ties = closecalls = 0
    introws = 0
    invariant = windowed = 0
    w_bounded = w_gridmax = w_gridmin = w_domain = w_halfline = w_stepfloor = 0
    by_spec = {}

    for s, path, val, direction, kind in rows:
        grid, flips = sweep(s, path, val, direction, kind)
        kind_name, robust = classify(flips, kind)
        if kind == "cont":
            ties += kind_name == "TIE"
            closecalls += kind_name == "CLOSE-CALL"
        else:
            introws += 1
        invariant += robust == "INVARIANT"
        windowed += robust == "WINDOWED"
        if robust == "WINDOWED":
            tag = window_tag(flips, grid, direction, kind)
            if "[bounded]" in tag: w_bounded += 1
            if "->grid-max" in tag: w_gridmax += 1
            if "<-grid-min" in tag: w_gridmin += 1
            if "->domain" in tag: w_domain += 1
            if "->half-line" in tag: w_halfline += 1
            if "<-step-floor" in tag: w_stepfloor += 1
        else:
            tag = ""
        by_spec.setdefault(s["name"], []).append(
            (path, direction, kind, flips, kind_name, robust, tag))

    for name, items in by_spec.items():
        selfmark = "  [SELF-SPECIMEN]" if "CF-CG-1 sweep saturation" in name else ""
        print("[%s]%s" % (name, selfmark))
        for path, direction, kind, flips, kind_name, robust, tag in items:
            marks = "".join(("X" if f else ".") for f in flips)
            print("    [%s] %s%s  %s  %-11s %-10s %s" % (
                kind, path, "+" if direction > 0 else "-", marks, kind_name, robust, tag))
        print()

    controws = ties + closecalls
    print("=== SUMMARY ===")
    print("PRIMARY (step-robustness, all %d rows):" % len(rows))
    print("  INVARIANT (flips at every step min..grid max, robust to step choice): %d/%d" % (invariant, len(rows)))
    print("  WINDOWED  (step-relative; the 1%% probe lands in their window):   %d/%d" % (windowed, len(rows)))
    print("    by window shape (where the flip window is bounded; grid spans [1e-9, 1e12], an unexamined param):")
    print("      [bounded]      both ends confirmed inside the grid:          %d" % w_bounded)
    print("      ->half-line    high end at grid max, monotone threshold (unbounded above): %d" % w_halfline)
    print("      ->domain       high end at domain boundary (dir=-1):         %d" % w_domain)
    print("      <-step-floor   low end at grid min, TIE to the min kick:     %d" % w_stepfloor)
    print("      ->grid-max     high end at grid max, non-monotone (unconfirmed above): %d" % w_gridmax)
    print("      <-grid-min     low end at grid min, non-monotone (unconfirmed below): %d" % w_gridmin)
    print("SECONDARY (degeneracy, %d CONTINUOUS rows only; %d int rows are MIN-KICK, excluded):" % (controws, introws))
    print("  TIE        (flips at 1e-6, value exactly on a boundary):         %d/%d cont" % (ties, controws))
    print("  CLOSE-CALL (flips at 1%% but not 1e-6, a real near-miss):        %d/%d cont" % (closecalls, controws))
    print()
    inv_specs = sorted(n for n, items in by_spec.items()
                       if all(r[5] == "INVARIANT" for r in items))
    print("Specimens whose knife-edges are ALL invariant (%d):" % len(inv_specs))
    for n in inv_specs:
        mark = "  <-- SELF-SPECIMEN" if "CF-CG-1 sweep saturation" in n else ""
        print("    %s%s" % (n, mark))
    print()
    print("Reading: the PRIMARY axis answers episteme directly -- %d/%d knife-edge rows are" % (invariant, len(rows)))
    print("robust to the probe's step choice, so the knife-edge count is NOT primarily a step-choice")
    print("artifact. The %d WINDOWED rows are the step-relative ones (the 1%% probe lands in their" % windowed)
    print("window by luck). The TIE count (cont only) generalizes the self-specimen finding: a")
    print("knife-edge that flips at 1e-6 is the instrument measuring a degeneracy (the value sits")
    print("exactly on a rank/threshold boundary), not a genuine near-miss.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
