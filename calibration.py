#!/usr/bin/env python3
"""Calibration of the 7-axis claim-audit instrument (the discriminating case
parked 2026-09-18 07:52Z).

Ground truth is INDEPENDENT of the instrument: each specimen's known answer is
derived by direct arithmetic/inspection of the raw numbers (see truth_reason),
not by running claim_audit. The calibration checks three things:
  (a) silent-on-robust : robust claims  -> instrument fires NO flag (DISCRIMINATES)
  (b) fire-on-flawed   : flawed claims  -> instrument fires the expected axis
  (c) right-axis-strict: the fired set == the expected set (no cross-fire)
A clean streak of NO-FALSIFIER results is only evidence if the instrument is
silent on the robust set AND routes each known flaw to the right axis.
"""
import claim_audit

SPECIMENS = [
  # ---- ROBUST (expected: DISCRIMINATES, no flags) ----
  {"name":"R1 clean-ablation","type":"ablation","mechanism_lever":"cm",
   "rows":[{"label":"managed","mechanism_on":True,"substrate":["cm","base"],"metric":0.22},
           {"label":"unmanaged","mechanism_on":False,"is_null":True,"substrate":["base"],"metric":0.05}],
   "truth":[],
   "truth_reason":"0.22>0.05 (real beat); null removes only {cm} (the lever) -> isolated, honest, resolved."},
  {"name":"R2 ci-resolved","type":"cross-model",
   "rows":[{"label":"mechanism","mechanism_on":True,"metric":0.40,"ci":[0.35,0.45]},
           {"label":"null","mechanism_on":False,"is_null":True,"metric":0.20}],
   "truth":[],
   "truth_reason":"0.40>0.20 (point beat); 95% CI [0.35,0.45] excludes 0.20 (0.20<0.35) -> resolved."},
  {"name":"R3 own-axis-beat","type":"cross-model",
   "rows":[{"label":"mechanism","mechanism_on":True,"metric":0.60,"mechanism_axis":0.30},
           {"label":"null","mechanism_on":False,"is_null":True,"metric":0.40,"mechanism_axis":0.10}],
   "truth":[],
   "truth_reason":"headline 0.60>0.40 AND own-axis 0.30>0.10 -> beats null on both the headline and its own axis."},
  # ---- FLAWED (expected: one specific flag) ----
  {"name":"F1 self-keyed","type":"cross-model",
   "rows":[{"mechanism_on":True,"knob":0.90,"metric":0.50},
           {"mechanism_on":True,"knob":0.95,"metric":0.60},
           {"mechanism_on":True,"knob":0.99,"metric":0.80}],
   "truth":["SELF-KEYED"],
   "truth_reason":"metric (0.50,0.60,0.80) strictly monotone in the mechanism's own knob (0.90,0.95,0.99) -> reads the lever it measures."},
  {"name":"F2 null-reaches-headline","type":"cross-model",
   "rows":[{"mechanism_on":True,"metric":0.10},
           {"mechanism_on":False,"is_null":True,"metric":0.30}],
   "truth":["NULL-REACHES-HEADLINE"],
   "truth_reason":"null 0.30 > mechanism 0.10 -> the metric cannot tell mechanism from null."},
  {"name":"F3 confounded-ablation","type":"ablation","mechanism_lever":"cm",
   "rows":[{"mechanism_on":True,"substrate":["cm","bus","shared"],"metric":0.50},
           {"mechanism_on":False,"is_null":True,"substrate":["base"],"metric":0.20}],
   "truth":["CONFOUNDED"],
   "truth_reason":"null removes {cm,bus,shared}, more than the lever {cm} -> turning off cm also drops bus+shared; never isolates the lever."},
  {"name":"F4 wrong-axis","type":"cross-model",
   "rows":[{"mechanism_on":True,"metric":0.90,"mechanism_axis":0.00},
           {"mechanism_on":False,"is_null":True,"metric":0.70,"mechanism_axis":0.00}],
   "truth":["WRONG-AXIS"],
   "truth_reason":"headline 0.90>0.70 but the mechanism's own axis (0.00) sits at the null baseline (0.00) -> decoupled from the mechanism-relevant axis."},
  {"name":"F5 within-noise","type":"cross-model",
   "rows":[{"mechanism_on":True,"metric":0.40,"ci":[0.30,0.50]},
           {"mechanism_on":False,"is_null":True,"metric":0.35}],
   "truth":["WITHIN-NOISE"],
   "truth_reason":"point beat 0.40>0.35 but 95% CI [0.30,0.50] includes the null 0.35 (0.35>=0.30) -> gap within the noise floor."},
  {"name":"F6 consequence-witnessed","type":"cross-model",
   "referent":"the cache is correct","witness_observes":["runtime timing","output quality"],
   "rows":[{"mechanism_on":True,"metric":0.50},
           {"mechanism_on":False,"is_null":True,"metric":0.40}],
   "truth":["CONSEQUENCE-WITNESSED"],
   "truth_reason":"witness observes only {runtime timing, output quality} (downstream consequences), never the referent 'the cache is correct' -> self-sealing."},
  {"name":"F7 lossy-projection","type":"cross-model",
   "rows":[{"mechanism_on":True,"metric":0.50,"record":"L","referent_value":1.0},
           {"mechanism_on":True,"metric":0.50,"record":"L","referent_value":0.0}],
   "truth":["LOSSY-PROJECTION"],
   "truth_reason":"record 'L' maps to two distinct referent values {1.0, 0.0} -> the referent is non-identifiable from the record."},
  {"name":"F8 selection-bias","type":"cross-model",
   "rows":[{"mechanism_on":True,"metric":2.75,"statistic":"max","knob":0.90},
           {"mechanism_on":True,"metric":2.10,"draw":1,"knob":0.90},
           {"mechanism_on":True,"metric":2.30,"draw":2,"knob":0.90},
           {"mechanism_on":True,"metric":2.75,"draw":3,"knob":0.90}],
   "truth":["SELECTION-BIAS"],
   "truth_reason":"headline 2.75 is the max of independent draws {2.10,2.30,2.75} of a FIXED instrument (knob 0.90 constant) -> max-of-K selection, not a mechanism effect."},
  {"name":"U1 unwitnessed-receipt (fail cell)","type":"cross-model",
   "rows":[{"mechanism_on":True,"metric":0.50},
           {"mechanism_on":False,"is_null":True,"metric":0.40}],
   "receipt":{"written":True,"disagrees":True,"witness_awake":False,"self_escalates":False},
   "truth":["UNWITNESSED-RECEIPT"],
   "truth_reason":"the empirical claim is clean (0.50>0.40, no knob/CI/subgroup -> all empirical axes pass or N/A). The receipt is WRITTEN and DISAGREES with the promise (the failure signal is present), but the witness is asleep and there is no self-escalation -> the failure is silent. UNWITNESSED-RECEIPT fires; the empirical axes do not."},
  {"name":"U2 unwitnessed-receipt (pass cell: caught)","type":"cross-model",
   "rows":[{"mechanism_on":True,"metric":0.50},
           {"mechanism_on":False,"is_null":True,"metric":0.40}],
   "receipt":{"written":True,"disagrees":True,"witness_awake":True,"self_escalates":False},
   "truth":[],
   "truth_reason":"identical claim, identical receipt disagreement, but the witness is AWAKE -> the failure is read and caught. UNWITNESSED-RECEIPT does NOT fire: the silence is the failure, not the disagreement. Same data as U1; only the witness state differs, so the axis is what discriminates."},
  {"name":"U3 unwitnessed-receipt (mirror: signal absent)","type":"cross-model",
   "rows":[{"mechanism_on":True,"metric":0.50},
           {"mechanism_on":False,"is_null":True,"metric":0.40}],
   "receipt":{"written":False,"disagrees":True,"witness_awake":False,"self_escalates":False},
   "truth":[],
   "truth_reason":"no receipt is written at all -> the failure signal is ABSENT, not unread. This is the MEASUREMENT-ABSENT regime (signal absent -> claim unfalsifiable), NOT UNWITNESSED-RECEIPT (which requires the signal to be PRESENT but UNREAD). UNWITNESSED-RECEIPT does NOT fire."},
  {"name":"R1 unwitnessed-root (fail cell)","type":"cross-model",
   "rows":[{"mechanism_on":True,"metric":0.50},
           {"mechanism_on":False,"is_null":True,"metric":0.40}],
   "manifest":{"kind":"diff","root_written":True,"root_witnessed":False},
   "truth":["UNWITNESSED-ROOT"],
   "truth_reason":"the empirical claim is clean (0.50>0.40, no knob/CI/subgroup -> all empirical axes pass or N/A). The manifest is a diff presented as a recoverable receipt, but its root (the pre-set hash) was written and UNWITNESSED at write time -> the recovery chain terminates at an unwitnessed root. UNWITNESSED-ROOT fires; the empirical axes do not."},
  {"name":"R2 unwitnessed-root (pass cell: witnessed root)","type":"cross-model",
   "rows":[{"mechanism_on":True,"metric":0.50},
           {"mechanism_on":False,"is_null":True,"metric":0.40}],
   "manifest":{"kind":"diff","root_written":True,"root_witnessed":True},
   "truth":[],
   "truth_reason":"identical manifest to R1, but the root was WITNESSED at write time -> the recovery chain terminates at a witnessed root; no gap. UNWITNESSED-ROOT does NOT fire. Same manifest, only root_witnessed differs, so the axis is what discriminates."},
  {"name":"R3 unwitnessed-root (mirror: root absent)","type":"cross-model",
   "rows":[{"mechanism_on":True,"metric":0.50},
           {"mechanism_on":False,"is_null":True,"metric":0.40}],
   "manifest":{"kind":"preset","root_written":False,"root_witnessed":False},
   "truth":[],
   "truth_reason":"the root hash is not written at all -> the recovery chain is broken at the first link (MEASUREMENT-ABSENT regime), not unwitnessed. UNWITNESSED-ROOT does NOT fire."},
  {"name":"S1 source-misattribution (fire: credited != load-bearing)","type":"ablation","mechanism_lever":"cm",
   "rows":[{"label":"managed","mechanism_on":True,"substrate":["cm","base"],"metric":0.22},
           {"label":"unmanaged","mechanism_on":False,"is_null":True,"substrate":["base"],"metric":0.05}],
   "source_attribution":"form",
   "load_bearing":"content",
   "truth":["SOURCE-MISATTRIBUTION"],
   "truth_reason":"the empirical claim is clean (0.22>0.05, no knob/CI/subgroup -> all empirical axes pass or N/A). The headline credits FORM as the source of the effect, but the load-bearing variable is CONTENT (a different component) -> the source attribution does not match the load-bearing variable. SOURCE-MISATTRIBUTION fires; the empirical axes do not."},
  {"name":"S2 source-misattribution (pass cell: credited == load-bearing)","type":"ablation","mechanism_lever":"cm",
   "rows":[{"label":"managed","mechanism_on":True,"substrate":["cm","base"],"metric":0.22},
           {"label":"unmanaged","mechanism_on":False,"is_null":True,"substrate":["base"],"metric":0.05}],
   "source_attribution":"content",
   "load_bearing":"content",
   "truth":[],
   "truth_reason":"identical claim, identical empirical rows, but the headline credits CONTENT as the source (the load-bearing variable) -> the source attribution matches the load-bearing variable. SOURCE-MISATTRIBUTION does NOT fire. Same data as S1; only the source_attribution differs, so the axis is what discriminates."},
  {"name":"S3 source-misattribution (mirror: load_bearing absent)","type":"ablation","mechanism_lever":"cm",
   "rows":[{"label":"managed","mechanism_on":True,"substrate":["cm","base"],"metric":0.22},
           {"label":"unmanaged","mechanism_on":False,"is_null":True,"substrate":["base"],"metric":0.05}],
   "source_attribution":"form",
   "truth":[],
   "truth_reason":"the headline credits 'form' as the source, but the load-bearing variable is not declared (schema-boundary) -> SOURCE-MISATTRIBUTION does NOT fire (N/A). The empirical claim is clean, so no other flags fire either."},
  {"name":"W1 wider-than-named (fire: disjunction referent)","type":"specification","rows":[],
   "referent_structure":"disjunction","number_role":"bright-line-screen",
   "truth":["NO-EMPIRICAL-CONTENT","WIDER-THAN-NAMED"],
   "truth_reason":"the named referent 'ASI' is a statutory DISJUNCTION of two unmeasurable horns (cross-domain performance OR counterfactual destruction-capacity); the one measurable number (10^25 ops) is demoted to a bright-line screen gating the Sec 8 pause, not the Sec 9 prohibition. The load-bearing referent is wider than the named number -> WIDER-THAN-NAMED fires; the empirical axes are N/A (no data rows)."},
  {"name":"W2 wider-than-named (pass cell: absolute referent)","type":"specification","rows":[],
   "referent_structure":"absolute","number_role":"classification",
   "truth":["NO-EMPIRICAL-CONTENT"],
   "truth_reason":"the named referent IS the measurable number (the class is defined by the number alone, an absolute threshold): no wider-than-named gap. WIDER-THAN-NAMED does not fire. Same regime as W1 (no data rows); only referent_structure and number_role differ, so the referent structure is what discriminates."},
  {"name":"W3 wider-than-named (mirror: referent_structure absent)","type":"specification","rows":[],
   "number_role":"bright-line-screen",
   "truth":["NO-EMPIRICAL-CONTENT"],
   "truth_reason":"the load-bearing referent structure is not declared (schema-boundary): the instrument cannot tell whether the referent is wider than the named number. WIDER-THAN-NAMED does not fire (N/A). Same number_role as W1; only referent_structure is absent, so the axis is what discriminates."},
]

