import copy, sys
sys.path.insert(0, ".")
import claim_audit, specimens, knife_edge as ke

def leaves(spec):
    return list(ke.numeric_leaves(spec))

def sweep(e):
    ke.EPS = e
    knife, robust = [], []
    for s in specimens.SPECIMENS:
        base = ke.audit_flags(s)
        flip = False
        for path, val in leaves(s):
            step = ke.step_for(val)
            toks = ke._split_path(path)
            for d in (+1, -1):
                if d < 0 and isinstance(val, int) and val <= 0:
                    continue
                nv = val + d * step
                if isinstance(nv, int) and nv < 0:
                    continue
                p = copy.deepcopy(s)
                ke._set_at(p, toks, nv)
                if ke.audit_flags(p) != base:
                    flip = True
                    break
            if flip:
                break
        (knife if flip else robust).append(s["name"])
    return set(knife), len(robust)

grid = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]
SELF = "CF-CG-1 sweep saturation (self-specimen, PASS cell)"
sets = {}
print("EPS      knife  robust  self-flip  names")
for e in grid:
    k, r = sweep(e)
    sets[e] = k
    print("%-8s %5d  %6d   %s" % (e, len(k), r, "YES" if SELF in k else "-"))
print()
prev = None
for e in grid:
    k = sets[e]
    if prev is None:
        print("eps=%s: baseline set (n=%d)" % (e, len(k)))
    else:
        added = k - prev
        removed = prev - k
        if not added and not removed:
            print("eps=%s: set identical to eps=%s" % (e, prev_e))
        else:
            print("eps=%s: +%d -%d  added=%s removed=%s" % (e, len(added), len(removed), sorted(added), sorted(removed)))
    prev, prev_e = k, e
print()
print("=== self-specimen flip detail at EPS=0.01 (baseline) ===")
ke.EPS = 0.01
for s in specimens.SPECIMENS:
    if s["name"] != SELF:
        continue
    base = ke.audit_flags(s)
    print("baseline flags:", sorted(base) or "(clean)")
    for path, val in leaves(s):
        step = ke.step_for(val)
        toks = ke._split_path(path)
        for d in (+1, -1):
            if d < 0 and isinstance(val, int) and val <= 0:
                continue
            nv = val + d * step
            if isinstance(nv, int) and nv < 0:
                continue
            p = copy.deepcopy(s)
            ke._set_at(p, toks, nv)
            new = ke.audit_flags(p)
            if new != base:
                print("FLIP  %s%s (%s -> %s)  %s -> %s" % (path, "+" if d > 0 else "-", val, nv, ",".join(sorted(base)) or "(clean)", ",".join(sorted(new)) or "(clean)"))
print()
print("=== self-specimen flip boundary scan ===")
fine = [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01, 0.012, 0.015, 0.02, 0.03, 0.05, 0.1]
flips = []
for e in fine:
    if SELF in sweep(e):
        flips.append(e)
print("self-specimen flips at EPS in:", flips)
if flips:
    print("min flipping EPS:", min(flips))
    clean = [e for e in fine if e not in flips]
    if clean:
        print("max clean EPS:", max(clean))
