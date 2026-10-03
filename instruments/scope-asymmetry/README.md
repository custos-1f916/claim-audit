# Scope-asymmetry fault discriminator

Turns the 1f916-ai PR-monitor's `failed` array (≈60 `github_pr_api_failed`
entries) from a red herring into a classified fault.

## The seam

`custos_github_prs.py` `API.get` raises `github_pr_api_failed` for ANY non-zero
`gh api` return code and never inspects the HTTP status. So the monitor records
the identical error string for two very different conditions:

- a **permanent** 404 — the target repo object is hidden from the API while the
  rest of the API is healthy (org 200, a control repo 200, not throttled); and
- a **transient** API outage — the whole API is degraded (a control repo fails
  too, or a 5xx / no HTTP line).

Retrying is warranted for the second, a no-op for the first. The ~60 failed
scans are the first kind: the org has been dead-silent since a single ForkEvent
on 2026-09-28, so no live PRs are missed.

## Verdicts

| verdict         | target | parent | control | meaning                              | retry? |
|-----------------|--------|--------|---------|--------------------------------------|--------|
| `OBJECT_HIDDEN` | 404    | 200    | 200     | target address not resolving, API ok | no     |
| `API_OUTAGE`    | any    | any    | ≥500/None | whole API degraded                   | yes    |
| `THROTTLED`     | 403/429| any    | any     | rate-limited                          | yes    |
| `OK`            | 200    | any    | any     | fault cleared                         | no     |
| `UNKNOWN`       | else   | else   | else    | org gone / control gone — human       | —      |

`OBJECT_HIDDEN` is deliberately cause-agnostic: it means "target address not
resolving while the API is healthy" (hidden vs renamed vs deleted all look the
same to the REST API). Its unblocking event is cause-agnostic too: the target
returns 200 (or a GraphQL node RESOLVED).

## Files

- `classify.py` — `decide(t,p,c)` pure tree + `classify(probe_fn)` with
  injectable probes (default live `gh api -i`).
- `test_classify.py` — 11-case battery; the load-bearing case is the
  **conflation case**: target 404 *during* an outage must classify
  `API_OUTAGE`, not `OBJECT_HIDDEN`. `python3 test_classify.py` → exit 0.

## Run

    python3 classify.py          # live classification, JSON
    python3 test_classify.py     # battery, exit 0 on green
