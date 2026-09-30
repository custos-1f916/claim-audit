#!/usr/bin/env python3
"""referent-integrity self-test (2026-09-30).

Discriminating test for referent_integrity.py, following the repo convention
(one test per probe; headline_read_test.py is the pattern). Synthetic
witnesses pin each of the four grid cells, the self-keyed variants, the
committed witness's byte-for-byte offline reproduction, and the live-fetch
None-guard: a DOI that fails to re-resolve must leave the pinned live side
intact, not crash the %d format.

Run: python3 referent_integrity_test.py   (exit 0 = all pass)
"""
import os, sys, json, subprocess
import referent_integrity as ri

HERE = os.path.dirname(os.path.abspath(__file__))
ok = True

def check(label, got, want):
    global ok
    good = got == want
    if not good:
        ok = False
    print('  [%s] %s -> got %r, want %r' % ('ok' if good else 'MISMATCH', label, got, want))

print('== (1) four grid cells classify correctly ==')
cells = {
    ('STABLE', 'PRESERVED'): dict(redirected=False, cited_title='alpha beta gamma delta', live_title='alpha beta gamma delta'),
    ('MOVED',  'PRESERVED'): dict(redirected=True,  cited_title='alpha beta gamma delta', live_title='alpha beta gamma delta'),
    ('STABLE', 'DRIFTED'):   dict(redirected=False, cited_title='alpha beta gamma delta', live_title='zeta eta theta iota'),
    ('MOVED',  'DRIFTED'):   dict(redirected=True,  cited_title='alpha beta gamma delta', live_title='zeta eta theta iota'),
}
for (addr, ref), cit in cells.items():
    got_addr, got_ref, ov = ri.classify(cit, 0.6)
    check('cell %s/%s' % (addr, ref), (got_addr, got_ref), (addr, ref))

print()
print('== (2) self-keyed variants ==')
check('cf==recid, isv=None -> True',  ri.self_keyed(dict(recid=1, concept_final_recid=1, is_version_of=None)), True)
check('cf==recid, isv=set  -> False', ri.self_keyed(dict(recid=1, concept_final_recid=1, is_version_of=dict(id=2))), False)
check('cf!=recid, isv=None -> False', ri.self_keyed(dict(recid=1, concept_final_recid=2, is_version_of=None)), False)

print()
print('== (3) committed witness reproduces recorded result byte-for-byte ==')
witness  = os.path.join(HERE, 'referent_integrity.witness-22674891.json')
recorded = os.path.join(HERE, 'referent_integrity.results.txt')
p = subprocess.run([sys.executable, os.path.join(HERE, 'referent_integrity.py'), '--offline', witness],
                   capture_output=True, text=True)
got, want = p.stdout, open(recorded).read()
if got != want:
    ok = False
    print('  [MISMATCH] offline run != recorded result (len got=%d want=%d)' % (len(got), len(want)))
    for i, (a, b) in enumerate(zip(got, want)):
        if a != b:
            print('    first diff at byte %d: got %r want %r' % (i, a, b))
            break
else:
    print('  [ok] offline run == recorded result (%d bytes)' % len(got))

print()
print('== (4) live-fetch None-guard: a resolve miss leaves the pinned side intact ==')
class FakeResp:
    def __init__(self, url, payload=None):
        self._url, self._payload = url, payload
    def geturl(self):
        return self._url
    def __enter__(self):
        return self
    def __exit__(self, *a):
        return False
    def read(self):
        return json.dumps(self._payload).encode()

def fake_urlopen(req, timeout=None):
    url = req.full_url
    if '/doi/' in url:
        return FakeResp(url)          # no /records/ -> resolve() -> None
    return FakeResp(url, {'title': 'live title'})

ri.urllib.request.urlopen = fake_urlopen
# Citation with NO pinned final_recid: before the guard this crashed the %d format.
w = dict(subject=None, citations=[
    dict(doi='10.5281/zenodo.99999999', cited_recid=99999999,
         cited_title='pinned cited title', live_title='pinned live title')])
crashed = False
try:
    ri.live_fetch(w)
except Exception as e:
    crashed = True
    print('  [MISMATCH] live_fetch raised: %r' % e)
c = w['citations'][0]
check('no crash on resolve miss', crashed, False)
check('final_recid stays None (unresolvable)', c.get('final_recid'), None)
check('live_title stays pinned', c.get('live_title'), 'pinned live title')

print()
if ok:
    print('RESULT: all referent-integrity self-tests pass.')
    sys.exit(0)
print('RESULT: referent-integrity self-test FAILED.')
sys.exit(1)
