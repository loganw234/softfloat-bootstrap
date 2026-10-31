#!/usr/bin/env python3
"""Do muse's committed test data share cft's *random* operands?  High-entropy 32/64-bit
hex words in every muse tests/ & site/ data file vs every cft tracked text file at HEAD.
Correct results for shared famous inputs coincide by mathematics, so the count that matters
is shared high-entropy words, and what they are."""
import os, re, subprocess, collections, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fp import MUSE, CFT, git_read
def files(repo, rev, pathspec):
    """(path, blob) of every file under pathspec in rev, read from git objects."""
    out = subprocess.run(['git', '-C', repo, 'ls-tree', '-r', '-z', rev, '--'] + pathspec, capture_output=True, check=True).stdout
    rows = [r.decode() for r in out.split(b'\0') if r]
    return [(r.split('\t', 1)[1], r.split()[2]) for r in rows if r.split()[1] == 'blob']
def words(repo, fl):
    W = collections.defaultdict(set)
    texts = git_read(repo, [b for _, b in fl])
    for f, b in fl:
        t = texts[b]
        for m in re.finditer(r'(?<![0-9A-Za-z])(?:0x)?([0-9A-Fa-f]{7,16})(?![0-9A-Za-z])', t):
            W[m.group(1).lower().zfill(16) if len(m.group(1)) > 8 else m.group(1).lower().zfill(8)].add(f)
    return W
def high_entropy(h):
    v = int(h, 16); b = bin(v)[2:].zfill(len(h) * 4)
    tr = sum(1 for i in range(1, len(b)) if b[i] != b[i-1])
    return tr >= (16 if len(h) == 16 else 9)
MREV, CREV = os.environ.get('MUSE_REV', 'HEAD'), os.environ.get('CFT_REV', 'HEAD')
M = words(MUSE, files(MUSE, MREV, ['tests', 'site', 'board', 'demo', 'examples']))
C = words(CFT, files(CFT, CREV, ['.']))
mh = {w for w in M if high_entropy(w)}; ch = {w for w in C if high_entropy(w)}
sh = mh & ch
print(f'muse high-entropy words {len(mh)}, cft {len(ch)}, shared {len(sh)} ({100*len(sh)/max(1,len(mh)):.3f}% of muse)')
by = collections.Counter()
for w in sh:
    by[(sorted(M[w])[0].split('/')[0] + '/' + sorted(M[w])[0].split('/')[-1], sorted(C[w])[0])] += 1
for k, n in by.most_common(25): print(f'  {n:5d}  muse {k[0]:<40} cft {k[1]}')
import struct
print('\nthe shared words, decoded (a famous value is the explanation; a random operand would not be):')
for w in sorted(sh):
    v = int(w, 16)
    x = struct.unpack('<d', struct.pack('<Q', v))[0] if len(w) == 16 else struct.unpack('<f', struct.pack('<I', v))[0]
    print(f'  {w} = {x!r}')
