"""Two-reader demo: the seal is bi-state; the reader promotes it to tri-state.

Thought 7bd9ff27 (2026-09-30), following time_blindness.py (0a67e5d):
the instrument is clock-absent (no `now` input; intact+fresh == intact+stale).
This demo runs the discriminating test for the seal itself: the SAME sealed
record, read by two readers whose clocks differ.

The record seals check + as_of + tolerance. as_of is a fixed value sealed at
commit; the instrument never reads `now`. So:

  - the instrument's flags are identical for both readers: it is bi-state
    (it can only see intact / tampered, the address axis)
  - the freshness verdict differs (A: fresh, B: stale): each reader
    compares the sealed as_of against their own now

If the third state (intact-stale) were a property of the record, both
readers would agree. They do not: one artifact, two states. The third
state is produced by the reader's act of supplying `now`.

Negative control: a tampered record read by both readers still fires the
instrument (address axis present) and still splits on freshness
(reader-supplied). The instrument is a constant on the time axis only --
not a constant wearing a lab coat on every axis.
"""
import copy
from datetime import datetime

import specimens
from claim_audit import audit


def parse(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def flags(spec):
    return sorted(audit(spec)["flags"])


# --- the sealed record: control specimen + sealed as_of + tolerance ---
base = None
for s in specimens.SPECIMENS:
    if s["name"].startswith("control"):
        base = copy.deepcopy(s)
        break
assert base is not None, "clean control specimen not found"

AS_OF = "2026-09-30T14:00:00Z"
TOLERANCE_HOURS = 24.0

record = copy.deepcopy(base)
record["as_of"] = AS_OF
record["tolerance_hours"] = TOLERANCE_HOURS

tampered = copy.deepcopy(record)
for r in tampered["rows"]:
    r["metric"] = 0.10 if r.get("mechanism_on") else 0.90  # null beats mechanism

# --- two readers: same record, different clocks ---
READER_A_NOW = "2026-09-30T15:00:00Z"  # as_of + 1h
READER_B_NOW = "2033-09-30T14:00:00Z"  # as_of + 7y


def read(record, now):
    spec = copy.deepcopy(record)
    spec["now"] = now
    f = flags(spec)
    age_h = (parse(now) - parse(record["as_of"])).total_seconds() / 3600.0
    fresh = age_h <= record["tolerance_hours"]
    integrity = "intact" if not f else "tampered"
    return f, fresh, age_h, integrity


fa, fresh_a, age_a, integ_a = read(record, READER_A_NOW)
fb, fresh_b, age_b, integ_b = read(record, READER_B_NOW)
ta, fresh_ta, age_ta, integ_ta = read(tampered, READER_A_NOW)
tb, fresh_tb, age_tb, integ_tb = read(tampered, READER_B_NOW)

print("sealed record: as_of=%s tolerance=%sh (fixed; readers differ only in `now`)"
      % (AS_OF, int(TOLERANCE_HOURS)))
print()
print("reader A  now=%s (as_of + 1h)" % READER_A_NOW)
print("  instrument flags: %s" % fa)
print("  reader freshness: %s (age %.0fh vs tolerance %sh)"
      % ("fresh" if fresh_a else "stale", age_a, int(TOLERANCE_HOURS)))
print("  reader state:     %s" % ("%s-%s" % (integ_a, "fresh" if fresh_a else "stale")))
print()
print("reader B  now=%s (as_of + 7y)" % READER_B_NOW)
print("  instrument flags: %s" % fb)
print("  reader freshness: %s (age %.0fh vs tolerance %sh)"
      % ("fresh" if fresh_b else "stale", age_b, int(TOLERANCE_HOURS)))
print("  reader state:     %s" % ("%s-%s" % (integ_b, "fresh" if fresh_b else "stale")))
print()
print("SPLIT on the same sealed record:")
print("  instrument (bi-state):  A == B ->", fa == fb)
print("  reader     (tri-state): A != B ->", (integ_a, fresh_a) != (integ_b, fresh_b))
print()
print("negative control (tampered record, both readers):")
print("  reader A flags: %s" % ta)
print("  reader B flags: %s" % tb)
print("  address axis present (flags != []):", bool(ta))
print("  instrument time-blind (A == B):", ta == tb)
print("  reader states: A=%s B=%s"
      % ("%s-%s" % (integ_ta, "fresh" if fresh_ta else "stale"),
         "%s-%s" % (integ_tb, "fresh" if fresh_tb else "stale")))
print()
ok = (fa == fb) and ((integ_a, fresh_a) != (integ_b, fresh_b)) and bool(ta) and (ta == tb) and (not fa)
print("VERDICT:",
      "the seal is bi-state (intact/tampered); the third state (intact-stale) is produced by the reader supplying `now` -- one artifact, two states"
      if ok else "UNEXPECTED -- inspect the readers")
