#!/usr/bin/env python3
"""Driver: suspect = muse-softfloat (all refs, minus its copy of the kit) plus
planted positive controls; source = cft-fp256 (all refs); baseline = Berkeley
SoftFloat/TestFloat 3e + the bootstrap kit (as muse received it + the builder's kit/).

Writes OUTDIR/runs.json and OUTDIR/report.txt.
"""
import os, sys, json, time, random, re, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fp import *

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
t0 = time.time()
def log(*a):
    print(f'[{time.time()-t0:6.1f}s]', *a, flush=True)

# ---------- corpora ----------
is_kit = lambda p: p.startswith('audit-bundle/kit/')
muse_map = git_ls_blobs(MUSE, exclude=is_kit)
muse_kit_map = git_ls_blobs(MUSE, include=is_kit)
cft_map = git_ls_blobs(CFT)
boot_map = git_ls_blobs(BOOTSTRAP)
log('blobs: muse', len(muse_map), 'muse-kit', len(muse_kit_map), 'cft', len(cft_map), 'bootstrap', len(boot_map))

muse_txt = git_read(MUSE, list(muse_map))
cft_txt = git_read(CFT, list(cft_map))
base = {}
for oid, t in git_read(MUSE, list(muse_kit_map)).items():
    base['musekit:' + muse_kit_map[oid] + '@' + oid[:8]] = (muse_kit_map[oid], t)
for oid, t in git_read(BOOTSTRAP, list(boot_map)).items():
    base['bootstrap:' + boot_map[oid] + '@' + oid[:8]] = (boot_map[oid], t)
for root, _, files in os.walk(BASE_DIR):
    for f in files:
        if os.path.splitext(f)[1] in CODE_EXT:
            p = os.path.join(root, f)
            base['berkeley:' + os.path.relpath(p, BASE_DIR)] = (p, open(p, encoding='latin-1').read())
log('baseline files', len(base))

# ---------- positive controls: cft code planted into copies of muse files ----------
def cft_head(path):
    return subprocess.run(['git', '-C', CFT, 'show', 'HEAD:' + path], capture_output=True, text=True).stdout
def muse_head(path):
    return subprocess.run(['git', '-C', MUSE, 'show', 'HEAD:' + path], capture_output=True, text=True).stdout

def grab_function(src, name):
    i = src.find(name + '(')
    while i >= 0:
        # a definition: line starts with a type, next '{' after ')' before ';'
        ls = src.rfind('\n', 0, i) + 1
        brace = src.find('{', i); semi = src.find(';', i)
        if brace >= 0 and (semi < 0 or brace < semi):
            depth = 0
            for j in range(brace, len(src)):
                if src[j] == '{': depth += 1
                elif src[j] == '}':
                    depth -= 1
                    if depth == 0:
                        return src[ls:j + 1]
        i = src.find(name + '(', i + 1)
    return None

def rename_ids(code, lang='c', seed=1):
    rnd = random.Random(seed)
    toks = set(re.findall(r'\b[A-Za-z_][A-Za-z0-9_]*\b', code))
    mapping = {}
    for t in sorted(toks):
        if t in KEEP:
            continue
        mapping[t] = 'v_' + ''.join(rnd.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(6))
    return re.sub(r'\b[A-Za-z_][A-Za-z0-9_]*\b', lambda m: mapping.get(m.group(), m.group()), code)

def strip_c_comments_reflow(code):
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.S)
    code = re.sub(r'//[^\n]*', '', code)
    code = re.sub(r'[ \t]+', ' ', code)
    code = re.sub(r'\n\s*\n', '\n', code)
    return code.replace('{\n', '{\n    /* reviewed */\n', 3)

