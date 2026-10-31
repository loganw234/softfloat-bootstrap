#!/usr/bin/env python3
"""Correctly rounded arbiter for exp2, exp2m1, log2, log2p1, sinPi, cosPi, rSqrt, hypot
at binary16/32/64, all five attributes, flags per IEEE 754-2019 9.2 / 9.2.1.

rSqrt and hypot are exact (integer square root of an exact rational, oracle.round_value
with sticky). The others: exact cases decided first; otherwise a Ziv loop with MPFR
(gmpy2) at rising precision, rounding both ends of the error interval exactly and
accepting only when result bits and flags agree.
"""
import os, sys
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gmpy2
from gmpy2 import mpfr
from oracle import decode, encode, Fmt, round_value, compute as basic_compute

def _nan_in(*xs):
    return any(x[0] == 'nan' for x in xs)

def _snan_in(*xs):
    return any(x[0] == 'nan' and not x[2] for x in xs)

def _inf(s, f):
    return encode(s, Fmt(f).einf, 0, f)

def _zero(s, f):
    return encode(s, 0, 0, f)

def _exact(s, v, f, rm, tiny):
    return round_value(s, v, f, rm, tiny)   # v an exact Fraction >= 0

def _sqrt_rational(v, f, rm, tiny):
    """Round sqrt(v) for a positive Fraction v."""
    from math import isqrt
    from oracle import ilog2
    k = 2 * (Fmt(f).p + 8) - ilog2(v)
    k += k & 1
    sc = v * Fraction(2) ** k if k >= 0 else v / Fraction(2) ** (-k)
    n = sc.numerator // sc.denominator
    exact_int = (sc.numerator % sc.denominator == 0)
    r = isqrt(n)
    sticky = not (exact_int and r * r == n)
    q = Fraction(r) / Fraction(2) ** (k // 2) if k >= 0 else Fraction(r) * Fraction(2) ** (-k // 2)
    return round_value(0, q, f, rm, tiny, sticky=sticky)

def _to_frac(m):
    n, d = m.as_integer_ratio()
    return Fraction(int(n), int(d))

def _ziv(fn, f, rm, tiny, sign_hint=None):
    """fn(prec) -> mpfr approximation with relative error <= 2^-(prec-8). Returns (bits, flags)."""
    for P in (160, 320, 640, 1280, 2560, 5120):
        with gmpy2.context(gmpy2.context(precision=P + 32, emin=-(1 << 40), emax=(1 << 40))):
            v = fn(P + 32)
        if gmpy2.is_zero(v) or gmpy2.is_nan(v) or gmpy2.is_infinite(v):
            raise ArithmeticError('degenerate approximation: exact case missed?')
        s = 1 if v < 0 else 0
        a = abs(_to_frac(v))
        eps = Fraction(1, 1 << (P - 8))
        lo, hi = a * (1 - eps), a * (1 + eps)
        r1, r2 = round_value(s, lo, f, rm, tiny), round_value(s, hi, f, rm, tiny)
        if r1 == r2:
            bits, fl = r1
            if 'x' not in fl:
                fl += 'x'          # not an exact case, so inexact (round_value saw a non-boundary)
            return bits, fl
    raise ArithmeticError('Ziv loop did not converge')

def _is_int(x):
    return x.denominator == 1

def _pow2_exponent(v):
    """k if v == 2^k exactly, else None (v > 0 Fraction)."""
    n, d = v.numerator, v.denominator
    if n & (n - 1) == 0 and d & (d - 1) == 0:
        return (n.bit_length() - 1) - (d.bit_length() - 1)
    return None

def _reduce_pi(x):
    """For exact Fraction x, return (r, sign) with sin(pi*x) = sign*sin(pi*r), r in [0, 1/2]."""
    r = x % 2                      # [0, 2)
    sign = 1
    if r >= 1:
        r -= 1; sign = -sign       # sin(pi(r+1)) = -sin(pi r)
    if r > Fraction(1, 2):
        r = 1 - r                  # sin(pi(1-r)) = sin(pi r)
    return r, sign

def _sin_pi_reduced(r, prec):
    """sin(pi r) for r in (0, 1/2], well conditioned: use cos(pi(1/2-r)) above 1/4."""
    pi = gmpy2.const_pi(prec + 16)
    if r <= Fraction(1, 4):
        return gmpy2.sin(pi * mpfr(r.numerator, prec + 16) / r.denominator)
    t = Fraction(1, 2) - r
    return gmpy2.cos(pi * mpfr(t.numerator, prec + 16) / t.denominator)

def compute(op, f, rm, bits_args, tiny='after'):
    if op in ('add', 'sub', 'mul', 'div', 'sqrt', 'fma'):
        return basic_compute(op, f, rm, bits_args, tiny)
    a = [decode(b, f) for b in bits_args]
    if op == 'hypot':
        x, y = a
        if _snan_in(x, y):
            return None, 'i'
        if x[0] == 'inf' or y[0] == 'inf':
            return _inf(0, f), ''
        if _nan_in(x, y):
            return None, ''
        v = x[2] * x[2] + y[2] * y[2]
        if v == 0:
            return _zero(0, f), ''
        return _sqrt_rational(v, f, rm, tiny)
    x, = a
    if x[0] == 'nan':
        return None, 'i' if not x[2] else ''
    s = x[1]
    if op == 'rSqrt':
        if x[0] == 'inf':
            return (None, 'i') if s else (_zero(0, f), '')
        if x[2] == 0:
            return _inf(s, f), 'z'
        if s:
            return None, 'i'
        return _sqrt_rational(1 / x[2], f, rm, tiny)
    if op == 'exp2':
        if x[0] == 'inf':
            return (_zero(0, f), '') if s else (_inf(0, f), '')
        v = -x[2] if s else x[2]
        if v == 0:
            return round_value(0, Fraction(1), f, rm, tiny)
        if _is_int(v):
            n = int(v)
            if n > 5000:
                return round_value(0, Fraction(2) ** 5000, f, rm, tiny)
            if n < -5000:
                return round_value(0, Fraction(1, 1 << 5000), f, rm, tiny)
            return round_value(0, Fraction(2) ** n, f, rm, tiny)
        if v > 5000:
            return round_value(0, Fraction(2) ** 5000, f, rm, tiny)
        if v < -5000:
            return round_value(0, Fraction(1, 1 << 5000), f, rm, tiny)   # tiny, inexact
        return _ziv(lambda P: gmpy2.exp2(mpfr(v.numerator, P) / v.denominator), f, rm, tiny)
    if op == 'exp2m1':
        if x[0] == 'inf':
            return (round_value(1, Fraction(1), f, rm, tiny)) if s else (_inf(0, f), '')
        v = -x[2] if s else x[2]
        if v == 0:
            return _zero(s, f), ''
        if _is_int(v) and -5000 < v < 5000:
            r = Fraction(2) ** int(v) - 1
            return round_value(1 if r < 0 else 0, abs(r), f, rm, tiny)
        if v > 5000:
            return round_value(0, Fraction(2) ** 5000, f, rm, tiny)
        if v < -5000:
            # -1 + 2^v, |2^v| below any rounding granule of -1: decided by Ziv with a tiny offset
            return round_value(1, 1 - Fraction(1, 1 << 5000), f, rm, tiny)
        def fn(P):
            y = mpfr(v.numerator, P) / v.denominator * gmpy2.const_log2(P)
            return gmpy2.expm1(y)
        return _ziv(fn, f, rm, tiny)
    if op == 'log2':
        if x[0] == 'inf':
            return (None, 'i') if s else (_inf(0, f), '')
        if x[2] == 0:
            return _inf(1, f), 'z'
        if s:
            return None, 'i'
        k = _pow2_exponent(x[2])
        if k is not None:
            return (_zero(0, f), '') if k == 0 else round_value(1 if k < 0 else 0, Fraction(abs(k)), f, rm, tiny)
        v = x[2]
        return _ziv(lambda P: gmpy2.log2(mpfr(v.numerator, P) / v.denominator), f, rm, tiny)
    if op == 'log2p1':
        if x[0] == 'inf':
            return (None, 'i') if s else (_inf(0, f), '')
        v = -x[2] if s else x[2]
        if v == 0:
            return _zero(s, f), ''
        if v < -1:
            return None, 'i'
        if v == -1:
            return _inf(1, f), 'z'
        k = _pow2_exponent(1 + v)
        if k is not None:
            return (_zero(0, f), '') if k == 0 else round_value(1 if k < 0 else 0, Fraction(abs(k)), f, rm, tiny)
        def fn(P):
            return gmpy2.log1p(mpfr(v.numerator, 2 * P + 2200) / v.denominator) / gmpy2.const_log2(P)
        return _ziv(fn, f, rm, tiny)
    if op in ('sinPi', 'cosPi'):
        if x[0] == 'inf':
            return None, 'i'
        v = -x[2] if s else x[2]
        if op == 'sinPi':
            if v == 0:
                return _zero(s, f), ''
            r, sg = _reduce_pi(v)
            if r == 0:
                return _zero(s, f), ''            # sinPi(+n)=+0, sinPi(-n)=-0
            if r == Fraction(1, 2):
                return round_value(0 if sg > 0 else 1, Fraction(1), f, rm, tiny)
            res_sign = 0 if sg > 0 else 1
            return _ziv(lambda P: (1 if res_sign == 0 else -1) * _sin_pi_reduced(r, P), f, rm, tiny)
        # cosPi(x) = sinPi(x + 1/2), with the 754 sign rules for its zeros and ones
        w = abs(v) + Fraction(1, 2)
        r, sg = _reduce_pi(w)
        if r == 0:
            return _zero(0, f), ''                 # cosPi(n + 1/2) = +0
        if r == Fraction(1, 2):
            return round_value(0 if sg > 0 else 1, Fraction(1), f, rm, tiny)
        res_sign = 0 if sg > 0 else 1
        return _ziv(lambda P: (1 if res_sign == 0 else -1) * _sin_pi_reduced(r, P), f, rm, tiny)
    raise ValueError(op)

if __name__ == '__main__':
    # self-check against the host libm on binary64 RNE where it is known correctly rounded (exp2/log2 at
    # simple points), plus exact-case spot checks; the cross-test is where this earns its keep.
    import struct
    d2b = lambda d: struct.unpack('<Q', struct.pack('<d', d))[0]
    b2d = lambda b: struct.unpack('<d', struct.pack('<Q', b))[0]
    checks = [('exp2', [d2b(3.0)], d2b(8.0), ''), ('exp2', [d2b(0.5)], d2b(2 ** 0.5), 'x'),
              ('log2', [d2b(1024.0)], d2b(10.0), ''), ('log2p1', [d2b(-0.75)], d2b(-2.0), ''),
              ('sinPi', [d2b(0.5)], d2b(1.0), ''), ('sinPi', [d2b(-3.0)], d2b(-0.0), ''),
              ('cosPi', [d2b(1.5)], d2b(0.0), ''), ('cosPi', [d2b(1.0)], d2b(-1.0), ''),
              ('sinPi', [d2b(1 / 6)], d2b(0.49999999999999994), 'x'), ('rSqrt', [d2b(4.0)], d2b(0.5), ''),
              ('rSqrt', [d2b(-0.0)], d2b(float('-inf')), 'z'), ('hypot', [d2b(3.0), d2b(4.0)], d2b(5.0), ''),
              ('exp2m1', [d2b(-2.0)], d2b(-0.75), ''), ('exp2', [d2b(-1075.0)], 0, 'ux'),
              ('exp2', [d2b(1024.0)], d2b(float('inf')), 'ox')]
    bad = 0
    for op, args, want, wfl in checks:
        got, fl = compute(op, 64, 'rne', args)
        ok = got == want and fl == wfl
        bad += not ok
        print('ok ' if ok else 'BAD', op, b2d(args[0]), '->', b2d(got) if got is not None else None, fl)
    import math, random
    rnd = random.Random(3); n = 0
    for i in range(3000):
        xv = rnd.uniform(-30, 30)
        got, fl = compute('exp2', 64, 'rne', [d2b(xv)])
        ref = 2.0 ** xv          # glibc's exp2/pow are correctly rounded in practice for these
        if got != d2b(ref) and abs(b2d(got) - ref) > 0:
            n += 1
    print('exp2 vs host pow, 3000 random in [-30,30]: ulp-level disagreements', n, '(host pow is not guaranteed CR)')
    print('exact spot checks bad:', bad)
