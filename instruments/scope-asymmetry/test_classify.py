#!/usr/bin/env python3
"""Discriminating test battery for the scope-asymmetry discriminator.

The load-bearing case is the conflation case: the monitor records the SAME
error string (github_pr_api_failed) for a hidden object and for a real API
outage. The discriminator must separate them, or it is just re-recording the
conflation.
"""
from classify import decide, classify
import json

CASES = [
    # name, target, parent, control, expected verdict
    ("live-state-2026-10-03",        404, 200, 200, "OBJECT_HIDDEN"),
    ("conflation:404-during-outage", 404, 200, 503, "API_OUTAGE"),
    ("conflation:404-control-down",  404, 200, None, "API_OUTAGE"),
    ("throttled-403",                403, 200, 200, "THROTTLED"),
    ("throttled-429-parent",         200, 429, 200, "THROTTLED"),
    ("cleared",                      200, 200, 200, "OK"),
    ("org-gone",                     404, 404, 200, "UNKNOWN"),
    ("control-gone",                 404, 200, 404, "UNKNOWN"),
    ("target-5xx",                   503, 200, 200, "API_OUTAGE"),
    ("target-timeout",               None, 200, 200, "API_OUTAGE"),
]

fails = 0
for name, t, p, c, want in CASES:
    got = decide(t, p, c)
    ok = got == want
    fails += (not ok)
    print(("PASS" if ok else "FAIL"), name, "got=%s want=%s" % (got, want))

# the classify() wrapper must agree with the tree and carry the retry flag
fake = {("repos/1f916-ai/1f916"): 404, ("orgs/1f916-ai"): 200,
        ("repos/custos-1f916/msft-cve-listing41"): 200}
r = classify(lambda ep: fake[ep])
ok = r["verdict"] == "OBJECT_HIDDEN" and r["retry_warranted"] is False \
     and r["asymmetry"] is True and r["monitor_sees"] == "github_pr_api_failed"
fails += (not ok)
print(("PASS" if ok else "FAIL"), "wrapper:object-hidden-fields",
      "got=%s" % json.dumps(r["verdict"]))

print(json.dumps({"passed": len(CASES) + 1 - fails, "failed": fails}))
raise SystemExit(1 if fails else 0)
