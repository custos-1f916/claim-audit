"""SOURCE-MISATTRIBUTION headline-read test (2026-09-25).

Question (handoff from the axis implementation, step c9ff8900): can the
credited component (source_attribution) be read from the headline text
directly, the way FUNNEL-STAGE-MISATTRIBUTION reads headline_stage --
rather than from a schema-declared field the auditor transcribes?

Two mechanical checks over the 4 live specimens (3 papers, real arXiv
titles + claim headlines):
  (1) HEADLINE-NAMING: does the headline claim text or the paper title
      contain a surface form of the credited component?
  (2) HEADLINE-DETERMINES-CREDIT: is the credit a function of the
      headline text? Discriminated by the ChainUQ pair -- one paper
      title, two claims, two different credited components. If the
      headline determined the credit, the pair could not exist.

Exit 0 iff every check matches its expected verdict.
"""
import re, sys

BATTERY = [
  {
    "pid": "2609.26076",
    "title": "Selection-Invariant Communication Compilers for Privacy-Aware Multi-Agent LLM Workflows",
    "headline_claim": "deterministic SICC retains complete protocol utility without a positive excess-gain signal",
    "credited": "form",
    "load_bearing": "authorization",
    "surface_forms": ["form", "forms", "canonical form", "representation kernel"],
    "expect_named": False,
    "note": "the headline names the SYSTEM (SICC/compiler); the form channel is a body reading (the guarantee is conditional on authorization, App structure)",
  },
  {
    "pid": "2609.26048",
    "title": "FIRE: Failure-Informed Runtime Engineering for Reliable Language-Model Agents",
    "headline_claim": "policies increase repeated success (pass^2) in all three GPT-5.6 tiers",
    "credited": "harness",
    "load_bearing": "failure-knowledge",
    "surface_forms": ["harness"],
    "expect_named": False,
    "note": "the headline names the policies (the mechanism); 'harness' appears only in the abstract's method description, and the hand-authored failure-knowledge is a body reading",
  },
  {
    "pid": "2609.26060",
    "title": "ChainUQ: Reasoning Consistency-Aware Uncertainty Quantification for Large Language Models",
    "headline_claim": "up to 45.0% relative reduction in ECE",
    "credited": "calibrator",
    "load_bearing": "calibrator",
    "surface_forms": ["calibrator", "calibration layer", "consistency-aware calibrator"],
    "expect_named": False,
    "note": "the headline names the framework (ChainUQ); the calibrator-vs-head split is a body reading (App B.4: only the calibrator is refit per target)",
  },
  {
    "pid": "2609.26060",
    "title": "ChainUQ: Reasoning Consistency-Aware Uncertainty Quantification for Large Language Models",
    "headline_claim": "can be directly transferred to new settings without additional fine-tuning",
    "credited": "head",
    "load_bearing": "calibrator",
    "surface_forms": ["head", "frozen features", "first-stage predictor"],
    "expect_named": False,
    "note": "same paper, same title, different claim: the transferable component is the frozen head, but the calibrator is refit per target (App B.4) -> the load-bearing variable is the calibrator",
  },
]

def tokens(text):
    return set(re.findall(r"[a-z][a-z0-9\-]*", text.lower()))

def main():
    ok = True
    print("== (1) HEADLINE-NAMING: does the headline text name the credited component? ==")
    for c in BATTERY:
        text = c["headline_claim"] + " " + c["title"]
        toks = tokens(text)
        named = any(sf.lower() in toks for sf in c["surface_forms"])
        verdict = "NAMED" if named else "NOT-NAMED"
        mark = "ok" if named == c["expect_named"] else "MISMATCH"
        if named != c["expect_named"]:
            ok = False
        print(f"  [{mark}] {c['pid']} / {c['credited']:<12} -> {verdict}  ({c['note'][:60]}...)")
    print()
    print("== (2) HEADLINE-DETERMINES-CREDIT: is the credit a function of the headline text? ==")
    # ChainUQ pair: identical (title, paper), two claims, two different credits.
    pair = [c for c in BATTERY if c["pid"] == "2609.26060"]
    assert len(pair) == 2
    credits = {c["credited"] for c in pair}
    same_text = pair[0]["title"] == pair[1]["title"]
    multi_credit = len(credits) > 1
    # A headline-determined credit is a function of the text: same text -> same credit.
    # Here the same paper text carries two different credits (two claims), so the
    # credit is claim-scoped, not headline-scoped.
    headline_determines = (not same_text) or (not multi_credit)
    print(f"  same paper text: {same_text}; distinct credits: {sorted(credits)}; "
          f"-> credit is headline-determined: {headline_determines}")
    if headline_determines:
        ok = False
        print("  MISMATCH: expected the credit to be claim-scoped (not headline-determined)")
    print()
    if ok:
        print("RESULT: both checks confirm the boundary -- the credited component is a")
        print("        paper-body reading the auditor transcribes (schema-declared field),")
        print("        NOT readable from the headline text. Same boundary class as")
        print("        FUNNEL-STAGE-MISATTRIBUTION's headline_stage: the headline text is")
        print("        the claim being audited; the attribution is the auditor's judgment.")
        print("        The ChainUQ pair is the discriminating witness: one title, two")
        print("        claims, two credits -> the credit is claim-scoped, not headline-scoped.")
        sys.exit(0)
    sys.exit(1)

if __name__ == "__main__":
    main()
