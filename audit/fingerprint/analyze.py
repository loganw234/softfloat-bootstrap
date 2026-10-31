#!/usr/bin/env python3
"""Summarise runs.json: controls first (must be caught), then every muse path's
strongest cft-only overlap, then side-by-side text of the longest runs.

Usage: analyze.py OUTDIR [T0 T1 NSHOW]
"""
import os, sys, json, collections, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fp import *

OUT = sys.argv[1]
T0 = int(sys.argv[2]) if len(sys.argv) > 2 else 50     # exact-token run worth reading
T1 = int(sys.argv[3]) if len(sys.argv) > 3 else 80     # normalised-token run worth reading
NSHOW = int(sys.argv[4]) if len(sys.argv) > 4 else 12
R = json.load(open(os.path.join(OUT, 'runs.json')))

def longest(rec, lvl):
    rr = rec[f'L{lvl}']['runs']
    return rr[0]['tokens'] if rr else 0

print('=== POSITIVE CONTROLS (cft code planted into a copy of muse src/msf32.c or tools/gen_tables.py) ===')
print('  caught = a run of >= T0 exact or >= T1 normalised tokens that overlaps the PLANTED lines; a run elsewhere')
print("  in the host file is the host's own and does not count")
ctl = [r for r in R if r['key'].startswith('CONTROL/')]
caught = 0
for r in ctl:
    a, b = r['planted']
    hits = [(lvl, run['tokens'], run['complexity'], run['src']) for lvl, T in ((0, T0), (1, T1))
            for run in r[f'L{lvl}']['runs'] if run['tokens'] >= T and run['lines'][1] >= a and run['lines'][0] <= b]
    best = max(hits, key=lambda h: h[1]) if hits else None
    caught += bool(hits)
    print(f"  {'CAUGHT' if hits else 'MISSED'}  {r['key']:<48} planted lines {a}-{b}  best "
          + (f"L{best[0]} {best[1]} tokens, complexity {best[2]}, from {best[3]}" if best else "none"))
print(f'  controls caught: {caught} of {len(ctl)}')

print('\n=== MUSE PATHS, strongest version, cft-only overlap (not in Berkeley 3e or the kit) ===')
by_path = collections.defaultdict(list)
for r in R:
    if r['key'].startswith('muse:'):
        by_path[r['path']].append(r)
rows = []
for p, recs in by_path.items():
    b0 = max(recs, key=lambda r: longest(r, 0)); b1 = max(recs, key=lambda r: longest(r, 1))
    rows.append(dict(path=p, versions=len(recs), l0=longest(b0, 0), l1=longest(b1, 1),
                     cov0=max(r['L0']['cov'] for r in recs), cov1=max(r['L1']['cov'] for r in recs),
                     covany0=max(r['L0']['cov_any'] for r in recs), k0=b0['key'], k1=b1['key']))
rows.sort(key=lambda x: -(x['l0'] / T0 + x['l1'] / T1))
flag = [x for x in rows if x['l0'] >= T0 or x['l1'] >= T1]
print(f'  {len(rows)} paths; {len(flag)} reach a run of >= {T0} exact or >= {T1} normalised tokens')
print(f"  {'path':<52} {'vers':>4} {'L0run':>6} {'L1run':>6} {'L0cov%':>7} {'L1cov%':>7} {'anyL0%':>7}")
for x in rows[:40]:
    print(f"  {x['path'][:52]:<52} {x['versions']:>4} {x['l0']:>6} {x['l1']:>6} {100*x['cov0']:>7.2f} {100*x['cov1']:>7.2f} {100*x['covany0']:>7.2f}")
lib = [x for x in rows if x['path'].startswith(('src/', 'include/', 'compat/', 'site/'))]
print('\n  library code only (src/ include/ compat/ site/):')
for x in lib[:15]:
    print(f"  {x['path'][:52]:<52} {x['versions']:>4} {x['l0']:>6} {x['l1']:>6} {100*x['cov0']:>7.2f} {100*x['cov1']:>7.2f}")

json.dump(dict(rows=rows, flagged=flag), open(os.path.join(OUT, 'summary.json'), 'w'), indent=1)

# ---------- side by side ----------
def muse_blob(key):
    path, oid8 = key[len('muse:'):].rsplit('@', 1)
    return subprocess.run(['git', '-C', MUSE, 'cat-file', '-p', oid8], capture_output=True, text=True, errors='replace').stdout

def cft_text(path):
    t = subprocess.run(['git', '-C', CFT, 'show', 'HEAD:' + path], capture_output=True, text=True, errors='replace')
    if t.returncode == 0:
        return t.stdout, 'HEAD'
    oid = subprocess.run(['git', '-C', CFT, 'log', '--all', '-1', '--format=%H', '--', path], capture_output=True, text=True).stdout.strip()
    t = subprocess.run(['git', '-C', CFT, 'show', f'{oid}~1:{path}'], capture_output=True, text=True, errors='replace')
    return t.stdout, oid[:8] + '~1'

def show(key, run, lvl):
    mt = muse_blob(key)
    path = key[len('muse:'):].rsplit('@', 1)[0]
    ml = mt.splitlines()
    a, b = run['lines']
    print(f"\n--- {key}  L{lvl} run {run['tokens']} tokens (complexity {run['complexity']}), muse lines {a}-{b}; best source {run['src']} lines {run['src_lines']}")
    for i in range(a - 1, min(b, a + 24)):
        print(f'   M{i+1:5d}| {ml[i][:150]}')
    if run['src'] and run['src_lines']:
        sp = run['src'].split(':', 1)[1]
        ct, ver = cft_text(sp)
        cl = ct.splitlines()
        sa, sb = run['src_lines']
        print(f'   (cft {sp} @ {ver}; line numbers are from the version that first matched, so this is approximate)')
        for i in range(max(0, sa - 1), min(len(cl), sa - 1 + min(25, b - a + 1))):
            print(f'   C{i+1:5d}| {cl[i][:150]}')

print(f'\n=== LONGEST RUNS (top {NSHOW} by exact tokens, then top {NSHOW} by normalised) ===')
allruns = []
for r in R:
    if r['key'].startswith('muse:'):
        for lvl in (0, 1):
            for run in r[f'L{lvl}']['runs'][:3]:
                allruns.append((lvl, run['tokens'], r['key'], run))
seen = set()
for lvl in (0, 1):
    cand = sorted([x for x in allruns if x[0] == lvl], key=lambda x: -x[1])
    shown = 0
    for _, ntok, key, run in cand:
        path = key.split('@')[0]
        sig = (path, lvl, run['src'])
        if sig in seen:
            continue
        seen.add(sig)
        show(key, run, lvl)
        shown += 1
        if shown >= NSHOW:
            break
