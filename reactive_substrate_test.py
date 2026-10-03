#!/usr/bin/env python3
"""REACTIVE-SUBSTRATE discriminating test (substrate_reactive for ISOLATED,
added 2026-10-03 from the logged-not-flagged ablation-substrate seam the
polyphonic paper 2609.36079 (Queloz & Beckmann, "A Polyphonic Conception of
AI Understanding") broke open).

The ablation axes (ISOLATED/CONFOUNDED, BEATS-NULL) model the substrate as
INERT: composition-constant = behavior-constant, so the gap between the
mechanism row and the null row is read as the mechanism's own contribution.
The polyphonic paper's signature is the opposite: a reactive coalition where
no member is indispensable, so dropping a member barely costs anything
because the coalition re-routes around it. A small gap then says nothing
about the mechanism's contribution.

The fix promotes the assumption to a spec-level variable: substrate_reactive
(bool, default false) plus reactive_gap_threshold (float, default 0.1). When
declared AND the relative gap (gap/on) is below the threshold,
check_isolated adds a LOGGED-NOT-FLAGGED note to the ISOLATED check's
"detail". It is a witness, not a flag: no new flag, no changed pass/fail, no
change to the firing set.

The discriminator is the substrate_reactive declaration, not the rows. The
polyphonic+no-polyphonic pair below differs ONLY on the substrate_reactive
field; the regression controls prove neither cell fires a new flag (the
firing set is unchanged), the declared cell adds the note, the undeclared
cell leaves the detail untouched, and a large-gap essential ablation
(monophonic control) with the declaration does NOT get the note (the gap
threshold discriminates, not just the declaration).
"""
import claim_audit

NOTE = ("reactive-substrate: the coalition re-routes around the dropped "
        "member")

# Shared shape: the polyphonic redundant-member ablation (2609.36079
# signature). The substrate is a multi-member coalition; dropping M costs
# little (0.90 -> 0.85) because the coalition routes around it. The gap is
# small (relative 0.0556 < 0.1), so the ablation is uninformative about M's
# contribution. ISOLATED passes (a null drops only the lever) and BEATS-NULL
# passes (0.9 > 0.85); no flag fires on either axis.
ROWS_POLY = [
    {"label": "full coalition (M on)", "mechanism_on": True,
     "substrate": ["M", "coal_A", "coal_B"], "metric": 0.90},
    {"label": "M dropped (coalition routes around)", "mechanism_on": False,
     "is_null": True, "substrate": ["coal_A", "coal_B"], "metric": 0.85},
]

BASE = dict(name="polyphonic redundant-member ablation (2609.36079 signature)",
            type="ablation", mechanism_lever="M", rows=ROWS_POLY)
A = dict(BASE, substrate_reactive=True)   # substrate_reactive declared
B = dict(BASE)                            # substrate_reactive undeclared

res_a = claim_audit.audit(A)
res_b = claim_audit.audit(B)

ok = True

# Neither cell fires a new flag (the note is a witness, not a flag; the
# firing set is unchanged in every cell).
for label, res in [("A (substrate_reactive declared)", res_a),
                   ("B (substrate_reactive undeclared)", res_b)]:
    got = list(res["flags"])
    good = (got == [])
    ok = ok and good
    print("%s %s fires no flags (flags=%r, want [])"
          % ("PASS" if good else "FAIL", label, got))

# Both cells are in the ISOLATED pass branch: the note is a logged-not-flagged
# witness on a PASSING check, not a flag.
for label, res in [("A", res_a), ("B", res_b)]:
    p = res["checks"]["ISOLATED"]["pass"]
    good = (p is True)
    ok = ok and good
    print("%s %s ISOLATED passes (pass=%r)" % ("PASS" if good else "FAIL", label, p))

# The declared cell adds the logged-not-flagged note to the ISOLATED detail.
det_a = res_a["checks"]["ISOLATED"]["detail"]
good = (NOTE in det_a)
ok = ok and good
print("%s A detail carries the reactive-substrate note (detail=%r)"
      % ("PASS" if good else "FAIL", det_a))

# The undeclared cell leaves the detail untouched (no note).
det_b = res_b["checks"]["ISOLATED"]["detail"]
good = (NOTE not in det_b)
ok = ok and good
print("%s B detail has no reactive-substrate note (detail=%r)"
      % ("PASS" if good else "FAIL", det_b))

# The polyphonic+no-polyphonic pair must differ ONLY on the
# substrate_reactive field.
diff = {k for k in set(A) | set(B) if A.get(k) != B.get(k)}
pair_ok = diff == {"substrate_reactive"}
ok = ok and pair_ok
print("%s substrate_reactive pair differs only on substrate_reactive (differs on %s)"
      % ("PASS" if pair_ok else "FAIL", ", ".join(sorted(diff))))

# Monophonic essential control: a large-gap ablation (0.90 -> 0.10, relative
# 0.889 >= 0.1) WITH the declaration must NOT get the note. This proves the
# gap threshold discriminates (a small gap is what makes the ablation
# uninformative), not just the declaration.
ROWS_MONO = [
    {"label": "M on", "mechanism_on": True, "substrate": ["M", "base"], "metric": 0.90},
    {"label": "M dropped (sole member)", "mechanism_on": False, "is_null": True,
     "substrate": ["base"], "metric": 0.10},
]
C = dict(name="monophonic essential ablation (control)", type="ablation",
         mechanism_lever="M", rows=ROWS_MONO, substrate_reactive=True)
res_c = claim_audit.audit(C)
det_c = res_c["checks"]["ISOLATED"]["detail"]
good = (NOTE not in det_c) and (res_c["flags"] == [])
ok = ok and good
print("%s C (monophonic essential, declared) has no note and no flags (detail=%r, flags=%r)"
      % ("PASS" if good else "FAIL", det_c, res_c["flags"]))

print("ALL PASS" if ok else "SOME FAIL")
raise SystemExit(0 if ok else 1)
