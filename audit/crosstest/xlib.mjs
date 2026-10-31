// xlib.mjs - thin adapters over the two prebuilt wasm softfloat modules.
//
//   import { loadMuse, loadCft, MUSE_RM, CFT_RM, FLAG } from "./xlib.mjs";
//
// Everything crosses as BigInt raw encodings (binary32 uses the low 32 bits) and comes back as
// { bits: BigInt, flags: number } (flags use the SAME bit layout on both sides).
// Nothing here computes: every value is a bit pattern one of the libraries produced.
import { readFileSync } from "node:fs";
import { fileURLToPath, pathToFileURL } from "node:url";
import { dirname, join, resolve } from "node:path";

// setup.sh exports both trees from git objects (MUSE_REV, CFT_REV) under AUDIT_WORK (default: dist/audit/).
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");
export const WORK = process.env.AUDIT_WORK ?? join(ROOT, "dist", "audit");
export const MUSE_TREE = join(WORK, "muse"), CFT_TREE = join(WORK, "cft");
export const MUSE_SITE = join(MUSE_TREE, "site");
const { loadModule } = await import(pathToFileURL(join(CFT_TREE, "bindings", "node", "lib.mjs")).href);

// Canonical rounding names used by the harness. The two libraries number them differently:
//   RNE=0/0  RTZ=1/1  RUP(+inf)= muse 2 / cft 3  RDN(-inf)= muse 3 / cft 2  RMM(ties away)=4/4
export const RM_NAMES = ["RNE", "RTZ", "RUP", "RDN", "RMM"];
export const MUSE_RM = { RNE: 0, RTZ: 1, RUP: 2, RDN: 3, RMM: 4 };
export const CFT_RM = { RNE: 0, RTZ: 1, RDN: 2, RUP: 3, RMM: 4 };
export const FLAG = { INVALID: 1, DIVZERO: 2, OVERFLOW: 4, UNDERFLOW: 8, INEXACT: 16 };
export const flagStr = (f) =>
  f ? [[1, "invalid"], [2, "divByZero"], [4, "overflow"], [8, "underflow"], [16, "inexact"]]
        .filter(([b]) => f & b).map(([, n]) => n).join("|") : "-";

export const FP = { 32: { code: 0, size: 4 }, 64: { code: 1, size: 8 } };
// cft_op numbers (host/include/cft.h). ADD/SUB read operands a and c; MUL reads a and b; FMA reads a,b,c.
export const OPC = { FMA: 0, ADD: 1, SUB: 2, MUL: 3, ABS: 4, NEG: 5, COPYSIGN: 6, MIN: 7, MAX: 8,
                     MINNUM: 9, MAXNUM: 10, SELECT: 11, CMPLT: 12, CMPLE: 13, CMPEQ: 14 };

// ------------------------------------------------------------------ muse
export async function loadMuse(dir = MUSE_SITE) {
  const ops = JSON.parse(readFileSync(`${dir}/ops.json`, "utf8"));
  const byName = new Map(ops.map((o) => [o.name, o]));
  const ex = (await WebAssembly.instantiate(readFileSync(`${dir}/msf.wasm`), {})).instance.exports;
  if (ex.msf_op_count() !== ops.length) throw new Error("ops.json does not match msf.wasm");
  const mask = (w) => (w >= 64 ? (1n << 64n) - 1n : (1n << BigInt(w)) - 1n);
  return {
    ex, ops, byName,
    has: (name) => byName.has(name) && byName.get(name).runnable,
    // rm: 0..4 (msf_rounding_t), or -1 for operations without an attribute. Result is masked to the
    // operation's declared result width (signed int results arrive sign-extended otherwise).
    run(name, rm, args = []) {
      const op = byName.get(name);
      if (!op) throw new Error(`no such muse op ${name}`);
      if (!op.runnable) throw new Error(`muse op ${name} is not runnable through msf.wasm`);
      const w = [];
      for (let k = 0; k < 3; k++) {
        const b = BigInt.asUintN(64, args[k] ?? 0n);
        w.push(Number(b & 0xffffffffn), Number(b >> 32n));
      }
      ex.msf_run(op.i, rm, ...w);
      const bits = (BigInt(ex.msf_result_hi() >>> 0) << 32n) | BigInt(ex.msf_result_lo() >>> 0);
      return { bits: bits & mask(op.retw), flags: ex.msf_result_flags() >>> 0, op };
    },
  };
}

