// opsmap.mjs - the operation table, executable. One descriptor per (operation, format):
//   id, F (result/format label), srcF (operand format), argKinds, rm (takes an attribute?),
//   kind ('f' bits | 'b' bool | 'i' int | 'cls' | 'num'), m(rm,args) -> {v,flags}, c(rm,args) -> {v,flags}
// m = muse.msf_run side, c = cft.cftw_* side.  Both return a comparable value v (BigInt, or number for 'num').
import { MUSE_RM, OPC } from "./xlib.mjs";
import { toNumber, isNaNBits, signBit, maskOf, geom } from "./corpus.mjs";

const DIRS = [["ties_to_even", "RNE"], ["ties_to_away", "RMM"], ["toward_zero", "RTZ"], ["toward_positive", "RUP"], ["toward_negative", "RDN"]];

export function buildOps(mu, cf) {
  const ops = [];
  const add = (o) => ops.push(o);
  const mrun = (name, rm, args) => { const r = mu.run(name, rm === null ? -1 : MUSE_RM[rm], args); return { v: r.bits, flags: r.flags }; };
  const cv = (r) => ({ v: r.bits, flags: r.flags });

  for (const F of [32, 64]) {
    const p = `msf${F}_`;
    const g = geom(F);
    // ---- 5.4.1 basic arithmetic
    add({ id: `add@${F}`, F, srcF: F, argKinds: ["f", "f"], rm: true, kind: "f", mname: p + "add",
          m: (rm, a) => mrun(p + "add", rm, a), c: (rm, a) => cv(cf.run(F, OPC.ADD, rm, a[0], 0n, a[1])) });
    add({ id: `sub@${F}`, F, srcF: F, argKinds: ["f", "f"], rm: true, kind: "f", mname: p + "sub",
          m: (rm, a) => mrun(p + "sub", rm, a), c: (rm, a) => cv(cf.run(F, OPC.SUB, rm, a[0], 0n, a[1])) });
    add({ id: `mul@${F}`, F, srcF: F, argKinds: ["f", "f"], rm: true, kind: "f", mname: p + "mul",
          m: (rm, a) => mrun(p + "mul", rm, a), c: (rm, a) => cv(cf.run(F, OPC.MUL, rm, a[0], a[1], 0n)) });
    add({ id: `div@${F}`, F, srcF: F, argKinds: ["f", "f"], rm: true, kind: "f", mname: p + "div",
          m: (rm, a) => mrun(p + "div", rm, a), c: (rm, a) => cv(cf.div(F, rm, a[0], a[1])) });
    add({ id: `sqrt@${F}`, F, srcF: F, argKinds: ["f"], rm: true, kind: "f", mname: p + "sqrt",
          m: (rm, a) => mrun(p + "sqrt", rm, a), c: (rm, a) => cv(cf.sqrt(F, rm, a[0])) });
    add({ id: `fma@${F}`, F, srcF: F, argKinds: ["f", "f", "f"], rm: true, kind: "f", mname: p + "fma",
          m: (rm, a) => mrun(p + "fma", rm, a), c: (rm, a) => cv(cf.run(F, OPC.FMA, rm, a[0], a[1], a[2])) });
    // ---- 5.3.1
    add({ id: `remainder@${F}`, F, srcF: F, argKinds: ["f", "f"], rm: false, kind: "f", mname: p + "remainder",
          m: (rm, a) => mrun(p + "remainder", null, a), c: (rm, a) => cv(cf.rem(F, a[0], a[1])) });
    for (const [d, r] of DIRS)
      add({ id: `roundToIntegral_${r}@${F}`, F, srcF: F, argKinds: ["f"], rm: false, kind: "f", mname: `${p}round_to_integral_${d}`,
            m: (_rm, a) => mrun(`${p}round_to_integral_${d}`, null, a), c: (_rm, a) => cv(cf.rint(F, r, false, a[0])) });
    add({ id: `roundToIntegralExact@${F}`, F, srcF: F, argKinds: ["f"], rm: true, kind: "f", mname: p + "round_to_integral_exact",
          m: (rm, a) => mrun(p + "round_to_integral_exact", rm, a), c: (rm, a) => cv(cf.rint(F, rm, true, a[0])) });
    add({ id: `nextUp@${F}`, F, srcF: F, argKinds: ["f"], rm: false, kind: "f", mname: p + "next_up",
          m: (rm, a) => mrun(p + "next_up", null, a), c: (rm, a) => cv(cf.unary(F, "nextUp", a[0])) });
    add({ id: `nextDown@${F}`, F, srcF: F, argKinds: ["f"], rm: false, kind: "f", mname: p + "next_down",
          m: (rm, a) => mrun(p + "next_down", null, a), c: (rm, a) => cv(cf.unary(F, "nextDown", a[0])) });
    // ---- 5.3.3 scaleB (muse: n is a binary64 ENCODING of an integral value; cft: int64 passed as two i32 halves)
    add({ id: `scaleB@${F}`, F, srcF: F, argKinds: ["f", "n"], rm: true, kind: "f", mname: p + "scale_b",
          m: (rm, a) => { const nb = fnum64(Number(a[1])); return mrun(p + "scale_b", rm, [a[0], nb]); },
          c: (rm, a) => cv(cf.scaleb(F, rm, a[0], a[1])) });
    // logB: muse returns a BINARY64 encoding for both formats; cft returns the operand's own format. Compare as numbers.
    add({ id: `logB@${F}`, F, srcF: F, argKinds: ["f"], rm: false, kind: "num", mname: p + "log_b",
          m: (rm, a) => { const r = mu.run(p + "log_b", -1, a); return { v: toNumber(64, r.bits), flags: r.flags }; },
          c: (rm, a) => { const r = cf.unary(F, "logb", a[0]); return { v: toNumber(F, r.bits), flags: r.flags }; } });
    // ---- sign / copy class
    add({ id: `abs@${F}`, F, srcF: F, argKinds: ["f"], rm: false, kind: "f", mname: p + "abs",
          m: (rm, a) => mrun(p + "abs", null, a), c: (rm, a) => cv(cf.run(F, OPC.ABS, "RNE", a[0])) });
    add({ id: `negate@${F}`, F, srcF: F, argKinds: ["f"], rm: false, kind: "f", mname: p + "negate",
          m: (rm, a) => mrun(p + "negate", null, a), c: (rm, a) => cv(cf.run(F, OPC.NEG, "RNE", a[0])) });
    add({ id: `copySign@${F}`, F, srcF: F, argKinds: ["f", "f"], rm: false, kind: "f", mname: p + "copy_sign",
          m: (rm, a) => mrun(p + "copy_sign", null, a), c: (rm, a) => cv(cf.run(F, OPC.COPYSIGN, "RNE", a[0], a[1])) });
    // ---- 9.6 min/max
    for (const [mn, opc] of [["minimum", OPC.MIN], ["maximum", OPC.MAX], ["minimum_number", OPC.MINNUM], ["maximum_number", OPC.MAXNUM]])
      add({ id: `${mn}@${F}`, F, srcF: F, argKinds: ["f", "f"], rm: false, kind: "f", mname: p + mn,
            m: (rm, a) => mrun(p + mn, null, a), c: (rm, a) => cv(cf.run(F, opc, "RNE", a[0], a[1])) });
    for (const [mn, which] of [["minimum_magnitude", "minMag"], ["maximum_magnitude", "maxMag"], ["minimum_magnitude_number", "minnumMag"], ["maximum_magnitude_number", "maxnumMag"]])
      add({ id: `${mn}@${F}`, F, srcF: F, argKinds: ["f", "f"], rm: false, kind: "f", mname: p + mn,
            m: (rm, a) => mrun(p + mn, null, a), c: (rm, a) => cv(cf.minmaxMag(F, which, a[0], a[1])) });
    // ---- 9.7 payloads
    for (const [mn, which] of [["get_payload", "getPayload"], ["set_payload", "setPayload"], ["set_payload_signaling", "setPayloadSignaling"]])
      add({ id: `${mn}@${F}`, F, srcF: F, argKinds: ["f"], rm: false, kind: "f", mname: p + mn,
            m: (rm, a) => mrun(p + mn, null, a), c: (rm, a) => cv(cf.payload(F, which, a[0])) });
    // ---- 9.2 functions both provide
    for (const [mn, fn, ar] of [["sin_pi", "sinpi", 1], ["cos_pi", "cospi", 1], ["r_sqrt", "rsqrt", 1], ["hypot", "hypot", 2],
                                ["exp2", "exp2", 1], ["exp2m1", "exp2m1", 1], ["log2", "log2", 1], ["log2p1", "log2p1", 1]])
      add({ id: `${mn}@${F}`, F, srcF: F, argKinds: ar === 1 ? ["f"] : ["f", "f"], rm: true, kind: "f", mname: p + mn, slow: true,
            m: (rm, a) => mrun(p + mn, rm, a),
            c: (rm, a) => cv(ar === 1 ? cf.math1(F, fn, rm, a[0]) : cf.math2(F, fn, rm, a[0], a[1])) });
    // ---- 5.7.2 classification
    add({ id: `class@${F}`, F, srcF: F, argKinds: ["f"], rm: false, kind: "cls", mname: p + "class",
          m: (rm, a) => mrun(p + "class", null, a), c: (rm, a) => ({ v: BigInt((cf.cls(F, a[0]) + 2) % 10), flags: 0 }) });
    const sets = { is_normal: [1, 6], is_finite: [1, 2, 3, 4, 5, 6], is_zero: [3, 4], is_subnormal: [2, 5], is_infinite: [0, 7], is_nan: [8, 9], is_signaling: [8] };
    for (const [mn, set] of Object.entries(sets))
      add({ id: `${mn}@${F}`, F, srcF: F, argKinds: ["f"], rm: false, kind: "b", mname: p + mn,
            m: (rm, a) => mrun(p + mn, null, a), c: (rm, a) => ({ v: set.includes(cf.cls(F, a[0])) ? 1n : 0n, flags: 0 }) });
    add({ id: `is_sign_minus@${F}`, F, srcF: F, argKinds: ["f"], rm: false, kind: "b", mname: p + "is_sign_minus",
          m: (rm, a) => mrun(p + "is_sign_minus", null, a), c: (rm, a) => ({ v: (a[0] & signBit(F)) ? 1n : 0n, flags: 0 }) });
    add({ id: `is_canonical@${F}`, F, srcF: F, argKinds: ["f"], rm: false, kind: "b", mname: p + "is_canonical",
          m: (rm, a) => mrun(p + "is_canonical", null, a), c: () => ({ v: 1n, flags: 0 }) });
    add({ id: `radix@${F}`, F, srcF: F, argKinds: ["f"], rm: false, kind: "b", mname: p + "radix",
          m: (rm, a) => mrun(p + "radix", null, a), c: () => ({ v: 2n, flags: 0 }) });
    // ---- 5.10 totalOrder
    add({ id: `totalOrder@${F}`, F, srcF: F, argKinds: ["f", "f"], rm: false, kind: "b", mname: p + "total_order",
          m: (rm, a) => mrun(p + "total_order", null, a), c: (rm, a) => ({ v: cf.totalOrder(F, a[0], a[1]) !== 0n ? 1n : 0n, flags: 0 }) });
    add({ id: `totalOrderMag@${F}`, F, srcF: F, argKinds: ["f", "f"], rm: false, kind: "b", mname: p + "total_order_mag",
          m: (rm, a) => mrun(p + "total_order_mag", null, a), c: (rm, a) => ({ v: cf.totalOrder(F, a[0], a[1], true) !== 0n ? 1n : 0n, flags: 0 }) });
    // ---- 5.6.1 / 5.11 comparisons (cft has only lt/le/eq; the rest are exact compositions)
    const PRED = makePred(cf, F);
    for (const [kindName, sig] of [["quiet", false], ["signaling", true]])
      for (const [pn, fnc] of Object.entries(PRED)) {
        if (sig && (pn === "unordered" || pn === "ordered")) continue;      // no compareSignalingUnordered/Ordered in muse's table
        add({ id: `compare_${kindName}_${pn}@${F}`, F, srcF: F, argKinds: ["f", "f"], rm: false, kind: "b", mname: `${p}compare_${kindName}_${pn}`,
              m: (rm, a) => mrun(`${p}compare_${kindName}_${pn}`, null, a), c: (rm, a) => fnc(sig, a[0], a[1]) });
        // mixed-format compare (muse: msf32_compare_*_f64 = binary32 vs binary64): widen the binary32 side exactly, compare in binary64
        const fm = F === 32 ? [32, 64] : [64, 32], PRED64 = makePred(cf, 64);
        add({ id: `compare_${kindName}_${pn}_mixed${fm[0]}_${fm[1]}`, F: 64, srcF: 64, argFmts: fm, argKinds: ["f", "f"], rm: false, kind: "b", mname: `${p}compare_${kindName}_${pn}_f${F === 32 ? 64 : 32}`,
              m: (rm, a) => mrun(`${p}compare_${kindName}_${pn}_f${F === 32 ? 64 : 32}`, null, a),
              c: (rm, a) => { const w = fm.map((X, i) => (X === 64 ? { bits: a[i], flags: 0 } : cf.convert(X, 64, "RNE", a[i])));
                              const r = PRED64[pn](sig, w[0].bits, w[1].bits); return { v: r.v, flags: r.flags | w[0].flags | w[1].flags }; } });
      }
    // ---- integer conversions (muse also has 8/16-bit; cft has 32/64 only)
    for (const kind of ["i32", "u32", "i64", "u64"]) {
      add({ id: `from_${kind}@${F}`, F, srcF: F, argKinds: [kind], rm: true, kind: "f", mname: `${p}from_${kind}`,
            m: (rm, a) => mrun(`${p}from_${kind}`, rm, a), c: (rm, a) => cv(cf.fromInt(F, rm, kind, a[0])) });
      const w = kind.endsWith("32") ? 32 : 64;
      for (const [d, r] of DIRS) for (const ex of [false, true])
        add({ id: `to_${kind}${ex ? "_exact" : ""}_${r}@${F}`, F, srcF: F, argKinds: ["f"], rm: false, kind: "i", w, mname: `${p}to_${kind}_${ex ? "exact_" : ""}${d}`,
              m: (rm, a) => mrun(`${p}to_${kind}_${ex ? "exact_" : ""}${d}`, null, a),
              c: (rm, a) => { const x = cf.toInt(F, r, ex, kind, a[0]); return { v: x.bits & maskOf(w), flags: x.flags }; } });
    }
  }
  // ---- 5.4.2 convertFormat
  for (const [sF, dF] of [[64, 32], [32, 64], [32, 32], [64, 64]])
    add({ id: `convertFormat_${sF}_to_${dF}`, F: dF, srcF: sF, argKinds: ["f"], rm: true, kind: "f", mname: `msf${dF}_from_f${sF}`,
          m: (rm, a) => mrun(`msf${dF}_from_f${sF}`, rm, a), c: (rm, a) => cv(cf.convert(sF, dF, rm, a[0])) });
  // ---- 5.4.1 formatOf (all operands in ONE source format; cft's sfmt/dfmt) - the muse names with equal operand formats
  for (const [sF, dF] of [[64, 32], [32, 64]]) {
    const q = `msf${dF}_`;
    for (const fn of ["add", "sub", "mul", "div"])
      add({ id: `formatOf_${fn}_${sF}_to_${dF}`, F: dF, srcF: sF, argKinds: ["f", "f"], rm: true, kind: "f", mname: `${q}${fn}_f${sF}_f${sF}`,
            m: (rm, a) => mrun(`${q}${fn}_f${sF}_f${sF}`, rm, a), c: (rm, a) => cv(cf.formatOf(fn, sF, dF, rm, a[0], a[1])) });
    add({ id: `formatOf_sqrt_${sF}_to_${dF}`, F: dF, srcF: sF, argKinds: ["f"], rm: true, kind: "f", mname: `${q}sqrt_f${sF}`,
          m: (rm, a) => mrun(`${q}sqrt_f${sF}`, rm, a), c: (rm, a) => cv(cf.formatOf("sqrt", sF, dF, rm, a[0])) });
    add({ id: `formatOf_fma_${sF}_to_${dF}`, F: dF, srcF: sF, argKinds: ["f", "f", "f"], rm: true, kind: "f", mname: `${q}fma_f${sF}_f${sF}_f${sF}`,
          m: (rm, a) => mrun(`${q}fma_f${sF}_f${sF}_f${sF}`, rm, a), c: (rm, a) => cv(cf.formatOf("fma", sF, dF, rm, a[0], a[1], a[2])) });
  }
  // ---- formatOf with operands of DIFFERENT formats (muse has these natively, e.g. msf32_add_f32_f64).
  // cft's formatOf takes ONE source format for all operands: widen the narrower operand to binary64 with
  // cftw_convert (exact, silent) and then call formatOf(64 -> D).  Same single rounding, same flags.
  // widening is exact and silent EXCEPT for a signaling NaN (quieted, invalid raised): keep that flag.
  const widenF = (X, a) => (X === 64 ? { bits: a, flags: 0 } : cf.convert(X, 64, "RNE", a));
  const mixed = (fn, D, fm, rm, a) => {
    const w = fm.map((X, i) => widenF(X, a[i]));
    const r = cf.formatOf(fn, 64, D, rm, w[0].bits, w[1].bits, w[2]?.bits ?? 0n);
    return { v: r.bits, flags: r.flags | w.reduce((p, x) => p | x.flags, 0) };
  };
  for (const D of [32, 64]) {
    for (const [X, Y] of [[32, 64], [64, 32]])
      for (const fn of ["add", "sub", "mul", "div"])
        add({ id: `formatOfMixed_${fn}_${X}_${Y}_to_${D}`, F: D, srcF: 64, argFmts: [X, Y], argKinds: ["f", "f"], rm: true, kind: "f", mname: `msf${D}_${fn}_f${X}_f${Y}`,
              m: (rm, a) => mrun(`msf${D}_${fn}_f${X}_f${Y}`, rm, a), c: (rm, a) => mixed(fn, D, [X, Y], rm, a) });
    for (const fm of [[32, 32, 64], [32, 64, 32], [64, 32, 32], [32, 64, 64], [64, 32, 64], [64, 64, 32]])
      add({ id: `formatOfMixed_fma_${fm.join("_")}_to_${D}`, F: D, srcF: 64, argFmts: fm, argKinds: ["f", "f", "f"], rm: true, kind: "f", mname: `msf${D}_fma_f${fm.join("_f")}`,
            m: (rm, a) => mrun(`msf${D}_fma_f${fm.join("_f")}`, rm, a), c: (rm, a) => mixed("fma", D, fm, rm, a) });
  }
  return ops;
}

