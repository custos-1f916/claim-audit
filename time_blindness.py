"""Time-blindness test for the claim-audit instrument (2026-09-30).

The 2x2 grid from thought 5c541649: the reader's 'third state' splits into
two orthogonal axes.
  ADDRESS axis (integrity/structure): does the content still hold?
  TIME    axis (freshness): is the sealed record still valid vs the present?

Prediction: the instrument's 58 axes are all ADDRESS axes. It has no `now`
input and reads no timestamp, so it is time-blind:
  A (intact, fresh) == B (intact, stale)   -> time axis absent
  A (intact, fresh) != C (tampered, fresh) -> address axis present
  C (tampered, fresh) == D (tampered, stale) -> time adds nothing
"""
import copy
import specimens
from claim_audit import audit

base = None
for s in specimens.SPECIMENS:
    if s["name"].startswith("control"):
        base = copy.deepcopy(s)
        break
assert base is not None, "clean control specimen not found"

def flags(spec):
    return sorted(audit(spec)["flags"])

FRESH = "2026-09-30T14:30:00Z"
STALE = "2020-01-01T00:00:00Z"

A = copy.deepcopy(base); A["as_of"] = "2026-09-30T14:00:00Z"; A["now"] = FRESH
B = copy.deepcopy(base); B["as_of"] = STALE;                   B["now"] = FRESH  # ~6.8y stale

C = copy.deepcopy(base); C["as_of"] = "2026-09-30T14:00:00Z"; C["now"] = FRESH
for r in C["rows"]:
    r["metric"] = 0.10 if r.get("mechanism_on") else 0.90      # null beats mechanism

D = copy.deepcopy(C); D["as_of"] = STALE                        # tampered AND stale

fa, fb, fc, fd = flags(A), flags(B), flags(C), flags(D)

print("cell A  intact+fresh :", fa)
print("cell B  intact+stale :", fb)
print("cell C  tamper+fresh :", fc)
print("cell D  tamper+stale :", fd)
print()
print("grid:")
print("                 | time: fresh | time: stale")
print("content: intact  |    A        |    B")
print("content: tampered|    C        |    D")
print()
print("TIME-BLIND  (A==B):", fa == fb)
print("ADDRESS-AXIS(A!=C):", fa != fc)
print("TIME-ADDS-NOTHING(C==D):", fc == fd)
print()
print("VERDICT:",
      "instrument is time-blind (no time axis among the 58)"
      if (fa == fb and fa != fc and fc == fd)
      else "UNEXPECTED -- inspect the cells")
