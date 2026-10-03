#!/usr/bin/env python3
"""Scope-asymmetry fault discriminator for the 1f916-ai PR-monitor blindness.

The monitor (custos_github_prs.py API.get) raises github_pr_api_failed for ANY
non-zero `gh api` return code and never inspects the HTTP status, so a
permanent 404 (object hidden) is indistinguishable from a transient 5xx. This
instrument separates the two using scope-asymmetry:

  OBJECT_HIDDEN  target 404 while parent org and a control repo both return
                 200 and nothing is rate-limited. Permanent. Retrying the
                 scan is a no-op; the unblocking event is the target returning
                 200 (or a GraphQL node RESOLVED). No live PRs are missed.
  API_OUTAGE     the control repo also fails (5xx / no HTTP line). Transient;
                 the whole API is degraded. Retrying is warranted.
  THROTTLED      a 403/429 on any probe. Transient; wait for the rate window.
  OK             target 200. The fault has cleared.
  UNKNOWN        anything else (org itself missing, control repo missing).
                 Needs a human, not a retry loop.

The pure decision tree is `decide(target, parent, control)`; the live probes
are injectable, so the conflation case (target 404 during an outage) is
testable without the network.
"""
import json
import re
import subprocess

TARGET = "repos/1f916-ai/1f916"
PARENT = "orgs/1f916-ai"
CONTROL = "repos/custos-1f916/msft-cve-listing41"

MONITOR_ERROR = "github_pr_api_failed"  # what the monitor records for all of these


def decide(target, parent, control):
    """Pure decision tree over three HTTP statuses (int or None = no line)."""
    if any(s in (403, 429) for s in (target, parent, control)):
        return "THROTTLED"
    if target == 200:
        return "OK"
    if target == 404 and parent == 200 and control == 200:
        return "OBJECT_HIDDEN"
    if (target is None or parent is None or control is None
            or control >= 500 or target >= 500):
        return "API_OUTAGE"
    return "UNKNOWN"


def _status_of(result):
    for line in (result.stdout + result.stderr).splitlines():
        m = re.match(r"HTTP/\S+\s+(\d{3})", line)
        if m:
            return int(m.group(1))
    return None


def probe(endpoint, timeout=15):
    try:
        r = subprocess.run(["gh", "api", "-i", endpoint],
                           capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None
    return _status_of(r)


def classify(probe_fn=probe):
    t = probe_fn(TARGET)
    p = probe_fn(PARENT)
    c = probe_fn(CONTROL)
    verdict = decide(t, p, c)
    return {
        "verdict": verdict,
        "monitor_sees": MONITOR_ERROR,
        "asymmetry": (t == 404 and p == 200 and c == 200),
        "retry_warranted": verdict in ("API_OUTAGE", "THROTTLED"),
        "unblocking_event": {
            "OBJECT_HIDDEN": "target repo returns 200 (or GraphQL node RESOLVED)",
            "API_OUTAGE": "control repo returns 200",
            "THROTTLED": "rate window clears",
            "OK": "n/a (cleared)",
            "UNKNOWN": "human review",
        }[verdict],
        "probes": {"target": t, "parent": p, "control": c},
    }


if __name__ == "__main__":
    print(json.dumps(classify(), indent=2))
