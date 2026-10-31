#!/usr/bin/env python3
"""The arbiter's own check: oracle.py against references that cannot share its mistakes.

  hostref   the x86 SSE unit (tininess after rounding): add, sub, mul, div, sqrt, fma; binary32 and
            binary64; roundTiesToEven and the three directed attributes; result bits and all five flags
  sfref     Berkeley SoftFloat 3e: the same operations under roundTiesToAway, roundTiesToEven and
            roundTowardZero, with tininess detected before rounding and after

Every case must agree, bits and flags; the one exception is fma(0, inf, quiet NaN), whose invalid flag
754-2019 7.2(c) leaves to the implementation. Exit 1 on any disagreement, 2 if a reference is missing.
Usage: validate_oracle.py [hostref cases per operation and attribute, default 1500] [sfref's, default 2000]
"""
import os, subprocess, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oracle import compute

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
BIN = os.path.join(os.environ.get('AUDIT_WORK', os.path.join(ROOT, 'dist', 'audit')), 'native', 'bin')
N = {'hostref': sys.argv[1] if len(sys.argv) > 1 else '1500', 'sfref': sys.argv[2] if len(sys.argv) > 2 else '2000'}
ARITY = {'add': 2, 'sub': 2, 'mul': 2, 'div': 2, 'sqrt': 1, 'fma': 3}

def is_nan(x, f):
    m, e = (23, 8) if f == 32 else (52, 11)
    return ((x >> m) & ((1 << e) - 1)) == (1 << e) - 1 and x & ((1 << m) - 1)

def check(name, lines, with_tiny):
    bad = collections.Counter(); n = 0; ex = []
    for line in lines:
        t = line.split()
        if with_tiny:
            op, f, rm, tiny, a, b, c, x = t[:8]; fl = t[8] if len(t) > 8 else ''
        else:
            op, f, rm, a, b, c, x = t[:7]; fl = t[7] if len(t) > 7 else ''; tiny = 'after'
        f = int(f)
        got, gfl = compute(op, f, rm, [int(a, 16), int(b, 16), int(c, 16)][:ARITY[op]], tiny=tiny)
        if gfl == 'i?':
            continue
        n += 1
        xv = int(x, 16)
        if not ((got is None and is_nan(xv, f)) or got == xv) or gfl != fl:
            bad[(op, f, rm, tiny)] += 1
            if len(ex) < 8: ex.append((line.strip(), hex(got) if got is not None else 'nan', gfl))
    print(f'{name}: {n} cases, {sum(bad.values())} disagreements {dict(bad) if bad else ""}')
    for e in ex: print('   ', e)
    return sum(bad.values())

rc = 0
for prog, tiny in (('hostref', False), ('sfref', True)):
    p = os.path.join(BIN, prog)
    if not os.path.exists(p):
        print(f'{prog}: not built (see setup.sh)'); rc = max(rc, 2); continue
    out = subprocess.run([p, N[prog]], capture_output=True, text=True, check=True).stdout.splitlines()
    if check(prog, out, tiny):
        rc = 1
sys.exit(rc)
