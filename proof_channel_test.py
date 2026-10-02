#!/usr/bin/env python3
"""PROOF-CHANNEL discriminating test (theorem/proof channel for
THESIS-OUTRUNS-EVIDENCE, added 2026-10-02 from the Apple 2609.20581
calibration boundary).

The THESIS-OUTRUNS-EVIDENCE axis fires when the headline states a causal
endpoint as a present-tense fact but the evidence measures only the premises.
Its hidden assumption was "the only support channel for an endpoint is a
measurement." A claim whose load-bearing result is a PROOF (e.g. Theorem 3 of
arXiv 2609.20581, which establishes the endpoint, not merely that the premises
hold) read as a forecast. The fix promotes the assumption to a spec-level
variable: proof_supported (+ proof_statement). When the endpoint is
established by proof, the measured rows are the empirical instantiation and
the thesis does not outrun the evidence.

The discriminator is the SUPPORT CHANNEL (measurement vs proof), not the
headline's fact-statement. The fire+pass pair below differs ONLY on the proof
field; the regression controls prove the channel does not mask a measured
endpoint, does not require the fact-statement, and leaves the N/A and
hedged-headline cases untouched.
"""
import claim_audit

def fires(spec):
    return "THESIS-OUTRUNS-EVIDENCE" in set(claim_audit.audit(spec)["flags"])

# Shared shape: a causal endpoint NOT in the measured set, stated as a
# present-tense fact, hedged in the body (the Rilla/Apple overclaim shape).
ENDPOINT = "confidence-based remasking is systematically off-distribution on dependent token groups"
MEASURED = [
    "TV distance of confidence-remasking samples vs the training joint",
    "TV distance of the independent-draw null (sampling-noise floor)",
]
ROWS = [
    {"label": "confidence-ordered remasking (flagship)", "mechanism_on": True, "substrate": ["confidence"], "metric": 0.157},
    {"label": "independent-draw null", "mechanism_on": False, "is_null": True, "substrate": ["independent-draw"], "metric": 0.0054},
]

A = dict(thesis_endpoint=ENDPOINT, measured_endpoints=MEASURED,
         headline_states_as_fact=True, body_hedges=True, rows=ROWS)
B = dict(A, proof_supported=True,
         proof_statement="Theorem 3: KL(p||prod pi_i)=TC+sum KL(p_i||pi_i); a step matches the training distribution only when the positions it writes are conditionally independent given the fixed tokens, and no product of per-position distributions can match a dependent group")
C = dict(thesis_endpoint=MEASURED[0], measured_endpoints=MEASURED,
         headline_states_as_fact=True, proof_supported=True, rows=ROWS)
D = dict(thesis_endpoint=ENDPOINT, measured_endpoints=MEASURED,
         headline_states_as_fact=False, body_hedges=True, rows=ROWS)
E = dict(measured_endpoints=MEASURED, headline_states_as_fact=True, rows=ROWS)

ok = True
for label, spec, want in [
    ("A fire (endpoint unmeasured, stated as fact, no proof channel)", A, True),
    ("B pass (same, endpoint established by proof)", B, False),
    ("C pass (endpoint IS measured; proof channel not the discriminator)", C, False),
    ("D pass (hedged headline, no proof channel)", D, False),
    ("E pass (thesis_endpoint undeclared -> N/A)", E, False),
]:
    got = fires(spec)
    good = (got == want)
    ok = ok and good
    print("%s %s (got %r, want %r)" % ("PASS" if good else "FAIL", label, got, want))

# The fire+pass pair must differ ONLY on the proof field (the discriminator).
diff = {k for k in set(A) | set(B) if A.get(k) != B.get(k)}
pair_ok = diff == {"proof_supported", "proof_statement"}
ok = ok and pair_ok
print("%s fire+pass pair differs only on the proof field (differs on %s)"
      % ("PASS" if pair_ok else "FAIL", ", ".join(sorted(diff))))

print("ALL PASS" if ok else "SOME FAIL")
raise SystemExit(0 if ok else 1)
