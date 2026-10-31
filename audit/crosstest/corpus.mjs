// corpus.mjs - operand pools for the differential run (deterministic: xorshift32, fixed seed).
const GEOM = { 32: { e: 8, m: 23 }, 64: { e: 11, m: 52 } };
const dv = new DataView(new ArrayBuffer(8));

export const geom = (F) => GEOM[F];
export const signBit = (F) => 1n << BigInt(F - 1);
export const maskOf = (F) => (1n << BigInt(F)) - 1n;
export function pack(F, sign, exp, man) {
  const g = GEOM[F];
  return (BigInt(sign) << BigInt(F - 1)) | (BigInt(exp) << BigInt(g.m)) | BigInt(man);
}
export function isNaNBits(F, v) {
  const g = GEOM[F];
  const e = (v >> BigInt(g.m)) & ((1n << BigInt(g.e)) - 1n), man = v & ((1n << BigInt(g.m)) - 1n);
  return e === (1n << BigInt(g.e)) - 1n && man !== 0n;
}
export function toNumber(F, v) {
  if (F === 32) { dv.setUint32(0, Number(v & 0xffffffffn)); return dv.getFloat32(0); }
  dv.setBigUint64(0, v & maskOf(64)); return dv.getFloat64(0);
}
export function fromNumber(F, x) {
  if (F === 32) { dv.setFloat32(0, x); return BigInt(dv.getUint32(0)); }
  dv.setFloat64(0, x); return dv.getBigUint64(0);
}

class Rng {
  constructor(seed) { this.s = seed >>> 0 || 1; }
  u32() { let x = this.s; x ^= x << 13; x >>>= 0; x ^= x >>> 17; x ^= x << 5; x >>>= 0; this.s = x; return x; }
  u64() { return (BigInt(this.u32()) << 32n) | BigInt(this.u32()); }
  below(n) { return this.u32() % n; }
  bits(F) { return F === 32 ? BigInt(this.u32()) : this.u64(); }
}
export { Rng };

export function specialPool(F) {
  const g = GEOM[F], bias = (1 << (g.e - 1)) - 1, emax = (1 << g.e) - 1, mall = (1n << BigInt(g.m)) - 1n;
  const qbit = 1n << BigInt(g.m - 1);
  const set = new Set();
  for (const s of [0, 1]) {
    const P = (e, m) => set.add(pack(F, s, e, m));
    P(0, 0); P(0, 1); P(0, 2); P(0, mall); P(0, mall - 1n); P(0, qbit);             // zero + subnormals
    P(1, 0); P(1, 1); P(2, 0);                                                      // smallest normals
    P(bias, 0); P(bias, 1); P(bias - 1, mall); P(bias, qbit);                        // 1, 1+ulp, 1-ulp, 1.5
    P(bias + 1, 0); P(bias + 1, qbit); P(bias - 1, 0); P(bias - 1, qbit);           // 2, 3, 0.5, 0.75
    P(bias + 2, qbit >> 1n); P(bias + 2, qbit); P(bias + 2, 0);                      // 2.5? 6, 4
    P(emax - 1, mall); P(emax - 1, mall - 1n); P(emax - 1, 0); P(emax - 2, mall);   // large finite
    P(emax, 0);                                                                     // infinity
    P(emax, qbit); P(emax, qbit | 5n); P(emax, mall);                               // quiet NaNs (default, payload, all-ones)
    P(emax, 1n); P(emax, qbit >> 1n); P(emax, 5n);                                  // signaling NaNs
  }
  const nums = [0.1, 1 / 3, Math.PI, 10, 100, 1e10, 1e-10, 255.5, 256, 65535.5, 65536, 0.3, 7, 1000.25, 123456.789,
    2.5, 3.5, 4.5, 5.5, -2.5, 8388608, 8388609, 16777216, 16777217, 2147483520, 2147483648, 4294967296,
    4503599627370496, 9007199254740992, 9223372036854775808, 18446744073709551616];
  for (const x of nums) { set.add(fromNumber(F, x)); set.add(fromNumber(F, -x)); }
  if (F === 64) for (const x of [2147483647, 2147483647.5, 4294967295, 4294967295.5, 9223372036854774784, 1e300, 1e-300, 5e-324, 2.2250738585072014e-308])
    { set.add(fromNumber(64, x)); set.add(fromNumber(64, -x)); }
  return [...set];
}