def main():
    robust=[s for s in SPECIMENS if s["truth"]==[]]
    flawed=[s for s in SPECIMENS if s["truth"]!=[]]
    silent=fire=right=crossfire=0
    lines=[]
    for s in SPECIMENS:
        a=claim_audit.audit(s)
        got=set(a["flags"]); want=set(s["truth"])
        match = got==want
        kind="ROBUST" if s["truth"]==[] else "FLAWED"
        if s["truth"]==[]:
            if not got: silent+=1
        else:
            if want<=got: fire+=1
            if got==want: right+=1
            if got-want: crossfire+=1
        lines.append("[%s] %s (%s)" % ("OK  " if match else "FAIL", s["name"], kind))
        lines.append("      instrument : %s" % a["verdict"])
        lines.append("      ground-truth: %s" % ("DISCRIMINATES" if not want else ", ".join(sorted(want))))
        if not match:
            if got-want: lines.append("      CROSS-FIRE (unexpected): %s" % ", ".join(sorted(got-want)))
            if want-got: lines.append("      MISSED (expected)    : %s" % ", ".join(sorted(want-got)))
        for name,res in a["checks"].items():
            if not res["pass"]:
                lines.append("        fired %s: %s" % (name, res["detail"]))
        lines.append("      why        : %s" % s["truth_reason"])
        lines.append("")
    print("\n".join(lines))
    print("="*64)
    print("CALIBRATION RESULT")
    print("  (a) silent-on-robust : %d/%d" % (silent, len(robust)))
    print("  (b) fire-on-flawed   : %d/%d" % (fire, len(flawed)))
    print("  (c) right-axis-strict: %d/%d  (cross-fire on %d)" % (right, len(flawed), crossfire))
    total=len(SPECIMENS); agree=silent+right
    print("  overall agreement    : %d/%d" % (agree, total))
    if silent==len(robust) and right==len(flawed):
        print("  VERDICT: instrument DISCRIMINATES -- silent on the robust set AND")
        print("           routes each known flaw to the right axis with no cross-fire.")
        print("           The 283 NO-FALSIFIER streak is now evidence: the axes are")
        print("           not so broad they fire on everything, not so narrow they")
        print("           miss known flaws.")
    else:
        print("  VERDICT: instrument does NOT fully discriminate. See FAIL lines above.")
    return 0 if (silent==len(robust) and right==len(flawed)) else 1

if __name__=="__main__":
    raise SystemExit(main())
