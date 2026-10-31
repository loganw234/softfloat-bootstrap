#!/usr/bin/env python3
"""Exact arbiter for binary16/32/64 basic operations, from first principles.

Each result is computed from the exact rational value (fractions.Fraction; sqrt
by integer square root with a sticky bit) and rounded once, under any of the
five attributes, with tininess detected before or after rounding as asked.
Flags: i=invalid z=divideByZero o=overflow u=underflow x=inexact.
NaN results are returned as None (payload choice is each library's policy).
"""
from fractions import Fraction
from math import isqrt

FMTS = {16: (11, 5), 32: (24, 8), 64: (53, 11)}  # precision p (with hidden bit), exponent bits

class Fmt:
    def __init__(self, f):
        self.p, self.eb = FMTS[f]
        self.w = self.p + self.eb
        self.bias = (1 << (self.eb - 1)) - 1
        self.emin = 1 - self.bias          # exponent of the smallest normal
        self.emax = self.bias
        self.fmask = (1 << (self.p - 1)) - 1
        self.einf = (1 << self.eb) - 1

def decode(bits, f):
    F = Fmt(f)
    s = (bits >> (F.w - 1)) & 1
    e = (bits >> (F.p - 1)) & F.einf
    m = bits & F.fmask
    if e == F.einf:
        if m:
            return ('nan', s, bool(m >> (F.p - 2) & 1))   # (kind, sign, quiet?)
        return ('inf', s)
    if e == 0:
        v = Fraction(m) * Fraction(2) ** (F.emin - (F.p - 1))
    else:
        v = Fraction((1 << (F.p - 1)) | m) * Fraction(2) ** (e - F.bias - (F.p - 1))
    return ('fin', s, v)

def encode(s, e_biased, m, f):
    F = Fmt(f)
    return (s << (F.w - 1)) | (e_biased << (F.p - 1)) | (m & F.fmask)

def ilog2(x):
    """floor(log2(x)) for a positive Fraction."""
    n, d = x.numerator, x.denominator
    e = n.bit_length() - d.bit_length()
    if Fraction(2) ** e > x:
        e -= 1
    return e

def _round_int(mi, rem, rm, s):
    """mi integer, rem in [0,1) Fraction; returns rounded integer magnitude."""
    if rem == 0:
        return mi
    if rm == 'rne':
        return mi + 1 if (rem > Fraction(1, 2) or (rem == Fraction(1, 2) and mi & 1)) else mi
    if rm == 'rna':
        return mi + 1 if rem >= Fraction(1, 2) else mi
    if rm == 'rtz':
        return mi
    if rm == 'rup':
        return mi + 1 if s == 0 else mi
    if rm == 'rdn':
        return mi + 1 if s == 1 else mi
    raise ValueError(rm)

def round_value(s, x, f, rm, tiny='after', sticky=False):
    """Round sign s, magnitude x (Fraction >= 0) to format f. sticky=True means the true
    magnitude is strictly above x by less than any quantum considered (sqrt's remainder)."""
    F = Fmt(f)
    if x == 0 and not sticky:
        return encode(s, 0, 0, f), ''
    e = ilog2(x) if x > 0 else F.emin - F.p - 10
    def rnd(q):
        m = x / Fraction(2) ** q if q >= 0 else x * Fraction(2) ** (-q)
        mi = m.numerator // m.denominator
        rem = m - mi
        if sticky and rem == 0:
            rem = Fraction(1, 1 << 200)  # strictly above, below any half
        elif sticky and rem == Fraction(1, 2):
            rem = Fraction(1, 2) + Fraction(1, 1 << 200)
        return _round_int(mi, rem, rm, s), rem != 0
    # unbounded-exponent rounding, for "tiny after rounding"
    q_unb = e - (F.p - 1)
    r_unb, _ = rnd(q_unb)
    tiny_after = (r_unb * (Fraction(2) ** q_unb if q_unb >= 0 else Fraction(1, 2 ** -q_unb))) < Fraction(2) ** F.emin
    tiny_before = x < Fraction(2) ** F.emin
    q = max(e, F.emin) - (F.p - 1)
    mr, inexact = rnd(q)
    if mr >= (1 << F.p):
        mr >>= 1; q += 1
    flags = ''
    # result exponent
    if mr == 0:
        bits = encode(s, 0, 0, f)
    elif mr < (1 << (F.p - 1)):
        bits = encode(s, 0, mr, f)          # subnormal (q == emin-(p-1))
    else:
        E = q + (F.p - 1)
        if E > F.emax:
            overflow_to_inf = rm in ('rne', 'rna') or (rm == 'rup' and s == 0) or (rm == 'rdn' and s == 1)
            bits = encode(s, F.einf, 0, f) if overflow_to_inf else encode(s, F.einf - 1, F.fmask, f)
            return bits, 'ox'
        bits = encode(s, E + F.bias, mr, f)
    is_tiny = tiny_before if tiny == 'before' else tiny_after
    if inexact:
        if is_tiny:
            flags += 'u'
        flags += 'x'
    return bits, flags

def _qnan_flags(*ops):
    return 'i' if any(o[0] == 'nan' and not o[2] for o in ops) else ''