// ------------------------------------------------------------------ cft
export async function loadCft() {
  const { M, C } = await loadModule();
  const pDev = M._malloc(4);
  const st0 = C.openSoftware(pDev);
  if (st0 !== 0) throw new Error(`cft_open(software): ${C.strerror(st0)}`);
  const dev = M.HEAPU32[pDev >> 2];
  const S = {};
  for (const k of ["a", "b", "c", "d", "e"]) S[k] = M._malloc(32);
  S.f = M._malloc(4); S.i = M._malloc(8); S.cls = M._malloc(4);
  const put = (p, bits, size) => { const u = M.HEAPU8; for (let i = 0; i < size; i++) u[p + i] = Number((bits >> BigInt(8 * i)) & 0xffn); };
  const get = (p, size) => { const u = M.HEAPU8; let v = 0n; for (let i = size - 1; i >= 0; i--) v = (v << 8n) | BigInt(u[p + i]); return v; };
  const chk = (st, what) => { if (st !== 0) throw new Error(`${what}: status ${st} ${C.strerror(st)} ${C.lastError()}`); };
  const sz = (F) => FP[F].size, fc = (F) => FP[F].code;
  const flags = () => M.HEAPU32[S.f >> 2] >>> 0;
  const clr = () => { M.HEAPU32[S.f >> 2] = 0; };
  const R = (n) => CFT_RM[n];
  const X = {
    M, C, dev, FP,
    // opcode group via cft_run: d = op(a,b,c). NOTE add/sub use (a,c); mul uses (a,b).
    run(F, opc, rm, a, b = 0n, c = 0n) {
      put(S.a, a, sz(F)); put(S.b, b, sz(F)); put(S.c, c, sz(F)); clr();
      chk(C.run(dev, opc, fc(F), R(rm), S.a, S.b, S.c, S.d, 1, S.f, 0), "cft_run");
      return { bits: get(S.d, sz(F)), flags: flags() };
    },
    div(F, rm, a, b) { put(S.a, a, sz(F)); put(S.b, b, sz(F)); clr(); chk(C.div(dev, fc(F), R(rm), S.a, S.b, S.d, 1, S.f, 0), "cft_div"); return { bits: get(S.d, sz(F)), flags: flags() }; },
    sqrt(F, rm, a) { put(S.a, a, sz(F)); clr(); chk(C.sqrt(dev, fc(F), R(rm), S.a, S.d, 1, S.f, 0), "cft_sqrt"); return { bits: get(S.d, sz(F)), flags: flags() }; },
    rem(F, a, b) { put(S.a, a, sz(F)); put(S.b, b, sz(F)); clr(); chk(C.rem(dev, fc(F), S.a, S.b, S.d, 1, S.f), "cft_rem"); return { bits: get(S.d, sz(F)), flags: flags() }; },
    rint(F, rm, exact, a) { put(S.a, a, sz(F)); clr(); chk(C.rint(dev, fc(F), R(rm), exact ? 1 : 0, S.a, S.d, 1, S.f, 0), "cft_rint"); return { bits: get(S.d, sz(F)), flags: flags() }; },
    scaleb(F, rm, a, n) {
      const u = BigInt.asUintN(64, n);
      put(S.a, a, sz(F)); clr();
      chk(C.scaleb(dev, fc(F), R(rm), S.a, Number(u & 0xffffffffn), Number(BigInt.asIntN(32, u >> 32n)), S.d, 1, S.f, 0), "cft_scaleb");
      return { bits: get(S.d, sz(F)), flags: flags() };
    },
    unary(F, which /* logb|nextUp|nextDown */, a) { put(S.a, a, sz(F)); clr(); chk(C[which](dev, fc(F), S.a, S.d, 1, S.f), `cft_${which}`); return { bits: get(S.d, sz(F)), flags: flags() }; },
    convert(sF, dF, rm, a) { put(S.a, a, sz(sF)); clr(); chk(C.convert(dev, fc(sF), fc(dF), R(rm), S.a, S.d, 1, S.f), "cft_convert"); return { bits: get(S.d, sz(dF)), flags: flags() }; },
    fromInt(F, rm, kind /* i32|u32|i64|u64 */, n) {
      const w = kind.endsWith("32") ? 4 : 8;
      put(S.i, BigInt.asUintN(64, n), w); clr();
      chk(C[{ i32: "cvtFromI32", u32: "cvtFromU32", i64: "cvtFromI64", u64: "cvtFromU64" }[kind]](dev, fc(F), R(rm), S.i, S.d, 1, S.f), "cft_cvt_from");
      return { bits: get(S.d, sz(F)), flags: flags() };
    },
    toInt(F, rm, exact, kind, a) {
      const w = kind.endsWith("32") ? 4 : 8;
      put(S.a, a, sz(F)); clr();
      chk(C[{ i32: "cvtToI32", u32: "cvtToU32", i64: "cvtToI64", u64: "cvtToU64" }[kind]](dev, fc(F), R(rm), exact ? 1 : 0, S.a, S.i, 1, S.f), "cft_cvt_to");
      return { bits: get(S.i, w), flags: flags() };            // raw two's-complement bits of the integer
    },
    cmpSig(F, opc, a, b) { put(S.a, a, sz(F)); put(S.b, b, sz(F)); clr(); chk(C.cmpSig(dev, opc, fc(F), S.a, S.b, S.d, 1, S.f, 0), "cft_cmp_sig"); return { bits: get(S.d, sz(F)), flags: flags() }; },
    cls(F, a) { put(S.a, a, sz(F)); chk(C.classOf(dev, fc(F), S.a, S.cls, 1), "cft_class"); return M.HEAPU8[S.cls]; },
    totalOrder(F, a, b, mag = false) { put(S.a, a, sz(F)); put(S.b, b, sz(F)); chk((mag ? C.totalOrderMag : C.totalOrder)(dev, fc(F), S.a, S.b, S.d, 1), "cft_total_order"); return get(S.d, sz(F)); },
    minmaxMag(F, which /* minMag|maxMag|minnumMag|maxnumMag */, a, b) { put(S.a, a, sz(F)); put(S.b, b, sz(F)); clr(); chk(C[which](dev, fc(F), S.a, S.b, S.d, 1, S.f), `cft_${which}`); return { bits: get(S.d, sz(F)), flags: flags() }; },
    math1(F, fn, rm, a) { put(S.a, a, sz(F)); clr(); chk(C[fn](dev, fc(F), R(rm), S.a, S.d, 1, S.f), `cft_${fn}`); return { bits: get(S.d, sz(F)), flags: flags() }; },
    math2(F, fn, rm, a, b) { put(S.a, a, sz(F)); put(S.b, b, sz(F)); clr(); chk(C[fn](dev, fc(F), R(rm), S.a, S.b, S.d, 1, S.f), `cft_${fn}`); return { bits: get(S.d, sz(F)), flags: flags() }; },
    // formatOf: operands in sF, result in dF, ONE rounding. fn: add|sub|mul|div|sqrt|fma
    formatOf(fn, sF, dF, rm, a, b = 0n, c = 0n) {
      const name = { add: "formatOfAdd", sub: "formatOfSub", mul: "formatOfMul", div: "formatOfDiv", sqrt: "formatOfSqrt", fma: "formatOfFma" }[fn];
      put(S.a, a, sz(sF)); put(S.b, b, sz(sF)); put(S.c, c, sz(sF)); clr();
      let st;
      if (fn === "sqrt") st = C[name](dev, fc(sF), fc(dF), R(rm), S.a, S.d, 1, S.f, 0);
      else if (fn === "fma") st = C[name](dev, fc(sF), fc(dF), R(rm), S.a, S.b, S.c, S.d, 1, S.f, 0);
      else st = C[name](dev, fc(sF), fc(dF), R(rm), S.a, S.b, S.d, 1, S.f, 0);
      chk(st, `cft_${name}`);
      return { bits: get(S.d, sz(dF)), flags: flags() };
    },
    payload(F, which /* getPayload|setPayload|setPayloadSignaling */, a) { put(S.a, a, sz(F)); chk(C[which](dev, fc(F), S.a, S.d, 1), `cft_${which}`); return { bits: get(S.d, sz(F)), flags: 0 }; },
    // device-level sticky status word (7.1 / 5.7.4)
    stickyFlags: () => C.saveAllFlags(dev) >>> 0,
    lowerFlags: (mask = 0x1f) => C.lowerFlags(dev, mask),
    raiseFlags: (mask) => C.raiseFlags(dev, mask),
  };
  return X;
}
