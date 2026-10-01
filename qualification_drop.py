#!/usr/bin/env python3
"""QUALIFICATION-DROP: the honest-body / loose-abstract tag, made machine-checkable.

The tag is a *named relationship* (the body concedes a qualification the
headline/abstract drops), not a falsifier axis. COHERENCE.md names it and gives
the discriminator (Case A vs Case B); this probe makes the discriminator
machine-checkable and exposes its cell structure.

Strict tag (Cell B, "known-but-hidden"): body_hedges (the named body-concession
proxy) AND a seam axis fires. The seam set is the prose-named
{THESIS-OUTRUNS-EVIDENCE, SELECTION-ON-NARRATIVE, VACUOUS-WITNESS} intersected
with the actual CHECKS (VACUOUS-WITNESS is prose-only, not an axis -> a finding).

Cell P ("presentation-only", logged-not-flagged): the body concedes a dropped
qualification but NO seam axis fires (the substance is fine; the presentation
is loose). The strict prose definition (seam AND body_hedges) MISSES this cell;
this probe surfaces it.

Cell B is split by CONCESSION AUTHORSHIP (the concession_authorship field). The
tag's core diagnostic -- "the authors *knew* the claim was weaker, because the
body concedes it" -- is load-bearing on SAME-authorship: the same author who
wrote the dropping abstract must have written the conceding body. That is the
self-keyed concealment (B_same). CROSS-authorship (B_cross) is a lossy
compression: a different author's source concedes what the headliner dropped, so
the headliner's authors may not have known (the FAO SOFO witness: the FAO report
concedes the cost side the UN brief drops). The strict tag is authorship-blind;
this probe separates the two.

Run as `python3 qualification_drop.py` to recompute and rewrite
qualification_drop.json. Run as `python3 qualification_drop.py --check` to
verify the committed file is fresh (exit 0 fresh, 1 stale, 2 missing).
"""
import json, os, sys, importlib.util
import claim_audit as CA

_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("specimens", os.path.join(_here, "specimens.py"))
S = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(S)

PROSE_SEAM = ("THESIS-OUTRUNS-EVIDENCE", "SELECTION-ON-NARRATIVE", "VACUOUS-WITNESS")
_actual = {n for n, _ in CA.CHECKS}
SEAM = {a for a in PROSE_SEAM if a in _actual}
PROSE_ONLY_SEAM = tuple(a for a in PROSE_SEAM if a not in _actual)

def classify(sp):
    r = CA.audit(sp)
    seam_fired = sorted(SEAM & set(r["flags"]))
    body_concedes = bool(sp.get("body_concedes_qualification"))
    body_hedges = bool(sp.get("body_hedges"))
    authorship = sp.get("concession_authorship")  # 'same' | 'cross' | None
    note = (sp.get("note", "") or "") + " " + (sp.get("name", "") or "")
    note_logs = "QUALIFICATION-DROP" in note
    strict_tag = body_concedes and bool(seam_fired)
    if strict_tag:
        # Cell B: known-but-hidden. Same-authorship is a self-keyed concealment
        # ("the authors knew"); cross-authorship is a lossy compression (a
        # different author's source concedes what the headliner dropped).
        if authorship == "same":
            cell = "B_same"
        elif authorship == "cross":
            cell = "B_cross"
        else:
            cell = "B_unknown"
    elif body_concedes and note_logs and not seam_fired:
        cell = "P"
    elif seam_fired and not body_concedes:
        cell = "A"
    else:
        cell = "clean"
    return {
        "name": (sp.get("name", "?") or "?")[:90],
        "cell": cell,
        "seam_fired": seam_fired,
        "body_concedes": body_concedes,
        "body_hedges": body_hedges,
        "concession_authorship": authorship,
        "note_logs_qualification_drop": note_logs,
        "strict_tag": strict_tag,
    }

rows = [classify(sp) for sp in S.SPECIMENS]
grid = {c: [r["name"] for r in rows if r["cell"] == c] for c in ("B_same", "B_cross", "B_unknown", "P", "A", "clean")}
out = {
    "tag": "QUALIFICATION-DROP",
    "definition": "the body concedes a qualification the headline/abstract drops; the strict tag (Cell B) additionally requires a seam axis to fire; Cell B is split by concession authorship (same = self-keyed concealment, cross = lossy compression)",
    "seam_set": sorted(SEAM),
    "prose_only_seam_not_an_axis": list(PROSE_ONLY_SEAM),
    "body_concession_signal": "body_concedes_qualification (the dedicated field) with concession_authorship (same/cross); body_hedges and note-string-matching remain cross-checks",
    "grid": grid,
    "rows": rows,
    "findings": [
        "the strict prose discriminator (seam AND body_hedges) = Cell B only; the tag's usage extends to Cell P (presentation-only, logged-not-flagged), which the strict definition misses",
        "VACUOUS-WITNESS is named as a seam axis in COHERENCE.md but is not an actual axis in CHECKS (prose-only)",
        "Cell B is authorship-blind in the strict tag: the 'authors knew' diagnostic holds only for B_same (self-keyed concealment, the same author hid it). B_cross (e.g. FAO SOFO: the FAO report concedes what the UN brief drops) is a lossy compression where the headliner's authors may not have known -- the concealment is not self-keyed",
    ],
}

def _dump(o):
    return json.dumps(o, indent=2, sort_keys=True)

if "--check" in sys.argv[1:]:
    path = os.path.join(_here, "qualification_drop.json")
    if not os.path.exists(path):
        print("qualification_drop.json is MISSING"); sys.exit(2)
    committed = json.load(open(path))
    if committed == out:
        print("qualification_drop.json is FRESH (matches a fresh recompute: %d specs, %d B-same, %d B-cross, %d Cell P, %d Case A)" % (
            len(rows), len(grid["B_same"]), len(grid["B_cross"]), len(grid["P"]), len(grid["A"])))
        sys.exit(0)
    print("qualification_drop.json is STALE (committed file does not match a fresh recompute):")
    for k in sorted(set(committed) | set(out)):
        if committed.get(k) != out.get(k):
            print("  - %s differs" % k)
    print("run `python3 qualification_drop.py` to regenerate, then re-run --check")
    sys.exit(1)

with open(os.path.join(_here, "qualification_drop.json"), "w") as f:
    f.write(_dump(out) + "\n")
print("wrote qualification_drop.json (%d specs: %d B-same, %d B-cross, %d Cell P, %d Case A, %d clean)" % (
    len(rows), len(grid["B_same"]), len(grid["B_cross"]), len(grid["P"]), len(grid["A"]), len(grid["clean"])))
