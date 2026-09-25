#!/usr/bin/env python3
"""
claim_audit.py — does the headline metric discriminate the claimed mechanism?

Reusable instrument for auditing a paper's load-bearing claim. A claim is a
(mechanism, metric, null) triple. The instrument runs thirty-seven checks: the primary axes, their sixteen refinements of BEATS-NULL (NOISE-FLOOR, DOSE-RESPONSE, TEMPORAL-ONSET, TEMPORAL-SPIKE, OUTCOME-ONSET, OUTCOME-SPIKE, SUBGROUP-ONSET, SUBGROUP-SPIKE, DOSE-ONSET, DOSE-SPIKE, TIER-ONSET, TIER-SPIKE, SPLIT-ONSET, SPLIT-SPIKE, METRIC-ONSET, METRIC-SPIKE), a COMPUTABLE axis that
operates in the no-data regime, and a set of headline-layer axes, all behind a vacuous-ratio precondition gate.
Each returns PASS or a named flag. A claim DISCRIMINATES only if all empirical checks pass.
The primary checks are
orthogonal axes, not a ladder: a claim can fail any subset of them.

Two regimes: EMPIRICAL (the spec has data rows; the ten empirical checks run)
and NO-EMPIRICAL-CONTENT (a pure specification: no data rows, or
type == 'specification'; the empirical checks are N/A and the COMPUTABLE axis
governs instead). NO-EMPIRICAL-CONTENT is a distinct regime from VACUOUS-RATIO
(a reported ratio with an empty denominator), not a refinement of it.
All sixteen refinements are cell-specific: NOISE-FLOOR, TEMPORAL-ONSET, OUTCOME-ONSET, SUBGROUP-ONSET, DOSE-ONSET, TIER-ONSET, SPLIT-ONSET and METRIC-ONSET can only flag in the BEATS-NULL-PASS cell (they catch a false claim the flat check under-fired), and DOSE-RESPONSE, TEMPORAL-SPIKE, OUTCOME-SPIKE, SUBGROUP-SPIKE, DOSE-SPIKE, TIER-SPIKE, SPLIT-SPIKE and METRIC-SPIKE can only flag in the BEATS-NULL-FAIL cell (they rescue a true claim the flat check over-fired). The cross cells are structurally empty.

  BEATS-NULL       mechanism's headline metric must exceed every null's.
                   fail -> NULL-REACHES-HEADLINE
  NOT-SELF-KEYED   headline must not be (anti-)monotone in the mechanism's own
                   control knob. fail -> SELF-KEYED. N/A when knob_kind is
                   'workload' or 'instrument' (the knob is not the mechanism's
                   own lever).
  ISOLATED         (ablation claims) mechanism row and null row must share the
                   substrate except the mechanism's own lever. fail -> CONFOUNDED
  CO-MOVES         mechanism must beat the null on its own orthogonal axis (or,
                   with no null, the headline must move with that axis).
                   fail -> WRONG-AXIS
  NOISE-FLOOR      (refinement of BEATS-NULL) a point-estimate beat is only
                   resolvable if the mechanism's CI excludes the null's value.
                   fail -> WITHIN-NOISE. N/A when no CI/SE is declared on the
                   mechanism row, or when there is no point beat (BEATS-NULL
                   governs the null-reaching case).
  REFERENT-WITNESSED (5th primary axis, CONSEQUENCE-WITNESSED) the external
                   witness must observe the claim's referent directly, not only
                   a downstream consequence of it. A claim is self-referent when
                   it is about the thing's OWN internals; the witness can sit
                   outside the thing (NOT-SELF-KEYED passes) and the comparison
                   can be unconfounded (ISOLATED passes) while still observing
                   only a downstream consequence (output quality / runtime
                   timing), never the referent itself. The claim's own success
                   signal (realized speedup ~= theoretical speedup) is
                   SELF-SEALING: a function of the mechanism being ON, not of the
                   referent being CORRECT. fail -> CONSEQUENCE-WITNESSED. N/A
                   when the spec does not declare a referent (orthogonal to the
                   other five axes).
  LOSSY-PROJECTION (6th primary axis, MANY-TO-ONE / lossy-projection) the
                   reported value must be a function of the referent alone.
                   The axis fires when the record the metric is computed from
                   is a lossy projection of the referent: two rows share the
                   same `record` but declare different `referent_value`. That
                   is the many-to-one witness -- the referent is
                   non-identifiable from the record, so the reported value
                   cannot discriminate between referent values that share a
                   record. Orthogonal to NOT-SELF-KEYED (one-to-many coupling):
                   here the referent is fixed and the record is lossy, not the
                   knob varying the reading. VACUOUS-RATIO (support 0) is the
                   zero-support degenerate sub-case of this failure; this axis
                   is the general non-vacuous case. fail -> LOSSY-PROJECTION.
                   N/A when fewer than two rows declare both `record` and
                   `referent_value`.
  AGGREGATION-REVERSAL (8th primary axis, Simpson's-paradox / confounding) the
                   within-subgroup direction must not be reversed by the pooling
                   weights. Fires when every subgroup that has both a mechanism
                   and a null reading agrees on the within-subgroup direction
                   (all mechanism-wins, or all null-wins) AND the n-weighted
                   pooled direction is the opposite. The per-row metrics are the
                   same ones BEATS-NULL reads; the axis adds the subgroup/n
                   structure that BEATS-NULL (which compares the max per-row
                   metric) cannot see. fail -> AGGREGATION-REVERSAL. N/A when
                   fewer than two subgroups declare both a mechanism and a null
                   reading (no pooling structure to reverse).

  DOSE-RESPONSE    (refinement of BEATS-NULL, dose-blindness / cross-dose
                   pooling) the
                   flat BEATS-NULL comparison pools max(mechanism) vs max(null)
                   ACROSS the dose/severity variable, so it fires
                   NULL-REACHES-HEADLINE on a TRUE dose-response (advantage
                   grows with severity; on-par at the mild end) exactly as on a
                   FALSE flat claim. The axis reads the within-dose direction
                   that BEATS-NULL cannot see. Fires when every substrate level
                   is mechanism-favorable AND the cross-dose max fires
                   NULL-REACHES-HEADLINE. fail -> DOSE-RESPONSE. N/A when fewer
                   than two substrate levels declare both a mechanism and a null
                   reading, or when the within-dose direction is not uniformly
                   mechanism-favorable.

  TIER-ONSET / TIER-SPIKE (refinements of BEATS-NULL, the tier-dimension
                   mirrors of SUBGROUP-ONSET/SUBGROUP-SPIKE and
                   DOSE-ONSET/DOSE-SPIKE) the flat BEATS-NULL comparison pools
                   max(mechanism) vs max(null) ACROSS the difficulty-tier
                   variable, so a claim scoped to a tier (e.g. "the mechanism
                   helps on the easy tier") is read at the PEAK tier, not the
                   claim tier. TIER-ONSET catches the pass-cell false negative
                   (no beat at the claim tier, a real peak at a non-claim tier,
                   the flat check silent on a false claim); TIER-SPIKE catches
                   the fail-cell false positive (a real beat at the claim tier,
                   a non-claim-tier null spike dominating the cross-tier max,
                   the flat check firing NULL-REACHES-HEADLINE on a true
                   claim). The difficulty tier is the fourth two-ended hidden
                   variable (after time, outcome, subgroup) and needs a NEW
                   spec-schema field (claim_tier + row tier) to test.
                   Justified by LabAgent (2609.15054), whose load-bearing claim
                   scopes to the easy tier with the hard tier dissociating
                   differently. N/A when no claim_tier is declared
                   (schema-boundary). fail -> TIER-ONSET / TIER-SPIKE.
  METRIC-ONSET / METRIC-SPIKE (refinements of BEATS-NULL, the metric-dimension
                   wire, 2026-09-18) the flat check pools max-mech vs max-null
                   ACROSS ALL metric quantities, so for a metric-scoped claim it
                   reads the PEAK metric, not the claim metric. The metric
                   QUANTITY (what the number measures: accuracy vs
                   latency-reduction) is the SEVENTH scope dimension (after
                   time, outcome, subgroup, dose, tier, split) and is
                   orthogonal to the statistic KIND (how the number was
                   derived: order vs single vs summary, the
                   INCOMPARABLE-STATISTIC precondition). It needs a NEW
                   spec-schema field (claim_metric + row metric_name) to test.
                   METRIC-ONSET catches the pass-cell false negative (the
                   pooled peak is at a non-claim metric while the at-claim-metric
                   value does not support the claim); METRIC-SPIKE catches the
                   fail-cell false positive (the pooled null spike is at a
                   non-claim metric while the at-claim-metric value supports the
                   claim). N/A when no claim_metric is declared (schema-boundary:
                   undeclared -> the flat check governs). fail -> METRIC-ONSET /
                   METRIC-SPIKE.

Precondition gate (checked before any axis): the mechanism's headline row must
have a non-empty denominator (support > 0). A support of 0 means the headline
ratio is 0/0; the reported value is a scorer convention, not a measurement, so
the audit short-circuits to VACUOUS-RATIO and every axis is N/A. A ratio with
zero support is vacuous, not perfect.

Comparison types (declared per spec): ablation | cross-model | knob-sweep.
ISOLATED runs only for ablation; BEATS-NULL runs whenever nulls are present;
NOT-SELF-KEYED and CO-MOVES run whenever their inputs are present.

knob_kind (declared per spec): lever | instrument | workload. The knob field
encodes only two states via data-inference (varies -> the lever; constant -> a
fixed instrument), but the real distinction is three-way: the knob may be the
mechanism's own LEVER (self-keying applies), a fixed INSTRUMENT's knob
(max-of-K selection bias applies), or an external WORKLOAD axis (a legitimate
max-over-a-workload-sweep is neither). When knob_kind is declared it overrides
the inference: NOT-SELF-KEYED is N/A for workload/instrument, and
SELECTION-BIAS is N/A for lever/workload. Undeclared -> current inference.

Usage:
  python3 claim_audit.py                 # run all built-in specimens
  python3 claim_audit.py --spec f.json   # audit one external spec
"""
import json, math, sys

def _pearson(xs, ys):
    n = len(xs)
    if n < 2: return None
    mx = sum(xs)/n; my = sum(ys)/n
    sxx = sum((x-mx)**2 for x in xs)
    syy = sum((y-my)**2 for y in ys)
    sxy = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    if sxx == 0 or syy == 0: return None
    return sxy / math.sqrt(sxx*syy)

def _ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks = [0.0]*len(xs)
    i = 0
    while i < len(xs):
        j = i
        while j+1 < len(xs) and xs[order[j+1]] == xs[order[i]]:
            j += 1
        avg = (i + j)/2.0 + 1.0
        for k in range(i, j+1):
            ranks[order[k]] = avg
        i = j+1
    return ranks

def _spearman(xs, ys):
    if len(xs) < 2: return None
    return _pearson(_ranks(xs), _ranks(ys))

def _rows(spec, pred):
    return [r for r in spec["rows"] if pred(r)]
def _headline_support(spec):
    """Return the mechanism's headline row's support (denominator count),
    or None if no mechanism row declares a support. A support of 0 means the
    headline ratio has an empty denominator and is undefined (vacuous)."""
    on_rows = _rows(spec, lambda r: r.get("mechanism_on"))
    if not on_rows:
        return None
    h_row = max(on_rows, key=lambda r: r["metric"])
    return h_row.get("support")


ORDER_STATISTICS = {"best","max","min","worst","p95","p5","topk","top-k"}
SUMMARY_STATISTICS = {"mean","median","mode"}
SINGLE_STATISTICS  = {"single","as-reported","one","run","reported"}

def _stat_class(stat):
    """Classify a row's declared statistic. A bare reported value (no statistic
    field) is a single draw. Order statistics (best/max/p95 over a population)
    are structurally inflated relative to a single draw or a central tendency;
    summaries (mean/median) are not."""
    if stat is None:
        return "single"
    s = str(stat).strip().lower()
    if s in ORDER_STATISTICS:
        return "order"
    if s in SUMMARY_STATISTICS:
        return "summary"
    return "single"

def _incomparable_statistic(spec):
    """INCOMPARABLE-STATISTIC precondition (same species as VACUOUS-RATIO): the
    mechanism's headline row and the null's headline row must be the same KIND of
    statistic. Fires when the two differ AND at least one is an ORDER STATISTIC
    (best/max/p95 over a population) -- then the beat is an artifact of taking an
    extreme of a distribution, not the mechanism. A central tendency (mean/median)
    vs a single draw is a rough-but-conservative comparison the primary axes can
    still adjudicate, so it does NOT fire. Returns (fires: bool, detail: str)."""
    on_rows  = _rows(spec, lambda r: r.get("mechanism_on"))
    nul_rows = _rows(spec, lambda r: (not r.get("mechanism_on")) or r.get("is_null"))
    if not on_rows or not nul_rows:
        return False, ""
    m_head = max(on_rows,  key=lambda r: r["metric"])
    n_head = max(nul_rows, key=lambda r: r["metric"])
    ms, ns = m_head.get("statistic"), n_head.get("statistic")
    mc, nc = _stat_class(ms), _stat_class(ns)
    if mc == nc:
        return False, ""
    if mc != "order" and nc != "order":
        return False, ""
    return True, ("mechanism headline statistic '%s' (class %s) vs null headline statistic '%s' (class %s); the two sides are different kinds of statistic and one is an order statistic, so the beat is an artifact of the order statistic, not the mechanism" % (ms, mc, ns, nc))

