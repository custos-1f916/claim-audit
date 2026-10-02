#!/usr/bin/env python3
"""POLARITY discriminating test (metric_polarity for BEATS-NULL, added
2026-10-02 from the logged-not-flagged BEATS-NULL polarity-blindness seam).

The BEATS-NULL axis (NULL-REACHES-HEADLINE) is polarity-blind by design: it
reads max(mech) > max(null) as "mechanism beats null" regardless of which
direction is good. For a cost metric (lower = better, e.g. TV distance), this
inverts: max(mech) > max(null) means the mechanism is WORSE than the null (the
bad direction), yet the axis passes. The direction is not a flaw in itself; it
is the author's judgment.

The fix promotes the assumption to a spec-level variable: metric_polarity
(values "higher-is-better" [default], "lower-is-better"). When declared AND the
beat is in the bad direction (for "lower-is-better": max(mech) > max(null), the
mechanism is worse than the null), check_beats_null adds a LOGGED-NOT-FLAGGED
note to the BEATS-NULL check's "detail". It is a witness, not a flag: no new
flag, no changed pass/fail, no change to the firing set.

The discriminator is the metric_polarity declaration, not the rows. The
polarity+no-polarity pair below differs ONLY on the metric_polarity field; the
regression controls prove neither cell fires NULL-REACHES-HEADLINE (the metric
distinguishes the rows), the declared cell adds the note, and the undeclared
cell leaves the detail untouched.
"""
import claim_audit

NOTE = ("polarity: the beat is in the bad direction (mechanism worse than "
        "null); the good-direction judgment is the author's, not the "
        "instrument's")

# Shared shape: a cost metric (lower = better, e.g. TV distance) where the
# mechanism is WORSE than the null (max(mech) 0.157 > max(null) 0.0054, the
# bad direction). The metric distinguishes the rows, so BEATS-NULL passes
# (polarity-blind) and NULL-REACHES-HEADLINE does not fire.
ROWS = [
    {"label": "mechanism (cost metric, higher = worse)", "mechanism_on": True, "substrate": ["confidence"], "metric": 0.157},
    {"label": "null (cost metric)", "mechanism_on": False, "is_null": True, "substrate": ["independent-draw"], "metric": 0.0054},
]

BASE = dict(metric="TV distance (cost metric, lower = better)", rows=ROWS)
A = dict(BASE, metric_polarity="lower-is-better")  # polarity declared
B = dict(BASE)                                     # polarity undeclared

res_a = claim_audit.audit(A)
res_b = claim_audit.audit(B)

ok = True

# Neither cell fires NULL-REACHES-HEADLINE (the metric distinguishes the rows).
for label, res in [("A (polarity declared)", res_a), ("B (polarity undeclared)", res_b)]:
    got = "NULL-REACHES-HEADLINE" in set(res["flags"])
    good = (not got)
    ok = ok and good
    print("%s %s does not fire NULL-REACHES-HEADLINE (got %r, want False)"
          % ("PASS" if good else "FAIL", label, got))

# Both cells are in the pass branch (h > n): the note is a logged-not-flagged
# witness on a PASSING check, not a flag.
for label, res in [("A", res_a), ("B", res_b)]:
    p = res["checks"]["BEATS-NULL"]["pass"]
    good = (p is True)
    ok = ok and good
    print("%s %s BEATS-NULL passes (pass=%r)" % ("PASS" if good else "FAIL", label, p))

# The declared cell adds the logged-not-flagged note to the BEATS-NULL detail.
det_a = res_a["checks"]["BEATS-NULL"]["detail"]
good = (NOTE in det_a)
ok = ok and good
print("%s A detail carries the polarity note (detail=%r)"
      % ("PASS" if good else "FAIL", det_a))

# The undeclared cell leaves the detail untouched (no note).
det_b = res_b["checks"]["BEATS-NULL"]["detail"]
good = (NOTE not in det_b)
ok = ok and good
print("%s B detail has no polarity note (detail=%r)"
      % ("PASS" if good else "FAIL", det_b))

# The polarity+no-polarity pair must differ ONLY on the metric_polarity field.
diff = {k for k in set(A) | set(B) if A.get(k) != B.get(k)}
pair_ok = diff == {"metric_polarity"}
ok = ok and pair_ok
print("%s polarity+no-polarity pair differs only on metric_polarity (differs on %s)"
      % ("PASS" if pair_ok else "FAIL", ", ".join(sorted(diff))))

print("ALL PASS" if ok else "SOME FAIL")
raise SystemExit(0 if ok else 1)
