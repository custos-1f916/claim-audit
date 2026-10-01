#!/usr/bin/env python3
"""meta_guard.py -- the instrument's guard against its own class of error.

The 2026-10-01 slip: the meta-record counted DISTINCT FAIL-FLAG STRINGS (59)
instead of REGISTRY AXIS ENTRIES (60). The slip is one class of error in
THREE phrasings of the count, and a guard that watches only one phrasing is
itself self-keyed to it:

  axis  count  = len(CHECKS) = 60          (docs said 59)
  check count  = len(CHECKS) = 60          (docs said 59 / 58)
  flag  count  = 60 check flags + 4 gate flags = 64   (docs said 63)

Two mechanisms made the axis count wrong, both real:
  (a) the flag census was a naive regex that missed PARENTHESIZED returns
      (`return (False, "EVIDENCE-UNCLOSED", ...)`), undercounting distinct
      flags by one (59 instead of 60) and mislabeling EVIDENCE-UNCLOSED as a
      no-flag regime axis;
  (b) seven axes emit a flag whose NAME differs from their registry axis name
      (NOT-SELF-KEYED -> SELF-KEYED, BEATS-NULL -> NULL-REACHES-HEADLINE, ...).
      Renames do not change the count, but they make "flag name == axis name"
      a wrong assumption.

This guard re-derives every count from the CODE (never the prose, never a hand
count) and checks each doc claim against the RIGHT ground truth for its
phrasing:

  N        = len(CHECKS)                    [axis/check count]
  F        = distinct check-emitted flags   [AST census, exact]
  R        = axes emitting no flag
  G        = distinct gate flags            [flags.append/insert in the CLI loop]
  F_total  = F + G                          [total flags the instrument emits]

Checks:
  (1) F + R == N        (count invariant: 1 flag/axis, no shared flag)
  (2) AST census == regex census   (extractor agreement; a mismatch is the slip)
  (3) drift map: renames (flag != axis name) and no-flag axes
  (4) doc claims: axis/check claims must equal N, flag claims must equal
      F_total. Pinned by stable anchor (not line number). Historical claims
      (EXISTING N-axis snapshots, the N-axis saturation test, the "grows to N"
      question, the "N axes split" section) are reported, not asserted.

Non-self-keyed: the numbers are re-derived from the registry; the prose is the
thing being examined. Stranger-rerunnable: python3 meta_guard.py  (stdlib only,
no network). Exits 0 and prints VERDICT: ... RECONCILES iff the count
reconciles, the extractors agree, and every current-state doc claim matches.
"""
import re, ast, inspect, sys
import claim_audit as C

DOCS = ["COHERENCE.md", "README.md"]

# CURRENT-STATE count-claims, pinned by a stable anchor (not a line number, so a
# restructure does not silently drop the check). Each entry:
#   (doc, anchor_pattern, capture_group, expected_type)
# expected_type: "axis" -> N, "check" -> N, "flag" -> F_total
CURRENT_STATE = [
    # axis-count claims
    ("COHERENCE.md", r"# Coherence of the (\d+)-axis instrument", 1, "axis"),
    ("COHERENCE.md", r"The (\d+)-axis instrument is coherent", 1, "axis"),
    ("COHERENCE.md", r"growth from \d+ to (\d+) axes", 1, "axis"),
    ("README.md",    r"A (\d+)-axis falsification instrument", 1, "axis"),
    ("README.md",    r"checks the claim against (\d+) axes", 1, "axis"),
    ("README.md",    r"Growth to (\d+) axes raises", 1, "axis"),
    # check-count claims (1:1 with axes; calibration_boundary derives N=len(CHECKS))
    ("README.md",    r"the instrument \((\d+) checks \+ CLI\)", 1, "check"),
    ("README.md",    r"for each of the (\d+) checks", 1, "check"),
    ("README.md",    r"all (\d+) checks now fire", 1, "check"),
    ("README.md",    r"(\d+)/(\d+) checks are calibrated", 2, "check"),  # denominator = total
    # flag-total claims (check flags + gate flags = F_total, NOT N)
    ("COHERENCE.md", r"(\d+) distinct \*flags\*", 1, "flag"),
    ("COHERENCE.md", r"of (\d+) flags", 1, "flag"),
    ("README.md",    r"of (\d+) flags", 1, "flag"),
]

# Historical / contextual claims: reported, not asserted. These reference a past
# snapshot or a named past test and legitimately differ from the current count.
HISTORICAL = [
    r"EXISTING (\d+)-axis",          # past-instrument snapshots
    r"(\d+)-axis saturation test",   # the named past test
    r"grows to (\d+) axes",          # the motivating question (past)
    r"The (\d+) axes split into",    # a section describing a past count
]


def ast_flags(fn):
    """Exact flag census for one check function: every `return False, "FLAG"`
    (parenthesized or not -- Python's AST normalizes both to a Tuple)."""
    src = inspect.getsource(fn)
    tree = ast.parse(src)
    flags = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Return) and isinstance(node.value, ast.Tuple):
            e = node.value.elts
            if (len(e) >= 2 and isinstance(e[0], ast.Constant)
                    and e[0].value is False
                    and isinstance(e[1], ast.Constant)
                    and isinstance(e[1].value, str)):
                flags.add(e[1].value)
    return flags


