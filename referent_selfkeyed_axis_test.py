#!/usr/bin/env python3
"""REFERENT-SELF-KEYED discriminating test (2026-10-02, 63rd axis).

referent_selfkeyed_test.py (4976ead) proved the ESCAPE: at the closing act the
writer declares BOTH sides of the FIDELITY byte-match, so they can re-label
referent_value == reading and make FIDELITY pass regardless of whether the
reading faithfully represents the reasoning performed. The full instrument was
blind to the relabel (0 fired).

This test builds the weight-1 REFERENT-SELF-KEYED instrument (the
stranger-rerunnable question "is the referent_value self-declared by the
writer?") and runs the discriminating cases that decide whether it is a
GENUINELY NEW axis or a relabeling of an existing one. The discriminating
structure:

  - The gap: the writer holds the referent_value declaration (referent_source
    = "self-declared"), so they can re-label it to match the reading.
  - The closure: an externally-witnessed referent_value (referent_source =
    "externally-witnessed") is anchored outside the writer's own declaration,
    so the writer cannot re-label it.

Independence to prove (each is a row where the candidate axis fires but the
existing axis it could be a relabeling of does NOT):

  1. vs FIDELITY: the relabel row. referent_value == reading (FIDELITY passes)
     AND referent_source = self-declared (REFERENT-SELF-KEYED fires). If
     REFERENT-SELF-KEYED were just FIDELITY, this row would be silent.
  2. vs TRUST: writer_trust = independently-established (TRUST N/A, the
     authority channel is closed) AND referent_source = self-declared
     (REFERENT-SELF-KEYED fires). If it were just TRUST, this row would be
     silent.
  3. vs the what-is-recorded terminus: no data rows (LOSSY-PROJECTION N/A, the
     lossy-function channel does not apply) AND referent_source = self-declared
     (REFERENT-SELF-KEYED fires). If it were just what-is-recorded, this row
     would be silent.

Pass cell: referent_source = externally-witnessed -> REFERENT-SELF-KEYED N/A
(the gap is closed: the writer cannot re-label an anchored referent).
"""
import sys
import claim_audit as ca

ok = True
def check(label, got, want):
    global ok
    good = (got == want)
    ok = ok and good
    print("%s %s (got %r, want %r)" % ("PASS" if good else "FAIL", label, got, want))

R  = "differential: ruled out A, B; chose X on finding F"
Rp = "differential: ruled out A; chose X on finding F"  # distorted copy (omits B)

# Row 1: the relabel row. referent_value == reading (FIDELITY passes),
# referent_source = self-declared (REFERENT-SELF-KEYED fires).
relabel = {"name": "relabel", "pathway_log_emitted": True,
           "referent_value": Rp, "reading": Rp, "referent_source": "self-declared"}
res = ca.audit(relabel)
check("relabel: FIDELITY passes (referent_value == reading)",
      res["checks"]["FIDELITY"]["pass"], True)
check("relabel: REFERENT-SELF-KEYED fires (self-declared referent)",
      res["checks"]["REFERENT-SELF-KEYED"]["pass"], False)
check("relabel: REFERENT-SELF-KEYED in flags",
      "REFERENT-SELF-KEYED" in res["flags"], True)

# Row 2: independence from TRUST. writer_trust = independently-established
# (TRUST N/A) AND referent_source = self-declared (REFERENT-SELF-KEYED fires).
trust_closed = {"name": "trust-closed", "pathway_log_emitted": True,
                "referent_value": Rp, "reading": Rp,
                "writer_trust": "independently-established",
                "referent_source": "self-declared"}
res = ca.audit(trust_closed)
check("trust-closed: TRUST N/A (writer_trust independently established)",
      res["checks"]["TRUST"]["pass"], True)
check("trust-closed: REFERENT-SELF-KEYED still fires (independent of TRUST)",
      res["checks"]["REFERENT-SELF-KEYED"]["pass"], False)

# Row 3: independence from the what-is-recorded terminus. No data rows
# (LOSSY-PROJECTION N/A) AND referent_source = self-declared (fires).
no_rows = {"name": "no-rows", "pathway_log_emitted": True,
           "referent_value": Rp, "reading": Rp, "referent_source": "self-declared"}
res = ca.audit(no_rows)
check("no-rows: LOSSY-PROJECTION N/A (no data rows; the lossy-function channel does not apply)",
      res["checks"]["LOSSY-PROJECTION"]["pass"], True)
check("no-rows: REFERENT-SELF-KEYED still fires (independent of what-is-recorded)",
      res["checks"]["REFERENT-SELF-KEYED"]["pass"], False)

# Pass cell: externally-witnessed referent. The writer cannot re-label an
# anchored referent_value, so the referent-declaration gap is closed.
anchored = {"name": "anchored", "pathway_log_emitted": True,
            "referent_value": R, "reading": Rp,
            "referent_source": "externally-witnessed"}
res = ca.audit(anchored)
check("anchored: REFERENT-SELF-KEYED N/A (externally-witnessed; gap closed)",
      res["checks"]["REFERENT-SELF-KEYED"]["pass"], True)
check("anchored: FIDELITY still fires (the distorted copy is caught by the byte-match)",
      res["checks"]["FIDELITY"]["pass"], False)

# Schema-boundary: referent_source undeclared -> N/A (does not infer).
undeclared = {"name": "undeclared", "pathway_log_emitted": True,
              "referent_value": Rp, "reading": Rp}
res = ca.audit(undeclared)
check("undeclared: REFERENT-SELF-KEYED N/A (referent_source not declared)",
      res["checks"]["REFERENT-SELF-KEYED"]["pass"], True)

print()
if ok:
    print("ALL CHECKS PASSED: REFERENT-SELF-KEYED is a genuinely new axis.")
    print("It fires on the self-declared referent_value declaration and is")
    print("independent of FIDELITY (the relabel row: FIDELITY passes, this fires),")
    print("TRUST (authority closed, this fires), and the what-is-recorded terminus")
    print("(no data rows, this fires). The externally-witnessed referent is the")
    print("pass cell: the writer cannot re-label an anchored referent_value, so the")
    print("referent-declaration gap is closed. The self-keyed family now has a fourth")
    print("channel (referent self-declaration) independent of openness, lossiness, and")
    print("source authority.")
    sys.exit(0)
else:
    print("SOME CHECKS FAILED")
    sys.exit(1)
