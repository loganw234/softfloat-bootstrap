#!/usr/bin/env python3
"""Token k-gram overlap between muse-softfloat (suspect) and cft-fp256 (source),
with permitted common sources (Berkeley SoftFloat/TestFloat 3e, the bootstrap kit)
as a baseline that explains a match away.

Every k-gram of every suspect blob is checked against every k-gram of every
source blob (no winnowing loss). Two levels:
  L0  exact tokens (comments dropped, numbers canonicalised)
  L1  identifiers -> I, numbers -> N, strings -> S (keywords and std types kept)

Usage: fp.py OUTDIR [--controls]
"""
import os, re, subprocess, sys, json, threading, zlib, collections
from pathlib import Path
import numpy as np

# Paths: like the builder, the sources sit in SOURCES (default: this repository's parent directory).
# Everything this audit makes goes under AUDIT_WORK (default: dist/audit/, which git ignores).
ROOT = Path(__file__).resolve().parents[2]
SOURCES = Path(os.environ.get('SOURCES', ROOT.parent))
MUSE = os.environ.get('MUSE_REPO', str(SOURCES / 'muse-softfloat'))
CFT = os.environ.get('CFT_REPO', str(SOURCES / 'cft-fp256'))
BOOTSTRAP = str(ROOT)
WORK = Path(os.environ.get('AUDIT_WORK', ROOT / 'dist' / 'audit'))
BASE_DIR = str(WORK / 'baseline' / 'src')          # Berkeley SoftFloat 3e and TestFloat 3e, unzipped by setup.sh

CODE_EXT = {'.c', '.h', '.inc', '.cpp', '.hpp', '.cc', '.ino', '.js', '.mjs', '.cjs',
            '.py', '.sh', '.html', '.S', '.s'}
K0, K1 = 24, 40

def lang_of(path):
    ext = os.path.splitext(path)[1]
    if ext == '.py':
        return 'py'
    if ext == '.sh':
        return 'sh'
    return 'c'

C_TOK = re.compile(r'''
 (?P<ws>\s+)
|(?P<com>//[^\n]*|/\*.*?(?:\*/|\Z))
|(?P<str>"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*'|`(?:\\.|[^`\\])*`)
|(?P<num>0[xX][0-9a-fA-F_]*\.?[0-9a-fA-F_]*(?:[pP][+-]?\d+)?[uUlLfFnN]*|\d[\d_]*\.?\d*(?:[eE][+-]?\d+)?[uUlLfFnN]*|\.\d+(?:[eE][+-]?\d+)?[fF]?)
|(?P<id>[A-Za-z_$][A-Za-z0-9_$]*)
|(?P<op>>>>=|===|!==|<<=|>>=|>>>|\.\.\.|\+\+|--|->|&&|\|\||<<|>>|<=|>=|==|!=|\+=|-=|\*=|/=|%=|&=|\|=|\^=|::|\#\#|=>|.)
''', re.S | re.X)

PY_TOK = re.compile(r'''
 (?P<ws>\s+)
|(?P<com>\#[^\n]*)
|(?P<str>[rRbBuUfF]{0,2}(?:"""(?:\\.|[^\\])*?"""|\'\'\'(?:\\.|[^\\])*?\'\'\'|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*'))
|(?P<num>0[xXoObB][0-9a-fA-F_]+|\d[\d_]*\.?[\d_]*(?:[eE][+-]?\d+)?[jJ]?|\.\d+(?:[eE][+-]?\d+)?)
|(?P<id>[A-Za-z_][A-Za-z0-9_]*)
|(?P<op>\*\*=|//=|>>=|<<=|\*\*|//|<<|>>|<=|>=|==|!=|->|\+=|-=|\*=|/=|%=|&=|\|=|\^=|:=|.)
''', re.S | re.X)

SH_TOK = re.compile(r'''
 (?P<ws>\s+)
|(?P<com>(?<![\w$\{])\#[^\n]*)
|(?P<str>"(?:\\.|[^"\\])*"|'[^']*')
|(?P<num>\d+)
|(?P<id>[A-Za-z_][A-Za-z0-9_]*)
|(?P<op>\$\{|\$\(\(|\$\(|&&|\|\||>>|<<|;;|\[\[|\]\]|.)
''', re.S | re.X)