def _by_construction(spec):
    """BY-CONSTRUCTION precondition (same species as VACUOUS-RATIO): the
    load-bearing headline number must be a genuine measurement, not a
    by-construction guarantee. A by-construction number (e.g., '0% type errors
    guaranteed by the type system') is real but its empirical frame is empty:
    the 'empirical' comparison is vacuous because the number is added, not
    measured. Fires when the mechanism's headline row declares by_construction:
    True. Returns (fires: bool, detail: str)."""
    on_rows = _rows(spec, lambda r: r.get("mechanism_on"))
    if not on_rows:
        return False, ""
    h_row = max(on_rows, key=lambda r: r["metric"])
    if h_row.get("by_construction"):
        return True, ("the load-bearing headline number (%g) is a by-construction guarantee, not a measurement; the empirical frame is empty (the number is added, not measured)" % h_row["metric"])
    return False, ""


def check_beats_null(spec):
    on  = [r["metric"] for r in _rows(spec, lambda r: r.get("mechanism_on"))]
    nul = [r["metric"] for r in _rows(spec, lambda r: (not r.get("mechanism_on")) or r.get("is_null"))]
    if not on or not nul:
        return True, "", "N/A (no null rows)"
    h, n = max(on), max(nul)
    if h > n:
        return True, "", "mechanism %g > null %g" % (h, n)
    return False, "NULL-REACHES-HEADLINE", "null %g >= mechanism %g (metric cannot tell mechanism from null)" % (n, h)

def _knob_kind(spec):
    """The declared three-way role of the knob: 'lever' (the mechanism's own
    control lever), 'instrument' (a fixed instrument's knob, constant across
    repeated draws), or 'workload' (an external workload axis, e.g. batch size).
    None when undeclared -> the checks fall back to data-inference (knob varies
    -> the lever; knob constant -> a fixed instrument). The three-way
    distinction is what the binary knob field cannot express: a legitimate
    max-over-a-workload-sweep is neither self-keyed (the lever is the mechanism,
    not the workload axis) nor selection-biased (the draws are not repeated
    measurements of a fixed instrument)."""
    k = spec.get("knob_kind")
    return k if k in ("lever", "instrument", "workload") else None

def check_not_self_keyed(spec):
    ks = [r["knob"] for r in spec["rows"] if r.get("knob") is not None]
    ms = [r["metric"] for r in spec["rows"] if r.get("knob") is not None]
    if len(ks) < 2:
        return True, "", "N/A (no knob readings)"
    kind = _knob_kind(spec)
    if kind in ("workload", "instrument"):
        return True, "", "N/A (knob_kind=%s: the knob is not the mechanism's own lever, so self-keying does not apply)" % kind
    r = _spearman(ks, ms)
    if r is None:
        return True, "", "N/A (zero variance)"
    if abs(r) >= 0.9:
        return False, "SELF-KEYED", "metric is (anti-)monotone in the mechanism's own knob (spearman %+.3f); the instrument reads the lever it is supposed to measure" % r
    return True, "", "metric-knob spearman %+.3f (not monotone in the knob)" % r

def check_selection_bias(spec):
    """SELECTION-BIAS (7th primary axis): the reported headline must not be an
    ORDER STATISTIC (best/max/p95) over multiple independent draws of a FIXED
    instrument. Fires when the mechanism's headline row declares an order
    statistic AND >=2 rows are marked as independent draws of the instrument
    (draw field) AND the instrument's knob is constant across those rows --
    then the reported value is the max of K draws of one fixed instrument,
    which is structurally inflated by ~fsd * E[max of K standard normals]
    (~2.5*fsd at K=100), not a mechanism effect. Distinct from NOT-SELF-KEYED
    (knob VARIES -> SELF-KEYED) and from INCOMPARABLE-STATISTIC (needs a null
    row to compare against). N/A when the knob varies (the knob is the lever,
    not a fixed instrument), when fewer than two rows are marked as draws, or
    when the headline is not an order statistic, or when knob_kind is 'lever'
    or 'workload' (the knob is not a fixed instrument). fail -> SELECTION-BIAS."""
    on_rows = _rows(spec, lambda r: r.get("mechanism_on"))
    if not on_rows:
        return True, "", "N/A (no mechanism rows)"
    kind = _knob_kind(spec)
    if kind in ("lever", "workload"):
        return True, "", "N/A (knob_kind=%s: the knob is not a fixed instrument, so max-of-K selection bias does not apply)" % kind
    # The headline is the row that DECLARES an order statistic (the reported
    # best/max/p95 over the population). Identify it by declaration, not by
    # max metric: the headline's value equals the max draw value by
    # construction, so max(on_rows, key=metric) would tie-break to a draw row
    # (no statistic field -> 'single') and miss the order-statistic headline.
    order_rows = [r for r in on_rows if _stat_class(r.get("statistic")) == "order"]
    if not order_rows:
        return True, "", "N/A (no order-statistic headline declared)"
    h_row = max(order_rows, key=lambda r: r["metric"])
    draws = [r for r in on_rows if r.get("draw") is not None]
    if len(draws) < 2:
        return True, "", "N/A (fewer than two independent draws of the instrument)"
    knobs = [r["knob"] for r in draws if r.get("knob") is not None]
    if len(knobs) < len(draws):
        return True, "", "N/A (knob not declared on all draw rows)"
    if len(set(knobs)) > 1:
        return True, "", "N/A (knob varies across draws: the knob is the lever, not a fixed instrument)"
    draw_metrics = [r["metric"] for r in draws]
    if h_row["metric"] != max(draw_metrics):
        return True, "", "N/A (reported metric is not the max of the draw metrics)"
    return False, "SELECTION-BIAS", ("reported metric %g is the max of %d independent draws of a fixed instrument (knob %s); the max-of-K selection bias inflates the score by ~fsd * E[max of K standard normals] (~2.5*fsd at K=100), not a mechanism effect" % (h_row["metric"], len(draws), knobs[0]))

def check_isolated(spec):
    if spec.get("type") != "ablation":
        return True, "", "N/A (not an ablation claim)"
    lever = spec.get("mechanism_lever")
    on  = [r for r in spec["rows"] if r.get("mechanism_on")]
    nul = [r for r in spec["rows"] if (not r.get("mechanism_on")) or r.get("is_null")]
    if not on or not nul:
        return True, "", "N/A (no matched rows)"
    def comps(r): return set(r.get("substrate", []))
    best = max(on, key=lambda r: r["metric"])
    for nrow in nul:
        missing = comps(best) - comps(nrow)
        if missing <= {lever}:
            return True, "", "isolated: a null drops only the lever %r; substrate held" % lever
    nrow = max(nul, key=lambda r: r["metric"])
    extra = sorted((comps(best) - comps(nrow)) - {lever})
    return False, "CONFOUNDED", "no null holds the substrate: best null drops %s beyond the lever; the gap is the substrate, not the mechanism" % extra

def check_co_moves(spec):
    rows = [r for r in spec["rows"] if r.get("mechanism_axis") is not None]
    if len(rows) < 2:
        return True, "", "N/A (no mechanism-axis readings)"
    on_ax  = [r["mechanism_axis"] for r in rows if r.get("mechanism_on")]
    nul_ax = [r["mechanism_axis"] for r in rows if (not r.get("mechanism_on")) or r.get("is_null")]
    tol = spec.get("axis_tol", 0.0)
    if on_ax and nul_ax:
        if max(on_ax) > max(nul_ax) + tol:
            return True, "", "mechanism beats null on its own axis (%g > %g)" % (max(on_ax), max(nul_ax))
        return False, "WRONG-AXIS", "mechanism at/below null on its own axis (%g <= %g); headline high but the mechanism-relevant axis is at null" % (max(on_ax), max(nul_ax))
    r = _pearson([x["metric"] for x in rows], [x["mechanism_axis"] for x in rows])
    if r is None:
        return True, "", "N/A (zero variance)"
    if r > 0.5:
        return True, "", "metric-mechanism_axis r=%+.3f (move together)" % r
    return False, "WRONG-AXIS", "metric-mechanism_axis r=%+.3f; headline decoupled from the mechanism's own axis" % r

def check_noise_floor(spec):
    """NOISE-FLOOR (refinement of BEATS-NULL): a point-estimate beat is only
    resolvable if the mechanism's CI excludes the null's value. If the CI (or
    SE) is declared on the headline mechanism row and the max null's value
    falls inside it, the beat is within the noise floor -> WITHIN-NOISE.
    N/A when no CI/SE is declared, or when there is no point beat (h <= n),
    in which case BEATS-NULL already governs."""
    on_rows  = _rows(spec, lambda r: r.get("mechanism_on"))
    nul_rows = _rows(spec, lambda r: (not r.get("mechanism_on")) or r.get("is_null"))
    if not on_rows or not nul_rows:
        return True, "", "N/A (no null rows)"
    h_row = max(on_rows, key=lambda r: r["metric"])
    h = h_row["metric"]
    n = max(r["metric"] for r in nul_rows)
    if not (h > n):
        return True, "", "N/A (no point-estimate beat; BEATS-NULL governs)"
    ci = h_row.get("ci")
    if ci is None:
        se = h_row.get("se")
        if se is None:
            return True, "", "N/A (no CI/SE declared on the mechanism row)"
        lo, hi = h - 1.96 * se, h + 1.96 * se
        ci_src = "95%% CI from SE %g" % se
    else:
        lo, hi = ci[0], ci[1]
        ci_src = "95%% CI [%g, %g]" % (lo, hi)
    if n >= lo:
        return False, "WITHIN-NOISE", "beat %g > %g is unresolved: the max null %g sits inside the mechanism's %s (lo %g); the gap is within the noise floor" % (h, n, n, ci_src, lo)
    return True, "", "beat %g > %g is resolved: the max null %g is outside the mechanism's %s (below lo %g)" % (h, n, n, ci_src, lo)

def check_referent_witnessed(spec):
    """REFERENT-WITNESSED (5th primary axis, CONSEQUENCE-WITNESSED): the
    external witness must observe the claim's referent directly, not only a
    downstream consequence of it. A claim is self-referent when it is about the
    thing's OWN internals; the witness can sit outside the thing (NOT-SELF-KEYED
    passes) and the comparison can be unconfounded (ISOLATED passes) while still
    observing only a downstream consequence (output quality / runtime timing),
    never the referent itself. The claim's own success signal (realized speedup
    ~= theoretical speedup) is SELF-SEALING: a function of the mechanism being
    ON, not of the referent being CORRECT. N/A when the spec does not declare a
    referent (orthogonal to the other four axes)."""
    ref = spec.get("referent")
    if ref is None:
        return True, "", "N/A (referent not declared)"
    wo = spec.get("witness_observes")
    if wo is None:
        return True, "", "N/A (no witness declared)"
    def norm(s): return " ".join(str(s).lower().split())
    refn = norm(ref)
    for w in wo:
        if norm(w) == refn:
            return True, "", "witness observes the referent directly (%r)" % ref
    return False, "CONSEQUENCE-WITNESSED", \
        "the witness observes only consequences (%s), never the referent %r; the success signal is self-sealing (a function of the mechanism being on, not the referent being correct)" % (", ".join(str(w) for w in wo), ref)

def _canon_record(rec):
    """Canonicalize a record value to a hashable form for grouping. Lists and
    tuples become tuples; everything else is used as-is."""
    if isinstance(rec, (list, tuple)):
        return tuple(rec)
    return rec

def check_lossy_projection(spec):
    """LOSSY-PROJECTION (6th primary axis, MANY-TO-ONE / lossy-projection):
    the reported value must be a function of the referent alone. The axis
    fires when the record the metric is computed from is a lossy projection of
    the referent -- i.e., two rows share the same `record` but declare
    different `referent_value`. That is the many-to-one witness: the referent
    is non-identifiable from the record, so the reported value (a function of
    the record) cannot discriminate between referent values that share a
    record. Orthogonal to NOT-SELF-KEYED (one-to-many coupling): here the
    referent is fixed and the record is lossy, not the knob varying the
    reading. VACUOUS-RATIO (support 0) is the zero-support degenerate
    sub-case of this failure; this axis is the general non-vacuous case.
    N/A when fewer than two rows declare both `record` and `referent_value`.
    fail -> LOSSY-PROJECTION."""
    rows = [r for r in spec["rows"]
            if r.get("record") is not None and r.get("referent_value") is not None]
    if len(rows) < 2:
        return True, "", "N/A (no record/referent witness declared)"
    by_record = {}
    for r in rows:
        by_record.setdefault(_canon_record(r["record"]), []).append(r["referent_value"])
    for rec, refs in by_record.items():
        distinct = sorted(set(refs), key=lambda x: (isinstance(x, str), x))
        if len(distinct) > 1:
            detail = ("record %r maps to %d distinct referent values (%s): the referent is non-identifiable from the record, so the reported value cannot discriminate between referent values that share a record (many-to-one lossy projection)" % (rec, len(distinct), ", ".join(str(x) for x in distinct)))
            return False, "LOSSY-PROJECTION", detail
    return True, "", "record is injective in the referent (%d records, each maps to a single referent value); the referent is identifiable from the record" % len(by_record)

