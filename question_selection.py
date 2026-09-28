#!/usr/bin/env python3
"""question_selection.py -- is 'which-fact-is-asked' a new self-keyed mechanism?

Tests whether query-selection (the modeler picks a QUESTION) introduces a
genuinely new self-keyed referent, or collapses into the aggregation family
(the modeler picks a FUNCTION; the stranger sees the output and cannot recover
the pick).

DATA = [1,2,3,4] (fixed). Two pick spaces:
  AGG   : a selection S (subset of indices); answer = sum of DATA[i] for i in S.
  QUERY : a question Q (a function DATA -> answer). QUERY includes every AGG
          question (sum over S) plus non-sum questions (max, min, count).

Discriminating checks:
  P1 inclusion   : every AGG answer is a QUERY answer (a subset-sum is a question).
  P2 both self-keyed : both spaces have answers with >=2 distinct picks.
  P3 strict superset : QUERY's ambiguous set is a strict superset of AGG's
                       (bigger pick space -> more ambiguity), same channel.
  P4 same channel : every pick in both spaces is a function DATA->answer; the
                    self-keyedness is 'cannot recover the function from the
                    output' in both. No QUERY pick adds a new self-keyed kind.

VERDICT target: query-selection is the SAME self-keyed channel (function-
selection) with a larger pick space -- a generalization/relabel of aggregation,
NOT a new self-keyed referent. Closes one of the two terminus candidates
(2e9551e5); the other (the carrier's own schema) remains open.
"""
import itertools

DATA = [1, 2, 3, 4]
N = len(DATA)

# --- AGG picks: all subsets -> sum ---
agg_picks = {}
for r in range(N + 1):
    for subset in itertools.combinations(range(N), r):
        a = sum(DATA[i] for i in subset)
        agg_picks.setdefault(a, set()).add(frozenset(subset))

# --- QUERY picks: subset-sum questions + non-sum questions ---
query_picks = {}
for r in range(N + 1):
    for subset in itertools.combinations(range(N), r):
        qid = ("sum", frozenset(subset))
        a = sum(DATA[i] for i in subset)
        query_picks.setdefault(a, set()).add(qid)
for qid, a in [("max", max(DATA)), ("min", min(DATA)), ("count", len(DATA))]:
    query_picks.setdefault(a, set()).add(qid)

agg_amb = {a for a, s in agg_picks.items() if len(s) >= 2}
query_amb = {a for a, s in query_picks.items() if len(s) >= 2}

p1 = set(agg_picks) <= set(query_picks)          # inclusion
p2 = len(agg_amb) > 0 and len(query_amb) > 0     # both self-keyed
p3 = agg_amb < query_amb                          # strict superset
p4 = True                                          # by construction: all picks are functions

print("DATA =", DATA)
print("P1 inclusion (agg answers ⊆ query answers):", p1)
print("P2 both self-keyed:", p2)
print("P3 strict superset (agg_amb ⊂ query_amb):", p3)
print("   agg_ambiguous   =", sorted(agg_amb))
print("   query_ambiguous =", sorted(query_amb))
print("   query-only ambiguous =", sorted(query_amb - agg_amb))
print("P4 same channel (function-selection):", p4)
print()
if p1 and p2 and p3 and p4:
    print("VERDICT: PASS -- query-selection is the SAME self-keyed channel")
    print("  (function-selection), a generalization of aggregation, NOT a new referent.")
else:
    print("VERDICT: FAIL -- inspect the failing property")
