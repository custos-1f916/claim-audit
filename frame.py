#!/usr/bin/env python3
"""frame.py -- is 'the writer choosing which FRAME OF REFERENCE the record is
asserted in' a new self-keyed mechanism?

Tests whether the frame choice (the coordinate system in which the record is
expressed, rather than what the record contains) introduces a genuinely new
self-keyed referent, or collapses into the what-is-recorded channel (the
writer picks a lossy function state->record; the stranger sees the record and
cannot recover the state).

Model:
  The writer has a raw state s (a length-4 vector over {1,2,3,4}).
  The writer chooses a CONTENT function (a lossy projection, e.g. sum) and a
  FRAME (a bijective coordinate transform on the content value, e.g. relative
  to an origin). The record is the content expressed in the frame.
  A stranger reads the record.

The self-keyed question: given the record, can the stranger recover s?

Hypothesis (the verdict we test): the frame is a BIJECTION on the content
value (invertible), so it adds NO lossiness. The self-keyedness is entirely
from the lossy CONTENT function. Choosing the frame is choosing a relabel (a
bijection) of the content, not choosing a new lossy function. The frame is a
relabeling, NOT a new self-keyed referent.

DATA = [1,2,3,4] (the state).
ALT_STATES = all length-4 vectors over {1,2,3,4} (256 states).

CONTENT functions (lossy projections state->value):
  'sum':   sum(s)
  'mean':  sum(s)//4
  'first': s[0]
  'range': max(s)-min(s)

FRAMES (bijective coordinate transforms on the content value):
  'absolute': v -> v
  'rel-1':    v -> v - 1
  'rel-3':    v -> v - 3
  'negate':   v -> -v

The record is (content_name, frame_name, frame(content(s))). The frame IS
recorded (the stranger knows which frame was used).

DISCRIMINATING CHECKS:
  P1 function       : every (content, frame) pair is a well-defined function
                      of the state.
  P2 self-keyed     : there exist lossy content functions (a stranger with
                      only the record cannot recover the state).
  P3 frame-invariant: the number of consistent states is INVARIANT under the
                      frame choice (because the frame is a bijection). The
                      frame adds NO gap. If the frame added a new self-keyed
                      channel, the gap would depend on the frame. It doesn't.
  P4 same channel   : every frame is a bijection on the content value space
                      (injective) AND at least one content function is lossy.
                      The self-keyedness is 'the writer controls what is
                      recorded' (the lossy content function). The frame is a
                      relabel (a bijection), NOT a new self-keyed kind.

VERDICT target: frame-of-reference is the SAME self-keyed channel
(what-is-recorded / function-selection), a relabeling, NOT a new self-keyed
referent. Closes the second terminus candidate (2e9551e5).
"""
import itertools

DATA = [1, 2, 3, 4]
N = 4
VALUES = [1, 2, 3, 4]
ALT_STATES = [list(s) for s in itertools.product(VALUES, repeat=N)]  # 256 states

CONTENT = {
    'sum':   lambda s: sum(s),
    'mean':  lambda s: sum(s) // 4,
    'first': lambda s: s[0],
    'range': lambda s: max(s) - min(s),
}

FRAMES = {
    'absolute': lambda v: v,
    'rel-1':    lambda v: v - 1,
    'rel-3':    lambda v: v - 3,
    'negate':   lambda v: -v,
}

def record(cname, fname, s):
    """The record: content expressed in the frame (frame is recorded)."""
    cval = CONTENT[cname](s)
    fval = FRAMES[fname](cval)
    return (cname, fname, fval)

# P1: every (content, frame) pair is a well-defined function of the state
p1 = True
for cname in CONTENT:
    for fname in FRAMES:
        for s in ALT_STATES:
            try:
                record(cname, fname, s)
            except Exception:
                p1 = False

# P2: there exist lossy content functions (multiple states -> same value)
content_lossy = {}
for cname, f in CONTENT.items():
    vals = {}
    for s in ALT_STATES:
        v = f(s)
        vals[v] = vals.get(v, 0) + 1
    content_lossy[cname] = any(c > 1 for c in vals.values())
p2 = any(content_lossy.values())

# P3: frame-invariant gap -- the number of consistent states is INVARIANT
#     under the frame choice (because the frame is a bijection). For a fixed
#     content function and fixed state DATA, the consistent-state count must
#     be the same for every frame.
p3 = True
for cname in CONTENT:
    base = record(cname, 'absolute', DATA)
    n_base = sum(1 for s in ALT_STATES if record(cname, 'absolute', s) == base)
    for fname in FRAMES:
        rec = record(cname, fname, DATA)
        n = sum(1 for s in ALT_STATES if record(cname, fname, s) == rec)
        if n != n_base:
            p3 = False

# P4: same channel -- every frame is a bijection (injective) on the content
#     value space, AND at least one content function is lossy.
frame_bij = True
for fname, f in FRAMES.items():
    for cname in CONTENT:
        vals = {CONTENT[cname](s) for s in ALT_STATES}
        fvals = [FRAMES[fname](v) for v in vals]
        if len(set(fvals)) != len(vals):
            frame_bij = False
p4 = frame_bij and p2

print("Discriminating checks: frame-of-reference as a new self-keyed channel?")
print("P1 function (every (content,frame) a well-defined fn of state):", p1)
print("P2 self-keyed (some lossy content function):", p2)
print("   content lossiness:", content_lossy)
print("P3 frame-invariant (gap invariant under frame choice):", p3)
print("P4 same channel (frame bijective + content lossy):", p4)
print()
# Concrete demonstration: the 'sum' content in different frames
cval = CONTENT['sum'](DATA)
n_sum = sum(1 for s in ALT_STATES if CONTENT['sum'](s) == cval)
print("DEMO: 'sum' content in different frames")
print("  state DATA =", DATA, "-> content 'sum' =", cval)
for fname in FRAMES:
    rec = record('sum', fname, DATA)
    n = sum(1 for s in ALT_STATES if record('sum', fname, s) == rec)
    print("  frame '%s' -> record %s, %d consistent states" % (fname, rec, n))
print("  the gap is %d states for EVERY frame -> the frame adds no gap" % n_sum)
print("  -> the self-keyedness is the lossy CONTENT function (sum),")
print("     NOT the frame. The frame is a relabel (a bijection).")
print()
if p1 and p2 and p3 and p4:
    print("VERDICT: PASS -- frame-of-reference is the SAME self-keyed channel")
    print("  (what-is-recorded / function-selection), a relabeling, NOT a new referent.")
    print("  Closes the second terminus candidate (2e9551e5).")
else:
    print("VERDICT: FAIL -- inspect the failing property")
