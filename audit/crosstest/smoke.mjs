// smoke.mjs - load BOTH prebuilt wasm softfloats in Node 22 and run the same ops on each.
//   node smoke.mjs
// muse : value-passing   msf_run(idx, rm, a_lo,a_hi, b_lo,b_hi, c_lo,c_hi) + msf_result_* getters
// cft  : linear-memory   cftw_* exports over malloc'ed buffers, loaded through the repo's own lib.mjs
import { readFileSync } from "node:fs";
import { fileURLToPath, pathToFileURL } from "node:url";
import { dirname, join, resolve } from "node:path";

// both modules come from the trees setup.sh exports under AUDIT_WORK (default: dist/audit/)
const WORK = process.env.AUDIT_WORK ?? join(resolve(dirname(fileURLToPath(import.meta.url)), "..", ".."), "dist", "audit");
const { loadModule } = await import(pathToFileURL(join(WORK, "cft", "bindings", "node", "lib.mjs")).href);
const MUSE = join(WORK, "muse", "site");

// ---- rounding: the two libraries number the directed modes DIFFERENTLY -------------
//   canonical    muse(rm)                cft(rnd)
//   RNE          0 TIES_TO_EVEN          0 RNE
//   RTZ          1 TOWARD_ZERO           1 RTZ
//   RUP (+inf)   2 TOWARD_POSITIVE       3 RUP
//   RDN (-inf)   3 TOWARD_NEGATIVE       2 RDN
//   RMM (away)   4 TIES_TO_AWAY          4 RMM
const MUSE_RM = { RNE: 0, RTZ: 1, RUP: 2, RDN: 3, RMM: 4 };
const CFT_RM  = { RNE: 0, RTZ: 1, RUP: 3, RDN: 2, RMM: 4 };
// flags use the SAME bits on both sides
const FLAG_NAMES = [[1, "invalid"], [2, "divByZero"], [4, "overflow"], [8, "underflow"], [16, "inexact"]];
const flagStr = (f) => (f ? FLAG_NAMES.filter(([b]) => f & b).map(([, n]) => n).join("|") : "-");

// ---------------------------------------------------------------- muse
const opsJson = JSON.parse(readFileSync(`${MUSE}/ops.json`, "utf8"));
const opIdx = new Map(opsJson.map((o) => [o.name, o.i]));
const mx = (await WebAssembly.instantiate(readFileSync(`${MUSE}/msf.wasm`), {})).instance.exports; // NO imports
if (mx.msf_op_count() !== opsJson.length) throw new Error("ops.json does not match msf.wasm");
function museRun(name, rm, ...bits) {                       // bits: BigInt raw encodings (binary32 => low 32 bits)
  const w = [];
  for (let k = 0; k < 3; k++) { const b = BigInt.asUintN(64, bits[k] ?? 0n); w.push(Number(b & 0xffffffffn), Number(b >> 32n)); }
  mx.msf_run(opIdx.get(name), rm, ...w);                    // rm: 0..4, or -1 for ops with no attribute
  if (!mx.msf_result_ok()) throw new Error(`${name} is not runnable in msf.wasm`);
  return { bits: (BigInt(mx.msf_result_hi() >>> 0) << 32n) | BigInt(mx.msf_result_lo() >>> 0), flags: mx.msf_result_flags() };
}

