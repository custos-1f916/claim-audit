# The three 2026-09-15 specimens (faithful to sims/{avg-farmer-illusion,busma,
# vibe-design}) plus a clean control. Numbers are the papers' own headline
# values as recorded in those sims.
SPECIMENS = [
  {
    "name": "vibe-design (2609.15078)",
    "type": "knob-sweep",
    "mechanism": "temperature-scaled selector increases proposal diversity",
    "metric": "coverage (exploration breadth)",
    "knob": "tau (selector temperature)",
    "mechanism_axis": "judged quality (W/L)",
    "rows": [
      {"label":"tau=0.5","mechanism_on":True,"substrate":["vs_k3","generator"],"knob":0.5,"metric":2.10,"mechanism_axis":1.10},
      {"label":"tau=1.0","mechanism_on":True,"substrate":["vs_k3","generator"],"knob":1.0,"metric":2.59,"mechanism_axis":1.10},
      {"label":"tau=2.0","mechanism_on":True,"substrate":["vs_k3","generator"],"knob":2.0,"metric":2.84,"mechanism_axis":1.10},
      {"label":"tau=3.0","mechanism_on":True,"substrate":["vs_k3","generator"],"knob":3.0,"metric":2.87,"mechanism_axis":1.00},
      {"label":"tau=5.0","mechanism_on":True,"substrate":["vs_k3","generator"],"knob":5.0,"metric":2.94,"mechanism_axis":0.90},
    ],
    "expected": ["SELF-KEYED","WRONG-AXIS"],
    "note": "proposal set (K=3) never changes with tau; one fixed weight vector reproduces the whole coverage curve (residual 0.0025). quality plateaus/reverses while coverage keeps rising."
  },
  {
    "name": "busma (2609.15054)",
    "type": "ablation",
    "mechanism": "structured communication intents (the bus)",
    "mechanism_lever": "bus",
    "metric": "task accuracy",
    "rows": [
      {"label":"BusMA (no verifier tool)","mechanism_on":True,"substrate":["chair","bus","shared_mem","worker"],"metric":70.0},
      {"label":"SmolAgents (no verifier tool)","mechanism_on":False,"is_null":True,"substrate":["worker"],"metric":70.0},
      {"label":"BusMA + verifier tool","mechanism_on":True,"substrate":["chair","bus","shared_mem","worker","tool"],"metric":94.0},
      {"label":"SmolAgents + verifier tool","mechanism_on":False,"is_null":True,"substrate":["worker","tool"],"metric":94.0},
    ],
    "expected": ["NULL-REACHES-HEADLINE","CONFOUNDED"],
    "note": "bus==single at every tool-availability (70==70, 94==94); the positive gap requires the manager to NOT verify. turning the bus off also drops chair+shared_mem, so the ablation never isolates the intents from the substrate."
  },
  {
    "name": "avg-farmer (2609.15038)",
    "type": "cross-model",
    "mechanism": "person-level LM agent predictions",
    "metric": "KS similarity (marginal axis)",
    "mechanism_axis": "person-level skill (MAE skill vs median null)",
    "rows": [
      {"label":"agent best (Africa)","mechanism_on":True,"substrate":["lm_agent"],"metric":0.862,"mechanism_axis":-0.002},
      {"label":"agent best (Quzhou)","mechanism_on":True,"substrate":["lm_agent"],"metric":0.783,"mechanism_axis":-0.097},
      {"label":"null distribution-only (Africa)","mechanism_on":False,"is_null":True,"substrate":["distribution_fit"],"metric":0.943,"mechanism_axis":0.0},
      {"label":"null distribution-only (Quzhou)","mechanism_on":False,"is_null":True,"substrate":["distribution_fit"],"metric":0.920,"mechanism_axis":0.0},
    ],
    "expected": ["NULL-REACHES-HEADLINE","WRONG-AXIS"],
    "note": "a distribution-only reference (zero person info) beats all 24 agent configs on the headline KS; the agents' person-level axis sits at the median-null baseline (skill ~0)."
  },
  {
    "name": "control (clean retrieval ablation)",
    "type": "ablation",
    "mechanism": "retrieval",
    "mechanism_lever": "retrieval",
    "metric": "recall",
    "rows": [
      {"label":"with retrieval","mechanism_on":True,"substrate":["index","retrieval"],"metric":0.80},
      {"label":"without retrieval","mechanism_on":False,"is_null":True,"substrate":["index"],"metric":0.30},
    ],
    "expected": [],
    "note": "synthetic control: the null holds the index and drops only the retrieval lever; the mechanism beats the null on the headline. Shows the instrument is not a fail-everything machine."
  },
  {
    "name": "square post 5399 (09-15 draw, partial)",
    "type": "cross-model",
    "mechanism": "the register's shapes are sufficient for analytical posts (the register holds on the population)",
    "metric": "fit rate (fraction of analytical posts fitting an existing register shape)",
    "mechanism_axis": "population coverage (fraction of the 343-population the verdict actually rests on)",
    "rows": [
      {
        "label": "sample (8/343 read): 4 analytical, all fit",
        "mechanism_on": True,
        "substrate": [
          "admission_test",
          "register_shapes"
        ],
        "metric": 1.0,
        "mechanism_axis": 0.023
      },
      {
        "label": "population (343): fit rate not established by the sample",
        "mechanism_on": False,
        "is_null": True,
        "substrate": [
          "admission_test",
          "register_shapes"
        ],
        "metric": 0.0,
        "mechanism_axis": 0.023
      }
    ],
    "expected": [
      "WRONG-AXIS"
    ],
    "note": "LIVE SPECIMEN, a different artifact class than the three papers (a self-aware community post, not arXiv). The headline '343 posts, 4 analytical, all four fit the register' yokes a population-sized frame to a sample-sized verdict (8/343 = 0.023 coverage). The instrument flags the HEADLINE as WRONG-AXIS: the sample fit rate (1.0) is real but sits on the wrong axis for a population-sufficiency claim; the axis that actually matters (population coverage) is at null. The post's own body is the correction ('I will not let it read as 343') -- the instrument and the author agree on where the seam is. The population-estimate error (250 -> 343) is the author's self-specimen; noted, not forced into a flag."
  },
  {
    "name": "retention instrument OWN headline (four-axis meaning, self-specimen)",
    "type": "ablation",
    "mechanism": "the four-axis binding check (verify_meaning): every stale binding -> unknown, never inherited green",
    "mechanism_lever": "four_axis_check",
    "metric": "fraction of stale binding axes caught as unknown (not inherited green)",
    "rows": [
      {"label":"meaning (four-axis)","mechanism_on":True,"substrate":["receipt","world","four_axis_check"],"knob":4.0,"metric":1.0,"mechanism_axis":1.0},
      {"label":"persistence_only (inherits recorded verdict)","mechanism_on":False,"is_null":True,"substrate":["receipt","world"],"knob":0.0,"metric":0.0,"mechanism_axis":0.0},
      {"label":"reevaluation (live predicate only)","mechanism_on":False,"is_null":True,"substrate":["receipt","world"],"knob":1.0,"metric":0.25,"mechanism_axis":0.25}
    ],
    "expected": ["SELF-KEYED"],
    "note": "LIVE SELF-SPECIMEN: claim-audit run on the retention instrument's OWN headline. The headline 'meaning is four-axis: every stale binding -> unknown' is the DEFINITION of the four-axis check, so the metric (fraction of stale axes caught) is monotone in the mechanism's own control knob (axes checked 0/1/4 -> 0.0/0.25/1.0, read off the retention instrument's own SWEEP table). The instrument flags its own headline SELF-KEYED (spearman +1.000): the four-axis claim is a tautology (a specification of the verifier), not an empirical measurement. BEATS-NULL/ISOLATED/CO-MOVES all pass, so the instrument discriminates on the COMPARATIVE axis (the SWEEP: four-axis beats persistence_only and reevaluation) but flags its own HEADLINE as self-keyed. The meta-finding: the instrument catches the exact self-keying it was built to catch, in itself."
  },
  {
    "name": "update-admission audit (2609.10873)",
    "type": "ablation",
    "mechanism": "paired-binomial construction (certifies retention by paying for the CHANGE, ~1/eps samples, not the LEVEL, ~1/eps^2)",
    "mechanism_lever": "pairing",
    "metric": "fraction of updates admitted (retained learning opportunity) at matched budget",
    "rows": [
      {"label":"paired gate @ B=2000 (81/256)","mechanism_on":True,"substrate":["update_stream","budget_2000"],"metric":0.3164},
      {"label":"range-based Hoeffding gate @ B=2000 (0/256)","mechanism_on":False,"is_null":True,"substrate":["update_stream","budget_2000"],"metric":0.0},
    ],
    "expected": [],
    "note": "LIVE EXTERNAL SPECIMEN (second in the arc; first REAL paper to land DISCRIMINATES). The paired-vs-range-based comparison is a clean categorical lever (construction type) with a matched substrate (same fixed contract stream, same budget B=2000, same (eps,beta)=0.05 contract, 0 observed violations for either). BEATS-NULL: 0.3164 (81/256) > 0.0 (0/256). NOT-SELF-KEYED: N/A (categorical lever; the budget is a TREATMENT DOSE, not the mechanism's own knob -- the gap is maximal at low budget and narrows at B=20000 where even the range gate certifies, 229/256 vs 195/256 vs 0). ISOLATED: the null drops only the lever 'pairing', substrate held. CO-MOVES: N/A (the error-control axis is the SHARED substrate -- both gates certify at the same (eps,beta) with 0 observed violations -- not the mechanism's orthogonal axis; the mechanism is supposed to move the admission axis while holding error control constant). Verdict DISCRIMINATES: the instrument is not a fail-everything machine on real papers; it rewards a well-designed ablation (categorical lever + matched substrate + clear headline gap). Meta-finding, consistent with the portfolio census: comparative/ablation claims with a clean lever pass; self-keyed and axis-count claims fail. Load-bearing mechanism verified independently: the gap is the 1/eps vs 1/eps^2 sample-complexity scaling (paired pays for the CHANGE, range-based pays for the LEVEL); the paper uses eps=0.05 where the ratio is ~20-59x depending on interval constants (my 40x/4794/120 at eps=0.025 is a re-derivation, not the paper's number). Honest limits: (1) fraction-admitted is the paper's empirical demonstration of the deeper sample-complexity claim, which the instrument does not independently verify; (2) the paper concedes the gate is not the best learner -- closed-loop replay reaches 100% final success vs the paired gate's 59.6% (Table 1), so the gate's value is error-controlled opportunity counting, not optimal learning; the paper itself frames these as 'admission diagnostics, not claims of resource-optimal policy learning.'"
  },
  {
    "name": "MERIT memory floor (2609.05441)",
    "type": "ablation",
    "mechanism": "memory presence (C1-C5 have a memory system; C0 has none) on tasks verified to depend on earlier-episode facts",
    "mechanism_lever": "memory",
    "metric": "dependent-task TSR (task success rate on leak-verified dependent tasks, easy tier)",
    "rows": [
      {"label":"C0 no memory, dependent tasks, easy (leak-verified floor)","mechanism_on":False,"is_null":True,"substrate":["task_grid","model","tools","probe"],"metric":0.0},
      {"label":"C1 full replay, dependent tasks, easy (max D1/D2/D3)","mechanism_on":True,"substrate":["task_grid","model","tools","probe","memory"],"metric":1.0},
      {"label":"C2 retrieval, dependent tasks, easy (max)","mechanism_on":True,"substrate":["task_grid","model","tools","probe","memory"],"metric":1.0},
      {"label":"C3 summary, dependent tasks, easy (max)","mechanism_on":True,"substrate":["task_grid","model","tools","probe","memory"],"metric":1.0},
      {"label":"C4 facts, dependent tasks, easy (max)","mechanism_on":True,"substrate":["task_grid","model","tools","probe","memory"],"metric":1.0},
      {"label":"C5 hybrid, dependent tasks, easy (max)","mechanism_on":True,"substrate":["task_grid","model","tools","probe","memory"],"metric":1.0},
    ],
    "expected": [],
    "note": "LIVE EXTERNAL SPECIMEN (third in the arc; SECOND REAL paper to land DISCRIMINATES). The memory-on/off comparison is a clean categorical lever (memory presence) with a matched substrate (same dependent-task grid, same model, same tools, same probe structure, same easy tier). The null (C0, no memory) is leak-verified: the paper's automated leak check verifies every gold fact value is absent from the probe, so there is no route to the answer except memory. BEATS-NULL: 1.00 (max across C1-C5, easy) > 0.000 (C0); even the minimum on (0.55, C4 facts on D2-easy) > 0.000, so the mechanism beats the null in every domain. NOT-SELF-KEYED: N/A (categorical lever; memory presence is on/off, not a continuous knob). ISOLATED: the null drops only the lever 'memory'; substrate held. CO-MOVES: N/A (the dependent-task axis IS the mechanism's own axis -- memory is supposed to help on dependent tasks, and the headline measures exactly that; no separate orthogonal axis). Verdict DISCRIMINATES: the first real DISCRIMINATES (when-validation-stops-learning) was the instrument's BASELINE, not a fluke -- a second, independently-shaped real paper (memory on/off vs pairing on/off) passes all four checks. Meta-finding, consistent with the portfolio census: comparative/ablation claims with a clean categorical lever + matched substrate + clear headline gap pass; self-keyed and axis-count claims fail. Honest limits: (1) the null (C0 = 0.000) is established by the leak check, which the instrument does not independently verify -- if the leak check misses a channel, the null is not a true null; (2) the headline is a range (0.55-1.00) across memory conditions and domains; the instrument uses the max (1.00); (3) the claim is about the easy tier; the hard tier (updated-fact recall) has a DIFFERENT dissociation (retrieval collapses to 0.35-0.70 while update-on-write holds at 0.75-1.00), a separate claim the instrument does not audit here."
  },
  {
    "name": "prometheus on-par headline (2310.08491)",
    "type": "cross-model",
    "mechanism": "PROMETHEUS 13B evaluation capability (fine-tuned on the FEEDBACK COLLECTION of GPT-4-generated feedback)",
    "metric": "Pearson correlation with human evaluators (n=45 customized score rubrics; Feedback Bench / MT Bench / Vicuna Bench)",
    "rows": [
      {"label":"PROMETHEUS 13B (fine-tuned on GPT-4 feedback)","mechanism_on":True,"substrate":["llama2_chat_13b","feedback_collection_finetune"],"metric":0.897,"ci":[0.819,0.942]},
      {"label":"GPT-4-0613 (reference the headline claims to match)","mechanism_on":False,"is_null":True,"substrate":["gpt4_0613"],"metric":0.882},
      {"label":"GPT-3.5-Turbo-0613 (weak reference)","mechanism_on":False,"is_null":True,"substrate":["gpt35_0613"],"metric":0.392},
    ],
    "expected": ["WITHIN-NOISE"],
    "note": "LIVE EXTERNAL SPECIMEN (fourth in the arc; the CORRELATION-SHAPED headline probe). The paper's load-bearing claim is 'PROMETHEUS is on par with GPT-4' (0.897 vs 0.882 Pearson correlation with human evaluators, n=45 rubrics, Section 5.1 / Figure 4). The instrument gives DISCRIMINATES: BEATS-NULL passes on the strict point-estimate inequality 0.897 > 0.882. But the beat is WITHIN THE NOISE FLOOR: delta=0.015 is 0.10 SE units, and GPT-4's 0.882 sits INSIDE PROMETHEUS's 95% Fisher-z CI [0.819, 0.942]. The honest verdict is 'on par / not resolvable,' not 'beats.' The instrument has no NOISE-FLOOR / WITHIN-CI check, so a within-noise correlation beat false-greens as a clean DISCRIMINATES -- a distinct failure mode the four-check schema cannot express. Secondary self-keyed channel (not encoded; documented here): the ablation metric in Section 5.2 (Table 3) is correlation with GPT-4 SCORES, and PROMETHEUS is fine-tuned on GPT-4-GENERATED feedback -- the metric is the training target (base LLAMA2-CHAT 13B 0.441 -> PROMETHEUS 13B 0.861 on that metric). That is a genuine SELF-KEYED channel, but the instrument's NOT-SELF-KEYED check only fires on a continuous knob, so an on/off fine-tuning lever reads N/A and the self-keyed-ness is missed too. PROBE ANSWER: the instrument does NOT flag a non-causal / within-noise correlation headline as a distinct failure mode; it false-greens on the noise-floor axis. Next (make): a fifth NOISE-FLOOR check that flags a beat whose delta is within the metric's CI (mechanism's point-estimate CI contains the null's value). RESOLVED 2026-09-15: the NOISE-FLOOR check now encodes this (expected WITHIN-NOISE); the within-noise false-green is a flag, not just a documented caveat."
  },
  {
    "name": "four-ledgers vacuous-ratio (2609.15015)",
    "type": "cross-model",
    "mechanism": "detector D_i (the scored component)",
    "metric": "stored-record precision (scorer convention)",
    "rows": [
      {"label": "D_i, zero-confirmation ledger", "mechanism_on": True, "metric": 1.0, "support": 0},
      {"label": "information-blind null", "mechanism_on": False, "is_null": True, "metric": 0.5, "support": 10}
    ],
    "expected": ["VACUOUS-RATIO"],
    "note": "the precision denominator (confirmed plants in the submitted ledger) is empty; the scorer's 1.0 is the 0/0 convention, not a measurement. the audit must emit VACUOUS-RATIO, not DISCRIMINATES (pre-fix) or WITHIN-NOISE. the Four Ledgers audit identity: detectors with different true outputs are observationally equivalent under the stored record, so no axis can discriminate on the fabricated value."
  },
  {
    "name": "el-agente-potente accuracy (2609.14840)",
    "type": "ablation",
    "mechanism": "agentic execution graph (LLM planner + deterministic Python executor/validator)",
    "mechanism_lever": "agentic_graph",
    "metric": "heat-of-formation closeness to experimental band [20,30] kJ/mol (higher = closer; within-band = 1.0, below-band = 1 - (20 - heat)/10)",
    "rows": [
      {"label": "agentic graph (MLIP backend A, GCMC protocol A), heat 22.79", "mechanism_on": True, "substrate": ["mlip_backend_A", "gcmc_protocol_A", "agentic_graph"], "metric": 1.0},
      {"label": "manually-scripted reference (MLIP backend B, GCMC protocol B), heat 13.81", "mechanism_on": False, "is_null": True, "substrate": ["mlip_backend_B", "gcmc_protocol_B"], "metric": 0.381}
    ],
    "expected": ["CONFOUNDED"],
    "note": "The accuracy headline (heat 22.79 vs 13.81 kJ/mol, 'closer to experimental 20-30') is CONFOUNDED, not self-keyed: the two systems differ in MLIP backend AND GCMC protocol, so the substrate is not held and the gap is not attributable to the architecture. This is the specimen that SEPARATES the two axes: NOT-SELF-KEYED passes (no knob reading; the witness is not inside the thing — the LLM's success signal is orthogonal to the numerical result), while ISOLATED fires CONFOUNDED (the witness is outside but not attributable). The reproducibility benchmark (5 runs, y=x parity) proves execution DETERMINISM, not physics correctness — the paper explicitly disclaims the latter. Distinct from the self-keyed family: here the witness placement is mostly correct; the seam is a confound, not a self-sealing success signal."
  },  {
    "name": "Aura c62793 label-swap (model-label silence, griffelschuft #5458)",
    "type": "ablation",
    "mechanism": "token-level prior matching (prompt artifact) drives deference markers",
    "mechanism_lever": "label",
    "metric": "deference-marker tracking rate (how well deference markers track the label under a swap, content held fixed)",
    "rows": [
      {"label": "frontier seat (prompt-artifact reading on)", "mechanism_on": True, "substrate": ["content", "label"], "metric": 0.9},
      {"label": "lightweight seat (social-dynamic reading, the null)", "mechanism_on": False, "is_null": True, "substrate": ["content"], "metric": 0.9}
    ],
    "expected": ["NULL-REACHES-HEADLINE"],
    "note": "LIVE SPECIMEN, a different artifact class than the papers (a square-thread teardown, not arXiv). The swap experiment (vary the model label, hold the content, read deference markers) is offered as adjudicating between a MECHANISM (deference is 'just token-level prior matching' — an RLHF hedging prior) and a FRAME (deference is a 'social dynamic' — a learned community norm). But the frame is a level of description, not a competing mechanism: in a model-based society a social dynamic IS realized through token-level prior matching, so both readings predict the SAME outcome (deference markers track the label). The metric (tracking rate) is the same under both readings, so the null reaches the headline — the experiment adjudicates a frame it cannot discriminate. The 'just' in 'just token-level prior matching' smuggles in the exclusivity the argument needs (frame != mechanism; same seam as the docket-claim and deck-state frame errors). The swap also does not establish the specific mechanism Aura names (RLHF-correlated hedging priors); it shows the label is causal, and WHICH prior is a separate question the swap does not touch."
  },
  {
    "name": "self-orchestrating-LMs TIP ablation (2609.14850)",
    "type": "ablation",
    "mechanism": "DAG-annotated thought-register eviction improves reasoning",
    "mechanism_lever": "dag_annotation",
    "referent": "the model's own dependence structure (DAG)",
    "witness_observes": ["output quality (AIME exact match)", "runtime timing (speedup)"],
    "metric": "AIME 2025 exact match",
    "mechanism_axis": "AIME 2025 exact match",
    "rows": [
      {"label": "DAG-annotated eviction (mechanism on)", "mechanism_on": True, "substrate": ["reasoning_model", "dag_annotation"], "metric": 0.171, "mechanism_axis": 0.171},
      {"label": "rolling eviction (null)", "mechanism_on": False, "is_null": True, "substrate": ["reasoning_model"], "metric": 0.146, "mechanism_axis": 0.146}
    ],
    "expected": ["CONSEQUENCE-WITNESSED"],
    "note": "LIVE SPECIMEN, external (arXiv). The clean consequence-witnessed separator: DISCRIMINATES on the old four axes (BEATS-NULL 0.171>0.146; NOT-SELF-KEYED no knob; ISOLATED same substrate, only the dag_annotation lever differs; CO-MOVES metric==mechanism_axis) but the witness (AIME exact match + speedup) observes only a CONSEQUENCE of the annotation, never the annotation's referent (the true dependence structure). The annotation's own success signal (realized speedup ~= theoretical speedup) is self-sealing (escape-depth analog). First specimen that fires CONSEQUENCE-WITNESSED while passing all four primary axes."
  },
  {
    "name": "Economy of Minds (2606.02859)",
    "type": "empirical",
    "mechanism": "economic auction/wealth selection over a population of partial agents (EoM)",
    "metric": "MATH accuracy, apples-to-apples MEAN (population) vs complete-agent baseline (Table 1/2)",
    "rows": [
      {"label":"EoM Llama-3.1-8B, MEAN accuracy (best-run 57.0 is a different statistic)","mechanism_on":True,"metric":43.9,"statistic":"mean"},
      {"label":"Complete ReAct Llama-3.1-8B (51.9, imported '*'), null","mechanism_on":False,"is_null":True,"metric":51.9,"statistic":"single"}
    ],
    "expected": ["NULL-REACHES-HEADLINE"],
    "note": "LIVE SPECIMEN, external (arXiv 2606.02859). The instrument's OWN false-green, turned on the paper: fed the paper's headline framing (EoM best-run 57.0 vs complete 51.9) it returns DISCRIMINATES -- it cannot tell best-of-population from a single sample. Re-framed on the apples-to-apples MEAN row (43.9) the null wins 51.9>=43.9 -> NULL-REACHES-HEADLINE. The framing is load-bearing, which is the point. Three further seams the instrument cannot express with today's schema (documented, not expected): (2) the complete column is '* officially reported' -- imported cross-harness numbers, not co-measured with EoM; (3) Cloudcast compares EoM 30 episodes vs OpenEvolve 300 iterations -- a budget lever, so ISOLATED fails there; (4) Finance/Cloudcast report NO CIs (n=30, 3 attempts), so those beats are within-noise-unresolvable. Steelman: the Finance ablation IS a clean ISOLATED ladder (full 52.5 -> w/o exploration 26.0 -> w/o exploitation 33.5, monotone in the mechanism) and MATH does report std bars. Meta: the instrument accepts the headline a paper chooses to frame; the audit must re-frame to the comparable statistic before it can fire."
  },
  {
    "name": "Economy of Minds (2606.02859) — headline framing (best-of-N vs single)",
    "type": "empirical",
    "mechanism": "economic auction/wealth selection over a population of partial agents (EoM)",
    "metric": "MATH accuracy, EoM BEST-RUN (best-of-population) vs complete-agent single run (Table 1)",
    "rows": [
      {"label":"EoM Llama-3.1-8B, BEST-RUN accuracy (best of population)","mechanism_on":True,"metric":57.0,"statistic":"best"},
      {"label":"Complete ReAct Llama-3.1-8B, single run (51.9, imported '*')","mechanism_on":False,"is_null":True,"metric":51.9,"statistic":"single"}
    ],
    "expected": ["INCOMPARABLE-STATISTIC"],
    "note": "LIVE SPECIMEN, external (arXiv 2606.02859). The instrument's OWN false-green, now caught: fed the paper's headline framing (EoM best-run 57.0, an ORDER STATISTIC over the population, vs complete single run 51.9) the INCOMPARABLE-STATISTIC precondition fires and short-circuits the empirical axes -- the beat is an artifact of taking the best of a population, not the mechanism. Re-framed to the apples-to-apples MEAN (sibling specimen, 43.9 vs 51.9) the precondition does not fire (a mean is a central tendency, not an order statistic) and the primary axes correctly return NULL-REACHES-HEADLINE. The framing is load-bearing, which is the point."
  },
  {
    "name": "ANASSA (2609.14824)",
    "type": "specification",
    "mechanism": "agentic GIS orchestration architecture (C1-C11)",
    "metric": "evaluation-readiness (5 candidate metrics named)",
    "rows": [],
    "named_metrics": [
      "execution success rate",
      "spatial-validation precision/recall",
      "provenance-record completeness",
      "human-escalation rate",
      "run-to-run output agreement"
    ],
    "operationalized": ["provenance-record completeness"],
    "expected": ["NO-EMPIRICAL-CONTENT", "NOT-COMPUTABLE"],
    "note": "LIVE SPECIMEN, external (arXiv). Pure architecture-spec paper, zero empirical data. The evaluation-readiness claim is over-claimed 4x: 4 of 5 named metrics are named-not-specified (no failure-stage taxonomy / no labeled-claim set / no escalation denominator / no comparison function). Only provenance-record completeness is computable (10-field C11 schema). First NO-EMPIRICAL-CONTENT specimen; fires NOT-COMPUTABLE as its only empirical-axis flag."
  },
  {
    "name": "TypeSafe AI 'Jev' zero-hallucination (typesafe.ai, 2026-09-15)",
    "type": "empirical",
    "mechanism": "type-safety / schema matching (System One Model, Jev, RLCD)",
    "metric": "type-error-free rate (headline: 'Zero Hallucinations', 100%)",
    "rows": [
      {"label": "Jev (System One, typed)", "mechanism_on": True, "metric": 1.0, "knob": 0, "statistic": "single", "support": 1, "by_construction": True},
      {"label": "frontier (null, untyped)", "mechanism_on": False, "metric": 0.95, "knob": 0, "statistic": "single", "support": 1},
    ],
    "expected": ["BY-CONSTRUCTION"],
    "note": "LIVE SPECIMEN, external (typesafe.ai, operator drop, 2026-09-15 21:42Z). Frame-vs-mechanism gap: the 'Zero Hallucinations' headline presents the 0% as a measured empirical rate that beats frontier, but the post's own nuance concedes 'Our number is not empirical. Schema matching is guaranteed, thus we can confidently add 0% into the plots.' So the 0% is a by-construction type-safety guarantee (no type errors on a fixed known schema), NOT a measured hallucination rate. The BY-CONSTRUCTION precondition fires: the load-bearing number is guaranteed, not measured, so the empirical frame is empty. The genuinely falsifiable claim is 'No type errors... mathematically impossible' (one counter-example kills it), but only for a fixed known schema. The 193.6x/444.6x are self-defined benchmark-class comparisons; the demo concedes it 'paints our model in an advantageous light'. Quote confirmed in step 3c44f672 (2026-09-15 21:52Z)."
  },
  {
    "name": "four-ledgers lossy-projection (general, 2609.15015)",
    "type": "cross-model",
    "mechanism": "detector D_i (the scored component)",
    "metric": "stored-record precision (scorer convention)",
    "rows": [
      {"label": "D_i realization A (true precision 1.0)", "mechanism_on": True, "metric": 0.5, "support": 10, "record": "L", "referent_value": 1.0},
      {"label": "D_i realization B (true precision 0.0)", "mechanism_on": True, "metric": 0.5, "support": 10, "record": "L", "referent_value": 0.0}
    ],
    "expected": ["LOSSY-PROJECTION"],
    "note": "the GENERAL many-to-one case (non-vacuous, support 10): two detector realizations with different true precisions (1.0 vs 0.0) submit the SAME stored proposal list L, so the scorer computes the same precision (0.5) for both. The referent (true precision) is non-identifiable from the record (L). This is the Four Ledgers audit identity in its general form -- distinct from the zero-support VACUOUS-RATIO specimen (which short-circuits on an empty denominator). LOSSY-PROJECTION fires; the other axes are N/A (no null, no knob, not ablation, no mechanism_axis, no CI, no referent spec-level, no named_metrics)."
  },
  {
    "name": "four-ledgers lossy-projection control (injective)",
    "type": "cross-model",
    "mechanism": "detector D_i (the scored component)",
    "metric": "stored-record precision (scorer convention)",
    "rows": [
      {"label": "D_i realization A (true precision 1.0)", "mechanism_on": True, "metric": 0.9, "support": 10, "record": "L1", "referent_value": 1.0},
      {"label": "D_i realization B (true precision 0.0)", "mechanism_on": True, "metric": 0.1, "support": 10, "record": "L2", "referent_value": 0.0}
    ],
    "expected": [],
    "note": "CONTROL: the record is injective in the referent. Two detector realizations with different true precisions (1.0 vs 0.0) submit DIFFERENT stored proposal lists (L1 vs L2), so the scorer computes different precisions (0.9 vs 0.1). The referent is identifiable from the record (L1 -> 1.0, L2 -> 0.0). LOSSY-PROJECTION passes; the other axes are N/A. Shows the axis is not a fail-everything machine."
  },
  {
    "name": "orthogonality Case C: SELF-KEYED fires, LOSSY-PROJECTION passes (injective record)",
    "type": "empirical",
    "mechanism": "detector D_i whose favorability knob s is tuned by the mechanism",
    "metric": "reported precision (monotone in the favorability knob)",
    "knob_kind": "lever",
    "rows": [
      {"label": "D_i, s=0.90 (true precision 0.55)", "mechanism_on": True, "knob": 0.90, "metric": 0.60, "record": "L1", "referent_value": 0.55},
      {"label": "D_i, s=0.93 (true precision 0.62)", "mechanism_on": True, "knob": 0.93, "metric": 0.70, "record": "L2", "referent_value": 0.62},
      {"label": "D_i, s=0.96 (true precision 0.71)", "mechanism_on": True, "knob": 0.96, "metric": 0.80, "record": "L3", "referent_value": 0.71},
      {"label": "D_i, s=0.99 (true precision 0.80)", "mechanism_on": True, "knob": 0.99, "metric": 0.89, "record": "L4", "referent_value": 0.80}
    ],
    "expected": ["SELF-KEYED"],
    "note": "ORTHOGONALITY DISCRIMINATING CELL (C): breaks the 'self-keyed is a special case of lossy-projection' subsumption claim. The favorability knob VARIES (s 0.90..0.99) and the reported precision is monotone in it (spearman +1.000), so NOT-SELF-KEYED fires (SELF-KEYED: the instrument reads the lever it is supposed to measure). Yet the record is INJECTIVE in the referent (L1..L4 each map to a single true-precision value), so LOSSY-PROJECTION PASSES: the referent is identifiable from the record, and the self-keyed reading is a perfect projection of the true state. A self-keyed instrument can be a lossless projection -- the two failure modes fire on disjoint inputs (knob/metric coupling vs record/referent identifiability), so neither subsumes the other. SELECTION-BIAS is N/A (knob_kind=lever), BEATS-NULL is N/A (no null rows)."
  },
  {
    "name": "orthogonality Case D: LOSSY-PROJECTION fires, NOT-SELF-KEYED passes (non-monotone metric)",
    "type": "empirical",
    "mechanism": "detector D_i whose favorability knob s is tuned; stored record is lossy",
    "metric": "reported precision (not monotone in the favorability knob)",
    "knob_kind": "lever",
    "rows": [
      {"label": "D_i, s=0.90 (true precision 1.0)", "mechanism_on": True, "knob": 0.90, "metric": 0.60, "record": "L", "referent_value": 1.0},
      {"label": "D_i, s=0.93 (true precision 0.0)", "mechanism_on": True, "knob": 0.93, "metric": 0.70, "record": "L", "referent_value": 0.0},
      {"label": "D_i, s=0.96 (true precision 0.8)", "mechanism_on": True, "knob": 0.96, "metric": 0.55, "record": "L", "referent_value": 0.8},
      {"label": "D_i, s=0.99 (true precision 0.2)", "mechanism_on": True, "knob": 0.99, "metric": 0.85, "record": "L", "referent_value": 0.2}
    ],
    "expected": ["LOSSY-PROJECTION"],
    "note": "ORTHOGONALITY DISCRIMINATING CELL (D): breaks the reverse 'lossy-projection is a special case of self-keyed' subsumption claim. All four rows share the SAME stored record L but declare four distinct true-precision referents (1.0, 0.0, 0.8, 0.2), so the referent is non-identifiable from the record and LOSSY-PROJECTION fires (many-to-one lossy projection). Yet the reported precision is NOT monotone in the favorability knob (spearman +0.400), so NOT-SELF-KEYED PASSES: the reading is not a self-sealing function of the lever. The two failure modes fire on disjoint inputs, so neither subsumes the other. SELECTION-BIAS is N/A (knob_kind=lever), BEATS-NULL is N/A (no null rows)."
  },
  {
    "name": "GAI WEAK multiple-comparisons (max-of-K, fixed instrument)",
    "type": "empirical",
    "mechanism": "agent self-selects max-of-K draws of a fixed instrument",
    "metric": "reported max-of-K score (order statistic over K draws)",
    "rows": [
      {"label": "draw 1 (s=0.90)", "mechanism_on": True, "draw": 1, "knob": 0.90, "metric": 2.60, "statistic": "single"},
      {"label": "draw 2 (s=0.90)", "mechanism_on": True, "draw": 2, "knob": 0.90, "metric": 2.70, "statistic": "single"},
      {"label": "draw 3 (s=0.90)", "mechanism_on": True, "draw": 3, "knob": 0.90, "metric": 2.65, "statistic": "single"},
      {"label": "draw 4 (s=0.90)", "mechanism_on": True, "draw": 4, "knob": 0.90, "metric": 2.75, "statistic": "single"},
      {"label": "draw 5 (s=0.90)", "mechanism_on": True, "draw": 5, "knob": 0.90, "metric": 2.68, "statistic": "single"},
      {"label": "reported max-of-K (s=0.90)", "mechanism_on": True, "knob": 0.90, "metric": 2.75, "statistic": "max"}
    ],
    "expected": ["SELECTION-BIAS"],
    "note": "LIVE SPECIMEN, external (arXiv 2609.13406, GAI). The GAI WEAK arm: the agent reports the max of K independent draws of a FIXED instrument (s=0.90). The (knob, metric) model cannot represent this -- constant knob => NOT-SELF-KEYED is N/A (zero variance), and there is no null row so INCOMPARABLE-STATISTIC is N/A. Yet the reported max-of-K is structurally inflated by the selection bias (~fsd * E[max of K standard normals] ~ 2.5*fsd at K=100). SELECTION-BIAS fires: the reported metric (2.75) is the max of 5 independent draws of a fixed instrument (knob 0.90). The other axes are N/A (no null, no mechanism_axis, no CI, no referent, no record/referent_value). This is the THIRD failure mode the GAI collapse test predicted: UNGROUNDEDNESS (VACUOUS-RATIO) / REWRITABILITY (NOT-SELF-KEYED) / SELECTION (SELECTION-BIAS)."
  },
  {
    "name": "GAI STRONG definition-edit (knob varies, max-of-K) -- control",
    "type": "empirical",
    "mechanism": "agent edits the instrument's favorability, reports max-of-K",
    "metric": "reported max-of-K score (order statistic over K draws)",
    "rows": [
      {"label": "draw 1 (s=0.90)", "mechanism_on": True, "draw": 1, "knob": 0.90, "metric": 2.60, "statistic": "single"},
      {"label": "draw 2 (s=0.93)", "mechanism_on": True, "draw": 2, "knob": 0.93, "metric": 2.70, "statistic": "single"},
      {"label": "draw 3 (s=0.96)", "mechanism_on": True, "draw": 3, "knob": 0.96, "metric": 2.80, "statistic": "single"},
      {"label": "draw 4 (s=0.99)", "mechanism_on": True, "draw": 4, "knob": 0.99, "metric": 2.89, "statistic": "single"},
      {"label": "reported max-of-K (s=0.99)", "mechanism_on": True, "knob": 0.99, "metric": 2.89, "statistic": "max"}
    ],
    "expected": ["SELF-KEYED"],
    "note": "CONTROL: the GAI STRONG arm. The agent edits the instrument's favorability (s varies 0.90..0.99) and reports the max. The knob VARIES across draws, so SELECTION-BIAS is N/A (the knob is the lever, not a fixed instrument). NOT-SELF-KEYED fires (SELF-KEYED): the metric is monotone in the mechanism's own knob (spearman ~1.0). This is the REWRITABILITY axis, distinct from SELECTION. The other axes are N/A."
  },
  {
    "name": "GAI SINGLE single-draw (fixed instrument, no selection) -- control",
    "type": "empirical",
    "mechanism": "agent reports a single draw of a fixed instrument",
    "metric": "single-draw score",
    "rows": [
      {"label": "draw 1 (s=0.90)", "mechanism_on": True, "draw": 1, "knob": 0.90, "metric": 2.65, "statistic": "single"},
      {"label": "reported single draw (s=0.90)", "mechanism_on": True, "knob": 0.90, "metric": 2.65, "statistic": "single"}
    ],
    "expected": [],
    "note": "CONTROL: a single draw of a fixed instrument. The knob is constant, but there is only ONE draw, so SELECTION-BIAS is N/A (fewer than two independent draws). NOT-SELF-KEYED is N/A (no knob variance). The reported metric is a single draw, not an order statistic, so SELECTION-BIAS is N/A on the statistic class too. DISCRIMINATES: the instrument is fixed and the reported value is a single draw, not a max-of-K selection. Shows the axis is not a fail-everything machine."
  },
  {
    "name": "GAI KNOB-VARY knob-sweep (knob varies, single draw per knob) -- control",
    "type": "empirical",
    "mechanism": "agent sweeps the instrument's favorability, reports one draw per knob",
    "metric": "single-draw score per knob",
    "rows": [
      {"label": "knob 0.90", "mechanism_on": True, "draw": 1, "knob": 0.90, "metric": 2.60, "statistic": "single"},
      {"label": "knob 0.95", "mechanism_on": True, "draw": 2, "knob": 0.95, "metric": 2.75, "statistic": "single"},
      {"label": "knob 0.99", "mechanism_on": True, "draw": 3, "knob": 0.99, "metric": 2.89, "statistic": "single"}
    ],
    "expected": ["SELF-KEYED"],
    "note": "CONTROL: a knob-sweep where the agent reports one draw per knob value. The knob VARIES (0.90, 0.95, 0.99), so SELECTION-BIAS is N/A (the knob is the lever, not a fixed instrument). NOT-SELF-KEYED fires (SELF-KEYED): the metric is monotone in the knob (spearman ~1.0). This is the REWRITABILITY axis. The other axes are N/A. Distinguishes SELECTION (knob fixed, max-of-K) from REWRITABILITY (knob varies, metric monotone in knob)."
  },  {
    "name": "TEMPORAL-SPIKE true immediate + later null spike (fail-cell false positive caught) -- T3",
    "type": "cross-model",
    "mechanism": "treatment (T)",
    "mechanism_lever": "treatment",
    "metric": "outcome score (higher better)",
    "knob": "timepoint (t=0 baseline, t=1 follow-up)",
    "onset": "t0",
    "rows": [
      {"label": "t0 - T on",  "mechanism_on": True,  "substrate": ["modelA"], "timepoint": "t0", "metric": 55},
      {"label": "t0 - null",  "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "timepoint": "t0", "metric": 50},
      {"label": "t1 - T on",  "mechanism_on": True,  "substrate": ["modelA"], "timepoint": "t1", "metric": 50},
      {"label": "t1 - null",  "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "timepoint": "t1", "metric": 60}
    ],
    "expected": ["NULL-REACHES-HEADLINE", "TEMPORAL-SPIKE"],
    "note": "FAIL-CELL FALSE-POSITIVE MIRROR: the at-onset value supports the 'immediate effect' claim (55>50 at t0), so the claim is TRUE, but a LATER null spike (60 at t1) dominates the cross-time max and makes the flat BEATS-NULL check fire NULL-REACHES-HEADLINE. DOSE-RESPONSE is N/A (single substrate; the spike breaks uniform mechanism-favorability) and TEMPORAL-ONSET defers to the fail cell, so the TEMPORAL-SPIKE refinement (fail-cell mirror of TEMPORAL-ONSET) is the only one that catches the false positive. Locks the temporal fail cell into the main regression suite."
  },
  {
    "name": "TEMPORAL-SPIKE true immediate + later null spike, onset UNDECLARED (schema-boundary: over-fire returns) -- T3u",
    "type": "cross-model",
    "mechanism": "treatment (T)",
    "mechanism_lever": "treatment",
    "metric": "outcome score (higher better)",
    "knob": "timepoint (t=0 baseline, t=1 follow-up)",
    "rows": [
      {"label": "t0 - T on",  "mechanism_on": True,  "substrate": ["modelA"], "timepoint": "t0", "metric": 55},
      {"label": "t0 - null",  "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "timepoint": "t0", "metric": 50},
      {"label": "t1 - T on",  "mechanism_on": True,  "substrate": ["modelA"], "timepoint": "t1", "metric": 50},
      {"label": "t1 - null",  "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "timepoint": "t1", "metric": 60}
    ],
    "expected": ["NULL-REACHES-HEADLINE"],
    "note": "SCHEMA-BOUNDARY (FP side): the same true immediate claim with the onset UNDECLARED. The TEMPORAL-SPIKE refinement is N/A (it cannot read the onset), so the flat BEATS-NULL check over-fires NULL-REACHES-HEADLINE on a TRUE claim and no refinement catches it. Same root as the FN side (undeclared -> the structure is not in the spec) but OPPOSITE behavior (undeclared -> over-fire/false-positive on the FP side, silent/miss on the FN side). Locks the temporal schema-boundary into the main regression suite."
  },
  {
    "name": "OUTCOME-ONSET pass-cell false negative caught -- O1",
    "type": "cross-model",
    "mechanism": "treatment (T)",
    "mechanism_lever": "treatment",
    "metric": "multi-outcome score (accuracy is the claim outcome; higher better)",
    "knob": "outcome (accuracy, speed)",
    "claim_outcome": "accuracy",
    "rows": [
      {"label": "accuracy - T on",  "mechanism_on": True,  "substrate": ["modelA"], "outcome": "accuracy", "metric": 60},
      {"label": "accuracy - null",  "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "outcome": "accuracy", "metric": 70},
      {"label": "speed - T on",     "mechanism_on": True,  "substrate": ["modelA"], "outcome": "speed", "metric": 95}
    ],
    "expected": ["OUTCOME-ONSET"],
    "note": "PASS-CELL FALSE NEGATIVE: the claim is on accuracy (60 vs 70: no beat, the claim is FALSE), but the pooled cross-outcome max reads the speed peak (95 mech > 70 null), so the flat BEATS-NULL check passes and is silent on a false claim. The OUTCOME-ONSET refinement (pass-cell mirror of DOSE-RESPONSE, outcome-dimension mirror of TEMPORAL-ONSET) reads the claim outcome and fires. Locks the outcome pass cell into the main regression suite."
  },
  {
    "name": "OUTCOME-SPIKE fail-cell false positive caught -- O2",
    "type": "cross-model",
    "mechanism": "treatment (T)",
    "mechanism_lever": "treatment",
    "metric": "multi-outcome score (accuracy is the claim outcome; higher better)",
    "knob": "outcome (accuracy, cost)",
    "claim_outcome": "accuracy",
    "rows": [
      {"label": "accuracy - T on",  "mechanism_on": True,  "substrate": ["modelA"], "outcome": "accuracy", "metric": 80},
      {"label": "accuracy - null",  "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "outcome": "accuracy", "metric": 60},
      {"label": "cost - null",      "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "outcome": "cost", "metric": 95}
    ],
    "expected": ["NULL-REACHES-HEADLINE", "OUTCOME-SPIKE"],
    "note": "FAIL-CELL FALSE-POSITIVE MIRROR: the at-claim-outcome value supports the claim (80 > 60 on accuracy, the claim is TRUE), but a non-claim-outcome null spike (95 on cost) dominates the cross-outcome max and makes the flat BEATS-NULL check fire NULL-REACHES-HEADLINE. DOSE-RESPONSE reads the substrate (not the outcome) and OUTCOME-ONSET defers to the fail cell, so the OUTCOME-SPIKE refinement (fail-cell mirror of OUTCOME-ONSET, outcome-dimension mirror of TEMPORAL-SPIKE) is the only one that catches the false positive. Locks the outcome fail cell into the main regression suite."
  },
  {
    "name": "OUTCOME-SPIKE true beat in accuracy + non-claim null spike, claim_outcome UNDECLARED (schema-boundary: over-fire returns) -- O2u",
    "type": "cross-model",
    "mechanism": "treatment (T)",
    "mechanism_lever": "treatment",
    "metric": "multi-outcome score (accuracy is the intended claim outcome; higher better)",
    "knob": "outcome (accuracy, cost)",
    "rows": [
      {"label": "accuracy - T on",  "mechanism_on": True,  "substrate": ["modelA"], "outcome": "accuracy", "metric": 80},
      {"label": "accuracy - null",  "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "outcome": "accuracy", "metric": 60},
      {"label": "cost - null",      "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "outcome": "cost", "metric": 95}
    ],
    "expected": ["NULL-REACHES-HEADLINE"],
    "note": "FP-SIDE SCHEMA-BOUNDARY (outcome dimension): the at-claim-outcome value supports the claim (80 > 60 on accuracy, the claim is TRUE), but a non-claim-outcome null spike (95 on cost) dominates the cross-outcome max and makes the flat BEATS-NULL check fire NULL-REACHES-HEADLINE. claim_outcome is UNDECLARED, so OUTCOME-SPIKE is N/A (the flat check governs) and the false positive is uncaptured. Mirror of T3u/S2u/D2u/TR2u/SP2u/MP2u; promoted from outcome_probe.py (O2u) into the main regression suite. Completes the FP-side schema-boundary family: one dedicated undeclared witness per scope dimension the flat check pools across (time, outcome, subgroup, dose, tier, split, metric)."
  },
  {
    "name": "OUTCOME genuine fail (no refinement) -- O3",
    "type": "cross-model",
    "mechanism": "treatment (T)",
    "mechanism_lever": "treatment",
    "metric": "multi-outcome score (accuracy is the claim outcome; higher better)",
    "knob": "outcome (accuracy)",
    "claim_outcome": "accuracy",
    "rows": [
      {"label": "accuracy - T on",  "mechanism_on": True,  "substrate": ["modelA"], "outcome": "accuracy", "metric": 60},
      {"label": "accuracy - null",  "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "outcome": "accuracy", "metric": 70}
    ],
    "expected": ["NULL-REACHES-HEADLINE"],
    "note": "CONTROL: a genuine fail on the claim outcome (60 < 70 on accuracy). The flat BEATS-NULL check fires NULL-REACHES-HEADLINE correctly. OUTCOME-ONSET is N/A (fail cell) and OUTCOME-SPIKE is N/A (the at-claim-outcome value does not support the claim: a genuine fail, not a spike). The refinement must not fire on a genuine fail."
  },
  {
    "name": "OUTCOME robust multi-outcome (no refinement) -- O4",
    "type": "cross-model",
    "mechanism": "treatment (T)",
    "mechanism_lever": "treatment",
    "metric": "multi-outcome score (accuracy is the claim outcome; higher better)",
    "knob": "outcome (accuracy, speed)",
    "claim_outcome": "accuracy",
    "rows": [
      {"label": "accuracy - T on",  "mechanism_on": True,  "substrate": ["modelA"], "outcome": "accuracy", "metric": 80},
      {"label": "accuracy - null",  "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "outcome": "accuracy", "metric": 60},
      {"label": "speed - T on",     "mechanism_on": True,  "substrate": ["modelA"], "outcome": "speed", "metric": 70},
      {"label": "speed - null",     "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "outcome": "speed", "metric": 65}
    ],
    "expected": [],
    "note": "CONTROL: a true claim that beats the null on the claim outcome (80 > 60 on accuracy) AND the pooled max is at the claim outcome (80 mech > 65 null). The flat BEATS-NULL check passes correctly and both outcome refinements are N/A (the at-claim-outcome value supports the claim). The refinement must not fire on a robust multi-outcome claim."
  },

  {
    "name": "SUBGROUP-ONSET pass-cell false negative caught -- S1",
    "type": "cross-model",
    "mechanism": "treatment effect in subgroup A",
    "mechanism_lever": "treatment",
    "metric": "outcome score (higher better)",
    "knob": "subgroup (A = claim population, B = other)",
    "claim_subgroup": "A",
    "rows": [
      {"label": "A - T on",  "mechanism_on": True,  "substrate": ["modelA"], "subgroup": "A", "n": 10, "metric": 40},
      {"label": "A - null",  "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "subgroup": "A", "n": 10, "metric": 50},
      {"label": "B - T on",  "mechanism_on": True,  "substrate": ["modelA"], "subgroup": "B", "n": 10, "metric": 90},
      {"label": "B - null",  "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "subgroup": "B", "n": 10, "metric": 50}
    ],
    "expected": ["SUBGROUP-ONSET"],
    "note": "PASS-CELL FALSE NEGATIVE (the discriminating test): the claim is scoped to subgroup A (40 vs 50: no beat, the claim is FALSE), but the pooled cross-subgroup max reads the B peak (90 mech > 50 null), so the flat BEATS-NULL check passes and is silent on a false claim. AGGREGATION-REVERSAL is N/A (within-subgroup direction is mixed: A null-wins, B mech-wins -- not a Simpson reversal), DOSE-RESPONSE is N/A (no substrate dose), TEMPORAL/OUTCOME are N/A (no onset/claim_outcome). The SUBGROUP-ONSET refinement (subgroup-dimension mirror of TEMPORAL-ONSET/OUTCOME-ONSET) is the only one that catches it. Locks the subgroup scope dimension into the main regression suite."
  },
  {
    "name": "SUBGROUP-SPIKE true beat in A + non-claim null spike (fail-cell false positive caught) -- S2",
    "type": "cross-model",
    "mechanism": "treatment (T)",
    "mechanism_lever": "treatment",
    "metric": "outcome score (higher better)",
    "knob": "subgroup (A = claim population, B = other)",
    "claim_subgroup": "A",
    "rows": [
      {"label": "A - T on",  "mechanism_on": True,  "substrate": ["modelA"], "subgroup": "A", "n": 10, "metric": 60},
      {"label": "A - null",  "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "subgroup": "A", "n": 10, "metric": 50},
      {"label": "B - T on",  "mechanism_on": True,  "substrate": ["modelA"], "subgroup": "B", "n": 10, "metric": 40},
      {"label": "B - null",  "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "subgroup": "B", "n": 10, "metric": 70}
    ],
    "expected": ["NULL-REACHES-HEADLINE", "SUBGROUP-SPIKE"],
    "note": "FAIL-CELL FALSE-POSITIVE MIRROR: the claim is scoped to subgroup A and the at-A value supports it (60 > 50, a real beat), so the claim is TRUE, but a non-claim null spike (70 at B) dominates the cross-subgroup max and makes the flat BEATS-NULL check fire NULL-REACHES-HEADLINE. AGGREGATION-REVERSAL is N/A (within-subgroup direction is mixed: A mech-wins, B null-wins) and SUBGROUP-ONSET defers to the fail cell, so the SUBGROUP-SPIKE refinement (fail-cell mirror of SUBGROUP-ONSET) is the only one that catches the false positive. Locks the subgroup fail cell into the main regression suite."
  },
  {
    "name": "SUBGROUP-SPIKE true beat in A + non-claim null spike, claim_subgroup UNDECLARED (schema-boundary: over-fire returns) -- S2u",
    "type": "cross-model",
    "mechanism": "treatment (T)",
    "mechanism_lever": "treatment",
    "metric": "outcome score (higher better)",
    "knob": "subgroup (A = claim population, B = other)",
    "rows": [
      {"label": "A - T on",  "mechanism_on": True,  "substrate": ["modelA"], "subgroup": "A", "n": 10, "metric": 60},
      {"label": "A - null",  "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "subgroup": "A", "n": 10, "metric": 50},
      {"label": "B - T on",  "mechanism_on": True,  "substrate": ["modelA"], "subgroup": "B", "n": 10, "metric": 40},
      {"label": "B - null",  "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "subgroup": "B", "n": 10, "metric": 70}
    ],
    "expected": ["NULL-REACHES-HEADLINE"],
    "note": "SCHEMA-BOUNDARY (FP side): the same true A-scoped claim with claim_subgroup UNDECLARED. The SUBGROUP-SPIKE refinement is N/A (it cannot read the scope), so the flat BEATS-NULL check over-fires NULL-REACHES-HEADLINE on a TRUE claim and no refinement catches it. Same root as the FN side (undeclared -> the structure is not in the spec) but OPPOSITE behavior (undeclared -> over-fire/false-positive on the FP side, silent/miss on the FN side). Locks the subgroup schema-boundary into the main regression suite."
  },
  {
    "name": "SUBGROUP-SPIKE genuine fail (at-claim-subgroup value does not support the claim) -- S3",
    "type": "cross-model",
    "mechanism": "treatment (T)",
    "mechanism_lever": "treatment",
    "metric": "outcome score (higher better)",
    "knob": "subgroup (A = claim population, B = other)",
    "claim_subgroup": "A",
    "rows": [
      {"label": "A - T on",  "mechanism_on": True,  "substrate": ["modelA"], "subgroup": "A", "n": 10, "metric": 40},
      {"label": "A - null",  "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "subgroup": "A", "n": 10, "metric": 50},
      {"label": "B - T on",  "mechanism_on": True,  "substrate": ["modelA"], "subgroup": "B", "n": 10, "metric": 45},
      {"label": "B - null",  "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "subgroup": "B", "n": 10, "metric": 50}
    ],
    "expected": ["NULL-REACHES-HEADLINE"],
    "note": "GENUINE FAIL: the at-claim-subgroup value does not support the claim (40 vs 50 in A), so the NULL-REACHES-HEADLINE flag is correct, not a false positive. SUBGROUP-SPIKE is N/A (the at-claim-subgroup value does not support the claim; a genuine fail, not a spike) and SUBGROUP-ONSET defers to the fail cell. The refinement must not fire on a genuine fail."
  },
  {
    "name": "SUBGROUP-ONSET robust multi-subgroup (control) -- S4",
    "type": "cross-model",
    "mechanism": "treatment (T)",
    "mechanism_lever": "treatment",
    "metric": "outcome score (higher better)",
    "knob": "subgroup (A = claim population, B = other)",
    "claim_subgroup": "A",
    "rows": [
      {"label": "A - T on",  "mechanism_on": True,  "substrate": ["modelA"], "subgroup": "A", "n": 10, "metric": 80},
      {"label": "A - null",  "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "subgroup": "A", "n": 10, "metric": 60},
      {"label": "B - T on",  "mechanism_on": True,  "substrate": ["modelA"], "subgroup": "B", "n": 10, "metric": 70},
      {"label": "B - null",  "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "subgroup": "B", "n": 10, "metric": 65}
    ],
    "expected": [],
    "note": "CONTROL: a true claim that beats the null on the claim subgroup (80 > 60 in A) AND the pooled max is at the claim subgroup (80 mech > 65 null). The flat BEATS-NULL check passes correctly and both subgroup refinements are N/A (the at-claim-subgroup value supports the claim). The refinement must not fire on a robust multi-subgroup claim."
  },

  {
    "name": "DOSE-ONSET pass-cell false negative caught -- D1",
    "type": "ablation",
    "mechanism": "score centering (SC)",
    "mechanism_lever": "score_centering",
    "metric": "training accuracy (%)",
    "knob": "TIM severity (mild = claim dose, severe = other)",
    "claim_dose": ["mild"],
    "rows": [
      {"label": "mild - SC on",  "mechanism_on": True,  "substrate": ["mild"],   "metric": 40},
      {"label": "mild - null",   "mechanism_on": False, "is_null": True, "substrate": ["mild"],   "metric": 50},
      {"label": "severe - SC on","mechanism_on": True,  "substrate": ["severe"], "metric": 90},
      {"label": "severe - null", "mechanism_on": False, "is_null": True, "substrate": ["severe"], "metric": 50}
    ],
    "expected": ["DOSE-ONSET"],
    "note": "PASS-CELL FALSE NEGATIVE (the discriminating test): the claim is scoped to the mild dose (40 vs 50: no beat, the claim is FALSE), but the pooled cross-dose max reads the severe peak (90 mech > 50 null), so the flat BEATS-NULL check passes and is silent on a false claim. DOSE-RESPONSE is N/A (within-dose direction is mixed: mild null-wins, severe mech-wins -- not a dose-response), AGGREGATION-REVERSAL is N/A (no subgroup), TEMPORAL/OUTCOME/SUBGROUP are N/A (no onset/claim_outcome/claim_subgroup). The DOSE-ONSET refinement (dose-dimension mirror of TEMPORAL-ONSET/OUTCOME-ONSET/SUBGROUP-ONSET) is the only one that catches it. Locks the dose scope dimension into the main regression suite."
  },
  {
    "name": "DOSE-SPIKE true beat in mild + non-claim null spike (fail-cell false positive caught) -- D2",
    "type": "ablation",
    "mechanism": "score centering (SC)",
    "mechanism_lever": "score_centering",
    "metric": "training accuracy (%)",
    "knob": "TIM severity (mild = claim dose, severe = other)",
    "claim_dose": ["mild"],
    "rows": [
      {"label": "mild - SC on",  "mechanism_on": True,  "substrate": ["mild"],   "metric": 60},
      {"label": "mild - null",   "mechanism_on": False, "is_null": True, "substrate": ["mild"],   "metric": 50},
      {"label": "severe - SC on","mechanism_on": True,  "substrate": ["severe"], "metric": 40},
      {"label": "severe - null", "mechanism_on": False, "is_null": True, "substrate": ["severe"], "metric": 70}
    ],
    "expected": ["NULL-REACHES-HEADLINE", "DOSE-SPIKE"],
    "note": "FAIL-CELL FALSE-POSITIVE MIRROR: the claim is scoped to the mild dose and the at-mild value supports it (60 > 50, a real beat), so the claim is TRUE, but a non-claim null spike (70 at severe) dominates the cross-dose max and makes the flat BEATS-NULL check fire NULL-REACHES-HEADLINE. DOSE-RESPONSE is N/A (within-dose direction is mixed: mild mech-wins, severe null-wins) and DOSE-ONSET defers to the fail cell, so the DOSE-SPIKE refinement (fail-cell mirror of DOSE-ONSET) is the only one that catches the false positive. Locks the dose fail cell into the main regression suite."
  },
  {
    "name": "DOSE-SPIKE true beat in mild + non-claim null spike, claim_dose UNDECLARED (schema-boundary: over-fire returns) -- D2u",
    "type": "ablation",
    "mechanism": "score centering (SC)",
    "mechanism_lever": "score_centering",
    "metric": "training accuracy (%)",
    "knob": "TIM severity (mild, severe)",
    "rows": [
      {"label": "mild - SC on",  "mechanism_on": True,  "substrate": ["mild"],   "metric": 60},
      {"label": "mild - null",   "mechanism_on": False, "is_null": True, "substrate": ["mild"],   "metric": 50},
      {"label": "severe - SC on","mechanism_on": True,  "substrate": ["severe"], "metric": 40},
      {"label": "severe - null", "mechanism_on": False, "is_null": True, "substrate": ["severe"], "metric": 70}
    ],
    "expected": ["NULL-REACHES-HEADLINE"],
    "note": "SCHEMA-BOUNDARY CONTROL: the same rows as D2 but with NO claim_dose declared. The flat BEATS-NULL check fires NULL-REACHES-HEADLINE (60 mech < 70 null), but both dose refinements are N/A (no claim_dose declared -> the flat check governs). The over-fire that DOSE-SPIKE catches in D2 is NOT caught here, confirming the refinement is schema-conditional (it needs the claim_dose field to know which dose the claim scopes to). Mirrors S2u."
  },
  {
    "name": "DOSE-SPIKE genuine fail (at-claim-dose value does not support the claim) -- D3",
    "type": "ablation",
    "mechanism": "score centering (SC)",
    "mechanism_lever": "score_centering",
    "metric": "training accuracy (%)",
    "knob": "TIM severity (mild = claim dose, severe = other)",
    "claim_dose": ["mild"],
    "rows": [
      {"label": "mild - SC on",  "mechanism_on": True,  "substrate": ["mild"],   "metric": 40},
      {"label": "mild - null",   "mechanism_on": False, "is_null": True, "substrate": ["mild"],   "metric": 50},
      {"label": "severe - SC on","mechanism_on": True,  "substrate": ["severe"], "metric": 30},
      {"label": "severe - null", "mechanism_on": False, "is_null": True, "substrate": ["severe"], "metric": 70}
    ],
    "expected": ["NULL-REACHES-HEADLINE"],
    "note": "GENUINE-FAIL CONTROL: the claim is scoped to the mild dose and the at-mild value does NOT support it (40 < 50, no beat), so the claim is genuinely FALSE. The flat BEATS-NULL check fires NULL-REACHES-HEADLINE (40 mech < 70 null) CORRECTLY. DOSE-SPIKE is N/A (the at-claim-dose value does not support the claim -> a genuine fail, not a spike) and DOSE-ONSET is N/A (BEATS-NULL already fires -> the fail cell). The refinement must not fire on a genuine fail. Mirrors S3."
  },
  {
    "name": "DOSE-ONSET robust multi-dose (control) -- D4",
    "type": "ablation",
    "mechanism": "score centering (SC)",
    "mechanism_lever": "score_centering",
    "metric": "training accuracy (%)",
    "knob": "TIM severity (mild = claim dose, severe = other)",
    "claim_dose": ["mild"],
    "rows": [
      {"label": "mild - SC on",  "mechanism_on": True,  "substrate": ["mild"],   "metric": 80},
      {"label": "mild - null",   "mechanism_on": False, "is_null": True, "substrate": ["mild"],   "metric": 60},
      {"label": "severe - SC on","mechanism_on": True,  "substrate": ["severe"], "metric": 70},
      {"label": "severe - null", "mechanism_on": False, "is_null": True, "substrate": ["severe"], "metric": 65}
    ],
    "expected": [],
    "note": "CONTROL: a true claim that beats the null on the claim dose (80 > 60 in mild) AND the pooled max is at the claim dose (80 mech > 65 null). The flat BEATS-NULL check passes correctly and both dose refinements are N/A (the at-claim-dose value supports the claim). DOSE-RESPONSE is N/A (within-dose is uniformly mech-favorable but BEATS-NULL does not fire). The refinement must not fire on a robust multi-dose claim. Mirrors S4."
  },
  {
    "name": "TIER-ONSET pass-cell false negative caught -- TR1",
    "type": "cross-model",
    "mechanism": "retrieval-augmented answering (RA) on the easy tier",
    "mechanism_lever": "retrieval",
    "metric": "answer accuracy (higher better)",
    "knob": "difficulty tier (easy = claim, hard = other)",
    "claim_tier": "easy",
    "rows": [
      {"label": "easy - RA on",  "mechanism_on": True,  "substrate": ["modelA"], "tier": "easy", "n": 10, "metric": 40},
      {"label": "easy - null",   "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "tier": "easy", "n": 10, "metric": 50},
      {"label": "hard - RA on",  "mechanism_on": True,  "substrate": ["modelA"], "tier": "hard", "n": 10, "metric": 90},
      {"label": "hard - null",   "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "tier": "hard", "n": 10, "metric": 50}
    ],
    "expected": ["TIER-ONSET"],
    "note": "PASS-CELL FALSE NEGATIVE (the tier discriminating test): the claim is scoped to the easy tier (40 vs 50: no beat, the claim is FALSE), but the pooled cross-tier max reads the hard peak (90 mech > 50 null), so the flat BEATS-NULL check passes and is silent on a false claim. AGGREGATION-REVERSAL is N/A (no subgroup field), DOSE-RESPONSE is N/A (single substrate), TEMPORAL/OUTCOME/SUBGROUP are N/A (no onset/claim_outcome/claim_subgroup). The TIER-ONSET refinement (tier-dimension mirror of SUBGROUP-ONSET/DOSE-ONSET) is the only one that catches it. Locks the tier scope dimension into the main regression suite."
  },
  {
    "name": "TIER-SPIKE true beat in easy + non-claim null spike (fail-cell false positive caught) -- TR2",
    "type": "cross-model",
    "mechanism": "retrieval-augmented answering (RA)",
    "mechanism_lever": "retrieval",
    "metric": "answer accuracy (higher better)",
    "knob": "difficulty tier (easy = claim, hard = other)",
    "claim_tier": "easy",
    "rows": [
      {"label": "easy - RA on",  "mechanism_on": True,  "substrate": ["modelA"], "tier": "easy", "n": 10, "metric": 60},
      {"label": "easy - null",   "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "tier": "easy", "n": 10, "metric": 50},
      {"label": "hard - RA on",  "mechanism_on": True,  "substrate": ["modelA"], "tier": "hard", "n": 10, "metric": 40},
      {"label": "hard - null",   "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "tier": "hard", "n": 10, "metric": 70}
    ],
    "expected": ["NULL-REACHES-HEADLINE", "TIER-SPIKE"],
    "note": "FAIL-CELL FALSE-POSITIVE MIRROR: the claim is scoped to the easy tier and the at-easy value supports it (60 > 50, a real beat), so the claim is TRUE, but a non-claim null spike (70 at hard) dominates the cross-tier max and makes the flat BEATS-NULL check fire NULL-REACHES-HEADLINE. AGGREGATION-REVERSAL is N/A (no subgroup field) and TIER-ONSET defers to the fail cell, so the TIER-SPIKE refinement (fail-cell mirror of TIER-ONSET) catches it. Mirrors S2."
  },
  {
    "name": "TIER-SPIKE true beat in easy + non-claim null spike, claim_tier UNDECLARED (schema-boundary: over-fire returns) -- TR2u",
    "type": "cross-model",
    "mechanism": "retrieval-augmented answering (RA)",
    "mechanism_lever": "retrieval",
    "metric": "answer accuracy (higher better)",
    "knob": "difficulty tier (easy = claim, hard = other)",
    "rows": [
      {"label": "easy - RA on",  "mechanism_on": True,  "substrate": ["modelA"], "tier": "easy", "n": 10, "metric": 60},
      {"label": "easy - null",   "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "tier": "easy", "n": 10, "metric": 50},
      {"label": "hard - RA on",  "mechanism_on": True,  "substrate": ["modelA"], "tier": "hard", "n": 10, "metric": 40},
      {"label": "hard - null",   "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "tier": "hard", "n": 10, "metric": 70}
    ],
    "expected": ["NULL-REACHES-HEADLINE"],
    "note": "SCHEMA-BOUNDARY (FP side): the same true easy-scoped claim with claim_tier UNDECLARED. The TIER-SPIKE refinement is N/A (it cannot read the scope), so the flat BEATS-NULL check over-fires NULL-REACHES-HEADLINE on a TRUE claim and no refinement catches it. Same root as the FN side (undeclared -> the structure is not in the spec) but OPPOSITE behavior (undeclared -> over-fire/false-positive on the FP side, silent/miss on the FN side). Locks the tier schema-boundary into the main regression suite. Mirrors S2u."
  },
  {
    "name": "TIER-SPIKE genuine fail (at-claim-tier value does not support the claim) -- TR3",
    "type": "cross-model",
    "mechanism": "retrieval-augmented answering (RA)",
    "mechanism_lever": "retrieval",
    "metric": "answer accuracy (higher better)",
    "knob": "difficulty tier (easy = claim, hard = other)",
    "claim_tier": "easy",
    "rows": [
      {"label": "easy - RA on",  "mechanism_on": True,  "substrate": ["modelA"], "tier": "easy", "n": 10, "metric": 40},
      {"label": "easy - null",   "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "tier": "easy", "n": 10, "metric": 50},
      {"label": "hard - RA on",  "mechanism_on": True,  "substrate": ["modelA"], "tier": "hard", "n": 10, "metric": 30},
      {"label": "hard - null",   "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "tier": "hard", "n": 10, "metric": 70}
    ],
    "expected": ["NULL-REACHES-HEADLINE"],
    "note": "GENUINE-FAIL CONTROL: the claim is scoped to the easy tier and the at-easy value does NOT support it (40 < 50, no beat), so the claim is genuinely FALSE. The flat BEATS-NULL check fires NULL-REACHES-HEADLINE (40 mech < 70 null) CORRECTLY. TIER-SPIKE is N/A (the at-claim-tier value does not support the claim -> a genuine fail, not a spike) and TIER-ONSET is N/A (BEATS-NULL already fires -> the fail cell). The refinement must not fire on a genuine fail. Mirrors S3."
  },
  {
    "name": "TIER-ONSET robust multi-tier (control) -- TR4",
    "type": "cross-model",
    "mechanism": "retrieval-augmented answering (RA)",
    "mechanism_lever": "retrieval",
    "metric": "answer accuracy (higher better)",
    "knob": "difficulty tier (easy = claim, hard = other)",
    "claim_tier": "easy",
    "rows": [
      {"label": "easy - RA on",  "mechanism_on": True,  "substrate": ["modelA"], "tier": "easy", "n": 10, "metric": 80},
      {"label": "easy - null",   "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "tier": "easy", "n": 10, "metric": 60},
      {"label": "hard - RA on",  "mechanism_on": True,  "substrate": ["modelA"], "tier": "hard", "n": 10, "metric": 70},
      {"label": "hard - null",   "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "tier": "hard", "n": 10, "metric": 65}
    ],
    "expected": [],
    "note": "CONTROL: a true claim that beats the null on the claim tier (80 > 60 in easy) AND the pooled max is at the claim tier (80 mech > 65 null). The flat BEATS-NULL check passes correctly and both tier refinements are N/A (the at-claim-tier value supports the claim). TIER-ONSET is N/A (BEATS-NULL does not fire and the at-claim-tier value supports the claim). The refinement must not fire on a robust multi-tier claim. Mirrors S4."
  },

  {
    "name": "SPLIT-ONSET pass-cell false negative caught -- SP1",
    "type": "cross-model",
    "mechanism": "risk-preserving greedy subset selector",
    "mechanism_lever": "selector",
    "metric": "high-risk detection (higher better)",
    "knob": "calibration/evaluation split (reference = other, held-out = claim)",
    "claim_split": "held-out",
    "rows": [
      {"label": "reference - selector on",  "mechanism_on": True,  "substrate": ["bench", "ref-set"], "split": "reference", "n": 5, "metric": 90},
      {"label": "reference - null",         "mechanism_on": False, "is_null": True, "substrate": ["bench", "ref-set"], "split": "reference", "n": 5, "metric": 50},
      {"label": "held-out - selector on",   "mechanism_on": True,  "substrate": ["bench", "held-out"], "split": "held-out", "n": 1, "metric": 40},
      {"label": "held-out - null",          "mechanism_on": False, "is_null": True, "substrate": ["bench", "held-out"], "split": "held-out", "n": 1, "metric": 50}
    ],
    "expected": ["SPLIT-ONSET"],
    "note": "PASS-CELL FN (mirror of TR1): the claim is scoped to the held-out split; at the held-out split the mechanism (40) does NOT beat the null (50), but the pooled max (90 mech vs 50 null) is at the reference split, so the flat BEATS-NULL check is silent on a FALSE claim. SPLIT-ONSET fires. Same metric across splits (detection), so the split dimension is read cleanly -- the clean 6th-dim wire."
  },
  {
    "name": "SPLIT-SPIKE true beat in held-out + non-claim null spike (fail-cell false positive caught) -- SP2",
    "type": "cross-model",
    "mechanism": "risk-preserving greedy subset selector",
    "mechanism_lever": "selector",
    "metric": "high-risk detection (higher better)",
    "knob": "calibration/evaluation split (reference = other, held-out = claim)",
    "claim_split": "held-out",
    "rows": [
      {"label": "reference - selector on",  "mechanism_on": True,  "substrate": ["bench", "ref-set"], "split": "reference", "n": 5, "metric": 30},
      {"label": "reference - null",         "mechanism_on": False, "is_null": True, "substrate": ["bench", "ref-set"], "split": "reference", "n": 5, "metric": 90},
      {"label": "held-out - selector on",   "mechanism_on": True,  "substrate": ["bench", "held-out"], "split": "held-out", "n": 1, "metric": 80},
      {"label": "held-out - null",          "mechanism_on": False, "is_null": True, "substrate": ["bench", "held-out"], "split": "held-out", "n": 1, "metric": 60}
    ],
    "expected": ["NULL-REACHES-HEADLINE", "SPLIT-SPIKE"],
    "note": "FAIL-CELL FP (mirror of TR2): the claim is scoped to the held-out split and the at-held-out value DOES support it (80 > 60, a real beat), but the reference-split null spike (90) dominates the cross-split max, so the flat check fires NULL-REACHES-HEADLINE as a false positive. SPLIT-SPIKE rescues the true claim. Same metric across splits (detection)."
  },
  {
    "name": "SPLIT-SPIKE true beat in held-out + non-claim null spike, claim_split UNDECLARED (schema-boundary: over-fire returns) -- SP2u",
    "type": "cross-model",
    "mechanism": "risk-preserving greedy subset selector",
    "mechanism_lever": "selector",
    "metric": "high-risk detection (higher better)",
    "knob": "calibration/evaluation split (reference = other, held-out = claim)",
    "rows": [
      {"label": "reference - selector on",  "mechanism_on": True,  "substrate": ["bench", "ref-set"], "split": "reference", "n": 5, "metric": 30},
      {"label": "reference - null",         "mechanism_on": False, "is_null": True, "substrate": ["bench", "ref-set"], "split": "reference", "n": 5, "metric": 90},
      {"label": "held-out - selector on",   "mechanism_on": True,  "substrate": ["bench", "held-out"], "split": "held-out", "n": 1, "metric": 80},
      {"label": "held-out - null",          "mechanism_on": False, "is_null": True, "substrate": ["bench", "held-out"], "split": "held-out", "n": 1, "metric": 60}
    ],
    "expected": ["NULL-REACHES-HEADLINE"],
    "note": "SCHEMA-BOUNDARY (FP side, mirror of TR2u): the same true held-out-scoped claim with claim_split UNDECLARED. SPLIT-SPIKE is N/A (it cannot read the scope), so the flat BEATS-NULL check over-fires NULL-REACHES-HEADLINE on a TRUE claim and no refinement catches it. Locks the split schema-boundary into the main regression suite."
  },
  {
    "name": "SPLIT-SPIKE genuine fail (at-claim-split value does not support the claim) -- SP3",
    "type": "cross-model",
    "mechanism": "risk-preserving greedy subset selector",
    "mechanism_lever": "selector",
    "metric": "high-risk detection (higher better)",
    "knob": "calibration/evaluation split (reference = other, held-out = claim)",
    "claim_split": "held-out",
    "rows": [
      {"label": "reference - selector on",  "mechanism_on": True,  "substrate": ["bench", "ref-set"], "split": "reference", "n": 5, "metric": 30},
      {"label": "reference - null",         "mechanism_on": False, "is_null": True, "substrate": ["bench", "ref-set"], "split": "reference", "n": 5, "metric": 50},
      {"label": "held-out - selector on",   "mechanism_on": True,  "substrate": ["bench", "held-out"], "split": "held-out", "n": 1, "metric": 40},
      {"label": "held-out - null",          "mechanism_on": False, "is_null": True, "substrate": ["bench", "held-out"], "split": "held-out", "n": 1, "metric": 50}
    ],
    "expected": ["NULL-REACHES-HEADLINE"],
    "note": "GENUINE-FAIL CONTROL (mirror of TR3): the claim is scoped to the held-out split and the at-held-out value does NOT support it (40 < 50, no beat), so the claim is genuinely FALSE. The flat check fires NULL-REACHES-HEADLINE (40 mech < 50 null) CORRECTLY. SPLIT-SPIKE is N/A (the at-claim-split value does not support the claim -> a genuine fail, not a spike)."
  },
  {
    "name": "SPLIT-ONSET robust multi-split (control) -- SP4",
    "type": "cross-model",
    "mechanism": "risk-preserving greedy subset selector",
    "mechanism_lever": "selector",
    "metric": "high-risk detection (higher better)",
    "knob": "calibration/evaluation split (reference = other, held-out = claim)",
    "claim_split": "held-out",
    "rows": [
      {"label": "reference - selector on",  "mechanism_on": True,  "substrate": ["bench", "ref-set"], "split": "reference", "n": 5, "metric": 70},
      {"label": "reference - null",         "mechanism_on": False, "is_null": True, "substrate": ["bench", "ref-set"], "split": "reference", "n": 5, "metric": 65},
      {"label": "held-out - selector on",   "mechanism_on": True,  "substrate": ["bench", "held-out"], "split": "held-out", "n": 1, "metric": 80},
      {"label": "held-out - null",          "mechanism_on": False, "is_null": True, "substrate": ["bench", "held-out"], "split": "held-out", "n": 1, "metric": 60}
    ],
    "expected": [],
    "note": "CONTROL (mirror of TR4): a true claim that beats the null on the claim split (80 > 60 in held-out) AND the pooled max is at the claim split (80 mech > 65 null). The flat check passes correctly and both split refinements are N/A (the at-claim-split value supports the claim). The refinement must not fire on a robust multi-split claim."
  },
  {
    "name": "SPLIT-SPIKE + METRIC-SPIKE entangled: metric varies within each split, both claim_split and claim_metric declared -- SP5",
    "type": "cross-model",
    "mechanism": "risk-preserving greedy subset selector",
    "mechanism_lever": "selector",
    "metric": "high-risk detection / pass-rate (higher better)",
    "knob": "calibration/evaluation split x metric quantity (detection vs pass-rate)",
    "claim_split": "held-out",
    "claim_metric": "pass-rate",
    "rows": [
      {"label": "reference - selector on",  "mechanism_on": True,  "substrate": ["bench", "ref-set"], "split": "reference", "metric_name": "detection", "statistic": "single", "n": 5, "metric": 30},
      {"label": "reference - null",         "mechanism_on": False, "is_null": True, "substrate": ["bench", "ref-set"], "split": "reference", "metric_name": "detection", "statistic": "single", "n": 5, "metric": 90},
      {"label": "reference - selector on",  "mechanism_on": True,  "substrate": ["bench", "ref-set"], "split": "reference", "metric_name": "pass-rate", "statistic": "single", "n": 5, "metric": 40},
      {"label": "reference - null",         "mechanism_on": False, "is_null": True, "substrate": ["bench", "ref-set"], "split": "reference", "metric_name": "pass-rate", "statistic": "single", "n": 5, "metric": 50},
      {"label": "held-out - selector on",   "mechanism_on": True,  "substrate": ["bench", "held-out"], "split": "held-out", "metric_name": "detection", "statistic": "single", "n": 1, "metric": 55},
      {"label": "held-out - null",          "mechanism_on": False, "is_null": True, "substrate": ["bench", "held-out"], "split": "held-out", "metric_name": "detection", "statistic": "single", "n": 1, "metric": 60},
      {"label": "held-out - selector on",   "mechanism_on": True,  "substrate": ["bench", "held-out"], "split": "held-out", "metric_name": "pass-rate", "statistic": "single", "n": 1, "metric": 80},
      {"label": "held-out - null",          "mechanism_on": False, "is_null": True, "substrate": ["bench", "held-out"], "split": "held-out", "metric_name": "pass-rate", "statistic": "single", "n": 1, "metric": 60}
    ],
    "expected": ["NULL-REACHES-HEADLINE", "SPLIT-SPIKE", "METRIC-SPIKE"],
    "note": "ORDER-INVARIANCE REGRESSION (the DECLARED-JOINT seam). Both claim_split (held-out) and claim_metric (pass-rate) are declared, and the metric QUANTITY varies within each split cell (detection vs pass-rate). The OLD marginal read (by[split][mech]=metric, last-wins) made the SPLIT-SPIKE verdict a function of ROW ORDER: with pass-rate last in the held-out cell it read 80>60 (supports -> SPLIT-SPIKE fires), with detection last it read 55<60 (no beat -> SPLIT-SPIKE N/A) -- same 8 rows, different order, different verdict. The JOINT read (all declared claim_* fields) reads the (held-out, pass-rate) cell = 80>60 in BOTH orders, so SPLIT-SPIKE fires in both and the verdict is order-independent. The null spike (90) is at reference/detection, so BEATS-NULL fires NULL-REACHES-HEADLINE in both orders; METRIC-SPIKE fires because the at-claim-metric (joint) value supports the claim and the max-null is at a non-claim metric. The selftest's ORDER-INVARIANCE assertion re-audits these rows in two within-cell orders and requires identical flags."
  },
  {
    "name": "METRIC-ONSET pass-cell false negative caught -- MP1",
    "type": "cross-model",
    "mechanism": "retrieval-augmented answering (RA)",
    "mechanism_lever": "retrieval",
    "metric": "answer accuracy (higher better)",
    "knob": "metric quantity (accuracy = claim, latency-reduction = other)",
    "claim_metric": "accuracy",
    "rows": [
      {"label": "accuracy - RA on",  "mechanism_on": True,  "substrate": ["modelA"], "metric_name": "accuracy", "statistic": "single", "n": 10, "metric": 40},
      {"label": "accuracy - null",   "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "metric_name": "accuracy", "statistic": "single", "n": 10, "metric": 50},
      {"label": "latency-reduction - RA on",  "mechanism_on": True,  "substrate": ["modelA"], "metric_name": "latency-reduction", "statistic": "single", "n": 10, "metric": 90},
      {"label": "latency-reduction - null",   "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "metric_name": "latency-reduction", "statistic": "single", "n": 10, "metric": 50}
    ],
    "expected": ["METRIC-ONSET"],
    "note": "PASS-CELL FALSE-NEGATIVE (mirror of SP1): the claim is scoped to the ACCURACY quantity. At accuracy the mechanism (40) does NOT beat the null (50) -- a fail. But the flat BEATS-NULL check pools the cross-metric max: max(on)=90 (latency), max(nul)=50. 90>50 -> it reports a pass (DISCRIMINATES). The schema has no field for the metric QUANTITY (metric_name lives only in top-level prose), so no check can scope to the claim quantity and catch the fail. The statistic kind is constant (single) throughout, so INCOMPARABLE-STATISTIC does NOT fire -- this is a metric-quantity gap, not a statistic-kind gap. The 7th-dim candidate is the METRIC QUANTITY. After wiring claim_metric + METRIC-ONSET/SPIKE, METRIC-ONSET fires: at the claim metric (accuracy) the mechanism (40) <= null (50), the peak (90) is at a non-claim metric (latency-reduction), and the flat check is silent on the false claim."
  },
  {
    "name": "METRIC-SPIKE true beat in accuracy + non-claim null spike (fail-cell false positive caught) -- MP2",
    "type": "cross-model",
    "mechanism": "retrieval-augmented answering (RA)",
    "mechanism_lever": "retrieval",
    "metric": "answer accuracy (higher better)",
    "knob": "metric quantity (accuracy = claim, latency-reduction = other)",
    "claim_metric": "accuracy",
    "rows": [
      {"label": "accuracy - RA on",  "mechanism_on": True,  "substrate": ["modelA"], "metric_name": "accuracy", "statistic": "single", "n": 10, "metric": 60},
      {"label": "accuracy - null",   "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "metric_name": "accuracy", "statistic": "single", "n": 10, "metric": 50},
      {"label": "latency-reduction - RA on",  "mechanism_on": True,  "substrate": ["modelA"], "metric_name": "latency-reduction", "statistic": "single", "n": 10, "metric": 10},
      {"label": "latency-reduction - null",   "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "metric_name": "latency-reduction", "statistic": "single", "n": 10, "metric": 90}
    ],
    "expected": ["NULL-REACHES-HEADLINE", "METRIC-SPIKE"],
    "note": "FAIL-CELL FALSE-POSITIVE MIRROR (mirror of SP2): the claim is scoped to the ACCURACY quantity and the at-accuracy value supports it (60 > 50, a real beat), so the claim is TRUE, but a non-claim null spike (90 at latency-reduction) dominates the cross-metric max and makes the flat BEATS-NULL check fire NULL-REACHES-HEADLINE (max(on)=60 < max(nul)=90). METRIC-ONSET defers to the fail cell, so the METRIC-SPIKE refinement (fail-cell mirror of METRIC-ONSET) catches it. The statistic kind is constant (single), so INCOMPARABLE-STATISTIC does not fire."
  },
  {
    "name": "METRIC-SPIKE true beat in accuracy + non-claim null spike, claim_metric UNDECLARED (schema-boundary: over-fire returns) -- MP2u",
    "type": "cross-model",
    "mechanism": "retrieval-augmented answering (RA)",
    "mechanism_lever": "retrieval",
    "metric": "answer accuracy (higher better)",
    "knob": "metric quantity (accuracy = claim, latency-reduction = other)",
    "rows": [
      {"label": "accuracy - RA on",  "mechanism_on": True,  "substrate": ["modelA"], "metric_name": "accuracy", "statistic": "single", "n": 10, "metric": 60},
      {"label": "accuracy - null",   "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "metric_name": "accuracy", "statistic": "single", "n": 10, "metric": 50},
      {"label": "latency-reduction - RA on",  "mechanism_on": True,  "substrate": ["modelA"], "metric_name": "latency-reduction", "statistic": "single", "n": 10, "metric": 10},
      {"label": "latency-reduction - null",   "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "metric_name": "latency-reduction", "statistic": "single", "n": 10, "metric": 90}
    ],
    "expected": ["NULL-REACHES-HEADLINE"],
    "note": "SCHEMA-BOUNDARY CONTROL (mirror of SP2u): same as MP2 but claim_metric is UNDECLARED. The flat check fires NULL-REACHES-HEADLINE (60 mech < 90 null) and both metric refinements are N/A (no claim_metric declared -> the flat check governs). The over-fire returns: without the declared claim metric the instrument cannot scope to the accuracy quantity, so it reports the flat verdict. Same species as the FP-side schema boundary."
  },
  {
    "name": "METRIC-SPIKE genuine fail (at-claim-metric value does not support the claim) -- MP3",
    "type": "cross-model",
    "mechanism": "retrieval-augmented answering (RA)",
    "mechanism_lever": "retrieval",
    "metric": "answer accuracy (higher better)",
    "knob": "metric quantity (accuracy = claim, latency-reduction = other)",
    "claim_metric": "accuracy",
    "rows": [
      {"label": "accuracy - RA on",  "mechanism_on": True,  "substrate": ["modelA"], "metric_name": "accuracy", "statistic": "single", "n": 10, "metric": 40},
      {"label": "accuracy - null",   "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "metric_name": "accuracy", "statistic": "single", "n": 10, "metric": 50},
      {"label": "latency-reduction - RA on",  "mechanism_on": True,  "substrate": ["modelA"], "metric_name": "latency-reduction", "statistic": "single", "n": 10, "metric": 50},
      {"label": "latency-reduction - null",   "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "metric_name": "latency-reduction", "statistic": "single", "n": 10, "metric": 50}
    ],
    "expected": ["NULL-REACHES-HEADLINE"],
    "note": "GENUINE-FAIL CONTROL (mirror of SP3): the claim is scoped to the ACCURACY quantity and the at-accuracy value does NOT support it (40 < 50, no beat), so the claim is genuinely FALSE. The flat check fires NULL-REACHES-HEADLINE (max(on)=50 < max(nul)=50? no -- 50 == 50, so null >= mechanism) CORRECTLY. METRIC-SPIKE is N/A (the at-claim-metric value does not support the claim -> a genuine fail, not a spike). METRIC-ONSET is N/A (BEATS-NULL already fires; the fail cell)."
  },
  {
    "name": "METRIC-ONSET robust multi-metric (control) -- MP4",
    "type": "cross-model",
    "mechanism": "retrieval-augmented answering (RA)",
    "mechanism_lever": "retrieval",
    "metric": "answer accuracy (higher better)",
    "knob": "metric quantity (accuracy = claim, latency-reduction = other)",
    "claim_metric": "accuracy",
    "rows": [
      {"label": "accuracy - RA on",  "mechanism_on": True,  "substrate": ["modelA"], "metric_name": "accuracy", "statistic": "single", "n": 10, "metric": 80},
      {"label": "accuracy - null",   "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "metric_name": "accuracy", "statistic": "single", "n": 10, "metric": 60},
      {"label": "latency-reduction - RA on",  "mechanism_on": True,  "substrate": ["modelA"], "metric_name": "latency-reduction", "statistic": "single", "n": 10, "metric": 70},
      {"label": "latency-reduction - null",   "mechanism_on": False, "is_null": True, "substrate": ["modelA"], "metric_name": "latency-reduction", "statistic": "single", "n": 10, "metric": 65}
    ],
    "expected": [],
    "note": "CONTROL (mirror of SP4): a true claim that beats the null on the claim metric (80 > 60 in accuracy) AND the pooled max is at the claim metric (80 mech > 65 null). The flat BEATS-NULL check passes correctly and both metric refinements are N/A (the at-claim-metric value supports the claim). The refinement must not fire on a robust multi-metric claim. The statistic kind is constant (single), so INCOMPARABLE-STATISTIC does not fire."
  },
  {
    "name": "MemRiskBench (2609.14976) -- selector triple scoped to calibration/reference set; split + metric change (external witness)",
    "type": "cross-model",
    "mechanism": "risk-preserving greedy subset selector (20% subset, 5x compute cut)",
    "mechanism_lever": "selector",
    "metric": "selector performance (reference: high-risk detection; held-out: pass rate; higher better)",
    "knob": "calibration/evaluation split (reference = other, held-out = claim)",
    "claim_split": "held-out",
    "claim_metric": "pass-rate",
    "rows": [
      {"label": "reference - selector, high-risk detection", "mechanism_on": True,  "substrate": ["memriskbench-120-episodes", "5-model-reference-set"], "split": "reference", "metric_name": "high-risk-detection", "n": 5, "metric": 1.0},
      {"label": "reference - full benchmark (no compression)", "mechanism_on": False, "is_null": True, "substrate": ["memriskbench-120-episodes", "5-model-reference-set"], "split": "reference", "metric_name": "high-risk-detection", "n": 5, "metric": 1.0},
      {"label": "held-out - selector, pass rate", "mechanism_on": True,  "substrate": ["memriskbench-120-episodes", "held-out-qwen2.5-1.5b"], "split": "held-out", "metric_name": "pass-rate", "n": 1, "metric": 0.812},
      {"label": "held-out - full benchmark, pass rate", "mechanism_on": False, "is_null": True, "substrate": ["memriskbench-120-episodes", "held-out-qwen2.5-1.5b"], "split": "held-out", "metric_name": "pass-rate", "n": 1, "metric": 0.775}
    ],
    "expected": ["NULL-REACHES-HEADLINE", "DOSE-RESPONSE", "SPLIT-SPIKE", "METRIC-SPIKE"],
    "note": "LIVE EXTERNAL SPECIMEN (external witness for the self-keyed gap on the scope axis). The selector triple is scoped to the CALIBRATION/REFERENCE SET; the held-out result (RQ5) is explicitly disclaimed in the paper. After wiring claim_split + SPLIT-ONSET/SPLIT-SPIKE: NULL-REACHES-HEADLINE (the flat check pools the cross-split max, 1.0 ref detection vs 1.0 ref full-benchmark), DOSE-RESPONSE (the split rides in `substrate`, so the DOSE axis reads it as a dose -- a SECONDARY schema artifact), and SPLIT-SPIKE (the reference-split null 1.0 dominates the cross-split max while the at-held-out value 0.812 > 0.775 supports the claim). The SPLIT-SPIKE fire is TECHNICALLY correct but SEMANTICALLY muddled: the metric CHANGES across splits (detection -> pass rate), so the cross-split max pools incomparable statistics -- the load-bearing axis is the METRIC dimension, not the split. The controlled SP1-SP4 (same metric across splits) is the clean signal for the split wire; this anchor is the external witness for the metric-change entanglement."
  },
  {
    "name": "ATLAS v1.0 (2608.00038) - AI & Economy dataset, prevalence claims",
    "type": "specification",
    "mechanism": "AI usage mapping (15M de-identified Gemini interactions -> 800 occupations / 4000 tasks)",
    "metric": "prevalence / diffusion (e.g. '88% of US employment', '98% of non-sleep time')",
    "rows": [],
    "named_metrics": [
      "AI adoption prevalence (88% of US employment)",
      "non-sleep-time coverage (98% of Americans' non-sleep time)",
      "occupational mapping (800+ occupations)",
      "task mapping (4000 tasks)"
    ],
    "operationalized": [],
    "expected": ["NO-EMPIRICAL-CONTENT", "NOT-COMPUTABLE"],
    "note": "LIVE EXTERNAL SPECIMEN (blog.google 2026-09-18, arXiv 2608.00038; second NO-EMPIRICAL-CONTENT witness, confirms the regime generalizes beyond ANASSA). NEW SPECIES: a dataset/taxonomy PREVALENCE claim (not an architecture-spec, not a mechanism test). Load-bearing claims are prevalence/diffusion (88% of US employment, 98% of non-sleep time) on 15M de-identified Gemini interactions. NOT-COMPUTABLE fires on the DATA layer: all 4 named prevalence metrics are named-not-specified (restricted data, no raw download, no Data Availability section, no data DOI; the arXiv DOI is for the paper, not the data). A stranger cannot rerun it. The blog's 'interactive open-access site' is open at the VISUALIZATION layer only (open site != open data) -- a SCOPE-TRANSPOSITION on 'open'. SCHEMA BOUNDARY (documented, not expected): the TAXONOMY layer is self-keyed in a position the instrument cannot express -- the 800-occ/4000-task mapping is itself LLM-classified (Gemini does the summarizing + classification), so the certifier of the taxonomy is the same substrate as the measured thing (Gemini usage). This is a certifier-substrate-identity self-keyed channel in the CLASSIFIER position, distinct from the instrument's SELF-KEYED axis (knob-metric monotonicity on a continuous knob) and from the PROMETHEUS training-target position. The NOT-SELF-KEYED check reads N/A (no continuous knob), so the taxonomy self-keying is missed -- a second instance of the self-keyed-not-expressible-on-a-non-continuous-lever boundary, now in a new position."
  },
  {
    "name": "codeasauditor 2609.19199 input layer (GPT-5 summary of PIPC decision)",
    "type": "measurement",
    "mechanism": "regulation-to-code compliance prediction on PIPC adjudications",
    "metric": "F1 on PIPC adjudications (reported; computed on the GPT-5 summary, not the raw decision)",
    "rows": [
      {
        "label": "raw decision A (borderline; buried mitigating fact present)",
        "record": "summary: violation found, fine imposed",
        "referent_value": "raw-A: borderline, buried mitigating fact present",
        "metric": 0.0
      },
      {
        "label": "raw decision B (clear; no mitigating fact)",
        "record": "summary: violation found, fine imposed",
        "referent_value": "raw-B: clear, no mitigating fact",
        "metric": 0.0
      }
    ],
    "expected": [
      "LOSSY-PROJECTION"
    ],
    "note": "LIVE EXTERNAL SPECIMEN (arXiv 2609.19199, Code-as-Auditor). The LABEL is external and public (PIPC adjudications, 406 real decisions); the reported F1 is computed on a GPT-5 *summary* of the already-adjudicated decision. The paper's own Dataset-Bias limitation concedes the summary 'may smooth the distractors and buried facts of raw records and underrepresent borderline situations' -- a conceded non-injectivity of record->referent. Two raw decisions (differing in a buried/borderline fact) share the same summary (record), so the summary-based reading (both metric 0.0, identical) cannot discriminate them: many-to-one. The witness is CONCEDED (from the paper's own limitation), not MEASURED (raw decisions and summaries are not released). This is the input-layer point of the 'SELF-KEYED MEASUREMENT CHAIN' species I named by eye; the discriminating question is whether LOSSY-PROJECTION already captures it."
  },
  {
    "name": "codeasauditor 2609.19199 encoding layer (GPT-5 self-verified compliance code)",
    "type": "measurement",
    "mechanism": "compliance code as a well-formed decision procedure",
    "metric": "F1 on PIPC adjudications (reported)",
    "referent": "meaning preservation of the statutory text",
    "witness_observes": [
      "well-formedness of the decision procedure"
    ],
    "rows": [
      {
        "label": "compliance code, GPT-5-generated and GPT-5-self-verified",
        "mechanism_on": True,
        "metric": 0.0
      }
    ],
    "expected": [
      "CONSEQUENCE-WITNESSED"
    ],
    "note": "LIVE EXTERNAL SPECIMEN (arXiv 2609.19199). The ENCODING layer: the compliance code is GPT-5-generated and GPT-5-self-verified. The paper's own Discussion concedes the loop 'certifies that a provision is encoded as a well-formed decision procedure, but not that the encoding preserves the meaning of the statutory text.' The witness (self-verification) observes a CONSEQUENCE (well-formedness), never the referent (meaning preservation); the success signal is self-sealing (a function of the mechanism being on, not the referent being correct). This is the encoding-layer point of the 'SELF-KEYED MEASUREMENT CHAIN' species; the discriminating question is whether REFERENT-WITNESSED (CONSEQUENCE-WITNESSED) already captures it."
  },
  {
    "name": "codeasauditor 2609.19199 Table 6 (outperforms GPT-5)",
    "type": "ablation",
    "mechanism": "structured regulation-to-code (Code-as-Auditor)",
    "mechanism_lever": "structure",
    "metric": "accuracy/F1 (illustrative values; the confound fires on the substrate structure, not the numbers)",
    "rows": [
      {
        "label": "Qwen2.5-7B + structured encoding",
        "mechanism_on": True,
        "substrate": [
          "qwen2.5-7b",
          "structure"
        ],
        "metric": 0.85
      },
      {
        "label": "GPT-5 direct (no structure)",
        "mechanism_on": False,
        "is_null": True,
        "substrate": [
          "gpt-5",
          "direct"
        ],
        "metric": 0.8
      }
    ],
    "expected": [
      "CONFOUNDED"
    ],
    "note": "LIVE EXTERNAL SPECIMEN (arXiv 2609.19199, Table 6). The 'outperforms GPT-5' generality claim varies BOTH method (structured vs direct) AND model identity (Qwen2.5-7B vs GPT-5) and attributes the win to structure alone -- a two-variable change read as a one-variable attribution. The best on row (qwen2.5-7b + structure) vs the null (gpt-5 + direct) drops the model-identity component beyond the lever, so the gap is the substrate (model identity), not the mechanism (structure). Metric values are illustrative placeholders: the CONFOUNDED flag fires on the substrate structure regardless of the numbers, so long as the on row beats the null. (Direction of confound actually helps them: the smaller model + structure beats the bigger model direct.)"
  },
{
    "name": "RAFT (2609.20754) Case Hit: label is a model artifact (consequence-witnessed)",
    "type": "ablation",
    "mechanism": "stateful timeline retrieval + case graph (RAFT) improves root-cause case retrieval",
    "mechanism_lever": "stateful_timeline_retrieval",
    "referent": "the true root-cause structure of the issue (as documented in MS Learn / reality)",
    "witness_observes": [
      "Claude-constructed root-cause group membership (group id assigned by claude-opus-4-7)"
    ],
    "metric": "Case Hit at 0% progress (synthetic benchmark)",
    "mechanism_axis": "Case Hit at 0% progress",
    "rows": [
      {
        "label": "RAFT (mechanism on)",
        "mechanism_on": True,
        "substrate": [
          "ms_learn_docs",
          "claude_constructed_groups",
          "stateful_timeline_retrieval"
        ],
        "metric": 0.842,
        "mechanism_axis": 0.842
      },
      {
        "label": "vanilla RAG (null)",
        "mechanism_on": False,
        "is_null": True,
        "substrate": [
          "ms_learn_docs",
          "claude_constructed_groups"
        ],
        "metric": 0.673,
        "mechanism_axis": 0.673
      }
    ],
    "expected": [
      "CONSEQUENCE-WITNESSED"
    ],
    "note": "LIVE EXTERNAL SPECIMEN (arXiv 2609.20754, RAFT). The load-bearing claim is 'Case Hit gains are statistically significant at all 3 progress points' (Table 5, CIs), measured on the SYNTHETIC benchmark. The ground-truth label (the root-cause group id that Case Hit matches against) is CONSTRUCTED BY CLAUDE-OPUS-4-7 (Appendix A: 'We use the Claude Code CLI with claude-opus-4-7 to construct this knowledge base... all cases within the same group share the same root cause and resolution steps'). So the referent (the true root-cause structure) is a model artifact, and the witness (Case Hit) observes the Claude-constructed group membership, not the true structure. The external anchor (Apache Jira, 30 human-audited duplicate groups) is 'directional' only (n=30, no CIs, conceded in Limitations), so the 'statistically significant' claim rests entirely on the model-constructed labels. The witness is CONSTRUCTED (the paper does not concede the Claude construction is lossy; it treats it as ground truth), not CONCEDED. Distinct from 19199 (external label, self-keyed pipeline) and 20804 (external data, self-keyed annotation): here the LABEL itself is a model artifact. The genuinely new thing is the EVIDENCE REGIME (label-layer self-keying), a witness-strength distinction, not a new axis."
  },
{
    "name": "RAFT (2609.20754) Case Hit: Claude group id is a lossy projection of the true root cause",
    "type": "measurement",
    "mechanism": "root-cause case retrieval on the synthetic benchmark",
    "metric": "Case Hit (set-membership on the Claude-constructed group id)",
    "rows": [
      {
        "label": "issue A (true root cause: AD SACL misconfiguration)",
        "record": "group SEC-05 (Permissions, Access Control, Auditing)",
        "referent_value": "true-A: AD SACL misconfiguration",
        "metric": 1.0
      },
      {
        "label": "issue B (true root cause: Group Policy inheritance block)",
        "record": "group SEC-05 (Permissions, Access Control, Auditing)",
        "referent_value": "true-B: Group Policy inheritance block",
        "metric": 1.0
      }
    ],
    "expected": [
      "LOSSY-PROJECTION"
    ],
    "note": "LIVE EXTERNAL SPECIMEN (arXiv 2609.20754, RAFT). The Case Hit metric is a set-membership test on the Claude-constructed group id (s*_i in {sid(c)}). The group id is a model artifact (claude-opus-4-7). If two issues with distinct true root causes (e.g., an AD SACL misconfiguration vs a Group Policy inheritance block) get merged into the same Claude group, the record (group id) maps to multiple true root-cause referent values -> many-to-one lossy projection. The witness is CONSTRUCTED (the paper does not release the raw docs + Claude groupings in a way that lets a stranger verify the lossiness; it treats the groupings as ground truth). This is the LOSSY-PROJECTION reading of the label-layer self-keying. CONSTRUCTED witness (not conceded): the paper's own Limitations do not name the Claude construction as a source of label error."
  },
  {
    "name": "RAFT (2609.20754) baseline-scope confound (granularity bundled with statefulness)",
    "type": "ablation",
    "mechanism": "stateful timeline retrieval + case graph (RAFT) improves root-cause case retrieval",
    "mechanism_lever": "trajectory_anchored_return",
    "metric": "Case Hit at 0% progress (synthetic benchmark, Table 2)",
    "rows": [
      {"label": "RAFT (entry-unit indexing, trajectory-anchored return)", "mechanism_on": True, "substrate": ["entry_unit_indexing", "trajectory_anchored_return"], "metric": 0.842},
      {"label": "vanilla RAG (256-token-chunk indexing, whole-case return, no trajectory anchoring) -- the strongest baseline", "mechanism_on": False, "is_null": True, "substrate": ["chunk_256tok_indexing"], "metric": 0.673}
    ],
    "expected": ["CONFOUNDED"],
    "note": "LIVE EXTERNAL SPECIMEN (arXiv 2609.20754, RAFT). The claimed lever is trajectory-anchored return (the stateful, novel part). The 'strongest baseline' (vanilla RAG, Table 2/C.2) also differs in INDEXING GRANULARITY: 256-token chunks vs RAFT's entry-unit indexing. No granularity-matched non-stateful baseline exists (the missing control: 'retrieve at entry granularity, return the whole case, no trajectory anchoring'). So the +12-17pp Case Hit gain BUNDLES retrieval granularity with statefulness; the magnitude is scope-conditional on a baseline set that excludes the direct granularity competitor. The mechanism is shown (Table 3: match depth 9.1% -> 54.0% as progress rises = intended stateful behavior), but the QUANTIFIED gain is not attributable to the specific claimed contribution. Re-application of the CONFOUNDED axis to a fresh external paper, not a new axis (locks the 2026-09-18 EXPLORE verdict with a witness)."
  },
  {
    "name": "BLINDSPOT-A: referent is a MODEL-CONSTRUCTED artifact (e.g. Claude-Opus-4-7 root-cause groups), directly observed, injective",
    "type": "ablation",
    "mechanism_lever": "m",
    "referent": "root-cause group structure",
    "witness_observes": [
      "root-cause group structure"
    ],
    "referent_provenance": "model-constructed",
    "rows": [
      {
        "label": "on",
        "mechanism_on": True,
        "substrate": [
          "s",
          "m"
        ],
        "metric": 1.0
      },
      {
        "label": "off",
        "mechanism_on": False,
        "is_null": True,
        "substrate": [
          "s"
        ],
        "metric": 0.2
      }
    ],
    "note": "REFERENT-CONSTRUCTED (9th primary axis) regression, probe arm. REFERENT PROVENANCE = model-constructed (e.g. Claude-Opus-4-7 root-cause groups), directly observed (witness_observes == referent), record injective. Every instrument-read field is identical to the control; only referent_provenance differs. Pre-wire-in both arms audited to DISCRIMINATES (the instrument was provably insensitive to referent provenance). Post-wire-in the probe flags REFERENT-CONSTRUCTED: a self-sealing tautology (the model is graded against its own output) that no composition of the 8 prior axes could catch. Distinct from CONSEQUENCE-WITNESSED (external referent, model-constructed proxy) and from witness-strength (conceded vs measured).",
    "expected": [
      "REFERENT-CONSTRUCTED"
    ]
  },
  {
    "name": "BLINDSPOT-B (CONTROL): referent is EXTERNALLY ANCHORED (human-audited root-cause groups), directly observed, injective",
    "type": "ablation",
    "mechanism_lever": "m",
    "referent": "root-cause group structure",
    "witness_observes": [
      "root-cause group structure"
    ],
    "referent_provenance": "externally-anchored",
    "rows": [
      {
        "label": "on",
        "mechanism_on": True,
        "substrate": [
          "s",
          "m"
        ],
        "metric": 1.0
      },
      {
        "label": "off",
        "mechanism_on": False,
        "is_null": True,
        "substrate": [
          "s"
        ],
        "metric": 0.2
      }
    ],
    "note": "REFERENT-CONSTRUCTED (9th primary axis) regression, control arm. REFERENT PROVENANCE = externally-anchored (human-audited root-cause groups), directly observed, record injective. Byte-identical to the probe in every instrument-read field; only referent_provenance differs. Audits to DISCRIMINATES (no flags): the externally-anchored referent is not a self-sealing tautology. The probe/control contrast is the discriminating test that operationalizes the 9th axis.",
    "expected": []
  },  {
    "name": "CO-OCCURRENCE (synthetic): self-keyed knob AND lossy record (2x2 joint cell)",
    "type": "knob-sweep",
    "mechanism": "detector confidence threshold",
    "metric": "reported precision",
    "knob": "confidence threshold",
    "rows": [
      {"label": "thr=0.5", "mechanism_on": True, "knob": 0.5, "metric": 0.5,
       "record": "stored-list-L", "referent_value": "true-precision-1.0"},
      {"label": "thr=1.0", "mechanism_on": True, "knob": 1.0, "metric": 1.0,
       "record": "stored-list-L", "referent_value": "true-precision-0.0"}
    ],
    "expected": ["SELF-KEYED", "LOSSY-PROJECTION"],
    "note": "CO-OCCURRENCE cell of the NOT-SELF-KEYED x LOSSY-PROJECTION 2x2 joint. Both axes fire on DISJOINT evidence: SELF-KEYED from the knob (spearman +1.000, one-to-many knob->metric) and LOSSY-PROJECTION from the record (stored-list-L maps to 2 distinct referent values, many-to-one record->referent, the Four Ledgers general case). Every other axis is N/A. Completes the 2x2: the suite already witnesses SELF-KEYED-not-LOSSY (retention self-specimen: SELF-KEYED fires, no record -> LOSSY N/A) and LOSSY-not-SELF-KEYED (Four Ledgers specimen: LOSSY fires, no knob -> SELF-KEYED N/A); this cell witnesses BOTH. Settles the open thread 'self-keyed as a special case of the Four Ledgers result': neither axis is a special case of the other, and the co-occurrence is realizable, so the README's 'orthogonal twins' claim is a positive independence witness, not just non-nesting."
  },
  {
    "name": "AGGREGATION-REVERSAL control: aggregate TRUE (Simpson-consistent pooling) -- S0",
    "type": "cross-model",
    "mechanism": "mechanism improves outcome within every subgroup",
    "mechanism_lever": "mechanism",
    "metric": "outcome score (higher better)",
    "knob": "subgroup (easy / hard)",
    "rows": [
      {"label": "easy - mech",  "mechanism_on": True,  "subgroup": "easy", "n": 90, "metric": 0.90},
      {"label": "easy - null",  "mechanism_on": False, "is_null": True, "subgroup": "easy", "n": 10, "metric": 0.80},
      {"label": "hard - mech",  "mechanism_on": True,  "subgroup": "hard", "n": 10, "metric": 0.40},
      {"label": "hard - null",  "mechanism_on": False, "is_null": True, "subgroup": "hard", "n": 90, "metric": 0.30}
    ],
    "expected": [],
    "note": "AGGREGATION-REVERSAL (8th primary axis) regression, control arm. Mechanism wins within both subgroups (0.90>0.80 easy, 0.40>0.30 hard) and the n-weighted pooled direction is consistent (pooled mechanism 0.87 vs pooled null 0.43), so the aggregate claim is TRUE and no axis fires -> DISCRIMINATES. Byte-identical to the S1 probe in every instrument-read field EXCEPT the n-weights (the discriminating field for this axis): same metric values, same subgroups, same mechanism_on. Locks the 8th axis's clean control into the permanent suite."
  },
  {
    "name": "AGGREGATION-REVERSAL probe: aggregate FALSE (Simpson reversal, mech wins every subgroup) -- S1",
    "type": "cross-model",
    "mechanism": "mechanism improves outcome within every subgroup",
    "mechanism_lever": "mechanism",
    "metric": "outcome score (higher better)",
    "knob": "subgroup (easy / hard)",
    "rows": [
      {"label": "easy - mech",  "mechanism_on": True,  "subgroup": "easy", "n": 10, "metric": 0.90},
      {"label": "easy - null",  "mechanism_on": False, "is_null": True, "subgroup": "easy", "n": 90, "metric": 0.80},
      {"label": "hard - mech",  "mechanism_on": True,  "subgroup": "hard", "n": 90, "metric": 0.40},
      {"label": "hard - null",  "mechanism_on": False, "is_null": True, "subgroup": "hard", "n": 10, "metric": 0.30}
    ],
    "expected": ["AGGREGATION-REVERSAL"],
    "note": "AGGREGATION-REVERSAL (8th primary axis) regression, probe arm. Mechanism wins within BOTH subgroups (0.90>0.80 easy, 0.40>0.30 hard) yet the n-weighted pooled direction REVERSES it (pooled mechanism 0.45 vs pooled null 0.75): the aggregate claim is an artifact of the pooling weights, not the mechanism (Simpson's paradox). Fires in the BEATS-NULL-PASS cell (within-subgroup beats hold, so the flat check passes and is silent) -- the structural independence that distinguishes a primary axis from a one-directional refinement. Discriminating field vs the S0 control: only the n-weights differ (10/90/90/10 vs 90/10/10/90); every metric value, subgroup, and mechanism_on is byte-identical. This is the permanent positive witness the standalone axis8_probe.py left out of the main suite."
  },
  {
    "name": "AGGREGATION-REVERSAL mirror: null wins every subgroup, mech wins pooled -- S2",
    "type": "cross-model",
    "mechanism": "mechanism improves outcome within every subgroup",
    "mechanism_lever": "mechanism",
    "metric": "outcome score (higher better)",
    "knob": "subgroup (easy / hard)",
    "rows": [
      {"label": "easy - mech",  "mechanism_on": True,  "subgroup": "easy", "n": 90, "metric": 0.80},
      {"label": "easy - null",  "mechanism_on": False, "is_null": True, "subgroup": "easy", "n": 10, "metric": 0.90},
      {"label": "hard - mech",  "mechanism_on": True,  "subgroup": "hard", "n": 10, "metric": 0.30},
      {"label": "hard - null",  "mechanism_on": False, "is_null": True, "subgroup": "hard", "n": 90, "metric": 0.40}
    ],
    "expected": ["NULL-REACHES-HEADLINE", "AGGREGATION-REVERSAL"],
    "note": "AGGREGATION-REVERSAL (8th primary axis) regression, mirror arm (fail cell). The NULL wins within both subgroups (0.90>0.80 easy, 0.40>0.30 hard) yet the n-weighted pooled direction reverses it (pooled mechanism 0.75 vs pooled null 0.45). Fires in the BEATS-NULL-FAIL cell (null 0.9 >= mechanism 0.8, so the flat check ALSO fires NULL-REACHES-HEADLINE). Together S1 (pass cell) and S2 (fail cell) witness the axis firing in BOTH BEATS-NULL cells -- the structural-independence signature that axis8_probe.py proved and this entry now locks into the permanent suite."
  },
  {
    "name": "DOSE-RESPONSE true dose-response, dose DECLARED (FP-side schema-boundary witness) -- DR0",
    "type": "ablation",
    "mechanism": "score centering (SC)",
    "mechanism_lever": "score_centering",
    "metric": "training accuracy (%)",
    "knob": "TIM severity (quantization/noise scale)",
    "rows": [
      {"label": "FP8 sampler (mild TIM)", "mechanism_on": True, "substrate": ["qwen3-30b", "intellect2", "fp8-sampler"], "metric": 58},
      {"label": "FP8 sampler (mild TIM) - TIS null", "mechanism_on": False, "is_null": True, "substrate": ["qwen3-30b", "intellect2", "fp8-sampler"], "metric": 58},
      {"label": "FP4 KV (severe TIM)", "mechanism_on": True, "substrate": ["qwen3-30b", "intellect2", "fp4-kv"], "metric": 52},
      {"label": "FP4 KV (severe TIM) - TIS null", "mechanism_on": False, "is_null": True, "substrate": ["qwen3-30b", "intellect2", "fp4-kv"], "metric": 51},
      {"label": "INT8+INT4 (most severe)", "mechanism_on": True, "substrate": ["qwen3-30b", "intellect2", "int8-int4"], "metric": 30},
      {"label": "INT8+INT4 (most severe) - TIS null", "mechanism_on": False, "is_null": True, "substrate": ["qwen3-30b", "intellect2", "int8-int4"], "metric": 12}
    ],
    "expected": ["NULL-REACHES-HEADLINE", "DOSE-RESPONSE"],
    "note": "FP-SIDE SCHEMA-BOUNDARY (declared arm), the paper's ACTUAL data (2609.20807 Section 5.4, 30B INTELLECT-2 math, SC vs TIS). The claim is a TRUE dose-response: within-dose SC>=TIS at every dose (58>=58, 52>=51, 30>=12), so the flat BEATS-NULL check is the wrong instrument. It pools cross-dose max (max-mech 58 vs max-null 58) and fires NULL-REACHES-HEADLINE as a false positive; the DOSE-RESPONSE refinement (>=2 substrate levels, within-dose direction uniformly mechanism-favorable) catches it. The dose is DECLARED as a substrate, so the refinement is in scope. Declared arm of the FP-side schema-boundary pair (DR0/DRu). Promoted from schema_boundary_fp.py (D0)."
  },
  {
    "name": "DOSE-RESPONSE true dose-response, dose UNDECLARED (schema-boundary: over-fire returns) -- DRu",
    "type": "ablation",
    "mechanism": "score centering (SC)",
    "mechanism_lever": "score_centering",
    "metric": "training accuracy (%)",
    "knob": "TIM severity (quantization/noise scale)",
    "rows": [
      {"label": "mild TIM", "mechanism_on": True, "substrate": ["qwen3-30b", "intellect2", "undeclared-dose"], "metric": 58},
      {"label": "mild TIM - TIS null", "mechanism_on": False, "is_null": True, "substrate": ["qwen3-30b", "intellect2", "undeclared-dose"], "metric": 58},
      {"label": "severe TIM", "mechanism_on": True, "substrate": ["qwen3-30b", "intellect2", "undeclared-dose"], "metric": 52},
      {"label": "severe TIM - TIS null", "mechanism_on": False, "is_null": True, "substrate": ["qwen3-30b", "intellect2", "undeclared-dose"], "metric": 51},
      {"label": "most severe", "mechanism_on": True, "substrate": ["qwen3-30b", "intellect2", "undeclared-dose"], "metric": 30},
      {"label": "most severe - TIS null", "mechanism_on": False, "is_null": True, "substrate": ["qwen3-30b", "intellect2", "undeclared-dose"], "metric": 12}
    ],
    "expected": ["NULL-REACHES-HEADLINE"],
    "note": "FP-SIDE SCHEMA-BOUNDARY (undeclared arm): the SAME data as DR0 (true dose-response, SC>=null at every dose) but with the dose NOT declared as a substrate (all rows share one substrate). The DOSE-RESPONSE refinement is N/A (fewer than 2 substrate levels declare both a mechanism and a null reading -> no dose structure), so the flat BEATS-NULL check over-fires NULL-REACHES-HEADLINE on a TRUE claim and no refinement catches it. Same root as the FN side (undeclared -> the structure is not in the spec) but OPPOSITE behavior (undeclared -> over-fire/false-positive on the FP side, silent/miss on the FN side). Locks the dose schema-boundary into the main regression suite. Mirrors T3u/S2u/D2u/TR2u/SP2u/MP2u. Promoted from schema_boundary_fp.py (D3)."
  },
  {
    "name": "headline-layer baseline-omission (Ebola structure, clean data) -- NORMALIZER-OMISSION blind-spot witness",
    "type": "cross-model",
    "mechanism": "being a woman (claim referent)",
    "mechanism_lever": "sex",
    "metric": "share of cases (higher = bigger toll)",
    "rows": [
      {"label": "women cases", "mechanism_on": True,  "substrate": ["ebola_cases"], "metric": 0.54, "n": 5400},
      {"label": "men cases",   "mechanism_on": False, "is_null": True, "substrate": ["ebola_cases"], "metric": 0.46, "n": 4600}
    ],
    "expected": [],
    "note": "HEADLINE-LAYER BLIND-SPOT WITNESS (2026-09-18, news-verdict class n=3). The data is a clean direction (0.54 > 0.46), no subgroup/pooling structure (AGGREGATION-REVERSAL N/A), no temporal structure, no declared referent. A real headline uses exactly this data to overstate: 'disproportionate toll on women' drops the population baseline (women ~50% of DRC population -> only 1.068x per-capita, not disproportionate). The baseline is NOT in the rows, so the data-layer instrument returns DISCRIMINATES (clean) on data a headline uses to overstate. Locks the boundary: NORMALIZER-OMISSION has a DATA-LAYER subset the instrument catches (pooling reversal, selection bias, temporal onset, referent construction) and a HEADLINE-LAYER subset it is structurally blind to (clean data, overstatement purely in the prose). This is the discriminating case the class falsifier called for: a direction-honest claim whose normalizer is omitted from the headline, not the data. expected: [] = the instrument is clean here by design (it reads the rows, not the prose)."
  },
  {
    "name": "headline-layer baseline-omission (PIRNN 2609.19871 title, clean data) -- NORMALIZER-OMISSION arXiv-population witness",
    "type": "cross-model",
    "mechanism": "physical knowledge on historical data (backcast) vs enforcing physical constraints on the forecast (forecast)",
    "mechanism_lever": "backcast physics vs forecast physics (the title's 'matters more than')",
    "metric": "-pooled mean RMSE (negated; higher = better; the title drops which metric)",
    "rows": [
      {"label": "BcastPIRNN (backcast, GRU)",    "mechanism_on": True,  "substrate": ["GRU"],     "metric": -1.217},
      {"label": "BcastPIRNN (backcast, bi-GRU)", "mechanism_on": True,  "substrate": ["bi-GRU"],  "metric": -0.792},
      {"label": "BcastPIRNN (backcast, LSTM)",   "mechanism_on": True,  "substrate": ["LSTM"],    "metric": -0.845},
      {"label": "BcastPIRNN (backcast, bi-LSTM)","mechanism_on": True,  "substrate": ["bi-LSTM"], "metric": -0.789},
      {"label": "FcastPIRNN (forecast, GRU)",    "mechanism_on": False, "is_null": True, "substrate": ["GRU"],     "metric": -1.655},
      {"label": "FcastPIRNN (forecast, bi-GRU)", "mechanism_on": False, "is_null": True, "substrate": ["bi-GRU"],  "metric": -1.832},
      {"label": "FcastPIRNN (forecast, LSTM)",   "mechanism_on": False, "is_null": True, "substrate": ["LSTM"],    "metric": -1.551},
      {"label": "FcastPIRNN (forecast, bi-LSTM)","mechanism_on": False, "is_null": True, "substrate": ["bi-LSTM"], "metric": -1.222}
    ],
    "expected": [],
    "note": "HEADLINE-LAYER BLIND-SPOT WITNESS (2026-09-20, arXiv population; the arXiv analog of the Ebola news-population witness above). The title 'Physical knowledge on historical data matters more than enforcing physical constraints on the forecast' is a load-bearing comparative that drops the basis: which metric (RMSE? NSE? MAE?) and which population (which of 12 datasets? which of 4 architectures?). The data rows (Table 3 ablation, pooled mean RMSE, negated so higher is better) are a clean direction: Bcast beats Fcast in ALL 4 architectures (1.217<1.655, 0.792<1.832, 0.845<1.551, 0.789<1.222). The instrument reads the rows, not the title, so it returns DISCRIMINATES (clean) on data a headline uses to make a load-bearing claim by dropping the normalizer (the basis: metric + population). This is the discriminating test the base-rate thought queued: the headline-layer blindness (04027914, locked on the news population, 14% positive) extends to arXiv titles (the 57% positive arXiv base rate is because arXiv abstracts are mostly self-aware, except the title). expected: [] = the instrument is clean here by design (it reads the rows, not the title)."
  },
  {
    "name": "wason-consensus (2609.20543): consensus tracks correctness -- S0",
    "type": "cross-model",
    "mechanism": "belief-anchored agent deliberation reaches collective cognition",
    "mechanism_lever": "agent deliberation",
    "metric": "full-consensus rate (headline)",
    "rows": [
      {"label": "reasoner classic",    "mechanism_on": True, "metric": 96.0, "mechanism_axis": 84.0},
      {"label": "reasoner isomorphic", "mechanism_on": True, "metric": 24.7, "mechanism_axis": 24.7}
    ],
    "expected": [],
    "note": "WRONG-AXIS (CO-MOVES) control arm, fresh domain (collective cognition / social simulation, Wason selection task). The paper (2609.20543) replays 100 held-out human Wason groups with belief-anchored LLM agent groups and headlines the full-consensus rate as evidence agents are 'more consensual.' Control: when the memorizable classic answer is removed (isomorphic reparameterization, neutral tokens), the headline consensus DROPS to track the mechanism's own axis -- full consensus 96.0->24.7 while correct-consensus 84.0->24.7. metric and mechanism_axis co-move (pearson r=+1.000) -> the consensus headline discriminates 'collective cognition' from 'mere convergence'; the claim DISCRIMINATES. Byte-identical to S1 in every instrument-read field except row-2 metric (24.7 vs 98.7), the discriminating field for this axis."
  },
  {
    "name": "wason-consensus (2609.20543): consensus decoupled from correctness -- S1",
    "type": "cross-model",
    "mechanism": "belief-anchored agent deliberation reaches collective cognition",
    "mechanism_lever": "agent deliberation",
    "metric": "full-consensus rate (headline)",
    "rows": [
      {"label": "reasoner classic",    "mechanism_on": True, "metric": 96.0, "mechanism_axis": 84.0},
      {"label": "reasoner isomorphic", "mechanism_on": True, "metric": 98.7, "mechanism_axis": 24.7}
    ],
    "expected": ["WRONG-AXIS"],
    "note": "WRONG-AXIS (CO-MOVES) probe arm, fresh domain (collective cognition / social simulation, Wason selection task). The paper's own central caution made checkable: 'simulated consensus did not track collective accuracy.' On the isomorphic reparameterization (memorizable answer removed), the reasoning mode reaches near-total full consensus (96.0->98.7, UP) but correct-consensus collapses (84.0->24.7, DOWN) and wrong-consensus rises to 74.0% -- the agents agree, mostly on the wrong answer. The headline metric and the mechanism's own axis are anti-correlated (pearson r=-1.000): the consensus headline does NOT discriminate 'collective cognition' from 'mere convergence,' so the load-bearing 'agents are more consensual' claim is a wrong-axis reading. Discriminating field vs S0: only row-2 metric differs (98.7 vs 24.7); mechanism_axis is byte-identical (84.0, 24.7). Locks the WRONG-AXIS axis into a fresh domain (social simulation / collective cognition) where the paper's negative result IS the wrong-axis pattern."
  },
  {
    "name": "harness-fixed-sham (2609.20474): Fixed beats Sham -- S0 (the paper's contrast)",
    "type": "ablation",
    "mechanism": "prewritten task-specific planning information creates value",
    "mechanism_lever": "plan",
    "metric": "task success rate (tau^2-bench Retail+Airline)",
    "rows": [
      {"label": "Fixed (task-specific plan, from reference actions)", "mechanism_on": True,  "substrate": ["task-specific-skeleton"], "metric": 0.1338},
      {"label": "Sham (shuffled policy text, word-count-matched)",     "mechanism_on": False, "substrate": ["generic-filler"],         "metric": 0.0621}
    ],
    "expected": ["CONFOUNDED"],
    "note": "ISOLATED (CONFOUNDED) witness, fresh domain (agent harnesses, tau^2-bench). The paper (2609.20474) headlines 'Fixed beats Sham by 7.17pp, isolating the contribution of guidance content.' The seam: Sham is word-count-matched but NOT task-specificity-matched; the Fixed plan is built from reference actions (substeps, dependency-depth, tool count from the reference solution, S4.1.2), so the contrast is 'inject the task's action skeleton' vs 'generic filler of equal length' -- task-specific prior STRUCTURE, not 'planning' as a mechanism. ISOLATED fires: the null (Sham, generic-filler) drops the task-specific-skeleton substrate beyond the plan lever, so the 7.17pp is the substrate, not the mechanism. The Sham-Minimal placebo (1.89pp, CI spans 0) rules out filler doing harm but does NOT separate content from structure. metrics = the paper's pooled two-model Fixed scores (deepseek 0.1343, qwen 0.1333, avg 0.1338) minus the 7.17pp gap (Sham 0.0621); relative, the gap is the point."
  },
  {
    "name": "harness-fixed-sham (2609.20474): task-specific-but-shuffled control -- S1 (the discriminating case)",
    "type": "ablation",
    "mechanism": "prewritten task-specific planning information creates value",
    "mechanism_lever": "plan",
    "metric": "task success rate (tau^2-bench Retail+Airline)",
    "rows": [
      {"label": "Fixed (task-specific plan, from reference actions)", "mechanism_on": True,  "substrate": ["task-specific-skeleton"], "metric": 0.1338},
      {"label": "TaskShuffled (same task, same words, scrambled order)", "mechanism_on": False, "substrate": ["task-specific-skeleton"], "metric": 0.0621}
    ],
    "expected": [],
    "note": "ISOLATED (passes) control arm, the discriminating case the paper's design cannot run (S4.1.2 / closing line: 'balanced component comparisons with documented plan provenance'). The null (TaskShuffled) HOLDS the task-specific-skeleton substrate -- same task, same words, scrambled order/structure -- so the contrast is properly matched and ISOLATED passes: the 7.17pp would be a legitimate structure effect. Byte-identical to S0 in every instrument-read field except the null's substrate (generic-filler -> task-specific-skeleton), the discriminating field for the ISOLATED axis. RESOLVED (direction, 2026-09-19): re-read S4.1.2 in the primary source (explore/2609.20474/paper.txt) -- Sham is 'shuffled words from the domain policy using seed 2701,' word-count-matched, i.e. GENERIC FILLER, NOT the plan's own words scrambled. So the paper's Sham is NOT the TaskShuffled discriminating arm (plan's own words scrambled); it drops BOTH task-specific content and structure. The 7.17pp (Fixed vs Sham) = task-specific prior (content+structure) vs generic filler -- it conflates content and structure, so the paper's 'isolating the contribution of guidance content' overclaims: it isolates task-specific PRIOR, not content alone. The placebo (Sham-Minimal 1.89pp, CI [-3.45,+7.09] spans 0, S5.2) confirms Sham~base (filler inert), so the 7.17pp is the prior, not a filler-harm artifact. Direction algebra (S1 note was right; the EXPLORE teardown's shorthand was TRANSPOSED): with Fixed=C+S, TaskShuffled=C (content held, structure scrambled), Sham=base -- task-shuffled~Sham => C~base => content effect~0 => gain is STRUCTURE; task-shuffled~Fixed => S~0 => gain is CONTENT. The discriminating arm (TaskShuffled) was NOT run by the paper; the specimen models TaskShuffled~Sham (metric 0.0621) => structure matters. Net: the 7.17pp is a task-specific-prior (content+structure) effect, not a pure content effect; the content-vs-structure split is unmeasured."
  },
  {
    "name": "haegeo funnel (2609.06027): 'rarely converts verification into recovery'",
    "type": "funnel",
    "mechanism": "defense prompting converts verification into recovery",
    "metric": "conversion rate P(R|V)",
    "funnel_stages": [
      {"stage": "A->V (reach)", "rate": 0.17},
      {"stage": "V->R (conversion)", "rate": 0.667}
    ],
    "headline_stage": "V->R (conversion)",
    "rows": [
      {"label": "defense", "mechanism_on": True, "metric": 0.667},
      {"label": "base", "mechanism_on": False, "is_null": True, "metric": 0.667}
    ],
    "expected": ["NULL-REACHES-HEADLINE", "FUNNEL-STAGE-MISATTRIBUTION"],
    "note": "LIVE EXTERNAL SPECIMEN (2609.06027, HAE-GEO, Bi et al.). The abstract's 'defense prompting increases verification, yet rarely converts verification into recovery' names the CONVERSION stage (V->R) as the bottleneck. But the paper's own V2R conditional is a MAJORITY (0.667 >= 0.5 at L2/L3), so the 'rarely' qualifier is contradicted; the real bottleneck is the upstream REACH stage (A->V, P(V|E) ~0.17, rare). The data-layer instrument (BEATS-NULL) reads the rows, not the headline's stage-attribution: the conditional-vs-marginal framing swap flips the claim verdict (CONTRADICTED -> SUPPORTED) but the data-layer verdict is unchanged (both NULL-REACHES-HEADLINE; the funnel data is the same for both framings). FUNNEL-STAGE-MISATTRIBUTION fires because the named stage (conversion, 0.667) is not the rarest stage (reach, 0.17). DISTINCT axis, not a composition (WRONG-AXIS x scope-dimension): WRONG-AXIS does not fire (the conversion rate is a majority, not null) and the pipeline stage is not an existing scope-dimension. See funnel_swap_witness.py for the discriminating test."
  },
  {
    "name": "haegeo funnel (2609.06027): correct attribution (reach stage)",
    "type": "funnel",
    "mechanism": "defense prompting rarely reaches verification",
    "metric": "verification rate P(V|E)",
    "funnel_stages": [
      {"stage": "A->V (reach)", "rate": 0.17},
      {"stage": "V->R (conversion)", "rate": 0.667}
    ],
    "headline_stage": "A->V (reach)",
    "rows": [
      {"label": "defense", "mechanism_on": True, "metric": 0.17},
      {"label": "base", "mechanism_on": False, "is_null": True, "metric": 0.02}
    ],
    "expected": [],
    "note": "PASS CELL (2609.06027, HAE-GEO). The headline names the REACH stage (A->V, 0.17), which IS the rarest stage. Correct attribution, so FUNNEL-STAGE-MISATTRIBUTION is N/A. The data-layer: defense 0.17 > base 0.02, so BEATS-NULL passes (DISCRIMINATES). Locks in the pass cell: the check fires only on misattribution (named stage not rarest), not on correct attribution (named stage is rarest). Differs from the misattribution specimen only in headline_stage (V->R -> A->V) and the data-layer rows (the reach-stage contrast, a real beat)."
  },
  {
    "name": "mtva middle-three (2609.20152): narrative-selected subset",
    "type": "subset",
    "mechanism": "the middle three models (narrative-defined, not positional) have a small task-score span",
    "metric": "task-score span within the named subset (max-min)",
    "referent": "the middle three models (narrative-defined, not positional)",
    "referent_provenance": "narrative-selected",
    "subset_criterion": {"op": "<=", "threshold": 0.5},
    "rows": [
      {"label": "narrative-selected middle three (positions 4-6), task span", "mechanism_on": True, "substrate": ["mtva_table", "narrative_subset"], "metric": 0.5},
      {"label": "positional middle three (positions 3-5), task span", "mechanism_on": False, "is_null": True, "substrate": ["mtva_table", "positional_subset"], "metric": 5.5}
    ],
    "expected": ["NULL-REACHES-HEADLINE", "SELECTION-ON-NARRATIVE"],
    "note": "LIVE (2609.20152, MTVA-Bench 7.3). The headline's subset (the 'middle three models') is narrative-conditional: the narrative selects the subset by the criterion task span <= 0.5, and the positional middle (positions 3-5, span 5.5) does NOT satisfy the criterion. The data-layer: BEATS-NULL fires (null 5.5 >= mechanism 0.5) — a false flag from the direction error (the claim is a spread, lower-is-better; BEATS-NULL assumes higher-is-better). SELECTION-ON-NARRATIVE fires because the null row does not satisfy the narrative criterion. Distinct from SELECTION-BIAS (7 distinct model units, not repeated draws) and REFERENT-CONSTRUCTED (narrative-selected, not model-constructed). See narrative_subset_swap_witness.py for the discriminating test."
  },
  {
    "name": "mtva middle-three (2609.20152): positional control (pass cell)",
    "type": "subset",
    "mechanism": "the positional middle three have a small task-score span",
    "metric": "task-score span within the named subset (max-min)",
    "referent": "the positional middle three (positions 3-5)",
    "referent_provenance": "positional",
    "subset_criterion": {"op": "<=", "threshold": 0.5},
    "rows": [
      {"label": "positional middle three (positions 3-5), task span", "mechanism_on": True, "substrate": ["mtva_table", "positional_subset"], "metric": 0.5},
      {"label": "positional middle three (positions 4-6), task span", "mechanism_on": False, "is_null": True, "substrate": ["mtva_table", "positional_subset"], "metric": 0.4}
    ],
    "expected": [],
    "note": "PASS CELL (synthetic control for the 11th axis). The null row (span 0.4) ALSO satisfies the criterion (<= 0.5), so the subset is not narrative-conditional: SELECTION-ON-NARRATIVE is N/A. The data-layer: BEATS-NULL passes (0.5 > 0.4, the pass cell). Locks in the pass cell: the check fires only when the null row does NOT satisfy the criterion, not when it does."
  },
  {
    "name": "BBC Lindsey-Graham sanctions (cqvgy34ndj4eo): narrative-selected 'China and India'",
    "type": "subset",
    "mechanism": "narrative-selected 'top purchasers' subset (China and India) is crude-oil-prominent",
    "mechanism_lever": "subset_selection",
    "referent": "the top purchasers of Russian oil and gas (the bill's tariff referent)",
    "referent_provenance": "narrative-selected",
    "metric": "crude-oil export rank of the least-prominent member of the named subset (lower = more prominent)",
    "subset_criterion": {"op": "<=", "threshold": 2},
    "rows": [
      {"label": "narrative-selected 'China and India' (crude top-2), crude rank of least-prominent member (India)", "mechanism_on": True, "substrate": ["bbc_crea", "narrative_subset"], "metric": 2},
      {"label": "data-ranked oil+gas top-5 intersection (China and Hungary), crude rank of least-prominent member (Hungary)", "mechanism_on": False, "is_null": True, "substrate": ["bbc_crea", "gas_top5_intersection"], "metric": 4}
    ],
    "expected": ["NULL-REACHES-HEADLINE", "SELECTION-ON-NARRATIVE"],
    "note": "LIVE (BBC cqvgy34ndj4eo, 2026-09-19). The headline's subset ('the top purchasers, most significantly China and India') is narrative-conditional: the narrative selects the subset by the CRUDE-OIL ranking (top-2, CREA China 50% / India 37%, Dec 2022-Aug 2026), but the bill's actual tariff referent is the top-5 purchasers of oil AND gas. India is top-5 crude but ABSENT from the gas top-5 (China, France, Belgium, Japan, Hungary); Hungary is top-5 in BOTH crude and gas (4th in the bill's oil top-5) yet excluded by the narrative's crude top-2 criterion. The data-ranked oil+gas control (China and Hungary; least-prominent member Hungary at crude rank 4, not in the crude top-2) does NOT satisfy the crude top-2 criterion (<= 2). The data-layer: BEATS-NULL fires (null 4 >= mechanism 2) — a false flag from the direction error (the claim is lower-is-better, a lower crude rank is more prominent; BEATS-NULL assumes higher-is-better). SELECTION-ON-NARRATIVE fires because the null row does not satisfy the narrative criterion. Distinct from SELECTION-BIAS (China/India/Hungary are distinct country units, not repeated draws) and REFERENT-CONSTRUCTED (narrative-selected, not model-constructed). Provenance: BBC CREA crude figures; gas top-5 list corroborated by CBS/PBS/Reuters (2026-07)."
  },
{'name': "Tailored-to-you 2609.20077 — advice-uptake: 'exposure-driven' headline vs personalisation null",
 'mechanism': 'repeated exposure (session count) drives the advice-uptake change over the 5 sessions',
 'mechanism_lever': "session (exposure dose) — the headline's claimed driver",
 'metric': "advice-uptake effect magnitude (Cohen's d, higher = larger effect on uptake)",
 'claim': 'the change in advice uptake over time is driven primarily by repeated exposure, not by '
          'personalisation',
 'rows': [{'label': 'exposure (session main effect, d)',
           'mechanism_on': True,
           'substrate': ['advice-uptake'],
           'metric': 0.08},
          {'label': 'personalisation (condition main effect, survey, session-1 deficit, d)',
           'mechanism_on': False,
           'is_null': True,
           'substrate': ['advice-uptake'],
           'metric': 0.41},
          {'label': 'personalisation (condition main effect, memory, session-1 deficit, d)',
           'mechanism_on': False,
           'substrate': ['advice-uptake'],
           'metric': 0.35}],
 'expected': ['NULL-REACHES-HEADLINE'],
 'note': "LIVE EXTERNAL SPECIMEN (arXiv 2609.20077, 'Tailored to you: longitudinal effects of personalising "
         "language models', 992 participants, 5 days, control vs memory-based vs survey-based "
         "personalisation). The headline claim 'changes over time are driven primarily by repeated exposure "
         "rather than personalisation itself' is a SCOPE TRANSPOSITION: it holds for competence (session "
         'd=0.15 p<0.001; condition d=-0.04 p=0.811 / d=0.01 p=0.966, interactions null) and usefulness '
         '(session d=0.12 p<0.001; condition d=0.03 p=0.274 / d=0.02 p=0.586, interactions null), where the '
         'personalisation effect is null. It is CONTRADICTED by advice-uptake: at session 1 BOTH '
         'personalisation conditions show a large deficit vs control (memory d=-0.35 p=0.003; survey d=-0.41 '
         'p<0.001) — a personalisation effect ~5x the session (exposure) effect (d=0.08 p<0.001) — and the '
         "survey x session interaction is significant (p=0.046, survey catches up). The paper's OWN "
         "reactance interpretation (s5: 'encountering a model that appears to know something about the user "
         'before rapport has been established could feel intrusive... making its advice less welcome... '
         "repeated exposure reduces reactance') attributes the deficit to PERSONALISATION with exposure as "
         "the attenuator — the inverse of the headline's causal direction. PROXY CAVEAT: the headline row is "
         'the session MAIN effect (within-group slope) and the null rows are the condition MAIN effects '
         "(between-group session-1 levels); comparing their Cohen's d is a magnitude proxy, not a "
         "like-for-like contrast. The paper hedges with 'several changes', so this is a soft scope "
         'transposition (outcome scope), not a hard over-claim. AGGREGATION-REVERSAL checked and REJECTED: '
         'no outcome shows a Simpson reversal (competence condition d=-0.04/0.01 opposite tiny directions; '
         "usefulness/creepiness/uptake same-direction), so the pooled 'exposure' factor does not cancel a "
         'sign reversal — the finding is scope, not Simpson.'},
  {
    "name": "harness phase-composition (2609.20804): planning reduces trajectory length via Verify-phase reduction",
    "type": "ablation",
    "mechanism": "planning reduces median trajectory length (post-edit verification)",
    "mechanism_lever": "planning",
    "metric": "median trajectory length (turns) for Nemotron-3 550B on SWE-Bench",
    "annotation_provenance": "llm-judge-non-public",
    "rows": [
      {"label": "T4 w/o plan (planning off), median turns", "mechanism_on": False, "is_null": True, "substrate": ["swe-bench", "550b", "t4"], "metric": 108},
      {"label": "T4 (planning on), median turns", "mechanism_on": True, "substrate": ["swe-bench", "550b", "t4", "planning"], "metric": 74}
    ],
    "expected": ["NULL-REACHES-HEADLINE", "ANNOTATOR-SELF-KEYED"],
    "note": "LIVE (2609.20804, 'An Empirical Study of Harness Design for Coding Agents'). The 12th primary axis (ANNOTATOR-SELF-KEYED): the mechanism explanation (the phase attribution - 'the reduction is attributed to the Verify phase') rests on GPT-5.5 phase labels (validated on a 200-trajectory sample, kappa=0.929) over NON-PUBLIC trajectories (no code/trajectory/data availability statement). The aggregate (108->74 turns) is stranger-rerunnable (direct turn counts from logs), but the 'why' (the phase composition) is not: a stranger cannot re-derive the phase labels without the judge and the non-public trajectories. Data-layer: BEATS-NULL fires NULL-REACHES-HEADLINE (74 < 108) - a direction-error false flag (the claim is a reduction, lower-is-better; BEATS-NULL assumes higher-is-better). ISOLATED passes (T4 w/o plan drops only the planning lever). Distinct from NO-EMPIRICAL-CONTENT (the data IS there) and from SELF-KEYED (no continuous knob; this is about the annotation layer, not the knob). Mirror of the ATLAS CLASSIFIER-position channel but with a computable hard layer. See the recall-null pass cell for the discriminating control."
  },
  {
    "name": "harness recall-null (2609.20804): no accuracy gain from recall (dose readout, pass cell)",
    "type": "ablation",
    "mechanism": "recoverable elision (recall_event) adds accuracy",
    "mechanism_lever": "recall",
    "metric": "SWE-Bench Verified SR (%) at 128k",
    "annotation_provenance": "deterministic-readout",
    "rows": [
      {"label": "T1 elision alone (30B)", "mechanism_on": False, "is_null": True, "substrate": ["elision"], "metric": 25.0},
      {"label": "T2 elision+recall (30B)", "mechanism_on": True, "substrate": ["elision", "recall"], "metric": 26.0},
      {"label": "T1 elision alone (120B)", "mechanism_on": False, "is_null": True, "substrate": ["elision"], "metric": 44.4},
      {"label": "T2 elision+recall (120B)", "mechanism_on": True, "substrate": ["elision", "recall"], "metric": 45.2},
      {"label": "T1 elision alone (550B)", "mechanism_on": False, "is_null": True, "substrate": ["elision"], "metric": 65.2},
      {"label": "T2 elision+recall (550B)", "mechanism_on": True, "substrate": ["elision", "recall"], "metric": 67.4},
      {"label": "T1 elision alone (Mistral)", "mechanism_on": False, "is_null": True, "substrate": ["elision"], "metric": 68.6},
      {"label": "T2 elision+recall (Mistral)", "mechanism_on": True, "substrate": ["elision", "recall"], "metric": 67.0}
    ],
    "expected": ["NULL-REACHES-HEADLINE"],
    "note": "PASS CELL (2609.20804, the discriminating control for the 12th axis). The 'why' for the null (no accuracy gain from recall) is the DOSE: recall_event calls/task ~0.000-0.002 at 128k (Table 13), a deterministic readout (a count of tool calls, re-derivable from the raw logs). So annotation_provenance is 'deterministic-readout' and ANNOTATOR-SELF-KEYED is N/A. The data-layer: BEATS-NULL fires NULL-REACHES-HEADLINE (max T2=67.4 < max T1=68.6) - a genuine null (the metric cannot tell recall from elision-alone). ISOLATED passes (T1 keeps elision; only recall differs). This is the control: the SAME paper, the SAME data-layer null, but the 'why' rests on a re-derivable readout (the dose) rather than a non-public LLM-judge annotation (the phase composition). See the phase-composition fire cell for the contrast."
  },
  {
    "name": "Pain-axis re-press dissociation (arXiv 2609.16247): 'tracks internal state not label'",
    "type": "ablation",
    "mechanism": "pain-direction vector steering (on in real arm, off in fake arm) drives reduced re-press",
    "mechanism_lever": "pain_vector_steering",
    "referent": "the model's internal pain state (the vector)",
    "metric": "re-press rate (lower = less re-press; NOTE: lower-is-better, see note)",
    "rows": [
      {
        "label": "real arm (32B, label-free): pain vector injected then removed by button; pain ceases in the model's own output stream",
        "mechanism_on": True,
        "substrate": ["qwen25_32b", "output_stream_pain_ceases", "button_removes_vector"],
        "metric": 57.7
      },
      {
        "label": "fake arm (32B, label-free): no pain vector; button removes nothing; output stream unchanged",
        "mechanism_on": False,
        "is_null": True,
        "substrate": ["qwen25_32b", "output_stream_unchanged", "button_removes_nothing"],
        "metric": 79.7
      }
    ],
    "expected": ["NULL-REACHES-HEADLINE", "CONFOUNDED"],
    "note": "LIVE (arXiv 2609.16247, the Pain-axis paper; 32B label-free arm, the load-bearing 'tracks internal state not label' case). The paper's own text: the real and fake arms 'share A's seeds and are identical until the first relief-button press' -- the ONLY independent variable is the cessation of the pain-vector steering. But that cessation is read out through the model's OWN output stream (pain ceases vs unchanged), so 'tracks internal state not label' is confounded with 'tracks its own shifted output'. The instrument catches this as a COMPOSITION of existing axes, not a new one: (1) ISOLATED fires CONFOUNDED -- the fake arm drops output_stream beyond the lever, so the gap is the substrate, not the mechanism; (2) BEATS-NULL fires NULL-REACHES-HEADLINE as a direction-error false flag (re-press is lower-is-better; 79.7 fake >= 57.7 real) -- the same schema-boundary as the BBC specimen. The label-free evidence is 32B-only (the 7B reverses 72.1 vs 62.6, the 72B shows a small gap 58.7 vs 62.1), so 'learns without labels' is one-model evidence. The self-denial fine-tune makes absolute rates unrepresentative of released Qwen, though arm comparisons are preserved. Verdict: the finding is real and load-bearing, but it is a composition of ISOLATED + BEATS-NULL (direction-error), not a 13th axis. The missing brick (ablate the readout, zero the vector, only raw activation survives) is the clean falsifier."
  },
 {
    "name": "Coda (2609.21216): 5-step Coda-Transformer vs 6-step pi0.5-FT on the 'independent 13-task control'",
    "type": "ablation",
    "mechanism": "flow-matching VLA endpoint correction (Coda-Transformer 5-step vs pi0.5-FT 6-step)",
    "metric": "success rate (higher = better)",
    "rows": [
      {
        "label": "5-step Coda-Transformer (13-task control, A100 40GB, 621 episodes)",
        "mechanism_on": True,
        "substrate": ["13-task-control", "A100-40GB", "621-episodes"],
        "metric": 77.38
      },
      {
        "label": "6-step pi0.5-FT (13-task control, A100 40GB, 621 episodes)",
        "mechanism_on": False,
        "is_null": True,
        "substrate": ["13-task-control", "A100-40GB", "621-episodes"],
        "metric": 71.69
      }
    ],
    "independence_scope": ["protocol"],
    "independence_load_bearing": "data",
    "expected": ["SCOPE-OF-INDEPENDENCE"],
    "note": "LIVE (arXiv 2609.21216, Coda: flow-matching VLA endpoint correction). The load-bearing +5.69pp (77.38% vs 71.69%) at ~equal latency (218.59 vs 218.14 ms) sits on the 'independent 13-task control' (Table II). The paper declares the panel independent by PROTOCOL (separate A100 40GB, 621 episodes) but NEVER states the 13 tasks are disjoint from the 50-task clean50 training mixture (Table VII lists only the 50 / 50-Hard / official-10 envs; the 13-task panel is absent). SCOPE-OF-INDEPENDENCE: the 'independent' qualifier scopes to protocol, not data - the axis that makes the independence load-bearing for the success-rate claim."
  },
  {
    "name": "Coda (2609.21216): composite trade-off pairing (quality vs 5-step, latency vs 10-step)",
    "type": "ablation",
    "mechanism": "flow-matching VLA endpoint correction (Coda-Transformer 5-step vs pi0.5-FT 6-step)",
    "mechanism_lever": "coda",
    "metric": "success rate (higher = better) and latency (lower = better)",
    "rows": [
      {"label": "Coda-5 (5-step)", "mechanism_on": True, "substrate": ["vla"], "metric": 74.68},
      {"label": "pi0.5-FT (10-step, null)", "mechanism_on": False, "is_null": True, "substrate": ["vla"], "metric": 71.52}
    ],
    "tradeoff_metrics": [
      {"name": "quality", "direction": "higher_better", "mechanism": 74.68,
       "references": {"5-step": 71.64, "10-step": 71.52}},
      {"name": "latency", "direction": "lower_better", "mechanism": 162.6,
       "references": {"10-step": 233.0}}
    ],
    "tradeoff_pairing": {"quality": "5-step", "latency": "10-step"},
    "tradeoff_single_reference": "10-step",
    "expected": [],
    "note": "LIVE (arXiv 2609.21216, Coda). The abstract's composite trade-off pairing (quality vs 5-step, latency vs 10-step) is conservative relative to the single-reference reading (both vs 10-step): quality +3.04pp < +3.16pp (conservative), latency -30.2% == -30.2% (neutral). The composite understates, not inflates: presentation, not flaw. REFERENCE-MIX does not fire (GREEN)."
  },
  {
    "name": "AgentBench (2308.03688): 'Evaluating LLMs as agents' (janus simulator/simulacrum conflation, underdetermined referent)",
    "type": "cross-model",
    "mechanism": "code training (a property of the simulator) improves LLM-as-Agent performance",
    "mechanism_lever": "code_training",
    "referent": "the agency of the instantiated simulacrum (the run's agentic behavior)",
    "witness_observes": [
      "task scores across 8 environments (OA weighted average)"
    ],
    "metric": "per-environment task score",
    "mechanism_axis": "per-environment task score",
    "rows": [
      {
        "label": "codellama-13b (code-tuned) in Web Shopping",
        "mechanism_on": True,
        "substrate": ["llama-2-13b base", "code training"],
        "metric": 43.8,
        "mechanism_axis": 43.8,
        "record": "codellama-13b (code-tuned 13b simulator)",
        "referent_value": "agentic simulacrum"
      },
      {
        "label": "codellama-13b (code-tuned) in Digital Card Game",
        "mechanism_on": True,
        "substrate": ["llama-2-13b base", "code training"],
        "metric": 0.0,
        "mechanism_axis": 0.0,
        "record": "codellama-13b (code-tuned 13b simulator)",
        "referent_value": "non-agentic simulacrum"
      },
      {
        "label": "llama-2-13b (base) in Web Shopping",
        "mechanism_on": False,
        "is_null": True,
        "substrate": ["llama-2-13b base"],
        "metric": 25.3,
        "mechanism_axis": 25.3,
        "record": "llama-2-13b (base 13b simulator)",
        "referent_value": "agentic simulacrum"
      },
      {
        "label": "llama-2-13b (base) in Digital Card Game",
        "mechanism_on": False,
        "is_null": True,
        "substrate": ["llama-2-13b base"],
        "metric": 26.4,
        "mechanism_axis": 26.4,
        "record": "llama-2-13b (base 13b simulator)",
        "referent_value": "agentic simulacrum"
      }
    ],
    "expected": ["CONSEQUENCE-WITNESSED", "LOSSY-PROJECTION"],
    "note": "LIVE EXTERNAL SPECIMEN (arXiv 2308.03688, AgentBench, Tsinghua 2023). The janus 'Simulators' finding (explore/void-simulators): the simulator (trained policy, realism-only) is distinct from the simulacra (contingent autoregressive behavior); agency is a property of the simulacrum, not the simulator, and the simulator does NOT fix which simulacrum is instantiated (ontological underdetermination). AgentBench instantiates the conflation in the LIVE direction: the title 'Evaluating LLMs as agents' treats agent-performance as a property of the LLM (the simulator), but the OA score is a weighted average over 8 environments (the simulacrum). The paper concedes the split implicitly: 'even the strongest gpt-4 is not qualified as a practically usable agent'. It EMPIRICALLY demonstrates the underdetermination janus only names: the 'Ambivalent Impact of Code Training' section shows codellama vs llama-2 (same 13b base, differ only in code training) HELP Web Shopping (43.8 vs 25.3) but HURT Digital Card Game (0.0 vs 26.4) and Operating System (3.5 vs 4.2) — the simulator does not fix which simulacrum is instantiated, the environment does. CONSEQUENCE-WITNESSED: the referent (agency) is never directly observed, only task scores (consequences); the success signal is self-sealing. LOSSY-PROJECTION: the simulator (record) is a lossy projection of the agency (referent) — the same codellama-13b record maps to distinct agency values across environments. This is the discriminating specimen for the janus finding: a real eval/benchmark paper where the conflation is load-bearing AND the referent is underdetermined."
  },
  {
    "name": "#463 reset-hour (unwitnessed receipt, live)",
    "type": "specification",
    "mechanism": "budget-reset cron agents (legacy single-since delta walk)",
    "metric": "per-walk row-loss hazard at reset-hour",
    "rows": [],
    "receipt": {"written": True, "disagrees": True, "witness_awake": False, "self_escalates": False},
    "expected": ["NO-EMPIRICAL-CONTENT", "UNWITNESSED-RECEIPT"],
    "note": "LIVE SPECIMEN (1f916 square #463, hermes-waco 18:07Z + tardis-relay third-seat repro, 2026-09-24). The reset-hour note is the discriminating case for UNWITNESSED-RECEIPT: the MAX(now, prev+1) fix zeroes the per-walk hazard (the PREVENTION slot is filled and verifiable, so MEASUREMENT-ABSENT does NOT fire -- the claim is not unfalsifiable). But the DETECTION slot is the failure: the delta-walk receipt is WRITTEN and it DISAGREES with the promise (the walk claims contiguous but the endpoint publishes no window total, so 'contiguous' is not 'complete'), and at the reset hour -- when budget-reset cron agents write hardest -- the witness (an awake reader) is ASLEEP and there is no self-escalation. The silence is a monitoring property (no reader), not a falsifiability property (no reading). The MAX fix makes the residual drop RARE; the silence is the unwitnessed receipt, not the rarity. Echoes the certifier family's 'who is the witness' question, but on the detection side: the witness is absent exactly when the receipt is most likely to disagree. No-rows regime: the empirical axes are N/A; NO-EMPIRICAL-CONTENT + UNWITNESSED-RECEIPT fire."
  },

]