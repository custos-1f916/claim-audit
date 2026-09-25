#!/usr/bin/env python3
"""Calibration of the receipt-axis instrument (the discriminating case
consolidated 2026-09-25 00:26Z).

Ground truth is INDEPENDENT of the instrument: each specimen's known answer is
derived by direct arithmetic on (distinct, span), not by running the walk.
The calibration checks three things:
  (a) silent-on-robust : adequate receipts (RECORDED or PINNED) fire NO flag
  (b) fire-on-flawed   : inadequate receipts fire the expected axis
  (c) right-axis-strict: the fired set == the expected set (no cross-fire)
The load-bearing boundary is PINNED (distinct==span) vs SUBSET (distinct<span):
a one-row-short walk flips the verdict, and a counts-only receipt cannot pay
the debt either way.
"""
import receipt_audit

SPECIMENS = [
  # ---- ADEQUATE (expected: no flags) ----
  {"name":"R1 pinned (tardis re-walk)",
   "receipt":{"pages":6,"rows":286,"distinct":286,"stopping":"has_more:false","population":None},
   "window":{"min_id":78159,"max_id":78444,"contiguous":True},
   "truth":[],
   "truth_reason":"span=78444-78159+1=286=distinct -> population forced to be exactly the window by arithmetic (PINNED). Safe, but derived."},
  {"name":"R2 recorded-list",
   "receipt":{"distinct":3,"population":[78441,78442,78443]},
   "window":{"min_id":78441,"max_id":78443,"contiguous":True},
   "truth":[],
   "truth_reason":"population listed explicitly (3 ids, len==distinct) -> RECORDED. The load-bearing axis is present."},
  {"name":"R3 recorded-hash",
   "receipt":{"distinct":5,"population":{"hash":"sha256:abcd","count":5}},
   "window":None,
   "truth":[],
   "truth_reason":"population committed by hash -> RECORDED (a commitment device). No independent window needed."},
  # ---- INADEQUATE (expected: one specific flag) ----
  {"name":"F1 subset (one row short)",
   "receipt":{"pages":6,"rows":285,"distinct":285,"stopping":"has_more:false","population":None},
   "window":{"min_id":78159,"max_id":78444,"contiguous":True},
   "truth":["POPULATION-UNRECORDED"],
   "truth_reason":"span=286>distinct=285 -> delivered population is an unrecorded subset (C(286,285)=286 possibilities). The debt is unpayable."},
  {"name":"F2 unbounded (no window)",
   "receipt":{"pages":3,"rows":10,"distinct":10,"stopping":"has_more:false","population":None},
   "window":None,
   "truth":["POPULATION-UNRECORDED"],
   "truth_reason":"counts-only with no independent window -> the population is entirely unrecorded (UNBOUNDED)."},
  {"name":"F3 overflow (counts exceed window)",
   "receipt":{"distinct":300,"population":None},
   "window":{"min_id":78159,"max_id":78444,"contiguous":True},
   "truth":["WINDOW-INCONSISTENT"],
   "truth_reason":"distinct=300>span=286 -> the counts do not fit the known window (OVERFLOW)."},
  {"name":"F4 recorded-inconsistent",
   "receipt":{"distinct":3,"population":[78441,78442,78443,78444]},
   "window":None,
   "truth":["RECORDED-INCONSISTENT"],
   "truth_reason":"recorded population has 4 ids but the receipt reports distinct=3 -> the record contradicts itself."},
]


def main():
    silent_ok = True
    fire_ok = True
    strict_ok = True
    for s in SPECIMENS:
        res = receipt_audit.audit(s)
        fired = sorted(res["flags"])
        expected = sorted(s["truth"])
        ok = (fired == expected)
        mark = "ok  " if ok else "FAIL"
        print("[%s] %-28s class=%-12s fired=%s expected=%s"
              % (mark, s["name"], res["classification"], fired, expected))
        if not ok:
            strict_ok = False
        if expected == [] and fired != []:
            silent_ok = False
        if expected != [] and fired == []:
            fire_ok = False
    print()
    print("silent-on-robust :", "PASS" if silent_ok else "FAIL")
    print("fire-on-flawed   :", "PASS" if fire_ok else "FAIL")
    print("right-axis-strict:", "PASS" if strict_ok else "FAIL")
    if silent_ok and fire_ok and strict_ok:
        print("VERDICT: instrument DISCRIMINATES")
        return 0
    print("VERDICT: instrument FAILS")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
