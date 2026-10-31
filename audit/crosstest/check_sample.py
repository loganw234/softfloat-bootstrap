#!/usr/bin/env python3
"""Check bigdiff's 1-in-997 sample against the exact oracle: are the two libraries not only
in agreement but right? Covers the basic operations, the eight shared 9.2 functions,
roundToIntegral (all forms), remainder, nextUp/Down, scaleB, convertFromInt and the 9.6
min/max family. NaN results match on NaN-ness (payload is policy), flags exactly."""
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from oracle import decode, encode, Fmt, round_value
import oracle_math

RMN = {'RNE': 'rne', 'RTZ': 'rtz', 'RUP': 'rup', 'RDN': 'rdn', 'RMM': 'rna', None: 'rne'}
FL = {'i': 1, 'z': 2, 'o': 4, 'u': 8, 'x': 16}
fl2int = lambda s: sum(FL[c] for c in s if c in FL)

def is_nan(b, f):
    return decode(b, f)[0] == 'nan'

def snan(k):
    return k[0] == 'nan' and not k[2]

def val(k):
    return (-1 if k[1] else 1) * k[2]

def qnan(f):
    F = Fmt(f); return encode(0, F.einf, 1 << (F.p - 2), f)

def from_value(v, f, sign_if_zero):
    """exact (representable) Fraction -> bits"""
    if v == 0:
        return encode(sign_if_zero, 0, 0, f)
    b, fl = round_value(1 if v < 0 else 0, abs(v), f, 'rne')
    assert 'x' not in fl, 'not exact'
    return b

def round_int(v, mode):
    import math
    fl = math.floor(v); r = v - fl
    if mode == 'rne': return fl + (1 if r > Fraction(1, 2) or (r == Fraction(1, 2) and fl % 2) else 0)
    if mode == 'rna': return fl + (1 if r >= Fraction(1, 2) else 0) if v >= 0 else -round_int(-v, 'rna')
    if mode == 'rtz': return math.trunc(v)
    if mode == 'rup': return math.ceil(v)
    if mode == 'rdn': return fl