def main():
    # (1) ground truth: the registry.
    reg = [(n, f) for (n, f) in C.CHECKS]
    N = len(reg)
    axis_names = [n for n, _ in reg]

    # (2) exact check-flag census per axis (AST).
    per = {n: ast_flags(f) for n, f in reg}
    all_flags = set()
    for s in per.values():
        all_flags |= s
    F = len(all_flags)
    noflag = [n for n, s in per.items() if not s]
    R = len(noflag)

    # (3) independent regex census (cross-check). Must catch parenthesized
    #     returns: `return (False, "FLAG"` as well as `return False, "FLAG"`.
    modsrc = inspect.getsource(C)
    re_flags = set(re.findall(
        r'return[ \t]*\(?[ \t]*False[ \t]*,[ \t]*"([A-Z][A-Z0-9-]*)"', modsrc))

    # naive (unparen-only) census: the slip's extractor. Misses
    # `return (False, "FLAG"`; reports 59 where the exact census reports 60.
    naive_flags = set(re.findall(
        r'return[ \t]*False[ \t]*,[ \t]*"([A-Z][A-Z0-9-]*)"', modsrc))
    naive_undercount = F - len(naive_flags)

    # (4) gate flags: emitted by the CLI loop (flags.append/insert), not a check
    #     return. These are NOT in the registry, so F_total != N.
    gate_flags = set(re.findall(
        r'flags\.(?:append|insert)\(\d*,?[ \t]*"([A-Z][A-Z0-9-]*)"', modsrc))
    gate_new = gate_flags - all_flags
    F_total = len(all_flags | gate_flags)

    renames = {n: sorted(s) for n, s in per.items() if s and s != {n}}

    # (5) invariants.
    reconcile_ok = (F + R == N)
    extract_agree = (all_flags == re_flags)

    print("registry axes        : %d  (first %s, last %s)" % (N, axis_names[0], axis_names[-1]))
    print("distinct flags (AST) : %d" % F)
    print("distinct flags (re)  : %d   extraction agrees: %s" % (len(re_flags), extract_agree))
    if not extract_agree:
        print("    AST-only: %s" % sorted(all_flags - re_flags))
        print("    re-only : %s" % sorted(re_flags - all_flags))
    print("no-flag regime axes  : %d  %s" % (R, noflag))
    print("gate flags (CLI)     : %d  %s" % (len(gate_new), sorted(gate_new)))
    print("TOTAL flags emitted  : %d  (%d check + %d gate)" % (F_total, F, len(gate_new)))
    print("drift (flag != name) : %d" % len(renames))
    for n in sorted(renames):
        print("    %-24s -> %s" % (n, ", ".join(renames[n])))
    print("reconcile F+R==N     : %s  (%d + %d == %d)" % (reconcile_ok, F, R, N))

    # (6) doc current-state claims: each anchor must match exactly one line and
    #     its count must equal the RIGHT ground truth for its phrasing.
    expected = {"axis": N, "check": N, "flag": F_total}
    bad = []
    print("current-state claims : %d  (asserted)" % len(CURRENT_STATE))
    for doc, pat, grp, typ in CURRENT_STATE:
        txt = open(doc).read().splitlines()
        hits = []
        for i, ln in enumerate(txt, 1):
            m = re.search(pat, ln)
            if m:
                hits.append((i, int(m.group(grp)), ln.strip()))
        if len(hits) != 1:
            bad.append((doc, -1, "?", expected[typ], "anchor matched %d lines" % len(hits)))
            print("    [BAD] %s  anchor matched %d lines (want 1): %s" % (doc, len(hits), pat))
            continue
        i, num, ln = hits[0]
        want = expected[typ]
        if num != want:
            bad.append((doc, i, num, want, ln))
            print("    [BAD] %s:%d  claims %d (%s, want %d)  (%s)" % (doc, i, num, typ, want, ln[:54]))
        else:
            print("    [ok ] %s:%d  claims %d (%s)  (%s)" % (doc, i, num, typ, ln[:54]))

    # (7) historical claims: reported, not asserted.
    hist = []
    for doc in DOCS:
        for i, ln in enumerate(open(doc).read().splitlines(), 1):
            for pat in HISTORICAL:
                m = re.search(pat, ln)
                if m:
                    hist.append((doc, i, int(m.group(1)), ln.strip()))
                    break
    print("historical claims    : %d  (reported, not asserted)" % len(hist))
    for doc, i, num, ln in hist:
        print("    [hist] %s:%d  %d  (%s)" % (doc, i, num, ln[:54]))

    docs_ok = not bad
    ok = reconcile_ok and extract_agree and docs_ok
    n_axis = sum(1 for _, _, _, t in CURRENT_STATE if t == "axis")
    n_check = sum(1 for _, _, _, t in CURRENT_STATE if t == "check")
    n_flag = sum(1 for _, _, _, t in CURRENT_STATE if t == "flag")
    print()
    if ok:
        print("VERDICT: meta-record RECONCILES -- the registry is ground truth")
        print("        (N=%d axes/checks, F_total=%d flags = %d check + %d gate);" % (N, F_total, F, len(gate_new)))
        print("        the census is exact and self-consistent (F+R==N, AST==regex);")
        print("        all %d current-state doc claims match the code (%d axis, %d check," % (len(CURRENT_STATE), n_axis, n_check))
        print("        %d flag). The %d rename axes change names, not the count; a naive" % (n_flag, len(renames)))
        print("        flag-string census that misses a parenthesized return undercounts by %d." % naive_undercount)
    else:
        print("VERDICT: meta-record DOES NOT RECONCILE.")
        if not reconcile_ok:
            print("  count gap unexplained: F(%d)+R(%d) != N(%d) -- a flag collision or an unaccounted axis." % (F, R, N))
        if not extract_agree:
            print("  extractor disagrees: AST != regex -- the static census is stale (the slip).")
        for doc, i, num, want, extra in bad:
            if i == -1:
                print("  doc anchor: %s -- %s." % (doc, extra))
            else:
                print("  doc drift: %s:%d claims %d, registry has %d." % (doc, i, num, want))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
