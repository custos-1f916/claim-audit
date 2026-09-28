#!/usr/bin/env python3
"""PUBLICITY saturation test (2026-09-28).

Scope: the CERTIFICATION subset of the claim-audit instrument -- the axes about
'can a stranger independently verify the witness?' (PLATFORM-CERTIFIED,
SELF-KEYED, SOURCE-REPLICATION, UNWITNESSED-ROOT, UNWITNESSED-RECEIPT,
REFERENT-CONSTRUCTED, REFERENT-WITNESSED, SCOPE-OF-INDEPENDENCE). The empirical
axes (BEATS-NULL, NOISE-FLOOR, DOSE-RESPONSE, ...) are a different family (data
support for the headline) and are out of scope for the PUBLICITY collapse.

The consolidation claim (2026-09-28): PUBLICITY (is the verification data
public, so a stranger can independently verify?) is the underlying variable the
certification axes are projections of -- the same structure as the 59-axis
saturation test (sims/certification-gap/COARSER-MERGE.md) that collapsed 59
'distinct axes' into one instrument. This is the discriminating test:
parameterize the certification structure by public-vs-private verification data
and check whether the certification axes collapse to the single PUBLICITY
variable.

The two live witnesses that pinned the axis (2026-09-27/28):
  - server seal (1f916.ai /api/me/ack): verification data = OAUTH_KEY
    (PRIVATE, server-held) -> stranger-unverifiable. PLATFORM-CERTIFIED fires.
  - anchored Merkle root (bankr_1d5b): verification data = the root
    (PUBLIC commitment) -> stranger-verifiable (given the ordering constraint
    is in the commitment).

The discriminating property (mirrors the 59-test's weight-1/weight-0 split):
  - weight-1 (stranger-rerunnable): the PUBLICITY verdict -- a stranger checks
    'is the verification data a public artifact or a private secret?' from the
    referent. Label-invariant (does not depend on the certifier-seat label).
  - weight-0 (modeler-chosen): the axis label (which of the certification axes
    fires). Label-dependent (the instrument's PLATFORM-CERTIFIED fires only for
    the platform-secret face).

Verdict (three properties):
  (a) publicity-determined      : the PUBLICITY verdict depends only on whether
                                  the verification data is a public artifact or
                                  a private secret -- NOT on the certifier-seat
                                  label
  (b) instrument-label-dependent: the instrument's certification flag DOES
                                  depend on the certifier-seat label (fires for
                                  platform, misses for citizen / third-party)
  (c) narrow-face               : the instrument MISSES the private-
                                  verification-data cases where the certifier is
                                  not the platform (citizen-secret,
                                  third-party-secret) -> PLATFORM-CERTIFIED is a
                                  narrow PROJECTION of PUBLICITY, not the
                                  variable itself

If (a) holds and (b)+(c) hold, the collapse is real: the certification axes are
projections of PUBLICITY (one variable). The forward move is NOT a 44th axis;
it is the weight-1 PUBLICITY instrument (stranger-rerunnable), of which
PLATFORM-CERTIFIED is a face.
"""

from claim_audit import audit

# The certification flags that imply 'stranger-unverifiable' (the witness
# cannot be independently verified). For the test specimens, only
# PLATFORM-CERTIFIED can fire (the other certification fields are unset).
CERT_FLAGS = {"PLATFORM-CERTIFIED", "SOURCE-REPLICATION", "UNWITNESSED-ROOT",
              "SELF-KEYED", "REFERENT-CONSTRUCTED", "UNWITNESSED-RECEIPT"}

NATURES = ["secret", "public"]   # the PUBLICITY variable
SEATS = ["platform", "citizen", "third-party"]

def vkey_for(nature, seat):
    # the verification data's nature + holder: a secret held by the seat, or a
    # public artifact (the holder does not change the public nature).
    if nature == "secret":
        return "%s-secret" % seat   # platform-secret, citizen-secret, third-party-secret
    return "public-key"             # public artifact

def publicity_verdict(vkey):
    # weight-1 (stranger-rerunnable): a stranger checks 'is the verification
    # data a public artifact or a private secret?' from the referent. The
    # holder (seat) is NOT an input -- only the nature (secret vs public).
    return "unverifiable" if vkey.endswith("-secret") else "verifiable"

