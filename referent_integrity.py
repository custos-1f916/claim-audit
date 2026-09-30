#!/usr/bin/env python3
"""
referent_integrity.py — does a cited address still resolve to the cited referent?

Mechanizes the address-vs-resolution grid. For each cited reference the probe
resolves the cited address and compares the cited referent (its title) to what
now lives at that address. Two orthogonal axes:

  ADDRESS axis — does the cited address still point at the same record?
    STABLE  the address 200s at the same record (no redirect)
    MOVED   the address redirects (302) to a different record

  REFERENT axis — does the cited title still match the live title?
    PRESERVED  cited title ~ live title (after normalization)
    DRIFTED    cited title != live title

Four cells:
    (STABLE, PRESERVED)  clean — the citation is intact
    (MOVED,  PRESERVED)  address moved, referent preserved (a version bump that
                         kept the work; the old address now forwards)
    (STABLE, DRIFTED)    address stable, referent drifted — the load-bearing
                         cell: the address is unchanged but the thing at it is
                         no longer the thing you cited
    (MOVED,  DRIFTED)    both changed

Plus a SELF-KEYED check on the subject record: does its conceptdoi dangle back
to the record itself (no independent version history)?

--offline FILE reads a pre-fetched witness JSON (stranger-rerunnable, no
network). The witness is the evidence; the classification is deterministic.
"""
import re, json, sys, unicodedata, argparse

THR_DEFAULT = 0.6

def norm_title(t):
    if not t:
        return []
    t = re.sub(r'\\mathbb\{([^}]*)\}', r'\1', t)
    t = re.sub(r'\\[a-zA-Z]+\{?([^}{}]*)\}?', r'\1', t)   # latex commands
    t = re.sub(r'[\$\\{}^_~]', ' ', t)
    t = unicodedata.normalize('NFKD', t)
    t = t.encode('ascii', 'ignore').decode()
    t = t.lower()
    t = re.sub(r'[^a-z0-9]+', ' ', t)
    return [w for w in t.split() if w]

def token_overlap(cited, live):
    c, l = set(cited), set(live)
    if not c:
        return 0.0
    return len(c & l) / len(c)

def classify(cit, thr):
    address = 'MOVED' if cit.get('redirected') else 'STABLE'
    ov = token_overlap(norm_title(cit.get('cited_title','')),
                       norm_title(cit.get('live_title','')))
    referent = 'PRESERVED' if ov >= thr else 'DRIFTED'
    return address, referent, ov

def self_keyed(subj):
    recid = subj.get('recid')
    cf = subj.get('concept_final_recid')
    isv = subj.get('is_version_of')
    return (cf == recid) and (not isv)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--offline', help='witness JSON file')
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--thr', type=float, default=THR_DEFAULT)
    args = ap.parse_args()

    if args.offline:
        w = json.load(open(args.offline))
    elif args.live:
        raise SystemExit('live fetch not exercised in this slice; use --offline')
    else:
        raise SystemExit('need --offline FILE')

    print('referent-integrity probe — address x resolution grid')
    print('=' * 60)
    cells = []
    for cit in w.get('citations', []):
        address, referent, ov = classify(cit, args.thr)
        cells.append((address, referent))
        print(cit['doi'])
        print('  address:  %s   (cited recid %s -> final %s)' % (address, cit.get('cited_recid'), cit.get('final_recid')))
        print('  referent: %s   (token overlap %.2f, thr %.2f)' % (referent, ov, args.thr))
        print('  cell:     (%s, %s)' % (address, referent))
        print()
    subj = w.get('subject')
    if subj:
        sk = self_keyed(subj)
        print('subject record %s: self-keyed = %s' % (subj.get('recid'), sk))
        print('  conceptdoi %s -> final recid %s; is_version_of = %s' % (subj.get('conceptdoi'), subj.get('concept_final_recid'), subj.get('is_version_of')))
        print()
    n = sum(1 for a, r in cells if a == 'STABLE' and r == 'DRIFTED')
    print('verdict: %d citation(s) in the (STABLE, DRIFTED) cell — address unchanged, referent no longer the cited thing.' % n)

if __name__ == '__main__':
    main()
