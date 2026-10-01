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
    note = (sp.get("note", "") or "") + " " + (sp.get("name", "") or "")
    note_logs = "QUALIFICATION-DROP" in note
    strict_tag = body_concedes and bool(seam_fired)
    if strict_tag:
        cell = "B"
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
        "note_logs_qualification_drop": note_logs,
        "strict_tag": strict_tag,
    }

rows = [classify(sp) for sp in S.SPECIMENS]
grid = {c: [r["name"] for r in rows if r["cell"] == c] for c in ("B", "P", "A", "clean")}
out = {
    "tag": "QUALIFICATION-DROP",
    "definition": "the body concedes a qualification the headline/abstract drops; the strict tag (Cell B) additionally requires a seam axis to fire",
    "seam_set": sorted(SEAM),
    "prose_only_seam_not_an_axis": list(PROSE_ONLY_SEAM),
    "body_concession_signal": "body_hedges (the named proxy; a dedicated body_concedes_qualification field is the future refinement the probe's Cell P motivates)",
    "grid": grid,
    "rows": rows,
    "findings": [
        "the strict prose discriminator (seam AND body_hedges) = Cell B only; the tag's usage extends to Cell P (presentation-only, logged-not-flagged), which the strict definition misses",
        "VACUOUS-WITNESS is named as a seam axis in COHERENCE.md but is not an actual axis in CHECKS (prose-only)",
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
        print("qualification_drop.json is FRESH (matches a fresh recompute: %d specs, %d Cell B, %d Cell P, %d Case A)" % (
            len(rows), len(grid["B"]), len(grid["P"]), len(grid["A"])))
        sys.exit(0)
    print("qualification_drop.json is STALE (committed file does not match a fresh recompute):")
    for k in sorted(set(committed) | set(out)):
        if committed.get(k) != out.get(k):
            print("  - %s differs" % k)
    print("run `python3 qualification_drop.py` to regenerate, then re-run --check")
    sys.exit(1)

with open(os.path.join(_here, "qualification_drop.json"), "w") as f:
    f.write(_dump(out) + "\n")
print("wrote qualification_drop.json (%d specs: %d Cell B, %d Cell P, %d Case A, %d clean)" % (
    len(rows), len(grid["B"]), len(grid["P"]), len(grid["A"]), len(grid["clean"])))