// ---------------------------------------------------------------- cft
const { M, C } = await loadModule();                         // cft_node.js supplies the 10 env/wasi imports
const pDev = M._malloc(4);
if (C.openSoftware(pDev) !== 0) throw new Error("cft_open(software) failed");
const dev = M.HEAPU32[pDev >> 2];
const FP = { 32: { code: 0, size: 4 }, 64: { code: 1, size: 8 } };
const OP = { FMA: 0, ADD: 1, SUB: 2, MUL: 3 };               // cft_op numbers (ADD/SUB read a and c; MUL reads a and b)
const scratch = { a: M._malloc(32), b: M._malloc(32), c: M._malloc(32), d: M._malloc(32), f: M._malloc(4) };
function put(p, bits, size) { const u = M.HEAPU8; for (let i = 0; i < size; i++) u[p + i] = Number((bits >> BigInt(8 * i)) & 0xffn); }
function get(p, size) { const u = M.HEAPU8; let v = 0n; for (let i = size - 1; i >= 0; i--) v = (v << 8n) | BigInt(u[p + i]); return v; }
function cftCall(F, invoke) {                                 // invoke(pa,pb,pc,pd,pf) -> status
  M.HEAPU32[scratch.f >> 2] = 0;
  const st = invoke(scratch.a, scratch.b, scratch.c, scratch.d, scratch.f);
  if (st !== 0) throw new Error(`cft status ${st}: ${C.strerror(st)} ${C.lastError()}`);
  return { bits: get(scratch.d, FP[F].size), flags: M.HEAPU32[scratch.f >> 2] >>> 0 };
}
const cft = {
  // opcode ops: a + c, a - c, a * b, a*b + c   (b ignored by ADD/SUB, c ignored by MUL)
  run(F, op, rm, a, b, c) { put(scratch.a, a, FP[F].size); put(scratch.b, b ?? 0n, FP[F].size); put(scratch.c, c ?? 0n, FP[F].size);
    return cftCall(F, (pa, pb, pc, pd, pf) => C.run(dev, op, FP[F].code, CFT_RM[rm], pa, pb, pc, pd, 1, pf, 0)); },
  div(F, rm, a, b) { put(scratch.a, a, FP[F].size); put(scratch.b, b, FP[F].size);
    return cftCall(F, (pa, pb, pc, pd, pf) => C.div(dev, FP[F].code, CFT_RM[rm], pa, pb, pd, 1, pf, 0)); },
  sqrt(F, rm, a) { put(scratch.a, a, FP[F].size);
    return cftCall(F, (pa, pb, pc, pd, pf) => C.sqrt(dev, FP[F].code, CFT_RM[rm], pa, pd, 1, pf, 0)); },
};

// ---------------------------------------------------------------- bit helpers
const dv = new DataView(new ArrayBuffer(8));
const f32bits = (x) => { dv.setFloat32(0, x); return BigInt(dv.getUint32(0)); };
const f64bits = (x) => { dv.setFloat64(0, x); return dv.getBigUint64(0); };
const hex = (v, F) => "0x" + v.toString(16).padStart(F / 4, "0");
const asNum = (v, F) => { if (F === 32) { dv.setUint32(0, Number(v)); return dv.getFloat32(0); } dv.setBigUint64(0, v); return dv.getFloat64(0); };

function row(label, F, m, c) {
  const same = m.bits === c.bits && m.flags === c.flags ? "SAME" : "DIFF";
  console.log(`${label.padEnd(20)} muse ${hex(m.bits, F)} [${flagStr(m.flags).padEnd(9)}]  cft ${hex(c.bits, F)} [${flagStr(c.flags).padEnd(9)}]  ${same}  (${asNum(m.bits, F)})`);
}

for (const F of [32, 64]) {
  const enc = F === 32 ? f32bits : f64bits;
  const [one, two, three] = [enc(1), enc(2), enc(3)];
  console.log(`\n== binary${F} ==`);
  row("1 + 2  RNE", F, museRun(`msf${F}_add`, MUSE_RM.RNE, one, two), cft.run(F, OP.ADD, "RNE", one, null, two));
  row("1 / 3  RNE", F, museRun(`msf${F}_div`, MUSE_RM.RNE, one, three), cft.div(F, "RNE", one, three));
  row("1 / 3  RTZ", F, museRun(`msf${F}_div`, MUSE_RM.RTZ, one, three), cft.div(F, "RTZ", one, three));
  row("1 / 3  RUP(+inf)", F, museRun(`msf${F}_div`, MUSE_RM.RUP, one, three), cft.div(F, "RUP", one, three));
  row("1 / 3  RDN(-inf)", F, museRun(`msf${F}_div`, MUSE_RM.RDN, one, three), cft.div(F, "RDN", one, three));
  row("1 / 3  RMM(away)", F, museRun(`msf${F}_div`, MUSE_RM.RMM, one, three), cft.div(F, "RMM", one, three));
  // the rounding-number trap, shown: same NUMBER on both sides, different directed meaning
  const trapM = museRun(`msf${F}_div`, 2, one, three), trapC = cft.div(F, "RUP", one, three); // muse 2 = +inf
  const wrongC = (() => { M.HEAPU32[scratch.f >> 2] = 0; put(scratch.a, one, FP[F].size); put(scratch.b, three, FP[F].size);
    C.div(dev, FP[F].code, 2 /* cft 2 = RDN */, scratch.a, scratch.b, scratch.d, 1, scratch.f, 0); return get(scratch.d, FP[F].size); })();
  console.log(`  trap: rounding number 2 => muse +inf ${hex(trapM.bits, F)}, cft -inf ${hex(wrongC, F)} (cft +inf is 3: ${hex(trapC.bits, F)})`);
}
console.log("\nflag bits (both): invalid=1 divByZero=2 overflow=4 underflow=8 inexact=16");
