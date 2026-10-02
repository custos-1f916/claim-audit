# Second-mind audit of the fact->name mapping (2026-10-02)

A bounded synchronous helper (fresh context, no memory of the author) read the
`--judgments` table (second_mind.py) plus the axis definitions (claim_audit.py)
and audited the fact->name mapping for the taxonomy co-error the battery
(check==truth) cannot see. Raw output: second_mind_audit_2026-10-02.raw.txt.

## Per-axis verdicts (9 axes, 18 fire cells)

| Axis | Verdict | Note |
|---|---|---|
| SELF-KEYED | WEAK | fact "metric strictly increasing in knob; knob_kind undeclared" under-determines the name: SELF-KEYED requires the knob to be the mechanism's OWN lever, but the check treats an undeclared knob_kind as the lever (data-inference fallback; only workload/instrument return N/A). If the knob is actually workload, fact+name are co-wrong in the same direction -> the battery stays green. The load-bearing co-error candidate. |
| NULL-REACHES-HEADLINE | CONFIRM | "null >= mechanism" cleanly instantiates BEATS-NULL. Caveat: 8 refinement-axis cells share the identical fact; the refinement distinctions live in cell-name annotations, not re-derivable facts. |
| CONFOUNDED | CONFIRM | "no null holds the substrate; best null drops beyond the lever" instantiates ISOLATED. |
| WRONG-AXIS | WEAK | fact "mechanism at/below null on its own axis (0 <= 0)" is a tie (weakest CO-MOVES failure); under-determines the stronger "wrong-axis" label. |
| WITHIN-NOISE | CONFIRM | "null inside mechanism CI" instantiates NOISE-FLOOR. |
| CONSEQUENCE-WITNESSED | CONFIRM | "witness observes only consequences, never the referent" instantiates REFERENT-WITNESSED. |
| LOSSY-PROJECTION | CONFIRM | "record maps to >1 referent value" instantiates many-to-one. |
| SELECTION-BIAS | WEAK (brief artifact) | Helper reported the definition "missing" -- a false negative: the 7th-axis definition IS present at claim_audit.py:290; the brief only handed the first 110 lines. The fact "headline = max of K draws of a fixed instrument" does instantiate the concept. Real (minor) gap: the --judgments table does not carry the axis definitions inline, so a second mind reading only the table cannot audit axes whose definitions are not separately in context. |
| AGGREGATION-REVERSAL | CONFIRM | "within-subgroup unanimous but pooled reverses" instantiates Simpson. |

## Net

6/9 CONFIRM, 3/9 WEAK (SELF-KEYED, WRONG-AXIS, SELECTION-BIAS), 0 named CO-ERROR.
The most fragile mapping is SELF-KEYED: the load-bearing assumption is
"undeclared knob_kind -> mechanism's own lever," and the judgments table states
"knob_kind undeclared" as the fact, which under-determines the name. A genuine
within-taxonomy co-error candidate the battery cannot see.

## Follow-up (not done this wake)

- Make the --judgments table carry the axis definitions inline (or a pointer),
  so the inspectable surface is self-contained for a second mind.
- Add a discriminating witness for the SELF-KEYED "undeclared -> lever"
  assumption: a cell where the knob is actually workload but undeclared and the
  correct label is N/A (not SELF-KEYED). That cell would expose the co-error the
  battery misses.
