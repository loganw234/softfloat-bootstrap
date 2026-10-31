// TestFloat-style operand generator for binary32 / binary64, as BigInt bit patterns.
// Deterministic (xoshiro128** seeded), weighted toward the cases that break softfloats:
// specials, subnormals, exponent extremes, runs of ones/zeros, near-ties, cancellation.

export const FMT = {
  32: { w: 32, p: 24, eb: 8, bias: 127n },
  64: { w: 64, p: 53, eb: 11, bias: 1023n },
};

export class Rng {
  constructor(seed) {
    let x = BigInt.asUintN(64, BigInt(seed) * 0x9e3779b97f4a7c15n + 0x632be59bd9b4e019n);
    this.s = new Uint32Array(4);
    for (let i = 0; i < 4; i++) {   // splitmix64 to seed
      x = BigInt.asUintN(64, x + 0x9e3779b97f4a7c15n);
      let z = x;
      z = BigInt.asUintN(64, (z ^ (z >> 30n)) * 0xbf58476d1ce4e5b9n);
      z = BigInt.asUintN(64, (z ^ (z >> 27n)) * 0x94d049bb133111ebn);
      this.s[i] = Number(BigInt.asUintN(32, z ^ (z >> 31n)));
    }
  }
  u32() {
    const s = this.s, r = Math.imul(rotl(Math.imul(s[1], 5), 7), 9) >>> 0, t = s[1] << 9;
    s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3]; s[2] ^= t; s[3] = rotl(s[3], 11);
    return r;
  }
  below(n) { return this.u32() % n; }
  bits(k) {   // k random bits as BigInt
    let r = 0n;
    for (let i = 0; i < k; i += 32) r = (r << 32n) | BigInt(this.u32());
    return BigInt.asUintN(k, r);
  }
}
function rotl(x, k) { return ((x << k) | (x >>> (32 - k))) >>> 0; }

const ones = (k) => (1n << BigInt(k)) - 1n;

export function pack(f, s, e, m) {
  const F = FMT[f];
  return (BigInt(s) << BigInt(F.w - 1)) | (BigInt(e) << BigInt(F.p - 1)) | (m & ones(F.p - 1));
}
export function fields(f, x) {
  const F = FMT[f];
  return { s: Number(x >> BigInt(F.w - 1)), e: Number((x >> BigInt(F.p - 1)) & ones(F.eb)), m: x & ones(F.p - 1) };
}
export function isNaN_(f, x) { const F = FMT[f], q = fields(f, x); return q.e === (1 << F.eb) - 1 && q.m !== 0n; }

export function specials(f) {
  const F = FMT[f], E = (1 << F.eb) - 1, fb = F.p - 1, out = [];
  for (const s of [0, 1]) {
    out.push(pack(f, s, 0, 0n), pack(f, s, 0, 1n), pack(f, s, 0, ones(fb)), pack(f, s, 0, 1n << BigInt(fb - 1)),
             pack(f, s, 1, 0n), pack(f, s, 1, 1n), pack(f, s, Number(F.bias), 0n), pack(f, s, Number(F.bias), 1n),
             pack(f, s, Number(F.bias) - 1, ones(fb)), pack(f, s, E - 1, ones(fb)), pack(f, s, E - 1, 0n),
             pack(f, s, E, 0n), pack(f, s, E, 1n << BigInt(fb - 1)), pack(f, s, E, 1n),
             pack(f, s, E, (1n << BigInt(fb - 1)) | 0x5an), pack(f, s, Number(F.bias) + F.p, 0n),
             pack(f, s, Number(F.bias) + F.p - 1, ones(fb)), pack(f, s, Number(F.bias) + 1, 1n << BigInt(fb - 1)));
  }
  return out;
}

function significand(r, fb) {
  switch (r.below(6)) {
    case 0: return r.bits(fb);
    case 1: { // a run of ones somewhere, zeros elsewhere
      const a = r.below(fb), b = r.below(fb); const lo = Math.min(a, b), hi = Math.max(a, b);
      return ones(hi - lo + 1) << BigInt(lo);
    }
    case 2: { // run of zeros in a field of ones
      const a = r.below(fb), b = r.below(fb); const lo = Math.min(a, b), hi = Math.max(a, b);
      return ones(fb) ^ (ones(hi - lo + 1) << BigInt(lo));
    }
    case 3: return BigInt(r.below(4)) << BigInt(r.below(fb));            // few bits
    case 4: return ones(fb) ^ (BigInt(1 + r.below(3)) << BigInt(r.below(fb - 1))); // all but few
    default: return r.bits(fb) & (r.below(2) ? ones(fb) << BigInt(r.below(fb)) : ones(r.below(fb) + 1));
  }
}

function exponent(r, f) {
  const F = FMT[f], E = (1 << F.eb) - 1, bias = Number(F.bias);
  switch (r.below(10)) {
    case 0: return 0;                                   // subnormal / zero
    case 1: return 1 + r.below(F.p + 2);                // just above subnormal
    case 2: return E - 1 - r.below(F.p + 2);            // near overflow
    case 3: return r.below(50) ? E - 1 : E;             // max exponent (rarely inf/NaN)
    case 4: case 5: return bias - F.p - 2 + r.below(2 * F.p + 5); // around 1
    default: return r.below(E);                         // anywhere finite
  }
}

export function operand(r, f) {
  if (r.below(40) === 0) { const sp = specials(f); return sp[r.below(sp.length)]; }
  const F = FMT[f];
  return pack(f, r.below(2), exponent(r, f), significand(r, F.p - 1));
}

// b related to a: same or nearby exponent, for cancellation and alignment edges
export function related(r, f, a) {
  const F = FMT[f], q = fields(f, a), E = (1 << F.eb) - 1;
  if (q.e === E) return operand(r, f);
  const d = [0, 1, -1, 2, -2, F.p - 1, F.p, F.p + 1, -(F.p), F.p + 2, -(F.p + 2)][r.below(11)];
  let e = Math.max(0, Math.min(E - 1, q.e + d));
  let m = r.below(2) ? q.m ^ (1n << BigInt(r.below(F.p - 1))) : significand(r, F.p - 1);
  return pack(f, r.below(2), e, m);
}

export function operands(r, f, arity, op) {
  const a = operand(r, f);
  if (arity === 1) return [a];
  const b = r.below(3) === 0 ? related(r, f, a) : operand(r, f);
  if (arity === 2) return [a, b];
  // fma: often choose c near -(a*b) by exponent, to hit massive cancellation
  let c = operand(r, f);
  if (r.below(3) === 0) {
    const F = FMT[f], qa = fields(f, a), qb = fields(f, b), E = (1 << F.eb) - 1;
    const e = qa.e + qb.e - Number(F.bias) + (r.below(5) - 2);
    if (qa.e && qb.e && qa.e < E && qb.e < E && e > 0 && e < E)
      c = pack(f, fields(f, a).s ^ fields(f, b).s ^ 1, e, significand(r, F.p - 1));
  }
  return [a, b, c];
}