def oracle(id_, rm, f, args):
    op = id_.split('@')[0]
    rmo = RMN[rm]
    basic = {'add': 'add', 'sub': 'sub', 'mul': 'mul', 'div': 'div', 'sqrt': 'sqrt', 'fma': 'fma'}
    math9 = {'sin_pi': 'sinPi', 'cos_pi': 'cosPi', 'r_sqrt': 'rSqrt', 'hypot': 'hypot', 'exp2': 'exp2',
             'exp2m1': 'exp2m1', 'log2': 'log2', 'log2p1': 'log2p1'}
    if op in basic:
        return oracle_math.compute(basic[op], f, rmo, args)
    if op in math9:
        return oracle_math.compute(math9[op], f, rmo, args)
    ks = [decode(a, f) for a in args] if not op.startswith('from_') else None
    if op.startswith('roundToIntegral'):
        mode = rmo if op == 'roundToIntegralExact' else {'RNE': 'rne', 'RMM': 'rna', 'RTZ': 'rtz', 'RUP': 'rup', 'RDN': 'rdn'}[op.split('_')[1]]
        k = ks[0]
        if k[0] == 'nan': return None, 'i' if snan(k) else ''
        if k[0] == 'inf': return args[0], ''
        v = val(k); n = round_int(v, mode)
        flags = 'x' if (op == 'roundToIntegralExact' and n != v) else ''
        return from_value(Fraction(n), f, k[1]), flags
    if op == 'remainder':
        x, y = ks
        if x[0] == 'nan' or y[0] == 'nan': return None, 'i' if (snan(x) or snan(y)) else ''
        if x[0] == 'inf' or (y[0] == 'fin' and y[2] == 0): return None, 'i'
        if y[0] == 'inf': return args[0], ''
        q = val(x) / val(y); n = round_int(q, 'rne')
        r = val(x) - n * val(y)
        return from_value(r, f, x[1]), ''
    if op in ('nextUp', 'nextDown'):
        k = ks[0]; F = Fmt(f); b = args[0]
        if k[0] == 'nan': return None, 'i' if snan(k) else ''
        def up(bits):
            kk = decode(bits, f)
            if kk[0] == 'inf': return bits if not kk[1] else encode(1, F.einf - 1, F.fmask, f)
            if kk[2] == 0: return encode(0, 0, 1, f)
            return bits + 1 if not kk[1] else bits - 1
        if op == 'nextUp': return up(b), ''
        neg = b ^ (1 << (F.w - 1))
        return up(neg) ^ (1 << (F.w - 1)), ''
    if op == 'scaleB':
        k = ks[0]; n = int(args[1]) if args[1] < (1 << 63) else int(args[1]) - (1 << 64)
        if k[0] == 'nan': return None, 'i' if snan(k) else ''
        if k[0] == 'inf' or k[2] == 0: return args[0], ''
        v = k[2] * (Fraction(2) ** n if n >= 0 else Fraction(1, 2 ** -n))
        return round_value(k[1], v, f, rmo)
    if op.startswith('from_'):
        kind = op.split('_')[1]; w = 32 if kind.endswith('32') else 64
        u = args[0] & ((1 << w) - 1)          # the sample stores a signed integer as a 64-bit pattern
        n = u if kind[0] == 'u' else (u - (1 << w) if u >> (w - 1) else u)
        if n == 0: return encode(0, 0, 0, f), ''
        return round_value(1 if n < 0 else 0, Fraction(abs(n)), f, rmo)
    if op in ('minimum', 'maximum', 'minimum_number', 'maximum_number', 'minimum_magnitude', 'maximum_magnitude',
              'minimum_magnitude_number', 'maximum_magnitude_number'):
        x, y = ks; inv = 'i' if (snan(x) or snan(y)) else ''
        number = op.endswith('_number'); mag = 'magnitude' in op; is_min = op.startswith('minimum')
        if x[0] == 'nan' or y[0] == 'nan':
            if not number or (x[0] == 'nan' and y[0] == 'nan'): return None, inv
            return (args[1] if x[0] == 'nan' else args[0]), inv
        key = lambda k: (abs(val(k)) if k[0] == 'fin' else Fraction(10) ** 400)
        sval = lambda k: (val(k) if k[0] == 'fin' else (-1 if k[1] else 1) * Fraction(10) ** 400)
        if mag and key(x) != key(y):
            pick = x if (key(x) < key(y)) == is_min else y
            return args[0] if pick is x else args[1], inv
        vx, vy = sval(x), sval(y)
        if vx == vy:   # equal value: -0 < +0 (and equal magnitudes of opposite sign by sign)
            if x[1] == y[1]: return args[0], inv
            neg = args[0] if x[1] else args[1]; pos = args[1] if x[1] else args[0]
            return (neg if is_min else pos), inv
        return (args[0] if (vx < vy) == is_min else args[1]), inv
    return 'skip', None

def main(path):
    tally = collections.Counter(); bad = []
    for line in open(path):
        s = json.loads(line)
        f, args = s['F'], [int(a, 16) for a in s['args']]
        try:
            ob, of = oracle(s['id'], s['rm'], f, args)
        except Exception as e:
            tally[(s['id'].split('@')[0], 'oracle-error')] += 1
            if len(bad) < 10: bad.append((s, repr(e)))
            continue
        if ob == 'skip':
            tally[('(not in oracle)', '')] += 1; continue
        if of == 'i?':
            of = None
        for side, b, fl in (('muse', int(s['m'], 16), s['mf']), ('cft', int(s['c'], 16), s['cf'])):
            vok = (ob is None and is_nan(b, f)) or b == ob
            fok = of is None or fl == fl2int(of)
            tally[(s['id'].split('@')[0], f'{side} {"ok" if vok and fok else "VALUE" if not vok else "FLAGS"}')] += 1
            if not (vok and fok) and len(bad) < 30:
                bad.append((s['id'], s['rm'], s['args'], side, hex(b), fl, 'oracle', hex(ob) if isinstance(ob, int) else ob, of))
    tot = sum(v for k, v in tally.items() if k[1].endswith('ok') or 'VALUE' in k[1] or 'FLAGS' in k[1])
    print('checked answers', tot)
    agg = collections.Counter()
    for (op, res), n in tally.items(): agg[res] += n
    for k, n in sorted(agg.items()): print(f'  {n:7d}  {k}')
    for k, n in sorted(tally.items()):
        if not k[1].endswith('ok'): print('  non-ok:', k, n)
    for b in bad: print('  ', b)

if __name__ == '__main__':
    main(sys.argv[1])