function fnum64(x) {                 // the binary64 ENCODING of a JS number (muse's scaleB takes n as one)
  const d = new DataView(new ArrayBuffer(8)); d.setFloat64(0, x); return d.getBigUint64(0);
}

// Quiet / signaling comparison predicates built from cft's three primitives (CMPLT, CMPLE, CMPEQ; the signaling
// forms via cft_cmp_sig).  Every muse predicate is an exact composition, flags included.
function makePred(cf, F) {
  const lt = (sig, a, b) => (sig ? cf.cmpSig(F, OPC.CMPLT, a, b) : cf.run(F, OPC.CMPLT, "RNE", a, b));
  const le = (sig, a, b) => (sig ? cf.cmpSig(F, OPC.CMPLE, a, b) : cf.run(F, OPC.CMPLE, "RNE", a, b));
  const eq = (sig, a, b) => (sig ? cf.cmpSig(F, OPC.CMPEQ, a, b) : cf.run(F, OPC.CMPEQ, "RNE", a, b));
  const T = (r) => r.bits !== 0n;                                      // cft predicates are 1.0 or +0.0
  const B = (t, f) => ({ v: t ? 1n : 0n, flags: f });
  return {
    equal: (s, a, b) => { const r = eq(s, a, b); return B(T(r), r.flags); },
    not_equal: (s, a, b) => { const r = eq(s, a, b); return B(!T(r), r.flags); },
    less: (s, a, b) => { const r = lt(s, a, b); return B(T(r), r.flags); },
    less_equal: (s, a, b) => { const r = le(s, a, b); return B(T(r), r.flags); },
    greater: (s, a, b) => { const r = lt(s, b, a); return B(T(r), r.flags); },
    greater_equal: (s, a, b) => { const r = le(s, b, a); return B(T(r), r.flags); },
    not_greater: (s, a, b) => { const r = lt(s, b, a); return B(!T(r), r.flags); },
    not_less: (s, a, b) => { const r = lt(s, a, b); return B(!T(r), r.flags); },
    less_unordered: (s, a, b) => { const r = le(s, b, a); return B(!T(r), r.flags); },       // a<b or unordered == !(b<=a)
    greater_unordered: (s, a, b) => { const r = le(s, a, b); return B(!T(r), r.flags); },    // a>b or unordered == !(a<=b)
    unordered: (s, a, b) => { const r1 = le(s, a, b), r2 = le(s, b, a); return B(!T(r1) && !T(r2), r1.flags | r2.flags); },
    ordered: (s, a, b) => { const r1 = le(s, a, b), r2 = le(s, b, a); return B(T(r1) || T(r2), r1.flags | r2.flags); },
  };
}