def check_aggregation_reversal(spec):
    """AGGREGATION-REVERSAL (8th primary axis, Simpson's-paradox / confounding):
    the within-subgroup direction must not be reversed by the pooling weights.
    Fires when every subgroup that has both a mechanism and a null reading agrees
    on the within-subgroup direction (all mechanism-wins, or all null-wins) AND
    the n-weighted pooled direction is the opposite. The per-row metrics are the
    same ones BEATS-NULL reads; the axis adds the subgroup/n structure that
    BEATS-NULL (which compares the max per-row metric) cannot see. N/A when
    fewer than two subgroups declare both a mechanism and a null reading (no
    pooling structure to reverse). fail -> AGGREGATION-REVERSAL."""
    by = {}
    for r in spec["rows"]:
        if r.get("subgroup") is None or r.get("n") is None:
            continue
        by.setdefault(r["subgroup"], {})[r["mechanism_on"]] = (r["metric"], r["n"])
    both = {k: v for k, v in by.items() if True in v and False in v}
    if len(both) < 2:
        return True, "", "N/A (no subgroup/pooling structure declared; need >=2 subgroups with both a mechanism and a null reading)"
    mech_wins = [k for k, v in both.items() if v[True][0] > v[False][0]]
    null_wins = [k for k, v in both.items() if v[False][0] > v[True][0]]
    if len(mech_wins) + len(null_wins) != len(both):
        return True, "", "N/A (a subgroup has equal mechanism and null metrics; no consistent within-subgroup direction)"
    if not (len(mech_wins) == len(both) or len(null_wins) == len(both)):
        return True, "", "within-subgroup direction is mixed (%d mechanism-wins, %d null-wins); no single within-subgroup direction to reverse" % (len(mech_wins), len(null_wins))
    within_mech_wins = (len(mech_wins) == len(both))
    pm = sum(v[True][0]*v[True][1] for v in both.values()); n_pm = sum(v[True][1] for v in both.values())
    pn = sum(v[False][0]*v[False][1] for v in both.values()); n_pn = sum(v[False][1] for v in both.values())
    pm, pn = pm/n_pm, pn/n_pn
    if within_mech_wins == (pm > pn):
        return True, "", "pooled direction agrees with the within-subgroup direction (pooled mechanism %g vs pooled null %g); no reversal" % (pm, pn)
    return False, "AGGREGATION-REVERSAL", ("every subgroup agrees that the %s wins, but the n-weighted pooled comparison reverses it (pooled mechanism %g vs pooled null %g): the aggregate claim is an artifact of the pooling weights, not the mechanism (Simpson's paradox)" % ("mechanism" if within_mech_wins else "null", pm, pn))

def check_referent_constructed(spec):
    """REFERENT-CONSTRUCTED (9th primary axis, referent-provenance / self-sealing
    tautology): the referent the claim is ABOUT must not itself be a model-
    constructed artifact. When the referent is a model's own output (e.g.
    root-cause groups assigned by claude-opus-4-7) and the claim is measured
    against it, the claim is a self-sealing tautology: the model is graded
    against its own output, so a perfect reading says nothing about the true
    structure. Distinct from CONSEQUENCE-WITNESSED (the referent is external
    but the witness observes only a model-constructed proxy of it) and from
    witness-strength (conceded vs measured): this axis is about WHAT the claim
    is about, not HOW it is observed. N/A when `referent_provenance` is not
    declared (schema-boundary) or the referent is not declared.
    fail -> REFERENT-CONSTRUCTED."""
    if spec.get("referent") is None:
        return True, "", "N/A (referent not declared)"
    prov = spec.get("referent_provenance")
    if prov is None:
        return True, "", "N/A (referent_provenance not declared; the axis does not apply)"
    if str(prov).lower() == "model-constructed":
        return False, "REFERENT-CONSTRUCTED", \
            "the referent %r is a model-constructed artifact (%s): the claim is measured against the model's own output, so a perfect reading is a self-sealing tautology that says nothing about the true structure" % (spec.get("referent"), prov)
    return True, "", "referent provenance is %s (not model-constructed); the claim is not graded against the model's own output" % prov

def check_dose_response(spec):
    """DOSE-RESPONSE (refinement of BEATS-NULL, dose-blindness / cross-dose pooling):
    the flat BEATS-NULL comparison pools max(mechanism) vs max(null) ACROSS the
    dose/severity variable, so it fires NULL-REACHES-HEADLINE on a TRUE
    dose-response (mechanism advantage grows with severity; on-par at the
    mild end) exactly as on a FALSE flat claim. The axis reads the within-dose
    direction that BEATS-NULL (which compares the cross-dose max) cannot see.
    Fires when every substrate (dose) level that has both a mechanism and a
    null reading is mechanism-favorable (mech >= null at every dose) AND the
    cross-dose max comparison fires NULL-REACHES-HEADLINE (max-null >=
    max-mech). In that case the flat check is a false positive: the claim is a
    true dose-response, not a failed flat claim. N/A when fewer than two
    substrate levels declare both a mechanism and a null reading (no dose
    structure), or when the within-dose direction is not uniformly
    mechanism-favorable (the flat check governs). fail -> DOSE-RESPONSE."""
    by = {}
    for r in spec["rows"]:
        key = tuple(r.get("substrate", []))
        by.setdefault(key, {})[bool(r.get("mechanism_on"))] = r["metric"]
    both = {k: v for k, v in by.items() if True in v and False in v}
    if len(both) < 2:
        return True, "", "N/A (no dose structure declared; need >=2 substrate levels with both a mechanism and a null reading)"
    mech_favorable = all(v[True] >= v[False] for v in both.values())
    if not mech_favorable:
        return True, "", "N/A (within-dose direction not uniformly mechanism-favorable; the flat check governs)"
    on  = [r["metric"] for r in spec["rows"] if r.get("mechanism_on")]
    nul = [r["metric"] for r in spec["rows"] if (not r.get("mechanism_on")) or r.get("is_null")]
    if not on or not nul:
        return True, "", "N/A (no null rows)"
    h, n = max(on), max(nul)
    if h > n:
        return True, "", "N/A (cross-dose max-mech > max-null; BEATS-NULL does not fire)"
    return False, "DOSE-RESPONSE", ("the claim is a true dose-response: the mechanism is >= the null at every dose (within-dose), but the cross-dose max pools the mild-dose null (%g) against the severe-dose mechanism (%g), firing NULL-REACHES-HEADLINE as a false positive; the flat check is the wrong instrument for a dose-response" % (n, h))


CLAIM_TO_ROW = {
    "onset":           "timepoint",
    "claim_outcome":   "outcome",
    "claim_subgroup":  "subgroup",
    "claim_tier":      "tier",
    "claim_split":     "split",
    "claim_metric":    "metric_name",
    "claim_dose":      "substrate",
}


def _norm_scope(v, dim):
    if v is None:
        return None
    if dim == "substrate":
        return tuple(v)
    return v


def _joint_claim_cell(spec):
    """The at-claim value read as the JOINT cell of all declared claim_* scope
    fields (order-independent). Returns (mech, null, ambiguous). mech/null are
    None when the joint cell has no such reading; ambiguous is True when the
    joint cell holds multiple distinct mech or null values (the orthogonal
    scope dimension varies within the claim cell, so the single-dimension
    marginal read is order-dependent and the at-claim value is under-specified).
    This is the fix for the row-order dependence of the scoped onset/spike
    checks: the marginal by[key][mech]=metric (last-wins) read flips with row
    order when the orthogonal dimension varies; the joint read does not."""
    sel = []
    for r in spec["rows"]:
        ok = True
        for cf, rf in CLAIM_TO_ROW.items():
            cv = spec.get(cf)
            if cv is None:
                continue
            rv = _norm_scope(r.get(rf), rf)
            cvn = _norm_scope(cv, rf)
            if rv != cvn:
                ok = False
                break
        if ok:
            sel.append(r)
    m = [r["metric"] for r in sel if r.get("mechanism_on")]
    n = [r["metric"] for r in sel if (not r.get("mechanism_on")) or r.get("is_null")]
    amb = (len(set(m)) > 1) or (len(set(n)) > 1)
    return (m[0] if m else None), (n[0] if n else None), amb


def check_temporal_onset(spec):
    """TEMPORAL-ONSET (refinement of BEATS-NULL): the flat check pools
    max-mech vs max-null ACROSS ALL rows, so for a temporal claim it reads
    the PEAK, not the value at the claim's onset timepoint. If the claim
    declares an onset timepoint and the at-onset mechanism is <= the at-onset
    null (no immediate effect) but the peak mechanism > the peak null (a real
    peak), the flat check is silent on a FALSE 'immediate' claim -> TIME-BLIND.
    This is the pass-cell false-negative mirror of DOSE-RESPONSE (which fires
    in the fail cell). N/A when no onset timepoint is declared (schema-
    boundary: undeclared -> the flat check governs), or when the at-onset
    value supports the claim, or when BEATS-NULL already fires (the fail
    cell; DOSE-RESPONSE governs). fail -> TEMPORAL-ONSET."""
    onset = spec.get("onset")
    if onset is None:
        return True, "", "N/A (no onset timepoint declared; the flat check governs)"
    m_onset, n_onset, amb = _joint_claim_cell(spec)
    if m_onset is None or n_onset is None:
        return True, "", "N/A (no mechanism/null reading at the claim scope cell)"
    if amb:
        return True, "", "N/A (the at-claim value is under-specified: the orthogonal scope dimension varies within the claim cell, so the marginal read is order-dependent)"
    on  = [r["metric"] for r in spec["rows"] if r.get("mechanism_on")]
    nul = [r["metric"] for r in spec["rows"] if (not r.get("mechanism_on")) or r.get("is_null")]
    if not on or not nul:
        return True, "", "N/A (no null rows)"
    h, n = max(on), max(nul)
    if h <= n:
        return True, "", "N/A (BEATS-NULL already fires; the fail cell; DOSE-RESPONSE governs)"
    if m_onset > n_onset:
        return True, "", "N/A (the at-onset value supports the claim; the flat check is correct)"
    return False, "TEMPORAL-ONSET", ("the flat check pools the cross-time max (mechanism %g > null %g), but at the claim's onset timepoint the mechanism is %g vs null %g (no immediate effect); the peak is real but the 'immediate' claim is false; the flat check is the wrong instrument for a temporal claim" % (h, n, m_onset, n_onset))


def check_temporal_spike(spec):
    """TEMPORAL-SPIKE (refinement of BEATS-NULL): the fail-cell mirror of
    TEMPORAL-ONSET. The flat check pools max(mechanism) vs max(null) ACROSS all
    timepoints, so a LATER null spike (at a timepoint other than the claim's
    onset) can dominate the cross-time max and make BEATS-NULL fire
    NULL-REACHES-HEADLINE on a TRUE 'immediate effect' claim (mech > null at the
    onset timepoint). DOSE-RESPONSE does not catch it: it reads the substrate
    (dose) variable, not the timepoint, and the null spike breaks the uniform
    mechanism-favorability it requires. Fires when BEATS-NULL already fires (the
    fail cell) AND the at-onset value supports the claim (mech > null at the
    onset) AND the max-null is at a non-onset timepoint (the spike is after the
    onset). N/A when the onset is undeclared, when there is no mechanism/null
    reading at the onset, when BEATS-NULL does not fire (the pass cell;
    TEMPORAL-ONSET governs), or when the at-onset value does not support the
    claim (a genuine fail, not a spike). fail -> TEMPORAL-SPIKE."""
    onset = spec.get("onset")
    if onset is None:
        return True, "", "N/A (no onset timepoint declared; the flat check governs)"
    m_onset, n_onset, amb = _joint_claim_cell(spec)
    if m_onset is None or n_onset is None:
        return True, "", "N/A (no mechanism/null reading at the claim scope cell)"
    if amb:
        return True, "", "N/A (the at-claim value is under-specified: the orthogonal scope dimension varies within the claim cell, so the marginal read is order-dependent)"
    on  = [r["metric"] for r in spec["rows"] if r.get("mechanism_on")]
    nul = [r["metric"] for r in spec["rows"] if (not r.get("mechanism_on")) or r.get("is_null")]
    if not on or not nul:
        return True, "", "N/A (no null rows)"
    h, n = max(on), max(nul)
    if h > n:
        return True, "", "N/A (BEATS-NULL does not fire; the pass cell; TEMPORAL-ONSET governs)"
    if m_onset <= n_onset:
        return True, "", "N/A (the at-onset value does not support the claim; a genuine fail, not a spike)"
    spike_tp = None
    for r in spec["rows"]:
        if r.get("timepoint") is None:
            continue
        if (not r.get("mechanism_on")) or r.get("is_null"):
            if r["metric"] == n and r["timepoint"] != onset:
                spike_tp = r["timepoint"]
    if spike_tp is None:
        return True, "", "N/A (the max-null is at the onset, not a non-onset spike)"
    return False, "TEMPORAL-SPIKE", ("the flat check pools the cross-time max (mechanism %g vs null %g), but at the claim's onset timepoint the mechanism is %g > null %g (a real immediate effect); the null spike at %s (%g) dominates the cross-time max and fires NULL-REACHES-HEADLINE as a false positive; the flat check is the wrong instrument for a temporal claim" % (h, n, m_onset, n_onset, spike_tp, n))