TOKRE = {'c': C_TOK, 'py': PY_TOK, 'sh': SH_TOK}

KEEP = set('''
auto break case char const continue default do double else enum extern float for goto if inline int long
register restrict return short signed sizeof static struct switch typedef union unsigned void volatile while
_Bool bool true false NULL nullptr uint8_t uint16_t uint32_t uint64_t int8_t int16_t int32_t int64_t size_t
__uint128_t __int128 unsigned_int128 define include ifdef ifndef endif elif undef pragma
var let function new this typeof instanceof delete in of class extends super import export from async await
yield try catch finally throw null undefined BigInt Number Math
def lambda None True False and or not is pass raise with as global nonlocal assert del elif self print range len
then fi esac done local echo exit set shift
'''.split())

def canon_num(t):
    t = t.lower().replace('_', '')
    t = t.rstrip('ulfn') if not t.startswith('0x') else t.rstrip('ul')
    return t

def tokenize(text, lang):
    """Return (L0 tokens, L1 tokens, line of each token, comments[(line, text)])."""
    rx = TOKRE[lang]
    l0, l1, lines, comments = [], [], [], []
    line = 1
    pos = 0
    for m in rx.finditer(text):
        kind = m.lastgroup
        s = m.group()
        if kind == 'ws':
            line += s.count('\n')
            continue
        if kind == 'com':
            comments.append((line, s))
            line += s.count('\n')
            continue
        if kind == 'num':
            l0.append(canon_num(s)); l1.append('N')
        elif kind == 'str':
            l0.append(s); l1.append('S')
        elif kind == 'id':
            l0.append(s); l1.append(s if s in KEEP else 'I')
        else:
            l0.append(s); l1.append(s)
        lines.append(line)
        line += s.count('\n')
    return l0, l1, lines, comments

MASK = (1 << 61) - 1
def tok_ids(toks):
    return np.fromiter((zlib.crc32(t.encode('utf-8', 'surrogatepass')) for t in toks), dtype=np.uint64, count=len(toks))

B = np.uint64(1000003)
def kgram_hashes(ids, k):
    n = len(ids)
    if n < k:
        return np.zeros(0, dtype=np.uint64)
    h = np.zeros(n - k + 1, dtype=np.uint64)
    with np.errstate(over='ignore'):
        for j in range(k):
            h = h * B + ids[j:n - k + 1 + j] + np.uint64(j * 7919 + 1)
    return h

def git_ls_blobs(repo, exts=CODE_EXT, exclude=None, include=None):
    out = subprocess.run(['git', '-C', repo, 'rev-list', '--all', '--objects'], capture_output=True, text=True, check=True).stdout
    seen = {}
    for ln in out.splitlines():
        parts = ln.split(' ', 1)
        if len(parts) != 2:
            continue
        oid, path = parts
        if os.path.splitext(path)[1] not in exts:
            continue
        if exclude and exclude(path):
            continue
        if include and not include(path):
            continue
        seen.setdefault(oid, path)
    return seen

def git_read(repo, oids):
    p = subprocess.Popen(['git', '-C', repo, 'cat-file', '--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    def writer():
        for o in oids:
            p.stdin.write((o + '\n').encode())
        p.stdin.close()
    t = threading.Thread(target=writer); t.start()
    res = {}
    for _ in oids:
        hdr = p.stdout.readline().split()
        size = int(hdr[2])
        data = p.stdout.read(size); p.stdout.read(1)
        res[hdr[0].decode()] = data.decode('utf-8', 'replace')
    t.join(); p.wait()
    return res

def first_commit_of_blob(repo, oid, path):
    r = subprocess.run(['git', '-C', repo, 'log', '--all', '--reverse', '--format=%h %ad', '--date=short',
                        '--find-object=' + oid, '--', path], capture_output=True, text=True)
    return (r.stdout.splitlines() or ['?'])[0]
