#!/usr/bin/env python3
"""Each documented-policy class native_replay.py reports, checked to be what it claims, case by case.

  1. decimal input of more than H = 20 significant digits: every case where the libraries differ is muse's
     documented two-step rule (msf_string.c's header: round the digit string to H digits under the attribute,
     inexact iff a nonzero digit was dropped, then convert, underflow from that pack alone), bits and flags,
     and cft's answer is the exact value correctly rounded
  2. decimal output: every case where the values differ asks for more than 20 digits; muse's is the correctly
     rounded 20 digits and zeros after them, cft's is correctly rounded to every digit asked for
  3. augmented pairs: every flag difference is muse 0x00 against cft 0x08 (underflow), on equal results whose
     tail is exact, nonzero and subnormal
  4. cft's refusals in its own corpus are exactly the records marked "refuse"
  5. no string muse accepts whole is refused by cft
Exit 1 if any check fails.
"""
import os, sys, collections
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'crosstest'))
from native_replay import build_requests, run, dec_value, sig_digits
from oracle import round_value, decode

RM = {'RNE': 'rne', 'RTZ': 'rtz', 'RUP': 'rup', 'RDN': 'rdn', 'RMM': 'rna'}
FLAG = {'i': 1, 'z': 2, 'o': 4, 'u': 8, 'x': 16}

def round_dec(v, n, mode):
    """v > 0 to n significant decimal digits: mode rne, rna, rtz, or up (away from zero). (value, dropped?)"""
    e = 0
    while v >= Fraction(10) ** (e + 1): e += 1
    while v < Fraction(10) ** e: e -= 1
    q = v / Fraction(10) ** (e - n + 1)
    i = q.numerator // q.denominator
    rem = q - i
    up = {'rne': rem > Fraction(1, 2) or (rem == Fraction(1, 2) and i % 2 == 1), 'rna': rem >= Fraction(1, 2),
          'rtz': False, 'up': rem > 0}[mode]
    return Fraction(i + (1 if up else 0)) * Fraction(10) ** (e - n + 1), rem != 0

def magnitude_mode(rm, negative):
    return {'RNE': 'rne', 'RMM': 'rna', 'RTZ': 'rtz', 'RUP': 'rtz' if negative else 'up', 'RDN': 'up' if negative else 'rtz'}[rm]

def subnormal_nonzero(t, F):
    m = 23 if F == 32 else 52
    return (t >> m) & ((1 << (31 - m if F == 32 else 63 - m)) - 1) == 0 and t & ((1 << m) - 1) != 0

reqs = build_requests()
out = run(reqs)
res = collections.Counter()
for (q, m), line in zip(reqs, out):
    _, mp, cp = line.split(' | ')
    mt, ct = mp.split()[1:], cp.split()[1:]
    F, fam, src = m['F'], m['fam'], m['src']
    if fam == 'from_decimal' and int(ct[0]) == 0:
        s = m['s']; n = sig_digits(s)
        mb, mf, cb, cf = int(mt[0], 16), int(mt[1], 16), int(ct[1], 16), int(ct[2], 16)
        if n is not None and n > 20 and (mb, mf) != (cb, cf):
            rm = q.split()[2]
            v = dec_value(s); sg = 1 if v < 0 else 0
            v20, dropped = round_dec(abs(v), 20, magnitude_mode(rm, sg))
            b, f2 = round_value(sg, v20, F, RM[rm], 'after')
            muse_rule = (b, sum(FLAG[c] for c in f2) | (16 if dropped else 0)) == (mb, mf)
            eb, ef = round_value(sg, abs(v), F, RM[rm], 'after')
            cft_exact = (eb, sum(FLAG[c] for c in ef)) == (cb, cf)
            res[f'1. >20-digit input, differing: muse follows its two-step rule {muse_rule}, cft exact {cft_exact}'] += 1
    if fam == 'to_decimal':
        mo, co = mt[0], ct[1]
        if dec_value(mo) != dec_value(co):
            dg, rm, a = int(q.split()[4]), q.split()[2], int(q.split()[3], 16)
            k = decode(a, F); x = (-1 if k[1] else 1) * k[2]
            mode = magnitude_mode(rm, x < 0)
            sign = -1 if x < 0 else 1
            muse20 = dec_value(mo) == sign * round_dec(abs(x), 20, mode)[0]
            cft_cr = dec_value(co) == sign * round_dec(abs(x), dg, mode)[0]
            res[f'2. decimal output, differing: asked > 20 digits {dg > 20}; muse = 20 correct digits then zeros {muse20}; cft correct to every digit {cft_cr}'] += 1
    if fam == 'augmented':
        mh, mtl, mf = int(mt[0], 16), int(mt[1], 16), int(mt[2], 16)
        cr, ce, cf = int(ct[1], 16), int(ct[2], 16), int(ct[3], 16)
        if (mh, mtl) == (cr, ce) and mf != cf:
            res[f'3. augmented flag difference: muse 0x{mf:02x} cft 0x{cf:02x}, tail exact nonzero subnormal {subnormal_nonzero(mtl, F)}'] += 1
    if src == 'cft' and fam in ('from_decimal', 'from_hex'):
        res[f"4. cft's own corpus: record {'refuses' if m['exp'] is None else 'accepts'}, cft {'refused' if int(ct[0]) else 'accepted'}"] += 1
    if src == 'muse' and fam in ('from_decimal', 'from_hex') and int(ct[0]) and m['C'] == len(m['s']):
        res['5. a string muse accepts whole that cft refuses'] += 1

bad = 0
for k, n in sorted(res.items()):
    ok = not ('False' in k or k.startswith('5.') or 'muse 0x00 cft 0x08' not in k and k.startswith('3.')
              or ('refuses, cft accepted' in k or 'accepts, cft refused' in k))
    bad += 0 if ok else n
    print(f"{n:7d}  {k}{'' if ok else '   <-- NOT AS CLAIMED'}")
if not any(k.startswith('5.') for k in res):
    print('      0  5. a string muse accepts whole that cft refuses')
print('every class is what it claims' if not bad else f'{bad} cases are not what their class claims')
sys.exit(1 if bad else 0)