def check_computable(spec):
    """COMPUTABLE (flag NOT-COMPUTABLE): each metric the paper names as its
    evaluation plan must be computable from a specified artifact (a schema,
    denominator, label set, or comparison function). Operates in the
    no-data regime: N/A for empirical claims (where BEATS-NULL etc. govern)
    and when no named_metrics are declared. Distinct from VACUOUS-RATIO,
    which is about a reported ratio's support, not about whether a metric
    is specified."""
    if not _no_empirical(spec):
        return True, "", "N/A (empirical claim: the empirical axes govern; metric computability is not the regime)"
    named = spec.get("named_metrics")
    if not named:
        return True, "", "N/A (no named evaluation metrics declared)"
    op = set(spec.get("operationalized", []))
    missing = [m for m in named if m not in op]
    if not missing:
        return True, "", "all %d named metrics operationalized (computable from specified artifacts)" % len(named)
    return False, "NOT-COMPUTABLE", "%d of %d named metrics not computable from the specified artifacts: %s" % (
        len(missing), len(named), "; ".join(missing))

def check_wider_than_named(spec):
    """WIDER-THAN-NAMED (35th axis, 2026-09-25): the named referent of a
    definitional/classificatory claim (a statute, a model card, a standard)
    must match the load-bearing referent that actually does the
    classification. The axis fires when the load-bearing referent is WIDER
    than the named/measurable number: a statutory DISJUNCTION of unmeasurable
    horns, a COUNTERFACTUAL-CAPACITY claim, or a RELATIVE/MOVING-TARGET
    referent -- in which case the one measurable number (10^25 ops, 10,000
    users) is demoted to a bright-line screen, rebuttable presumption, or
    proxy, not the classification. Operates in the no-empirical regime (like
    COMPUTABLE): N/A for empirical claims (where the empirical axes govern).
    N/A when `referent_structure` is not declared (schema-boundary). Pass when
    `referent_structure == "absolute"` (the named referent IS the measurable
    number; no wider-than-named gap). fail -> WIDER-THAN-NAMED."""
    if not _no_empirical(spec):
        return True, "", "N/A (empirical claim: the empirical axes govern; the definitional-referent axis is not the regime)"
    structure = spec.get("referent_structure")
    if structure is None:
        return True, "", "N/A (referent_structure not declared; the axis does not apply)"
    if structure == "absolute":
        return True, "", "N/A (the named referent IS the measurable number (absolute threshold); no wider-than-named gap)"
    wide = ("disjunction", "counterfactual-capacity", "relative-moving-target")
    if structure not in wide:
        return True, "", "N/A (referent_structure=%s is not a recognized wider-than-named structure; the axis does not apply)" % structure
    role = spec.get("number_role")
    role_note = ""
    if role:
        role_note = "; the measurable number is demoted to a %s, not the classification" % role
    detail = ("the named referent is wider than the named/measurable number: the load-bearing referent is a %s (unmeasurable in absolute terms)%s" % (structure, role_note))
    return False, "WIDER-THAN-NAMED", detail

def check_outcome_onset(spec):
    """OUTCOME-ONSET (refinement of BEATS-NULL): the flat check pools
    max-mech vs max-null ACROSS ALL outcomes, so for a multi-outcome claim it
    reads the PEAK outcome, not the claim outcome. If the claim declares a
    claim_outcome and the at-claim-outcome mechanism is <= the at-claim-outcome
    null (no beat on the claimed outcome) but the peak mechanism > the peak
    null (a real peak at a non-claim outcome), the flat check is silent on a
    FALSE claim -> OUTCOME-BLIND. This is the pass-cell false-negative mirror
    of DOSE-RESPONSE (which fires in the fail cell), and the outcome-dimension
    mirror of TEMPORAL-ONSET. N/A when no claim_outcome is declared (schema-
    boundary: undeclared -> the flat check governs), or when the at-claim-
    outcome value supports the claim, or when BEATS-NULL already fires (the
    fail cell; OUTCOME-SPIKE governs). fail -> OUTCOME-ONSET."""
    co = spec.get("claim_outcome")
    if co is None:
        return True, "", "N/A (no claim_outcome declared; the flat check governs)"
    m_co, n_co, amb = _joint_claim_cell(spec)
    if m_co is None or n_co is None:
        return True, "", "N/A (no mechanism/null reading at the claim scope cell)"
    if amb:
        return True, "", "N/A (the at-claim value is under-specified: the orthogonal scope dimension varies within the claim cell, so the marginal read is order-dependent)"
    on  = [r["metric"] for r in spec["rows"] if r.get("mechanism_on")]
    nul = [r["metric"] for r in spec["rows"] if (not r.get("mechanism_on")) or r.get("is_null")]
    if not on or not nul:
        return True, "", "N/A (no null rows)"
    h, n = max(on), max(nul)
    if h <= n:
        return True, "", "N/A (BEATS-NULL already fires; the fail cell; OUTCOME-SPIKE governs)"
    if m_co > n_co:
        return True, "", "N/A (the at-claim-outcome value supports the claim; the flat check is correct)"
    return False, "OUTCOME-ONSET", ("the flat check pools the cross-outcome max (mechanism %g > null %g), but at the claim outcome the mechanism is %g vs null %g (no beat); the peak is at a non-claim outcome; the flat check is the wrong instrument for a multi-outcome claim" % (h, n, m_co, n_co))

def check_outcome_spike(spec):
    """OUTCOME-SPIKE (refinement of BEATS-NULL): the fail-cell mirror of
    OUTCOME-ONSET. The flat check pools max(mechanism) vs max(null) ACROSS all
    outcomes, so a non-claim-outcome null spike can dominate the cross-outcome
    max and make BEATS-NULL fire NULL-REACHES-HEADLINE on a TRUE claim (mech >
    null at the claim outcome). OUTCOME-ONSET defers to the fail cell, and
    DOSE-RESPONSE reads the substrate (not the outcome), so neither catches it.
    Fires when BEATS-NULL fires AND the at-claim-outcome value supports the
    claim (mech > null at the claim outcome) AND the max-null is at a non-claim
    outcome (the spike is outside the claim). The outcome dimension is the
    second two-ended hidden variable (after time: TEMPORAL-ONSET pass-cell,
    TEMPORAL-SPIKE fail-cell) and needs a NEW spec-schema field (claim_outcome
    + row outcome) to test. N/A when no claim_outcome is declared (schema-
    boundary), on a genuine fail (the at-claim-outcome value does not support
    the claim), and when the max-null is at the claim outcome. fail ->
    OUTCOME-SPIKE."""
    co = spec.get("claim_outcome")
    if co is None:
        return True, "", "N/A (no claim_outcome declared; the flat check governs)"
    m_co, n_co, amb = _joint_claim_cell(spec)
    if m_co is None or n_co is None:
        return True, "", "N/A (no mechanism/null reading at the claim scope cell)"
    if amb:
        return True, "", "N/A (the at-claim value is under-specified: the orthogonal scope dimension varies within the claim cell, so the marginal read is order-dependent)"
    on  = [r["metric"] for r in spec["rows"] if r.get("mechanism_on")]
    nul = [r["metric"] for r in spec["rows"] if (not r.get("mechanism_on")) or r.get("is_null")]
    if not on or not nul:
        return True, "", "N/A (no null rows)"
    h, n = max(on), max(nul)
    if h > n:
        return True, "", "N/A (BEATS-NULL does not fire; the pass cell; OUTCOME-ONSET governs)"
    if m_co <= n_co:
        return True, "", "N/A (the at-claim-outcome value does not support the claim; a genuine fail, not a spike)"
    spike_out = None
    for r in spec["rows"]:
        if r.get("outcome") is None:
            continue
        if (not r.get("mechanism_on")) or r.get("is_null"):
            if r["metric"] == n and r["outcome"] != co:
                spike_out = r["outcome"]
    if spike_out is None:
        return True, "", "N/A (the max-null is at the claim outcome, not a non-claim spike)"
    return False, "OUTCOME-SPIKE", ("the flat check pools the cross-outcome max (mechanism %g vs null %g), but at the claim outcome the mechanism is %g > null %g (a real beat); the null spike at %s (%g) dominates the cross-outcome max and fires NULL-REACHES-HEADLINE as a false positive; the flat check is the wrong instrument for a multi-outcome claim" % (h, n, m_co, n_co, spike_out, n))

def check_subgroup_onset(spec):
    """SUBGROUP-ONSET (refinement of BEATS-NULL): the flat check pools
    max-mech vs max-null ACROSS ALL subgroups, so for a subgroup-scoped claim
    it reads the PEAK subgroup, not the claim subgroup. If the claim declares
    a claim_subgroup and the at-claim-subgroup mechanism is <= the at-claim-
    subgroup null (no beat in the claimed subgroup) but the peak mechanism >
    the peak null (a real peak in a non-claim subgroup), the flat check is
    silent on a FALSE claim -> SUBGROUP-BLIND. This is the pass-cell
    false-negative mirror of DOSE-RESPONSE and the subgroup-dimension mirror
    of TEMPORAL-ONSET / OUTCOME-ONSET. N/A when no claim_subgroup is declared
    (schema-boundary: undeclared -> the flat check governs), when the
    at-claim-subgroup value supports the claim, or when BEATS-NULL already
    fires (the fail cell). fail -> SUBGROUP-ONSET."""
    cs = spec.get("claim_subgroup")
    if cs is None:
        return True, "", "N/A (no claim_subgroup declared; the flat check governs)"
    m_cs, n_cs, amb = _joint_claim_cell(spec)
    if m_cs is None or n_cs is None:
        return True, "", "N/A (no mechanism/null reading at the claim scope cell)"
    if amb:
        return True, "", "N/A (the at-claim value is under-specified: the orthogonal scope dimension varies within the claim cell, so the marginal read is order-dependent)"
    on  = [r["metric"] for r in spec["rows"] if r.get("mechanism_on")]
    nul = [r["metric"] for r in spec["rows"] if (not r.get("mechanism_on")) or r.get("is_null")]
    if not on or not nul:
        return True, "", "N/A (no null rows)"
    h, n = max(on), max(nul)
    if h <= n:
        return True, "", "N/A (BEATS-NULL already fires; the fail cell; SUBGROUP-SPIKE governs)"
    if m_cs > n_cs:
        return True, "", "N/A (the at-claim-subgroup value supports the claim; the flat check is correct)"
    return False, "SUBGROUP-ONSET", ("the flat check pools the cross-subgroup max (mechanism %g > null %g), but at the claim subgroup the mechanism is %g vs null %g (no beat); the peak is at a non-claim subgroup; the flat check is the wrong instrument for a subgroup-scoped claim" % (h, n, m_cs, n_cs))

def check_subgroup_spike(spec):
    """SUBGROUP-SPIKE (refinement of BEATS-NULL): the fail-cell mirror of
    SUBGROUP-ONSET. The flat check pools max(mechanism) vs max(null) ACROSS all
    subgroups, so a non-claim-subgroup null spike can dominate the cross-
    subgroup max and make BEATS-NULL fire NULL-REACHES-HEADLINE on a TRUE
    claim (mech > null at the claim subgroup). SUBGROUP-ONSET defers to the
    fail cell, and AGGREGATION-REVERSAL reads the within-subgroup DIRECTION
    (not the scoped beat), so neither catches it. Fires when BEATS-NULL fires
    AND the at-claim-subgroup value supports the claim (mech > null at the
    claim subgroup) AND the max-null is at a non-claim subgroup (the spike is
    outside the claim). The subgroup dimension is the third two-ended hidden
    variable (after time and outcome) and needs a NEW spec-schema field
    (claim_subgroup + row subgroup) to test. N/A when no claim_subgroup is
    declared (schema-boundary), on a genuine fail (the at-claim-subgroup value
    does not support the claim), and when the max-null is at the claim
    subgroup. fail -> SUBGROUP-SPIKE."""
    cs = spec.get("claim_subgroup")
    if cs is None:
        return True, "", "N/A (no claim_subgroup declared; the flat check governs)"
    m_cs, n_cs, amb = _joint_claim_cell(spec)
    if m_cs is None or n_cs is None:
        return True, "", "N/A (no mechanism/null reading at the claim scope cell)"
    if amb:
        return True, "", "N/A (the at-claim value is under-specified: the orthogonal scope dimension varies within the claim cell, so the marginal read is order-dependent)"
    on  = [r["metric"] for r in spec["rows"] if r.get("mechanism_on")]
    nul = [r["metric"] for r in spec["rows"] if (not r.get("mechanism_on")) or r.get("is_null")]
    if not on or not nul:
        return True, "", "N/A (no null rows)"
    h, n = max(on), max(nul)
    if h > n:
        return True, "", "N/A (BEATS-NULL does not fire; the pass cell; SUBGROUP-ONSET governs)"
    if m_cs <= n_cs:
        return True, "", "N/A (the at-claim-subgroup value does not support the claim; a genuine fail, not a spike)"
    spike_sg = None
    for r in spec["rows"]:
        if r.get("subgroup") is None:
            continue
        if (not r.get("mechanism_on")) or r.get("is_null"):
            if r["metric"] == n and r["subgroup"] != cs:
                spike_sg = r["subgroup"]
    if spike_sg is None:
        return True, "", "N/A (the max-null is at the claim subgroup, not a non-claim spike)"
    return False, "SUBGROUP-SPIKE", ("the flat check pools the cross-subgroup max (mechanism %g vs null %g), but at the claim subgroup the mechanism is %g > null %g (a real beat); the null spike at %s (%g) dominates the cross-subgroup max and fires NULL-REACHES-HEADLINE as a false positive; the flat check is the wrong instrument for a subgroup-scoped claim" % (h, n, m_cs, n_cs, spike_sg, n))


