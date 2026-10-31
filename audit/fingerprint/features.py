#!/usr/bin/env python3
"""Feature-level overlap: numeric constants, identifiers, string literals and
comment phrases shared by muse-softfloat and cft-fp256 (all refs), minus what a
permitted common source (Berkeley 3e, the kit as muse received it) also holds.

Usage: features.py OUTDIR
"""
import os, sys, re, json, collections
from decimal import Decimal, InvalidOperation
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fp import *

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
is_kit = lambda p: p.startswith('audit-bundle/kit/')
PROSE = {'.md', '.txt', '.html'}

def corpus_code(repo, **kw):
    m = git_ls_blobs(repo, **kw)
    t = git_read(repo, list(m))
    return [(m[o], o, t[o]) for o in m]

muse = corpus_code(MUSE, exclude=is_kit)
cft = corpus_code(CFT)
base = corpus_code(MUSE, include=is_kit) + corpus_code(BOOTSTRAP)
for root, _, files in os.walk(BASE_DIR):
    for f in files:
        if os.path.splitext(f)[1] in CODE_EXT:
            p = os.path.join(root, f)
            base.append((p, None, open(p, encoding='latin-1').read()))
# prose baseline: the kit's texts as muse received them
kit_prose = corpus_code(MUSE, exts=PROSE, include=is_kit)
kit_prose += corpus_code(BOOTSTRAP, exts=PROSE, include=lambda p: p.startswith('kit/'))
print('files: muse', len(muse), 'cft', len(cft), 'base', len(base), 'kit prose', len(kit_prose), flush=True)

def num_value(tok):
    t = tok.lower().replace('_', '').replace("'", '')
    try:
        if t.startswith('0x') and 'p' not in t and '.' not in t:
            return int(t.rstrip('ul') or '0', 16)
        if t.startswith('0b'):
            return int(t[2:].rstrip('ul'), 2)
        if re.fullmatch(r'\d+[ul]*', t):
            return int(t.rstrip('ul'))
        if t.startswith('0x'):
            return ('hexfloat', float.fromhex(t.rstrip('fl')).hex())
        d = Decimal(t.rstrip('fl'))
        if d == d.to_integral_value() and len(t) < 20 and 'e' not in t:
            return int(d)
        return ('dec', str(d.normalize()))
    except (ValueError, InvalidOperation):
        return None

def transitions(v):
    if v < 0: v = -v
    b = bin(v)[2:]
    return sum(1 for i in range(1, len(b)) if b[i] != b[i - 1]), len(b)

def interesting_num(v, tok):
    """High-entropy constants only: not masks, not powers of two, not small."""
    if isinstance(v, int):
        if v < 1 << 20:
            return False
        tr, nb = transitions(v)
        return tr >= 6
    kind, s = v
    digits = re.sub(r'[^0-9]', '', s.split('E')[0]) if kind == 'dec' else re.sub(r'[^0-9a-f]', '', s.split('p')[0])
    return len(digits.strip('0')) >= 8

ID_OK = re.compile(r'^[A-Za-z_][A-Za-z0-9_]{5,}$')
def features(items):
    nums = collections.defaultdict(list); ids = collections.defaultdict(set); strs = collections.defaultdict(set)
    shingles = collections.defaultdict(set)
    for path, oid, text in items:
        l0, l1, lines, com = tokenize(text, lang_of(path))
        for tok, ln, tl1 in zip(l0, lines, l1):
            if tl1 == 'N':
                v = num_value(tok)
                if v is not None and interesting_num(v, tok):
                    nums[v].append((path, ln))
            elif tl1 == 'I' and ID_OK.match(tok):
                ids[tok].add(path)
            elif tl1 == 'S' and len(tok) >= 18:
                strs[tok[1:-1] if tok[0] in '"\'`' else tok].add(path)
        for ln, c in com:
            words = re.findall(r'[a-z0-9]+', c.lower())
            for i in range(len(words) - 7):
                shingles[' '.join(words[i:i + 8])].add((path, ln))
    return nums, ids, strs, shingles

def prose_shingles(items):
    sh = set()
    for path, oid, text in items:
        words = re.findall(r'[a-z0-9]+', text.lower())
        for i in range(len(words) - 7):
            sh.add(' '.join(words[i:i + 8]))
    return sh

mN, mI, mS, mC = features(muse)
cN, cI, cS, cC = features(cft)
bN, bI, bS, bC = features(base)
kitsh = prose_shingles(kit_prose) | set(bC)
print('features done', flush=True)

def line_of(repo, path, ln, oid=None):
    try:
        t = subprocess.run(['git', '-C', repo, 'show', 'HEAD:' + path], capture_output=True, text=True).stdout.splitlines()
        return t[ln - 1].strip()[:160] if 0 < ln <= len(t) else ''
    except Exception:
        return ''

rep = {}
sharedN = [v for v in mN if v in cN and v not in bN]
rep['constants_shared'] = len([v for v in mN if v in cN])
rep['constants_shared_explained_by_baseline'] = len([v for v in mN if v in cN and v in bN])
rep['constants_shared_unexplained'] = [
    dict(value=(hex(v) if isinstance(v, int) else v), muse=sorted(set(p for p, _ in mN[v]))[:4],
         cft=sorted(set(p for p, _ in cN[v]))[:4], muse_ex=mN[v][0], cft_ex=cN[v][0])
    for v in sorted(sharedN, key=lambda v: str(v))]
sharedI = sorted(i for i in mI if i in cI and i not in bI)
rep['identifiers_shared_unexplained'] = [dict(id=i, muse=sorted(mI[i])[:3], cft=sorted(cI[i])[:3], ncft_files=len(cI[i])) for i in sharedI]
sharedS = sorted(s for s in mS if s in cS and s not in bS)
rep['strings_shared_unexplained'] = [dict(s=s[:120], muse=sorted(mS[s])[:3], cft=sorted(cS[s])[:3]) for s in sharedS]
sharedC = sorted(s for s in mC if s in cC and s not in kitsh)
rep['comment_shingles_shared_unexplained'] = len(sharedC)
# merge overlapping shingles into passages per muse location
by_loc = collections.defaultdict(set)
for s in sharedC:
    for (p, ln) in mC[s]:
        by_loc[(p, ln)].add(s)
rep['comment_passages'] = [dict(muse=f'{p}:{ln}', n_shingles=len(v), sample=sorted(v)[0],
                                cft=sorted(set(f'{q}:{l}' for s in v for (q, l) in cC[s]))[:3])
                           for (p, ln), v in sorted(by_loc.items(), key=lambda kv: -len(kv[1]))[:80]]
json.dump(rep, open(os.path.join(OUT, 'features.json'), 'w'), indent=1, default=str)
print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in rep.items()}, indent=1))
