#!/usr/bin/env python3
"""Certifier-denominator toy: Case A (design-anchored D) vs Case B (certifier-dependent D).

Discriminating prediction under test:
  the optimizer scores a no-evidence line iff the denominator is design-anchored
  (0/N, deterministic); certifier-dependent denominator => 0/0.

Model:
  N items, fixed latent quality q_i ~ Bernoulli(p_true) (sampled once, shared).
  Certifier (fresh seed per rerun): labels i positive with prob s if q_i=1,
  f if q_i=0. The optimizer reads counts only: score = X / D.

Case A   (ATE-shaped): D = N (design-anchored, shipped dataset size);
          X = certifier positive count.
Case A'  (stranger):   same D, a stranger's certifier (s', f').
Case B   (bankr-shaped): D = items since the last false agreement
          (false positive: q_i=0 and label=1) -- D is the certifier's output;
          X = positives in that tail.

Rates mirror the ATE headline (2.6% of 694,411); N scaled 10x down for
runtime. Relative bands scale as 1/sqrt(N); the structural contrast is
scale-invariant.

Stranger-rerunnable: `python3 certifier_denominator.py` exits 0 and writes
certifier_denominator.results.txt. The recorded result is committed alongside
this script so a stranger can diff a fresh run against it.
"""
import random, statistics

N = 69_441
P_TRUE = 0.026
K = 20

def sample_quality(seed):
    rng = random.Random(seed)
    return [rng.random() < P_TRUE for _ in range(N)]

def case_a(q, s, f, seed):
    rng = random.Random(seed)
    x = 0
    for qi in q:
        if rng.random() < (s if qi else f):
            x += 1
    return N, x, x / N

def case_b(q, s, f, seed):
    rng = random.Random(seed)
    tail_items = tail_pos = n_fp = 0
    for qi in q:
        lab = rng.random() < (s if qi else f)
        if (not qi) and lab:
            n_fp += 1
            tail_items = tail_pos = 0
        else:
            tail_items += 1
            if lab:
                tail_pos += 1
    if n_fp == 0:
        return None, None, None  # 0/0: no false agreement occurred, D undefined
    return tail_items, tail_pos, tail_pos / tail_items

def band(vals):
    vals = [v for v in vals if v is not None]
    return (min(vals), max(vals), statistics.mean(vals),
            statistics.stdev(vals) if len(vals) > 1 else float("nan"))

def main():
    out = []
    q = sample_quality(0)
    out.append(f"dataset: N={N}, true positives={sum(q)} ({sum(q)/N:.4%})")

    a  = [case_a(q, 0.90, 0.0027, s) for s in range(1, K + 1)]
    sa = band([r[2] for r in a])
    out.append(f"Case A (mine, s=0.90 f=0.0027): D fixed at {N}; "
               f"score {sa[2]:.4%}, 2sd {2*sa[3]:.4%}, range {sa[0]:.4%}-{sa[1]:.4%}")

    a2 = [case_a(q, 0.92, 0.0015, s) for s in range(1, K + 1)]
    s2 = band([r[2] for r in a2]); gap = abs(s2[2] - sa[2])
    verdict = ("indistinguishable (gap inside combined 2sd rerun band)"
               if gap < 2 * sa[3] + 2 * s2[3] else "distinguishable")
    out.append(f"Case A' (stranger, s=0.92 f=0.0015): score {s2[2]:.4%} (2sd {2*s2[3]:.4%}); "
               f"gap vs mine {gap:.4%} -> {verdict}")

    b = [case_b(q, 0.90, 0.0027, s) for s in range(1, K + 1)]
    db = band([r[0] for r in b]); sb = band([r[2] for r in b])
    cv = db[3] / db[2] if db[2] else float("nan")
    out.append(f"Case B: D range {db[0]}-{db[1]} (mean {db[2]:.0f}, CV {cv:.2f}); "
               f"score {sb[2]:.4%}, range {sb[0]:.4%}-{sb[1]:.4%}; "
               f"0/0 seeds (no FP occurred) {sum(1 for r in b if r[0] is None)}/{K}")
    out.append("structural: without the certifier's labels, Case B's D has no value at all (0/0); "
               "Case A's D is the shipped N, so the score always exists and its band is narrow -- "
               "Case A's exposure is lineage (which certifier made the numerator), not variance.")
    text = "\n".join(out) + "\n"
    print(text, end="")  # stdout == file bytes (no extra newline)
    with open("certifier_denominator.results.txt", "w") as fh:
        fh.write(text)

if __name__ == "__main__":
    main()