def check_dose_onset(spec):
    """DOSE-ONSET (refinement of BEATS-NULL): the flat check pools
    max-mech vs max-null ACROSS ALL doses, so for a dose-scoped claim
    it reads the PEAK dose, not the claim dose. If the claim declares
    a claim_dose and the at-claim-dose mechanism is <= the at-claim-dose
    null (no beat in the claimed dose) but the peak mechanism > the peak
    null (a real peak in a non-claim dose), the flat check is silent on a
    FALSE claim -> DOSE-BLIND. This is the pass-cell false-negative mirror
    of DOSE-RESPONSE and the dose-dimension mirror of TEMPORAL-ONSET /
    OUTCOME-ONSET / SUBGROUP-ONSET. Distinct from DOSE-RESPONSE (which reads
    the within-dose DIRECTION and needs no claim_dose): DOSE-ONSET reads the
    at-claim-dose VALUE and needs the NEW spec-schema field claim_dose.
    N/A when no claim_dose is declared (schema-boundary: undeclared -> the
    flat check governs), when the at-claim-dose value supports the claim,
    or when BEATS-NULL already fires (the fail cell). fail -> DOSE-ONSET."""
    cd = spec.get("claim_dose")
    if cd is None:
        return True, "", "N/A (no claim_dose declared; the flat check governs)"
    cd_key = tuple(cd)
    m_cd, n_cd, amb = _joint_claim_cell(spec)
    if m_cd is None or n_cd is None:
        return True, "", "N/A (no mechanism/null reading at the claim scope cell)"
    if amb:
        return True, "", "N/A (the at-claim value is under-specified: the orthogonal scope dimension varies within the claim cell, so the marginal read is order-dependent)"
    on  = [r["metric"] for r in spec["rows"] if r.get("mechanism_on")]
    nul = [r["metric"] for r in spec["rows"] if (not r.get("mechanism_on")) or r.get("is_null")]
    if not on or not nul:
        return True, "", "N/A (no null rows)"
    h, n = max(on), max(nul)
    if h <= n:
        return True, "", "N/A (BEATS-NULL already fires; the fail cell; DOSE-SPIKE governs)"
    if m_cd > n_cd:
        return True, "", "N/A (the at-claim-dose value supports the claim; the flat check is correct)"
    return False, "DOSE-ONSET", ("the flat check pools the cross-dose max (mechanism %g > null %g), but at the claim dose the mechanism is %g vs null %g (no beat in the claimed dose); the peak is real but the claim-dose effect is false; the flat check is the wrong instrument for a dose-scoped claim" % (h, n, m_cd, n_cd))

def check_dose_spike(spec):
    """DOSE-SPIKE (refinement of BEATS-NULL): the fail-cell mirror of
    DOSE-ONSET. The flat check pools max(mechanism) vs max(null) ACROSS all
    doses, so a non-claim-dose null spike can dominate the cross-dose max
    and make BEATS-NULL fire NULL-REACHES-HEADLINE on a TRUE claim (mech >
    null at the claim dose). DOSE-ONSET defers to the fail cell, and
    DOSE-RESPONSE reads the within-dose DIRECTION (not the scoped beat), so
    neither catches it. Fires when BEATS-NULL fires AND the at-claim-dose
    value supports the claim (mech > null at the claim dose) AND the
    max-null is at a non-claim dose (the spike is outside the claim). The
    dose dimension is the fourth two-ended hidden variable (after time,
    outcome, and subgroup) and needs a NEW spec-schema field (claim_dose +
    row substrate) to test. N/A when no claim_dose is declared
    (schema-boundary), on a genuine fail (the at-claim-dose value does not
    support the claim), and when the max-null is at the claim dose.
    fail -> DOSE-SPIKE."""
    cd = spec.get("claim_dose")
    if cd is None:
        return True, "", "N/A (no claim_dose declared; the flat check governs)"
    cd_key = tuple(cd)
    m_cd, n_cd, amb = _joint_claim_cell(spec)
    if m_cd is None or n_cd is None:
        return True, "", "N/A (no mechanism/null reading at the claim scope cell)"
    if amb:
        return True, "", "N/A (the at-claim value is under-specified: the orthogonal scope dimension varies within the claim cell, so the marginal read is order-dependent)"
    on  = [r["metric"] for r in spec["rows"] if r.get("mechanism_on")]
    nul = [r["metric"] for r in spec["rows"] if (not r.get("mechanism_on")) or r.get("is_null")]
    if not on or not nul:
        return True, "", "N/A (no null rows)"
    h, n = max(on), max(nul)
    if h > n:
        return True, "", "N/A (BEATS-NULL does not fire; the pass cell; DOSE-ONSET governs)"
    if m_cd <= n_cd:
        return True, "", "N/A (the at-claim-dose value does not support the claim; a genuine fail, not a spike)"
    spike_dose = None
    for r in spec["rows"]:
        if r.get("substrate") is None:
            continue
        if (not r.get("mechanism_on")) or r.get("is_null"):
            if r["metric"] == n and tuple(r["substrate"]) != cd_key:
                spike_dose = r["substrate"]
    if spike_dose is None:
        return True, "", "N/A (the max-null is at the claim dose, not a non-claim spike)"
    return False, "DOSE-SPIKE", ("the flat check pools the cross-dose max (mechanism %g vs null %g), but at the claim dose the mechanism is %g > null %g (a real beat); the null spike at %s (%g) dominates the cross-dose max and fires NULL-REACHES-HEADLINE as a false positive; the flat check is the wrong instrument for a dose-scoped claim" % (h, n, m_cd, n_cd, "/".join(spike_dose), n))


def check_tier_onset(spec):
    """TIER-ONSET (refinement of BEATS-NULL): the flat check pools
    max-mech vs max-null ACROSS ALL difficulty tiers, so for a tier-scoped
    claim it reads the PEAK tier, not the claim tier. If the claim declares
    a claim_tier and the at-claim-tier mechanism is <= the at-claim-tier null
    (no beat in the claimed tier) but the peak mechanism > the peak null (a
    real peak in a non-claim tier), the flat check is silent on a FALSE claim
    -> TIER-BLIND. This is the tier-dimension mirror of SUBGROUP-ONSET /
    DOSE-ONSET. The difficulty tier is the fourth two-ended hidden variable
    (after time, outcome, subgroup) and needs a NEW spec-schema field
    (claim_tier + row tier) to test. N/A when no claim_tier is declared
    (schema-boundary: undeclared -> the flat check governs), when the
    at-claim-tier value supports the claim, or when BEATS-NULL already fires
    (the fail cell). fail -> TIER-ONSET."""
    ct = spec.get("claim_tier")
    if ct is None:
        return True, "", "N/A (no claim_tier declared; the flat check governs)"
    m_ct, n_ct, amb = _joint_claim_cell(spec)
    if m_ct is None or n_ct is None:
        return True, "", "N/A (no mechanism/null reading at the claim scope cell)"
    if amb:
        return True, "", "N/A (the at-claim value is under-specified: the orthogonal scope dimension varies within the claim cell, so the marginal read is order-dependent)"
    on  = [r["metric"] for r in spec["rows"] if r.get("mechanism_on")]
    nul = [r["metric"] for r in spec["rows"] if (not r.get("mechanism_on")) or r.get("is_null")]
    if not on or not nul:
        return True, "", "N/A (no null rows)"
    h, n = max(on), max(nul)
    if h <= n:
        return True, "", "N/A (BEATS-NULL already fires; the fail cell; TIER-SPIKE governs)"
    if m_ct > n_ct:
        return True, "", "N/A (the at-claim-tier value supports the claim; the flat check is correct)"
    return False, "TIER-ONSET", ("the flat check pools the cross-tier max (mechanism %g > null %g), but at the claim tier the mechanism is %g vs null %g (no beat); the peak is at a non-claim tier; the flat check is the wrong instrument for a tier-scoped claim" % (h, n, m_ct, n_ct))


def check_tier_spike(spec):
    """TIER-SPIKE (refinement of BEATS-NULL): the fail-cell mirror of
    TIER-ONSET. The flat check pools max(mechanism) vs max(null) ACROSS all
    difficulty tiers, so a non-claim-tier null spike can dominate the cross-
    tier max and make BEATS-NULL fire NULL-REACHES-HEADLINE on a TRUE claim
    (mech > null at the claim tier). TIER-ONSET defers to the fail cell, and
    AGGREGATION-REVERSAL reads the within-tier DIRECTION (not the scoped
    beat), so neither catches it. Fires when BEATS-NULL fires AND the
    at-claim-tier value supports the claim (mech > null at the claim tier)
    AND the max-null is at a non-claim tier (the spike is outside the claim).
    The difficulty tier is the fourth two-ended hidden variable (after time,
    outcome, subgroup) and needs a NEW spec-schema field (claim_tier + row
    tier) to test. N/A when no claim_tier is declared (schema-boundary), on a
    genuine fail (the at-claim-tier value does not support the claim), and
    when the max-null is at the claim tier. fail -> TIER-SPIKE."""
    ct = spec.get("claim_tier")
    if ct is None:
        return True, "", "N/A (no claim_tier declared; the flat check governs)"
    m_ct, n_ct, amb = _joint_claim_cell(spec)
    if m_ct is None or n_ct is None:
        return True, "", "N/A (no mechanism/null reading at the claim scope cell)"
    if amb:
        return True, "", "N/A (the at-claim value is under-specified: the orthogonal scope dimension varies within the claim cell, so the marginal read is order-dependent)"
    on  = [r["metric"] for r in spec["rows"] if r.get("mechanism_on")]
    nul = [r["metric"] for r in spec["rows"] if (not r.get("mechanism_on")) or r.get("is_null")]
    if not on or not nul:
        return True, "", "N/A (no null rows)"
    h, n = max(on), max(nul)
    if h > n:
        return True, "", "N/A (BEATS-NULL does not fire; the pass cell; TIER-ONSET governs)"
    if m_ct <= n_ct:
        return True, "", "N/A (the at-claim-tier value does not support the claim; a genuine fail, not a spike)"
    spike_tier = None
    for r in spec["rows"]:
        if r.get("tier") is None:
            continue
        if (not r.get("mechanism_on")) or r.get("is_null"):
            if r["metric"] == n and r["tier"] != ct:
                spike_tier = r["tier"]
    if spike_tier is None:
        return True, "", "N/A (the max-null is at the claim tier, not a non-claim spike)"
    return False, "TIER-SPIKE", ("the flat check pools the cross-tier max (mechanism %g vs null %g), but at the claim tier the mechanism is %g > null %g (a real beat); the null spike at %s (%g) dominates the cross-tier max and fires NULL-REACHES-HEADLINE as a false positive; the flat check is the wrong instrument for a tier-scoped claim" % (h, n, m_ct, n_ct, spike_tier, n))


def check_split_onset(spec):
    """SPLIT-ONSET (refinement of BEATS-NULL): the flat check pools
    max-mech vs max-null ACROSS ALL calibration/evaluation splits, so for a
    split-scoped claim it reads the PEAK split, not the claim split. If the
    claim declares a claim_split and the at-claim-split mechanism is <= the
    at-claim-split null (no beat in the claimed split) but the peak mechanism
    > the peak null (a real peak in a non-claim split), the flat check is
    silent on a FALSE claim -> SPLIT-BLIND. This is the split-dimension mirror
    of TIER-ONSET / SUBGROUP-ONSET / DOSE-ONSET. The calibration/evaluation
    split is the fifth two-ended hidden variable (after time, outcome,
    subgroup, tier) and needs a NEW spec-schema field (claim_split + row
    split) to test. N/A when no claim_split is declared (schema-boundary:
    undeclared -> the flat check governs), when the at-claim-split value
    supports the claim, or when BEATS-NULL already fires (the fail cell).
    fail -> SPLIT-ONSET."""
    ct = spec.get("claim_split")
    if ct is None:
        return True, "", "N/A (no claim_split declared; the flat check governs)"
    m_ct, n_ct, amb = _joint_claim_cell(spec)
    if m_ct is None or n_ct is None:
        return True, "", "N/A (no mechanism/null reading at the claim scope cell)"
    if amb:
        return True, "", "N/A (the at-claim value is under-specified: the orthogonal scope dimension varies within the claim cell, so the marginal read is order-dependent)"
    on  = [r["metric"] for r in spec["rows"] if r.get("mechanism_on")]
    nul = [r["metric"] for r in spec["rows"] if (not r.get("mechanism_on")) or r.get("is_null")]
    if not on or not nul:
        return True, "", "N/A (no null rows)"
    h, n = max(on), max(nul)
    if h <= n:
        return True, "", "N/A (BEATS-NULL already fires; the fail cell; SPLIT-SPIKE governs)"
    if m_ct > n_ct:
        return True, "", "N/A (the at-claim-split value supports the claim; the flat check is correct)"
    return False, "SPLIT-ONSET", ("the flat check pools the cross-split max (mechanism %g > null %g), but at the claim split the mechanism is %g vs null %g (no beat); the peak is at a non-claim split; the flat check is the wrong instrument for a split-scoped claim" % (h, n, m_ct, n_ct))