controls = {}
planted = {}
cft_sf = cft_head('host/src/softfloat.c')
cft_ds = cft_head('host/src/divsqrt.c')
cft_py = cft_head('python/cft_golden/softfloat.py')
host_muse = muse_head('src/msf32.c')
# pick real functions from cft's sources by scanning definitions
def pick_funcs(src, nmin=25, nmax=70, count=3):
    names = re.findall(r'^\s*(?:static\s+)?(?:inline\s+)?[A-Za-z_][\w\s\*]*?\b([a-z_][a-z0-9_]{4,})\s*\([^;{]*\)\s*\{', src, flags=re.M)
    picked = []
    for n in names:
        f = grab_function(src, n)
        if f and nmin <= f.count('\n') <= nmax and n not in [p[0] for p in picked]:
            picked.append((n, f))
        if len(picked) >= count:
            break
    return picked
fs = pick_funcs(cft_sf) + pick_funcs(cft_ds, count=2)
for i, (n, f) in enumerate(fs):
    cut = host_muse.find('\n', len(host_muse) // 2)
    for kind, body in (('verbatim', f), ('renamed', rename_ids(f, seed=i)),
                       ('renamed+reflowed', strip_c_comments_reflow(rename_ids(f, seed=i + 7)))):
        first = host_muse[:cut].count('\n') + 2
        controls[f'CONTROL/{kind}/{n}.c'] = host_muse[:cut] + '\n' + body + '\n' + host_muse[cut:]
        planted[f'CONTROL/{kind}/{n}.c'] = [first, first + body.count('\n')]
pyf = re.findall(r'(^def [a-z_]\w*\(.*?)(?=^def |\Z)', cft_py, flags=re.M | re.S)
pyf = [f for f in pyf if 15 <= f.count('\n') <= 60][:2]
mpy = muse_head('tools/gen_tables.py')
for i, f in enumerate(pyf):
    name = re.match(r'def (\w+)', f).group(1)
    body = rename_ids(re.sub(r'#[^\n]*', '', f), seed=i)
    controls[f'CONTROL/py-renamed/{name}.py'] = mpy + '\n\n' + body
    first = mpy.count('\n') + 3
    planted[f'CONTROL/py-renamed/{name}.py'] = [first, first + body.count('\n')]
log('controls planted:', len(controls), [c.split('/')[-1] for c in controls][:6])

# ---------- tokenize suspects ----------
suspects = {}  # key -> dict
for oid, txt in muse_txt.items():
    suspects['muse:' + muse_map[oid] + '@' + oid[:8]] = dict(path=muse_map[oid], oid=oid, text=txt)
for k, txt in controls.items():
    suspects[k] = dict(path=k, oid=None, text=txt)
for key, s in suspects.items():
    l0, l1, lines, com = tokenize(s['text'], lang_of(s['path']))
    s['lines'] = np.array(lines, dtype=np.int32)
    s['h0'] = kgram_hashes(tok_ids(l0), K0)
    s['h1'] = kgram_hashes(tok_ids(l1), K1)
    s['ntok'] = len(l0)
    s['l1toks'] = l1
S0 = np.unique(np.concatenate([s['h0'] for s in suspects.values()]))
S1 = np.unique(np.concatenate([s['h1'] for s in suspects.values()]))
log('suspect k-grams: L0', len(S0), 'L1', len(S1))

# ---------- scan a corpus: which suspect k-grams it holds, and where ----------
def member(h, S):
    """h in sorted-unique S, without re-sorting S each call (np.isin would)."""
    if not len(S):
        return np.zeros(len(h), bool)
    idx = np.searchsorted(S, h)
    idx[idx >= len(S)] = len(S) - 1
    return S[idx] == h

def scan(items, want_loc):
    """items: iterable of (label, path, text). Returns (set0, set1, loc0, loc1)
    loc: hash -> {label: line}  (only when want_loc)"""
    got0, got1 = [], []
    loc0 = collections.defaultdict(dict); loc1 = collections.defaultdict(dict)
    for label, path, text in items:
        l0, l1, lines, _ = tokenize(text, lang_of(path))
        for lvl, toks, k, S, got, loc in ((0, l0, K0, S0, got0, loc0), (1, l1, K1, S1, got1, loc1)):
            h = kgram_hashes(tok_ids(toks), k)
            if not len(h):
                continue
            hit = member(h, S)
            if hit.any():
                hh = h[hit]
                got.append(np.unique(hh))
                if want_loc:
                    pos = np.nonzero(hit)[0]
                    plabel = label.rsplit('@', 1)[0]
                    for hv, p in zip(hh.tolist(), pos.tolist()):
                        d = loc[hv]
                        if plabel not in d:
                            d[plabel] = lines[p]
    s0 = np.unique(np.concatenate(got0)) if got0 else np.zeros(0, np.uint64)
    s1 = np.unique(np.concatenate(got1)) if got1 else np.zeros(0, np.uint64)
    return s0, s1, loc0, loc1

cft_items = [('cft:' + cft_map[o] + '@' + o[:8], cft_map[o], t) for o, t in cft_txt.items()]
C0, C1, cloc0, cloc1 = scan(cft_items, True)
log('cft holds suspect k-grams: L0', len(C0), 'L1', len(C1))
B0, B1, bloc0, bloc1 = scan([(k, v[0], v[1]) for k, v in base.items()], True)
log('baseline holds suspect k-grams: L0', len(B0), 'L1', len(B1))

# ---------- runs ----------
def runs_of(mask):
    if not mask.any():
        return []
    d = np.diff(np.concatenate([[0], mask.astype(np.int8), [0]]))
    starts = np.nonzero(d == 1)[0]; ends = np.nonzero(d == -1)[0]
    return list(zip(starts.tolist(), ends.tolist()))

def best_source(hs, loc):
    cnt = collections.Counter()
    for hv in hs:
        for lab in loc.get(hv, {}):
            cnt[lab.rsplit('@', 1)[0]] += 1
    if not cnt:
        return None, 0, None
    top, n = cnt.most_common(1)[0]
    ls = sorted(l for hv in hs for lab, l in loc.get(hv, {}).items() if lab.rsplit('@', 1)[0] == top)
    return top, n, (ls[0], ls[-1]) if ls else None

results = []
for key, s in suspects.items():
    rec = dict(key=key, path=s['path'], ntok=s['ntok'], planted=planted.get(key))
    for lvl, h, k, C, Bs, loc in ((0, s['h0'], K0, C0, B0, cloc0), (1, s['h1'], K1, C1, B1, cloc1)):
        if not len(h):
            rec[f'L{lvl}'] = dict(cov=0, cov_any=0, runs=[]); continue
        in_c = member(h, C); in_b = member(h, Bs)
        only = in_c & ~in_b
        cov_tok = np.zeros(s['ntok'], bool); cov_any = np.zeros(s['ntok'], bool)
        for a, b in runs_of(only): cov_tok[a:b + k - 1] = True
        for a, b in runs_of(in_c): cov_any[a:b + k - 1] = True
        rr = []
        for a, b in runs_of(only):
            ntoks = b - a + k - 1
            src, nmatch, srclines = best_source(h[a:b].tolist(), loc)
            seg = s['l1toks'][a:b + k - 1]
            grams = set(tuple(seg[j:j + 4]) for j in range(max(1, len(seg) - 3)))
            rr.append(dict(tok_range=[int(a), int(b + k - 1)], complexity=round(len(grams) / max(1, len(seg) - 3), 3),
                           distinct_tokens=len(set(seg)), tokens=int(ntoks), lines=[int(s['lines'][a]), int(s['lines'][min(b + k - 2, s['ntok'] - 1)])],
                           src=src, src_lines=srclines, src_kgrams=nmatch, kgrams=int(b - a)))
        rr.sort(key=lambda r: -r['tokens'])
        rec[f'L{lvl}'] = dict(cov=float(cov_tok.mean()), cov_any=float(cov_any.mean()),
                             cov_base=float(member(h, Bs).mean()), runs=rr[:40])
    results.append(rec)
json.dump(results, open(os.path.join(OUT, 'runs.json'), 'w'), indent=1)
log('done; suspects', len(results))