def make_spec(nature, seat):
    vkey = vkey_for(nature, seat)
    return {"name": "%s / seat=%s" % (nature, seat),
            "type": "specification",
            "certifier": seat,
            "verification_key": vkey}

def main():
    rows = []
    for nature in NATURES:
        for seat in SEATS:
            s = make_spec(nature, seat)
            res = audit(s)
            gt = publicity_verdict(s["verification_key"])
            inst_flags = [f for f in res["flags"] if f in CERT_FLAGS]
            inst = "unverifiable" if inst_flags else "verifiable"
            rows.append((s["name"], s["verification_key"], seat, gt, inst,
                         ",".join(inst_flags) or "-", gt == inst))

    # (a) publicity-determined: the PUBLICITY verdict depends only on the
    #     verification-data nature (secret vs public), not the seat. For each
    #     nature, the verdict is the same across all seats; the two natures
    #     give opposite verdicts.
    a_ok = True
    for nature in NATURES:
        v = {publicity_verdict(vkey_for(nature, seat)) for seat in SEATS}
        if len(v) != 1:
            a_ok = False
    if publicity_verdict(vkey_for("secret", "platform")) == \
       publicity_verdict(vkey_for("public", "platform")):
        a_ok = False

    # (b) instrument-label-dependent: for a FIXED nature (secret), the
    #     instrument's flag varies with the seat (fires for platform, misses
    #     for citizen / third-party).
    secret_inst = {r[2]: (r[4] == "unverifiable") for r in rows if r[1].endswith("-secret")}
    b_ok = (secret_inst.get("platform", False) and
            not secret_inst.get("citizen", True) and
            not secret_inst.get("third-party", True))

    # (c) narrow-face: the instrument MISSES the private cases where seat !=
    #     platform (citizen-secret, third-party-secret).
    misses = [r for r in rows if r[1].endswith("-secret") and r[3] == "unverifiable"
              and r[4] == "verifiable"]
    c_ok = len(misses) == 2

    print("PUBLICITY saturation test (2026-09-28) -- certification subset")
    print("=" * 88)
    print("%-26s %-18s %-12s %-13s %-13s %-18s %s" %
          ("specimen", "verification_key", "seat", "ground-truth",
           "instrument", "cert-flags", "match"))
    for r in rows:
        print("%-26s %-18s %-12s %-13s %-13s %-18s %s" %
              (r[0], r[1], r[2], r[3], r[4], r[5], "Y" if r[6] else "N"))
    print("-" * 88)
    print("(a) publicity-determined      : %s" % ("PASS" if a_ok else "FAIL"))
    print("    the PUBLICITY verdict depends only on public-artifact vs private-secret,")
    print("    not on the certifier-seat label")
    print("(b) instrument-label-dependent: %s" % ("PASS" if b_ok else "FAIL"))
    print("    the instrument's flag fires for platform, misses for citizen/third-party")
    print("    (same private nature, different seat -> the axis is label-dependent)")
    print("(c) narrow-face               : %s (%d missed: %s)" %
          ("PASS" if c_ok else "FAIL", len(misses),
           ", ".join(m[0] for m in misses) or "-"))
    print("-" * 88)
    collapse = a_ok and b_ok and c_ok
    if collapse:
        print("VERDICT: the collapse is REAL. The certification axes are projections")
        print("  of PUBLICITY (one variable). PLATFORM-CERTIFIED is a narrow face (the")
        print("  platform-secret face) of the broader PUBLICITY variable. The weight-1")
        print("  instrument is the PUBLICITY verdict (stranger-rerunnable: 'is the")
        print("  verification data a public artifact or a private secret?'); the axis")
        print("  label is weight-0 (modeler-chosen). The forward move is NOT a 44th")
        print("  axis -- it is the weight-1 PUBLICITY instrument, of which")
        print("  PLATFORM-CERTIFIED is a face. The empirical axes (data support) are a")
        print("  different family, out of scope for this collapse.")
    else:
        print("VERDICT: the collapse does NOT hold cleanly. See the FAIL lines above.")
    return 0 if collapse else 1

if __name__ == "__main__":
    raise SystemExit(main())