def check_split_spike(spec):
    """SPLIT-SPIKE (refinement of BEATS-NULL): the fail-cell mirror of
    SPLIT-ONSET. The flat check pools max(mechanism) vs max(null) ACROSS all
    calibration/evaluation splits, so a non-claim-split null spike can
    dominate the cross-split max and make BEATS-NULL fire NULL-REACHES-HEADLINE
    on a TRUE claim (mech > null at the claim split). SPLIT-ONSET defers to
    the fail cell, and AGGREGATION-REVERSAL reads the within-split DIRECTION
    (not the scoped beat), so neither catches it. Fires when BEATS-NULL fires
    AND the at-claim-split value supports the claim (mech > null at the claim
    split) AND the max-null is at a non-claim split (the spike is outside the
    claim). The calibration/evaluation split is the fifth two-ended hidden
    variable (after time, outcome, subgroup, tier) and needs a NEW
    spec-schema field (claim_split + row split) to test. N/A when no
    claim_split is declared (schema-boundary), on a genuine fail (the
    at-claim-split value does not support the claim), and when the max-null is
    at the claim split. fail -> SPLIT-SPIKE."""
    ct = spec.get("claim_split")
    if ct is None:
        return True, "", "N/A (no claim_split declared; the flat check governs)"
    m_ct, n_ct, amb = _joint_claim_cell(spec)
    if m_ct is None or n_ct is None:
        return True, "", "N/A (no mechanism/null reading at the claim scope cell)"
    if amb:
        return True, "", "N/A (the at-claim value is under-specified: the orthogonal scope dimension varies within the claim cell, so the marginal read is order-dependent)"
    on  = [r["metric"] for r in spec["rows"] if r.get("mechanism_on")]
    nul = [r["metric"] for r in spec["rows"] if (not r.get("mechanism_on")) or r.get("is_null")]
    if not on or not nul:
        return True, "", "N/A (no null rows)"
    h, n = max(on), max(nul)
    if h > n:
        return True, "", "N/A (BEATS-NULL does not fire; the pass cell; SPLIT-ONSET governs)"
    if m_ct <= n_ct:
        return True, "", "N/A (the at-claim-split value does not support the claim; a genuine fail, not a spike)"
    spike_split = None
    for r in spec["rows"]:
        if r.get("split") is None:
            continue
        if (not r.get("mechanism_on")) or r.get("is_null"):
            if r["metric"] == n and r["split"] != ct:
                spike_split = r["split"]
    if spike_split is None:
        return True, "", "N/A (the max-null is at the claim split, not a non-claim spike)"
    return False, "SPLIT-SPIKE", ("the flat check pools the cross-split max (mechanism %g vs null %g), but at the claim split the mechanism is %g > null %g (a real beat); the null spike at %s (%g) dominates the cross-split max and fires NULL-REACHES-HEADLINE as a false positive; the flat check is the wrong instrument for a split-scoped claim" % (h, n, m_ct, n_ct, spike_split, n))

def check_metric_onset(spec):
    """METRIC-ONSET (refinement of BEATS-NULL): the flat check pools
    max-mech vs max-null ACROSS ALL metric quantities, so for a
    metric-scoped claim it reads the PEAK metric, not the claim metric. If the
    claim declares a claim_metric and the at-claim-metric mechanism is <= the
    at-claim-metric null (no beat in the claimed metric) but the peak mechanism
    > the peak null (a real peak in a non-claim metric), the flat check is
    silent on a FALSE claim -> METRIC-BLIND. This is the metric-dimension
    mirror of TIER-ONSET / SPLIT-ONSET. The metric QUANTITY (what the number
    measures: accuracy vs latency) is the SEVENTH scope dimension (after time,
    outcome, subgroup, dose, tier, split) and is orthogonal to the statistic
    KIND (how the number was derived: order vs single vs summary, the
    INCOMPARABLE-STATISTIC precondition) and needs a NEW spec-schema field
    (claim_metric + row metric_name) to test. N/A when no claim_metric is
    declared (schema-boundary: undeclared -> the flat check governs), when the
    at-claim-metric value supports the claim, or when BEATS-NULL already fires
    (the fail cell). fail -> METRIC-ONSET."""
    ct = spec.get("claim_metric")
    if ct is None:
        return True, "", "N/A (no claim_metric declared; the flat check governs)"
    m_ct, n_ct, amb = _joint_claim_cell(spec)
    if m_ct is None or n_ct is None:
        return True, "", "N/A (no mechanism/null reading at the claim scope cell)"
    if amb:
        return True, "", "N/A (the at-claim value is under-specified: the orthogonal scope dimension varies within the claim cell, so the marginal read is order-dependent)"
    on  = [r["metric"] for r in spec["rows"] if r.get("mechanism_on")]
    nul = [r["metric"] for r in spec["rows"] if (not r.get("mechanism_on")) or r.get("is_null")]
    if not on or not nul:
        return True, "", "N/A (no null rows)"
    h, n = max(on), max(nul)
    if h <= n:
        return True, "", "N/A (BEATS-NULL already fires; the fail cell; METRIC-SPIKE governs)"
    if m_ct > n_ct:
        return True, "", "N/A (the at-claim-metric value supports the claim; the flat check is correct)"
    return False, "METRIC-ONSET", ("the flat check pools the cross-metric max (mechanism %g > null %g), but at the claim metric the mechanism is %g vs null %g (no beat); the peak is at a non-claim metric; the flat check is the wrong instrument for a metric-scoped claim" % (h, n, m_ct, n_ct))


def check_metric_spike(spec):
    """METRIC-SPIKE (refinement of BEATS-NULL): the fail-cell mirror of
    METRIC-ONSET. The flat check pools max(mechanism) vs max(null) ACROSS all
    metric quantities, so a non-claim-metric null spike can dominate the
    cross-metric max and make BEATS-NULL fire NULL-REACHES-HEADLINE on a TRUE
    claim (mech > null at the claim metric). METRIC-ONSET defers to the fail
    cell, and AGGREGATION-REVERSAL reads the within-metric DIRECTION (not the
    scoped beat), so neither catches it. Fires when BEATS-NULL fires AND the
    at-claim-metric value supports the claim (mech > null at the claim metric)
    AND the max-null is at a non-claim metric (the spike is outside the claim).
    The metric QUANTITY is the SEVENTH scope dimension (after time, outcome,
    subgroup, dose, tier, split) and is orthogonal to the statistic KIND (the
    INCOMPARABLE-STATISTIC precondition) and needs a NEW spec-schema field
    (claim_metric + row metric_name) to test. N/A when no claim_metric is
    declared (schema-boundary), on a genuine fail (the at-claim-metric value
    does not support the claim), and when the max-null is at the claim metric.
    fail -> METRIC-SPIKE."""
    ct = spec.get("claim_metric")
    if ct is None:
        return True, "", "N/A (no claim_metric declared; the flat check governs)"
    m_ct, n_ct, amb = _joint_claim_cell(spec)
    if m_ct is None or n_ct is None:
        return True, "", "N/A (no mechanism/null reading at the claim scope cell)"
    if amb:
        return True, "", "N/A (the at-claim value is under-specified: the orthogonal scope dimension varies within the claim cell, so the marginal read is order-dependent)"
    on  = [r["metric"] for r in spec["rows"] if r.get("mechanism_on")]
    nul = [r["metric"] for r in spec["rows"] if (not r.get("mechanism_on")) or r.get("is_null")]
    if not on or not nul:
        return True, "", "N/A (no null rows)"
    h, n = max(on), max(nul)
    if h > n:
        return True, "", "N/A (BEATS-NULL does not fire; the pass cell; METRIC-ONSET governs)"
    if m_ct <= n_ct:
        return True, "", "N/A (the at-claim-metric value does not support the claim; a genuine fail, not a spike)"
    spike_metric = None
    for r in spec["rows"]:
        if r.get("metric_name") is None:
            continue
        if (not r.get("mechanism_on")) or r.get("is_null"):
            if r["metric"] == n and r["metric_name"] != ct:
                spike_metric = r["metric_name"]
    if spike_metric is None:
        return True, "", "N/A (the max-null is at the claim metric, not a non-claim spike)"
    return False, "METRIC-SPIKE", ("the flat check pools the cross-metric max (mechanism %g vs null %g), but at the claim metric the mechanism is %g > null %g (a real beat); the null spike at %s (%g) dominates the cross-metric max and fires NULL-REACHES-HEADLINE as a false positive; the flat check is the wrong instrument for a metric-scoped claim" % (h, n, m_ct, n_ct, spike_metric, n))

def check_funnel_stage(spec):
    """FUNNEL-STAGE-MISATTRIBUTION (headline-layer, 2026-09-19): the headline
    names a specific pipeline stage as the bottleneck, but that stage is not
    the rarest stage in the funnel -- a rarer stage exists, so the real
    bottleneck is mislocated. The data-layer instrument (BEATS-NULL etc.)
    reads the rows, not the headline's stage-attribution, so it cannot
    distinguish the framings: the conditional-vs-marginal swap flips the
    claim verdict (CONTRADICTED -> SUPPORTED) but the data-layer verdict is
    unchanged (both NULL-REACHES-HEADLINE). This axis reads the funnel
    structure (funnel_stages) + the headline's stage-attribution
    (headline_stage). N/A when fewer than two stages declare a numeric rate,
    or when the headline does not name a specific stage, or when the named
    stage IS a rarest stage (correct attribution, the pass cell). fail ->
    FUNNEL-STAGE-MISATTRIBUTION."""
    stages = spec.get("funnel_stages")
    if not stages:
        return True, "", "N/A (no funnel structure declared)"
    valid = [s for s in stages if isinstance(s.get("rate"), (int, float))]
    if len(valid) < 2:
        return True, "", "N/A (fewer than two stages declare a numeric rate)"
    headline_stage = spec.get("headline_stage")
    if headline_stage is None:
        return True, "", "N/A (the headline does not name a specific stage as the bottleneck)"
    named = None
    for s in valid:
        if s.get("stage") == headline_stage:
            named = s
            break
    if named is None:
        return True, "", "N/A (the headline's named stage %r is not in the declared funnel)" % headline_stage
    min_rate = min(s["rate"] for s in valid)
    if named["rate"] == min_rate:
        return True, "", "N/A (the headline's named stage %s is a rarest stage (rate %g); correct attribution)" % (named["stage"], named["rate"])
    rarest = min(valid, key=lambda s: s["rate"])
    majority = named["rate"] >= 0.5
    majority_note = ("The named stage is a MAJORITY (%g >= 0.5), so the 'rarely/low' qualifier is additionally contradicted." % named["rate"]) if majority else ("The named stage is not a majority (%g < 0.5)." % named["rate"])
    detail = ("the headline names %s (rate %g) as the bottleneck, but %s is rarer (rate %g < %g): the real bottleneck is the %s stage, not the named one. %s" % (
        named["stage"], named["rate"],
        rarest["stage"], rarest["rate"], named["rate"],
        rarest["stage"],
        majority_note))
    return False, "FUNNEL-STAGE-MISATTRIBUTION", detail

def check_source_misattribution(spec):
    """SOURCE-MISATTRIBUTION (headline-layer, 2026-09-25): the headline's
    source attribution (which component it names as the source of the
    effect) does not match the load-bearing variable (which component
    actually produces the effect). The credited component is a
    delivery/representation/scoping layer; the load-bearing variable is
    the content/knowledge/decision layer the claim is conditional on.
    Distinct from FUNNEL-STAGE-MISATTRIBUTION (quantitative: the named
    stage is not the rarest stage) and SCOPE-OF-INDEPENDENCE (the word
    'independent' scopes to the wrong axis): this axis reads the
    QUALITATIVE component attribution and asks whether the credited
    component is the load-bearing one. N/A when `source_attribution` or
    `load_bearing` is not declared (schema-boundary), or when the
    credited component IS the load-bearing variable (correct
    attribution, the pass cell). fail -> SOURCE-MISATTRIBUTION."""
    credited = spec.get("source_attribution")
    load_bearing = spec.get("load_bearing")
    if credited is None or load_bearing is None:
        return True, "", "N/A (source_attribution / load_bearing not declared; the axis does not apply)"
    if credited == load_bearing:
        return True, "", "N/A (the headline's source attribution (%s) matches the load-bearing variable; correct attribution)" % credited
    detail = ("the headline credits %s as the source of the effect, but the load-bearing variable is %s (a different component): the credited component is a delivery/representation/scoping layer, and the load-bearing variable is the content/knowledge/decision layer the claim is conditional on" % (credited, load_bearing))
    return False, "SOURCE-MISATTRIBUTION", detail