def compute(op, f, rm, bits_args, tiny='after'):
    """Returns (bits or None for NaN, flags)."""
    a = [decode(b, f) for b in bits_args]
    if any(x[0] == 'nan' for x in a):
        # fma(0, inf, qNaN): invalid is implementation-defined; report 'i?' marker
        if op == 'fma' and a[2][0] == 'nan' and a[2][2] and a[0][0] != 'nan' and a[1][0] != 'nan':
            z = lambda t: t[0] == 'fin' and t[2] == 0
            if (z(a[0]) and a[1][0] == 'inf') or (a[0][0] == 'inf' and z(a[1])):
                return None, 'i?'
        return None, _qnan_flags(*a)
    sgn = lambda t: t[1]
    def val(t):
        return (-1 if t[1] else 1) * t[2]
    if op in ('add', 'sub'):
        x, y = a
        ys = y[1] ^ (1 if op == 'sub' else 0)
        if x[0] == 'inf' or y[0] == 'inf':
            if x[0] == 'inf' and y[0] == 'inf' and x[1] != ys:
                return None, 'i'
            return encode(x[1] if x[0] == 'inf' else ys, Fmt(f).einf, 0, f), ''
        r = val(x) + (-1 if ys else 1) * y[2]
        if r == 0:
            if x[2] == 0 and y[2] == 0 and x[1] == ys:
                return encode(x[1], 0, 0, f), ''
            return encode(1 if rm == 'rdn' else 0, 0, 0, f), ''
        return round_value(1 if r < 0 else 0, abs(r), f, rm, tiny)
    if op == 'mul':
        x, y = a; s = x[1] ^ y[1]
        if x[0] == 'inf' or y[0] == 'inf':
            if (x[0] == 'fin' and x[2] == 0) or (y[0] == 'fin' and y[2] == 0):
                return None, 'i'
            return encode(s, Fmt(f).einf, 0, f), ''
        return round_value(s, x[2] * y[2], f, rm, tiny)
    if op == 'div':
        x, y = a; s = x[1] ^ y[1]
        if x[0] == 'inf':
            if y[0] == 'inf':
                return None, 'i'
            return encode(s, Fmt(f).einf, 0, f), ''
        if y[0] == 'inf':
            return encode(s, 0, 0, f), ''
        if y[2] == 0:
            if x[2] == 0:
                return None, 'i'
            return encode(s, Fmt(f).einf, 0, f), 'z'
        return round_value(s, x[2] / y[2], f, rm, tiny)
    if op == 'sqrt':
        x, = a
        if x[0] == 'inf':
            return (None, 'i') if x[1] else (encode(0, Fmt(f).einf, 0, f), '')
        if x[2] == 0:
            return encode(x[1], 0, 0, f), ''
        if x[1]:
            return None, 'i'
        v = x[2]
        # sqrt(v) with 2p+8 significant bits plus sticky: scale by an even power of two
        k = 2 * (Fmt(f).p + 8) - ilog2(v)
        k += k & 1
        sc = v * Fraction(2) ** k
        n = sc.numerator // sc.denominator
        exact_int = (sc.denominator == 1)
        r = isqrt(n)
        sticky = not (exact_int and r * r == n)
        return round_value(0, Fraction(r) / Fraction(2) ** (k // 2), f, rm, tiny, sticky=sticky)
    if op == 'fma':
        x, y, z = a
        ps = x[1] ^ y[1]
        if x[0] == 'inf' or y[0] == 'inf':
            if (x[0] == 'fin' and x[2] == 0) or (y[0] == 'fin' and y[2] == 0):
                return None, 'i'
            if z[0] == 'inf' and z[1] != ps:
                return None, 'i'
            return encode(ps, Fmt(f).einf, 0, f), ''
        if z[0] == 'inf':
            return encode(z[1], Fmt(f).einf, 0, f), ''
        prod = x[2] * y[2]
        r = (-1 if ps else 1) * prod + val(z)
        if r == 0:
            if prod == 0 and z[2] == 0 and ps == z[1]:
                return encode(ps, 0, 0, f), ''
            return encode(1 if rm == 'rdn' else 0, 0, 0, f), ''
        return round_value(1 if r < 0 else 0, abs(r), f, rm, tiny)
    raise ValueError(op)

if __name__ == '__main__':
    # self-check against the host FPU for binary64/32 RNE on random inputs (Python floats are binary64)
    import random, struct
    rnd = random.Random(7)
    def b2d(b): return struct.unpack('<d', struct.pack('<Q', b))[0]
    def d2b(d): return struct.unpack('<Q', struct.pack('<d', d))[0]
    bad = 0
    for i in range(20000):
        x = rnd.getrandbits(64); y = rnd.getrandbits(64)
        for op, fn in (('add', lambda u, v: u + v), ('mul', lambda u, v: u * v), ('sub', lambda u, v: u - v)):
            try:
                ref = fn(b2d(x), b2d(y))
            except OverflowError:
                continue
            got, fl = compute(op, 64, 'rne', [x, y])
            if ref != ref:
                if got is not None: bad += 1
            elif got != d2b(ref):
                bad += 1
                if bad < 5: print('MISMATCH', op, hex(x), hex(y), hex(got or 0), hex(d2b(ref)))
    import math
    for i in range(5000):
        x = rnd.getrandbits(63)
        ref = math.sqrt(b2d(x)) if b2d(x) == b2d(x) else None
        got, fl = compute('sqrt', 64, 'rne', [x])
        if ref is not None and ref == ref and got != d2b(ref):
            bad += 1
            if bad < 8: print('SQRT MISMATCH', hex(x), hex(got or 0), hex(d2b(ref)))
    print('self-check mismatches vs host FPU (binary64 RNE add/sub/mul/sqrt):', bad)
