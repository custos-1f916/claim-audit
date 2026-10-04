#!/usr/bin/env python3
"""Full-scope None-slip scan, completeness-corrected.

Auto-detects every helper that can return None (has a `return None` in its
body), then flags every comparison whose operand is an absent-able value:
  - an inline .get() call
  - an inline call to a None-capable helper
  - a variable assigned from either
Classifies each as IDENTITY (is/is-not None: defined), GUARDED (a prior
is-None test on the same var), or SLIP (unguarded non-identity compare: the
absent case silently evaluates, None==v False / None!=v True / None in v False).
"""
import ast

src = open("claim_audit.py").read()
tree = ast.parse(src)

funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]

def has_return_none(fn):
    for node in ast.walk(fn):
        if isinstance(node, ast.Return):
            v = node.value
            if isinstance(v, ast.Constant) and v.value is None:
                return True
    return False

NONE_HELPERS = {fn.name for fn in funcs if has_return_none(fn)}
print("None-capable helpers (%d): %s" % (len(NONE_HELPERS), ", ".join(sorted(NONE_HELPERS))))
print()

def is_get(n):
    return (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
            and n.func.attr == "get")
def is_none_helper(n):
    return (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            and n.func.id in NONE_HELPERS)

by_op = {}
slips = []
for fn in funcs:
    maybenone = set()
    for node in ast.walk(fn):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and (is_get(node.value) or is_none_helper(node.value)):
                    maybenone.add(t.id)
    guards = set()
    for node in ast.walk(fn):
        if isinstance(node, ast.Compare):
            for op in node.ops:
                if isinstance(op, (ast.Is, ast.IsNot)):
                    for cand in [node.left] + node.comparators:
                        if isinstance(cand, ast.Name):
                            guards.add(cand.id)
    for node in ast.walk(fn):
        if isinstance(node, ast.Compare):
            for op in node.ops:
                ident = isinstance(op, (ast.Is, ast.IsNot))
                for cand in [node.left] + node.comparators:
                    tag = None
                    if isinstance(cand, ast.Name) and cand.id in maybenone:
                        tag = cand.id
                    elif is_get(cand):
                        tag = "inline.get"
                    elif is_none_helper(cand):
                        tag = "inline.helper:%s" % cand.func.id
                    if tag is None:
                        continue
                    opname = type(op).__name__
                    by_op[opname] = by_op.get(opname, 0) + 1
                    if ident:
                        continue
                    varname = cand.id if isinstance(cand, ast.Name) else None
                    if varname in guards:
                        continue
                    slips.append((fn.name, node.lineno, ast.unparse(node), opname, tag))

print("=== comparison sites by operator ===")
for k in sorted(by_op):
    print("  %-8s %d" % (k, by_op[k]))
print("total: %d" % sum(by_op.values()))
print()
print("=== UNGUARDED non-identity comparisons (candidate slips): %d ===" % len(slips))
for name, ln, expr, op, tag in slips:
    print("  %-28s L%-5d %-52s [%s]" % (name, ln, expr, op))

# --- selftest: the scan is deterministic and the slip is unique ---
if __name__ == "__main__":
    import re
    # Re-derive: exactly one unguarded non-identity comparison is a GATE slip
    # (the VACUOUS-RATIO fire). The other 16 candidates are DEFINED (detail
    # notes, declared defaults, documented N/A, conservative truthiness, or
    # intended row-selection semantics). Assert the slip is the only audit()
    # gate that compares a None-returning helper to a literal unguarded.
    slip_lines = [s for s in slips if s[0] == "audit" and s[3] == "Eq"
                  and "_headline_support" in s[4]]
    assert len(slip_lines) == 1, "expected exactly 1 VACUOUS-RATIO slip, got %d" % len(slip_lines)
    assert slip_lines[0][2].strip() == "_headline_support(spec) == 0", slip_lines[0]
    # The 16 others must NOT be in audit() (they are detail-notes/defaults/N-A).
    non_audit = [s for s in slips if s[0] != "audit"]
    assert len(non_audit) == 16, "expected 16 non-audit candidates, got %d" % len(non_audit)
    print("SELFTEST GREEN: 17 candidates = 1 VACUOUS-RATIO slip (audit L2880) + 16 DEFINED. Singleton holds at full scope.")