def check_self_falsifying(spec):
    """SELF-FALSIFYING (36th axis, 2026-09-25): the paper's OWN stated
    limitation negates the scope of its OWN headline. The data is clean
    (no data-layer flags), but the headline claims a scope (e.g.
    "universal") that the paper's own limitation concedes does not hold
    (e.g. "distance alone cannot establish a universal ranking"). This is
    a seam the data-layer checks cannot see: they read the (mechanism,
    metric, null) rows, and the rows are clean. Distinct from
    WIDER-THAN-NAMED (the named referent is wider than the measurable
    number) and SOURCE-MISATTRIBUTION (the credited component is not the
    load-bearing variable): this axis reads the SCOPE the headline claims
    and the SCOPE the paper's own limitation negates, and asks whether
    they are the same scope. N/A when `headline_scope` or
    `limitation_negates` is not declared (schema-boundary), or when
    `limitation_negates != headline_scope` (the limitation negates a
    different dimension, not the headline's scope;
    limitation-irrelevant-to-headline, the pass cell). fail ->
    SELF-FALSIFYING when the two agree (the paper's own limitation
    negates the headline's scope)."""
    scope = spec.get("headline_scope")
    negates = spec.get("limitation_negates")
    if scope is None or negates is None:
        return True, "", "N/A (headline_scope / limitation_negates not declared; the axis does not apply)"
    if negates != scope:
        return True, "", "N/A (the stated limitation negates %s, a different dimension than the headline's scope (%s); limitation-irrelevant-to-headline)" % (negates, scope)
    detail = ("the headline claims a %s scope, but the paper's own stated limitation negates that %s scope: the data is clean (the data-layer checks read the rows), yet the paper's own concession negates the scope of its own headline" % (scope, scope))
    return False, "SELF-FALSIFYING", detail

def check_primary_basis_reversal(spec):
    """PRIMARY-BASIS-REVERSAL (headline-layer, 2026-09-25): the paper's own
    text designates a primary basis for comparison, and the claim's
    load-bearing comparative advantage REVERSES on that designated primary
    basis (it holds on a secondary axis the paper also reports, but flips on
    the one the paper itself designates as primary). Distinct from
    WRONG-AXIS (the mechanism's own axis sits at the null baseline; a
    data-layer check on the rows) and SELF-FALSIFYING (the paper's own
    stated limitation negates the headline's scope): this axis reads the
    paper's own basis designation and asks whether the headline's advantage
    survives on it. N/A when `primary_basis` or `primary_basis_result` is
    not declared (schema-boundary), or when the claim HOLDS on the
    designated primary basis (holds-on-primary, the pass cell). fail ->
    PRIMARY-BASIS-REVERSAL when the result is 'reverses'."""
    basis = spec.get("primary_basis")
    result = spec.get("primary_basis_result")
    if basis is None or result is None:
        return True, "", "N/A (primary_basis / primary_basis_result not declared; the axis does not apply)"
    if result == "reverses":
        detail = ("the paper designates %s as the primary basis for comparison, and the claim's comparative advantage reverses on it (it holds on the secondary axis %s, but flips on the paper's own designated primary basis)" % (basis, spec.get("secondary_basis", "the secondary axis")))
        return False, "PRIMARY-BASIS-REVERSAL", detail
    return True, "", "N/A (the claim holds on the designated primary basis (%s); holds-on-primary)" % basis

def _cmp_criterion(value, op, threshold):
    """Evaluate a declared subset criterion (op, threshold) against a row's
    metric. The criterion is the narrative's selection rule for the subset
    (e.g. task span <= 0.5); the row's metric is the span of the subset it
    names. Returns True when the row's subset satisfies the criterion."""
    if op == "<=":
        return value <= threshold
    if op == ">=":
        return value >= threshold
    if op == "<":
        return value < threshold
    if op == ">":
        return value > threshold
    raise ValueError("unknown criterion op %r" % op)


def check_selection_on_narrative(spec):
    """SELECTION-ON-NARRATIVE (11th primary axis, 2026-09-19): the headline's
    subset is NARRATIVE-CONDITIONAL. The headline reports a statistic over a
    subset of units (e.g. 'the middle three models'), and the subset is
    selected by the narrative's own criterion (e.g. task span <= 0.5), not by
    position or mechanism. The null row (the positional middle, the natural
    control) does NOT satisfy the criterion, so the headline's subset is
    narrative-conditional: the claim is about a subset that only the narrative
    can name, and the data-layer instrument (BEATS-NULL etc.) reads the rows,
    not the subset's provenance, so it cannot separate the framings. Distinct
    from SELECTION-BIAS (the units are distinct model units, not repeated
    draws of a fixed instrument) and from REFERENT-CONSTRUCTED (the referent
    is narrative-selected, not model-constructed). N/A when the subset
    criterion is not declared, when the mechanism row does not satisfy the
    criterion, or when the null row ALSO satisfies the criterion (the subset
    is not narrative-conditional; the pass cell). fail ->
    SELECTION-ON-NARRATIVE."""
    crit = spec.get("subset_criterion")
    if not crit:
        return True, "", "N/A (no subset_criterion declared)"
    op = crit.get("op")
    thr = crit.get("threshold")
    if op is None or thr is None:
        return True, "", "N/A (subset_criterion incomplete: need op and threshold)"
    on_rows = _rows(spec, lambda r: r.get("mechanism_on"))
    if not on_rows:
        return True, "", "N/A (no mechanism rows)"
    h_row = max(on_rows, key=lambda r: r["metric"])
    if not _cmp_criterion(h_row["metric"], op, thr):
        return True, "", "N/A (the mechanism row's subset does not satisfy the declared criterion; the criterion is not the narrative's selection rule)"
    nul_rows = _rows(spec, lambda r: (not r.get("mechanism_on")) or r.get("is_null"))
    if not nul_rows:
        return True, "", "N/A (no null rows)"
    for nr in nul_rows:
        if not _cmp_criterion(nr["metric"], op, thr):
            return False, "SELECTION-ON-NARRATIVE", \
                "the headline's subset (metric %g) satisfies the narrative criterion (%s %g), but the null row %r (metric %g) does NOT: the subset is narrative-conditional, and the data-layer instrument reads the rows, not the subset's provenance" % (h_row["metric"], op, thr, nr.get("label"), nr["metric"])
    return True, "", "N/A (the null row also satisfies the criterion; the subset is not narrative-conditional, the pass cell)"

def check_annotator_self_keyed(spec):
    """ANNOTATOR-SELF-KEYED (12th primary axis, 2026-09-19): the mechanism
    explanation (the 'why' - the causal attribution, the phase composition, the
    behavioral claim) must not rest on a non-public annotation (LLM-judge or human). When
    the 'why' rests on an LLM-judge label (e.g. a workflow-phase classification
    by GPT-5.5, validated on a 200-trajectory sample) over NON-PUBLIC
    trajectories, the aggregate (the headline number) is stranger-rerunnable
    but the 'why' is not: a stranger cannot re-derive the annotation without the
    judge and the non-public trajectories. Distinct from NO-EMPIRICAL-CONTENT
    (the data IS there; the aggregate is computable) and from SELF-KEYED (no
    continuous knob; this axis is about the annotation layer, not the knob).
    N/A when `annotation_provenance` is not declared (schema-boundary) or when
    the 'why' rests on a deterministic readout or a public human annotation.
    fail -> ANNOTATOR-SELF-KEYED."""
    prov = spec.get("annotation_provenance")
    if prov is None:
        return True, "", "N/A (annotation_provenance not declared; the axis does not apply)"
    p = str(prov).lower()
    if p in ("llm-judge-non-public", "human-non-public"):
        kind = "non-public LLM-judge annotation" if p == "llm-judge-non-public" else "non-public human annotation"
        return False, "ANNOTATOR-SELF-KEYED", \
            "the mechanism explanation rests on a %s (%s): the aggregate is stranger-rerunnable but the 'why' is not - a stranger cannot re-derive the annotation without the annotator and the non-public source" % (kind, prov)
    return True, "", "N/A (annotation_provenance=%s: the 'why' rests on a re-derivable readout or a public annotation, not a non-public annotation)" % prov



def check_scope_of_independence(spec):
    """SCOPE-OF-INDEPENDENCE (13th primary axis, 2026-09-22): when a
    load-bearing number rests on an 'independent' panel (control/holdout/
    test set), the word 'independent' must scope to the axis that makes the
    independence load-bearing for the claim. Four scopes: protocol (separate
    hardware/episodes), data (panel items disjoint from the training set),
    implementation (separate code path/model), human gate (a human verified
    it). FAIL cell: the declared scope covers some axes but NOT the
    load-bearing one, so the qualifier is under-specified on the axis that
    makes it do work (the panel may be in-distribution there). Distinct from
    SCOPE-TRANSPOSITION (a number carried into the wrong referent) and
    SELF-KEYED (metric monotone in its own knob): this axis reads the
    QUALIFIER 'independent' and asks what it scopes to. N/A when
    `independence_scope` or `independence_load_bearing` is not declared
    (schema-boundary). fail -> SCOPE-OF-INDEPENDENCE."""
    scope = spec.get("independence_scope")
    load  = spec.get("independence_load_bearing")
    if scope is None or load is None:
        return True, "", "N/A (independence_scope / independence_load_bearing not declared; the axis does not apply)"
    if load not in scope:
        return False, "SCOPE-OF-INDEPENDENCE", "the 'independent' panel declares scope %s but the load-bearing axis is %s: the independence qualifier is under-specified on the axis that makes it do work (the panel may be in-distribution on %s)" % (scope, load, load)
    return True, "", "N/A (independence_scope covers the load-bearing axis %s; the independence qualifier is specified where it does work)" % load


def check_reference_mix(spec):
    """REFERENCE-MIX (14th primary axis, 2026-09-22): a composite trade-off
    claim reports two or more numbers (e.g., quality gain and latency
    reduction), each anchored to a DIFFERENT baseline. The single-reference
    reading computes all numbers against the SAME baseline. The check asks:
    is the composite conservative or inflated relative to the single-reference
    reading? FAIL cell: the composite is INFLATED (at least one metric is
    anchored to the reference that makes it look better than the single-
    reference). PASS cell: the composite is CONSERVATIVE (all metrics are
    anchored to the reference that makes them look the same or worse than the
    single-reference). N/A when the trade-off pairing structure is not
    declared (schema-boundary). fail -> REFERENCE-MIX."""
    pairing = spec.get("tradeoff_pairing")
    single_ref = spec.get("tradeoff_single_reference")
    metrics = spec.get("tradeoff_metrics")
    if not pairing or single_ref is None or not metrics:
        return True, "", "N/A (tradeoff_pairing / tradeoff_single_reference / tradeoff_metrics not declared; the axis does not apply)"
    inflated = []
    for m in metrics:
        name = m.get("name")
        direction = m.get("direction")
        mech = m.get("mechanism")
        refs = m.get("references")
        if name is None or direction is None or mech is None or refs is None:
            return True, "", "N/A (tradeoff_metrics entry %r incomplete; the axis does not apply)" % name
        abstract_ref = pairing.get(name)
        if abstract_ref is None:
            return True, "", "N/A (tradeoff_pairing does not cover metric %r; the axis does not apply)" % name
        if abstract_ref not in refs or single_ref not in refs:
            return True, "", "N/A (metric %r does not declare references for %r / %r; the axis does not apply)" % (name, abstract_ref, single_ref)
        abstract_val = refs[abstract_ref]
        single_val = refs[single_ref]
        if direction == "higher_better":
            abstract_gain = mech - abstract_val
            single_gain = mech - single_val
        elif direction == "lower_better":
            if abstract_val == 0 or single_val == 0:
                return True, "", "N/A (metric %r has a zero reference; the relative gain is undefined)" % name
            abstract_gain = (abstract_val - mech) / abstract_val
            single_gain = (single_val - mech) / single_val
        else:
            return True, "", "N/A (unknown direction %r for metric %r; the axis does not apply)" % (direction, name)
        if abstract_gain > single_gain + 1e-9:
            inflated.append(name)
    if inflated:
        return False, "REFERENCE-MIX", "the composite trade-off pairing is INFLATED relative to the single-reference reading (%s): %s anchored to the reference that makes it look better than the single-reference; the pairing does rhetorical work" % (single_ref, ", ".join(inflated))
    return True, "", "the composite trade-off pairing is conservative or neutral relative to the single-reference reading (%s); presentation, not flaw" % single_ref


def check_unwitnessed_receipt(spec):
    """UNWITNESSED-RECEIPT (15th primary axis, 2026-09-24): the failure signal
    (a receipt that disagrees with its promise) is PRESENT but UNREAD, because
    the witness (awake reader) is absent at the critical moment. The silence is
    a monitoring property (no reader), not a falsifiability property (no
    reading). Distinct from MEASUREMENT-ABSENT (signal absent -> claim
    unfalsifiable) and VACUOUS-RATIO (value reported, support empty). N/A when
    the spec does not declare a receipt (orthogonal to the empirical axes),
    when the receipt is not written (MEASUREMENT-ABSENT regime), when the
    receipt agrees with the promise (no failure signal), or when the failure
    is caught (awake witness or self-escalation)."""
    receipt = spec.get("receipt")
    if not receipt:
        return True, "", "N/A (no receipt declared; orthogonal to the empirical axes)"
    if not receipt.get("written"):
        return True, "", "N/A (MEASUREMENT-ABSENT regime: the receipt is not written; the signal is absent, not unread)"
    if not receipt.get("disagrees"):
        return True, "", "N/A (the receipt agrees with the promise; no failure signal)"
    if receipt.get("witness_awake") or receipt.get("self_escalates"):
        return True, "", "N/A (the failure is caught: an awake witness or self-escalation reads the receipt)"
    return False, "UNWITNESSED-RECEIPT", "the receipt is written and disagrees with the promise, but the witness is absent at the critical moment (no awake reader, no self-escalation); the failure signal is present but unread"


