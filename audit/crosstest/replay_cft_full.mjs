// replay_cft_full.mjs - cft-fp256's published fp32/fp64 conformance corpus (all sets whose
// operation muse also has) through BOTH wasm modules:
//   control: cft's own module must reproduce every record exactly (validates the adapters)
//   cross:   muse's module, judged against cft's record, disagreements classified
// node replay_cft_full.mjs [dir with fp32*.jsonl/fp64*.jsonl, default AUDIT_WORK/cft/vectors/out] [--json out.json]
import { readFileSync, readdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { loadMuse, loadCft, flagStr, WORK } from "./xlib.mjs";
import { buildOps } from "./opsmap.mjs";
import { isNaNBits } from "./corpus.mjs";

const DIR = process.argv[2] && !process.argv[2].startsWith("--") ? process.argv[2] : join(WORK, "cft", "vectors", "out");
const ji = process.argv.indexOf("--json");
const mu = await loadMuse(), cf = await loadCft();
const byId = new Map(buildOps(mu, cf).map((o) => [o.id, o]));
const RM = { rne: "RNE", rtz: "RTZ", rdn: "RDN", rup: "RUP", rmm: "RMM" };
const H = (x) => BigInt(x);

const OPCODE = { add: ["add", "ac"], sub: ["sub", "ac"], mul: ["mul", "ab"], fma: ["fma", "abc"], abs: ["abs", "a"], neg: ["negate", "a"],
  copysign: ["copySign", "ab"], min: ["minimum", "ab"], max: ["maximum", "ab"], minnum: ["minimum_number", "ab"], maxnum: ["maximum_number", "ab"],
  cmplt: ["compare_quiet_less", "ab", "b"], cmple: ["compare_quiet_less_equal", "ab", "b"], cmpeq: ["compare_quiet_equal", "ab", "b"] };
const TRANS = { exp2: "exp2", exp2m1: "exp2m1", log2: "log2", log2p1: "log2p1", sinpi: "sin_pi", cospi: "cos_pi", rsqrt: "r_sqrt", hypot: "hypot" };
const MAG = { minimumMagnitude: "minimum_magnitude", maximumMagnitude: "maximum_magnitude", minimumMagnitudeNumber: "minimum_magnitude_number", maximumMagnitudeNumber: "maximum_magnitude_number" };
const PAY = { get_payload: "get_payload", set_payload: "set_payload", set_payload_signaling: "set_payload_signaling" };

function plan(file, r) {     // -> { id, args, rm, F, boolRes } or null (no muse counterpart)
  const F = file.startsWith("fp32") ? 32 : 64;
  const rm = RM[r.rnd ?? "rne"];
  const slots = { a: r.a, b: r.b, c: r.c };
  if (/^fp\d+(-r..)?\.jsonl$/.test(file)) {
    const m = OPCODE[r.op]; if (!m) return null;
    return { id: `${m[0]}@${F}`, args: [...m[1]].map((k) => H(slots[k])), rm, F, boolRes: m[2] === "b", want: H(r.d), flags: r.flags };
  }
  if (file.includes("-transcend")) {
    const t = TRANS[r.fn]; if (!t) return null;
    return { id: `${t}@${F}`, args: r.b !== undefined ? [H(r.a), H(r.b)] : [H(r.a)], rm, F, want: H(r.d), flags: r.flags };
  }
  if (file.includes("-minmaxmag")) return { id: `${MAG[r.fn]}@${F}`, args: [H(r.a), H(r.b)], rm: null, F, want: H(r.d), flags: r.flags };
  if (file.includes("-formatof")) {
    const S = r.sfmt === "fp32" ? 32 : 64, D = r.dfmt === "fp32" ? 32 : 64;
    const args = r.fn === "sqrt" ? [H(r.a)] : r.fn === "fma" ? [H(r.a), H(r.b), H(r.c)] : [H(r.a), H(r.b)];
    return { id: S === D ? `${r.fn}@${D}` : `formatOf_${r.fn}_${S}_to_${D}`, args, rm, F: D, want: H(r.d), flags: r.flags };
  }
  if (file.includes("-character") && PAY[r.fn]) return { id: `${PAY[r.fn]}@${F}`, args: [H(r.a)], rm: null, F, want: H(r.d), flags: r.flags ?? 0 };
  return null;
}

function judge(p, res) {
  const v = p.boolRes ? (res.v !== 0n ? 1n : 0n) : res.v, want = p.boolRes ? (p.want !== 0n ? 1n : 0n) : p.want;
  const valEq = v === want, nanEq = !p.boolRes && isNaNBits(p.F, v) && isNaNBits(p.F, want);
  if (valEq && res.flags === p.flags) return "ok";
  if (nanEq && res.flags === p.flags) return "nan-payload";
  if ((valEq || nanEq) && (res.flags ^ p.flags) === 1 && p.id.includes("fma")) return "fma(0,inf,qNaN) invalid";
  if (valEq || nanEq) return `flags ${flagStr(p.flags)} -> ${flagStr(res.flags)}`;
  return "VALUE";
}

const tally = {}, ex = {};
let unmapped = 0, mapped = 0;
const files = readdirSync(DIR).filter((f) => /^fp(32|64).*\.jsonl$/.test(f) && !f.includes("reduce") && !f.includes("augmented")).sort();
for (const file of files) {
  for (const ln of readFileSync(`${DIR}/${file}`, "utf8").split("\n")) {
    if (!ln) continue;
    const r = JSON.parse(ln);
    const p = plan(file, r);
    if (!p || p.id.includes("undefined")) { unmapped++; continue; }
    const d = byId.get(p.id);
    if (!d) throw new Error(`no descriptor ${p.id} (${file})`);
    mapped++;
    const fam = file.replace(/-r(tz|dn|up|mm)\.jsonl$|\.jsonl$/, "").replace(/^fp(32|64)-?/, "") || "opcode";
    for (const [side, fn] of [["cft(control)", d.c], ["muse(cross)", d.m]]) {
      const res = fn(p.rm, p.args);
      const cat = judge(p, res);
      const key = `${side}\t${fam}\t${p.id}\t${cat}`;
      tally[key] = (tally[key] ?? 0) + 1;
      if (cat !== "ok" && (ex[key] ??= []).length < 3)
        ex[key].push(`${p.rm ?? "-"} ${p.args.map((x) => "0x" + x.toString(16)).join(",")} want 0x${p.want.toString(16)}[${flagStr(p.flags)}] got 0x${res.v.toString(16)}[${flagStr(res.flags)}]`);
    }
  }
}
const sum = (pred) => Object.entries(tally).filter(([k]) => pred(k)).reduce((s, [, n]) => s + n, 0);
console.log(`files ${files.length}; records mapped ${mapped}, without a muse counterpart ${unmapped}`);
console.log(`control (cft module vs cft record): ok ${sum((k) => k.startsWith("cft") && k.endsWith("\tok"))}, not ok ${sum((k) => k.startsWith("cft") && !k.endsWith("\tok"))}`);
console.log(`cross   (muse module vs cft record): ok ${sum((k) => k.startsWith("muse") && k.endsWith("\tok"))}, not ok ${sum((k) => k.startsWith("muse") && !k.endsWith("\tok"))}`);
const cats = {};
for (const [k, n] of Object.entries(tally)) { const [side, fam, id, cat] = k.split("\t"); if (cat !== "ok") cats[`${side} | ${cat}`] = (cats[`${side} | ${cat}`] ?? 0) + n; }
console.log("\nnon-ok classes:"); for (const [k, n] of Object.entries(cats).sort()) console.log(`  ${String(n).padStart(8)}  ${k}`);
console.log("\nby op (non-ok only):");
for (const [k, n] of Object.entries(tally).sort()) if (!k.endsWith("\tok")) console.log(`  ${String(n).padStart(8)}  ${k.replaceAll("\t", " | ")}`);
console.log("\nexamples:"); for (const [k, l] of Object.entries(ex)) for (const e of l) console.log(`  [${k.replaceAll("\t", " | ")}] ${e}`);
if (ji > 0) writeFileSync(process.argv[ji + 1], JSON.stringify({ tally, ex, mapped, unmapped }, null, 1));