export function randomPool(F, n, seed) {
  const g = GEOM[F], bias = (1 << (g.e - 1)) - 1, emax = (1 << g.e) - 1;
  const r = new Rng(seed), out = [];
  const man = () => r.bits(F) & ((1n << BigInt(g.m)) - 1n);
  for (let i = 0; i < n; i++) {
    const s = r.below(2);
    switch (i % 7) {
      case 0: out.push(r.bits(F)); break;                                              // anything (NaN/inf occasionally)
      case 1: out.push(pack(F, s, bias - 8 + r.below(17), man())); break;               // near 1
      case 2: out.push(pack(F, s, 0, man())); break;                                    // subnormal
      case 3: out.push(pack(F, s, emax - 3 + r.below(3), man())); break;                // near overflow
      case 4: out.push(pack(F, s, 1 + r.below(emax - 1), man() >> BigInt(r.below(g.m)) << BigInt(r.below(g.m)) & ((1n << BigInt(g.m)) - 1n))); break; // sparse mantissa
      case 5: out.push(pack(F, s, 1 + r.below(10), man())); break;                      // near underflow
      default: out.push(pack(F, s, 1 + r.below(emax - 1), man())); break;               // any finite normal
    }
  }
  return out;
}

export const INT_SPECIALS = {
  i32: [0n, 1n, -1n, 2n, 127n, 128n, -128n, -129n, 255n, 256n, 32767n, -32768n, 65535n, 65536n, 16777215n, 16777216n, 16777217n, -16777217n,
        16777219n, 123456789n, -123456789n, 2147483647n, -2147483648n, 2147483646n, -2147483647n],
  u32: [0n, 1n, 2n, 255n, 256n, 65535n, 65536n, 16777216n, 16777217n, 16777219n, 123456789n, 2147483647n, 2147483648n, 4294967295n, 4294967294n, 3000000000n],
  i64: [0n, 1n, -1n, 16777217n, 9007199254740992n, 9007199254740993n, -9007199254740993n, 9007199254740995n, 4611686018427387904n,
        9223372036854775807n, -9223372036854775808n, 9223372036854775806n, -9223372036854775807n, 123456789012345678n, 4294967296n, -4294967296n, 2147483648n, -2147483649n],
  u64: [0n, 1n, 16777217n, 9007199254740993n, 9007199254740995n, 9223372036854775807n, 9223372036854775808n, 18446744073709551615n, 18446744073709551614n, 12345678901234567890n, 4294967296n],
};
export function intPool(kind, n, seed) {
  const w = kind.endsWith("32") ? 32 : 64, signed = kind[0] === "i";
  const r = new Rng(seed), out = [...INT_SPECIALS[kind]];
  for (let i = 0; i < n; i++) {
    let v = w === 32 ? BigInt(r.u32()) : r.u64();
    v >>= BigInt(r.below(w));                                   // vary the magnitude
    if (signed) { v = BigInt.asIntN(w, v); if (r.below(2)) v = -v; if (v < -(1n << BigInt(w - 1))) v = -(1n << BigInt(w - 1)); if (v >= (1n << BigInt(w - 1))) v = (1n << BigInt(w - 1)) - 1n; }
    out.push(v);
  }
  return out;
}
export const SCALE_N = [0n, 1n, -1n, 2n, -2n, 3n, 7n, -7n, 23n, 24n, 25n, 52n, 53n, 100n, -100n, 126n, 127n, 128n, -126n, -127n, -128n, -149n, -150n, -151n,
  1022n, 1023n, 1024n, -1022n, -1023n, -1074n, -1075n, -1076n, 2000n, -2000n, 9999n, -9999n, 10000n, -10000n, 2147483647n, -2147483648n, 1099511627776n, -1099511627776n,
  9007199254740991n, -9007199254740991n];