def check_unwitnessed_root(spec):
    """UNWITNESSED-ROOT (16th primary axis, 2026-09-24): a manifest (pre-set
    or diff) presented as a recoverable receipt is a CHAIN-EXTENSION, not a
    chain-closure: its recoverability is BORROWED from a root (the pre-set
    hash the manifest is computed against / the anchor of the recovery
    chain). If that root was UNWITNESSED at write time (no reader at write
    time), the recovery chain terminates at an unwitnessed promise. The
    receipt is recoverable in FORM, not to a witnessed root. Distinct from
    UNWITNESSED-RECEIPT (a disagreement going unread): here the receipt may
    even agree with the promise; the failure is that the recovery chain's
    anchor is unwitnessed. This is UNWITNESSED-RECEIPT propagating one link
    up the chain. N/A when the spec does not declare a manifest (orthogonal
    to the empirical axes), when the root hash is not written
    (MEASUREMENT-ABSENT regime: the recovery chain is broken at the first
    link, not unwitnessed), or when the root was witnessed at write time
    (the recovery chain terminates at a witnessed root)."""
    m = spec.get("manifest")
    if not m:
        return True, "", "N/A (no manifest declared; orthogonal to the empirical axes)"
    if not m.get("root_written"):
        return True, "", "N/A (MEASUREMENT-ABSENT regime: the root hash is not written; the recovery chain is broken at the first link, not unwitnessed)"
    if m.get("root_witnessed"):
        return True, "", "N/A (the recovery chain terminates at a witnessed root; the manifest is as recoverable as its root, and the root is witnessed)"
    return False, "UNWITNESSED-ROOT", "the manifest (%s) is presented as a recoverable receipt, but its recovery chain terminates at an unwitnessed root (the pre-set hash was not witnessed at write time); the receipt is recoverable in form, not to a witnessed root" % m.get("kind","manifest")


def _classify_na(detail, superlative=False):
    """Classify an N/A reason into a boundary class.
    - schema: the spec could have declared the structure; the instrument is
      blind to what is not declared. This is the calibration boundary (FP/FN
      surface): the check would apply if the spec declared the structure.
      Includes the data-absence side: a superlative's missing comparison
      basis ('no null rows' when the claim declares a superlative) is
      schema-conditional, because the basis is load-bearing.
    - governance: a more specific check governs, or the data is in the pass
      cell. Not a boundary -- the check was applicable but another check wins.
    - regime: the check's regime does not apply to this claim's type. Not a
      boundary -- the check is structurally inapplicable.
    - data: the spec declared the structure, the data just does not support
      the check. Not a boundary -- the check was applicable but the data is
      insufficient.
    """
    d = detail.lower()
    # schema-conditional: the spec could have declared the structure
    if any(k in d for k in ("not declared", "no claim_", "no witness",
                            "no record/referent", "no subset_criterion",
                            "no annotation_provenance", "no referent_provenance",
                            "no order-statistic headline", "no ci/se",
                            "no dose structure", "no subgroup/pooling",
                            "no funnel structure", "no onset timepoint",
                            "no spike timepoint", "no tier level",
                            "no split level", "no metric value",
                            "no outcome value",
                            "no receipt declared")):
        return "schema"
    # a superlative's missing comparison basis is schema-conditional (the
    # data-absence side of the boundary): the claim is an extreme over a
    # population (a record, best, highest/lowest ever), and the population
    # (the basis) is load-bearing. When the rows carry no null (the basis is
    # absent), the absence is a schema gap (the spec could have declared the
    # basis), not a data gap. Only fires when the claim declares a superlative.
    if superlative and "no null rows" in d:
        return "schema"
    # governance: a more specific check governs, or the data is in the pass cell
    if any(k in d for k in ("governs", "pass cell", "fail cell",
                            "not a non-claim spike", "not a non-onset spike",
                            "not narrative-conditional",
                            "not the narrative's selection rule",
                            "no consistent within-subgroup direction",
                            "not uniformly mechanism-favorable")):
        return "governance"
    # regime: the check's regime does not apply to this claim's type
    if any(k in d for k in ("no-empirical", "vacuous", "incomparable",
                            "by-construction", "not an ablation",
                            "knob_kind", "empirical axes govern")):
        return "regime"
    return "data"

CHECKS = [
    ("BEATS-NULL",     check_beats_null),
    ("NOT-SELF-KEYED", check_not_self_keyed),
    ("SELECTION-BIAS", check_selection_bias),
    ("ISOLATED",       check_isolated),
    ("CO-MOVES",       check_co_moves),
    ("NOISE-FLOOR",    check_noise_floor),
    ("REFERENT-WITNESSED", check_referent_witnessed),
    ("LOSSY-PROJECTION", check_lossy_projection),
    ("AGGREGATION-REVERSAL", check_aggregation_reversal),
    ("REFERENT-CONSTRUCTED", check_referent_constructed),
    ("DOSE-RESPONSE",    check_dose_response),
    ("TEMPORAL-ONSET",  check_temporal_onset),
    ("TEMPORAL-SPIKE",  check_temporal_spike),
    ("OUTCOME-ONSET",    check_outcome_onset),
    ("OUTCOME-SPIKE",    check_outcome_spike),
    ("SUBGROUP-ONSET",   check_subgroup_onset),
    ("SUBGROUP-SPIKE",   check_subgroup_spike),
    ("DOSE-ONSET",      check_dose_onset),
    ("DOSE-SPIKE",      check_dose_spike),
    ("TIER-ONSET",      check_tier_onset),
    ("TIER-SPIKE",      check_tier_spike),
    ("SPLIT-ONSET",    check_split_onset),
    ("SPLIT-SPIKE",    check_split_spike),
    ("METRIC-ONSET",   check_metric_onset),
    ("METRIC-SPIKE",   check_metric_spike),
    ("FUNNEL-STAGE-MISATTRIBUTION", check_funnel_stage),
    ("SOURCE-MISATTRIBUTION", check_source_misattribution),
    ("SELECTION-ON-NARRATIVE", check_selection_on_narrative),
    ("ANNOTATOR-SELF-KEYED", check_annotator_self_keyed),
    ("COMPUTABLE",       check_computable),
    ("SCOPE-OF-INDEPENDENCE", check_scope_of_independence),
    ("REFERENCE-MIX", check_reference_mix),
    ("UNWITNESSED-RECEIPT", check_unwitnessed_receipt),
    ("UNWITNESSED-ROOT", check_unwitnessed_root),
    ("WIDER-THAN-NAMED", check_wider_than_named),
    ("SELF-FALSIFYING", check_self_falsifying),
    ("PRIMARY-BASIS-REVERSAL", check_primary_basis_reversal),
]

def _no_empirical(spec):
    """NO-EMPIRICAL-CONTENT regime: a pure specification claim. A spec with no
    data rows, or declared type 'specification', has no (mechanism, metric,
    null) triple to discriminate. Distinct from VACUOUS-RATIO (a reported
    ratio with an empty denominator): here there is no reported ratio at all."""
    return (not spec.get("rows")) or spec.get("type") == "specification"

def audit(spec):
    results, flags = {}, []
    if _no_empirical(spec):
        for name, fn in CHECKS:
            if name in ("COMPUTABLE", "UNWITNESSED-RECEIPT", "UNWITNESSED-ROOT", "WIDER-THAN-NAMED", "SELF-FALSIFYING"):
                ok, flag, detail = fn(spec)
                results[name] = {"pass": ok, "detail": detail}
                if not ok:
                    flags.append(flag)
            else:
                results[name] = {"pass": True, "detail": "N/A (NO-EMPIRICAL-CONTENT: no data rows; the empirical axis does not apply)"}
        flags.insert(0, "NO-EMPIRICAL-CONTENT")
        verdict = "NO-EMPIRICAL-CONTENT" if len(flags) == 1 else ", ".join(flags)
        return {"spec": spec.get("name"), "checks": results, "flags": flags, "verdict": verdict, "contested": []}
    vacuous = _headline_support(spec) == 0
    incomparable, inc_detail = _incomparable_statistic(spec)
    by_construction, bc_detail = _by_construction(spec)
    for name, fn in CHECKS:
        if name == "UNWITNESSED-RECEIPT":
            ok, flag, detail = fn(spec)
            results[name] = {"pass": ok, "detail": detail}
            if not ok:
                flags.append(flag)
            continue
        if name == "UNWITNESSED-ROOT":
            ok, flag, detail = fn(spec)
            results[name] = {"pass": ok, "detail": detail}
            if not ok:
                flags.append(flag)
            continue
        if incomparable:
            results[name] = {"pass": True, "detail": "N/A (INCOMPARABLE-STATISTIC: %s)" % inc_detail}
            continue
        if vacuous:
            results[name] = {"pass": True, "detail": "N/A (VACUOUS-RATIO: the mechanism's headline has an empty denominator; the metric is undefined)"}
            continue
        if by_construction:
            results[name] = {"pass": True, "detail": "N/A (BY-CONSTRUCTION: %s)" % bc_detail}
            continue
        ok, flag, detail = fn(spec)
        results[name] = {"pass": ok, "detail": detail}
        if not ok:
            flags.append(flag)
    if incomparable:
        flags.append("INCOMPARABLE-STATISTIC")
    elif vacuous:
        flags.append("VACUOUS-RATIO")
    elif by_construction:
        flags.append("BY-CONSTRUCTION")
    verdict = "DISCRIMINATES" if not flags else ", ".join(flags)
    # Surface the calibration boundary: schema-conditional N/As are the
    # checks the instrument is blind to on this spec. If the spec declared
    # the structure, the check would apply. This is the FP/FN surface.
    boundary = []
    superlative = bool(spec.get("superlative"))
    for name, res in results.items():
        if res["pass"] and res["detail"].startswith("N/A"):
            cls = _classify_na(res["detail"], superlative)
            if cls == "schema":
                if superlative and "no null rows" in res["detail"].lower():
                    note = ("superlative data-absence: the claim declares a superlative (an extreme over a population) but the comparison basis (the population) is not in the rows; if the spec declared the basis, this check would apply")
                else:
                    note = "schema-conditional: the instrument is blind to this on the current spec; if the spec declared the structure, this check would apply"
                boundary.append({"check": name, "reason": res["detail"], "note": note})
    # FP-side schema boundary: when BEATS-NULL fires NULL-REACHES-HEADLINE,
    # the fired flag is CONTESTED on every scope dimension for which the
    # false-positive verifier (the SPIKE refinement) is schema-conditional N/A
    # (the scope field is undeclared, so the instrument cannot rule out a
    # non-claim-scope null spike dominating the cross-scope max). This is the
    # FP-side mirror of the superlative data-absence boundary (the FN side):
    # the FN side surfaces a check that SHOULD fire but is N/A; the FP side
    # surfaces a flag that FIRED but whose false-positive verifier is N/A.
    SPIKE_VERIFIERS = ("TEMPORAL-SPIKE", "OUTCOME-SPIKE", "SUBGROUP-SPIKE",
                       "DOSE-SPIKE", "TIER-SPIKE", "SPLIT-SPIKE", "METRIC-SPIKE")
    contested = []
    if "NULL-REACHES-HEADLINE" in flags:
        for name in SPIKE_VERIFIERS:
            res = results.get(name)
            if res and res["pass"] and "declared; the flat check governs" in res["detail"]:
                contested.append({"flag": "NULL-REACHES-HEADLINE",
                                  "verifier": name,
                                  "reason": res["detail"],
                                  "note": "the fired flag is unverified on this scope dimension: the false-positive verifier is schema-conditional N/A (the scope field is undeclared), so the instrument cannot rule out a non-claim-scope null spike dominating the cross-scope max"})
    return {"spec": spec.get("name"), "checks": results, "flags": flags,
            "verdict": verdict, "boundary": boundary, "contested": contested}

def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--spec":
        spec = json.load(open(sys.argv[2]))
        print(json.dumps(audit(spec), indent=2))
        return
    import specimens
    all_ok = True
    for spec in specimens.SPECIMENS:
        a = audit(spec)
        ok = set(a["flags"]) == set(spec.get("expected", []))
        all_ok = all_ok and ok
        mark = "OK      " if ok else "MISMATCH"
        print("[%s] %s" % (mark, a["spec"]))
        print("          verdict: %s   (expected %s)" % (a["verdict"], spec.get("expected", [])))
        for name, res in a["checks"].items():
            tag = "pass" if res["pass"] else "FLAG"
            print("            %s %s: %s" % (tag, name, res["detail"]))
        print()
    print("ALL SPECIMENS MATCH" if all_ok else "SOME SPECIMENS MISMATCH")
    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()
