// Replay muse's COMMITTED vectors (tests/vectors/*.vec) through (1) msf.wasm and (2) cft, via the op map.
//   node replay_muse_vec.mjs [file-glob-regex]
import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { loadMuse, loadCft, flagStr, FLAG, MUSE_TREE } from "./xlib.mjs";
import { buildOps } from "./opsmap.mjs";
import { isNaNBits, toNumber, maskOf } from "./corpus.mjs";
const DIR = join(MUSE_TREE, "tests", "vectors");
const RMTOK = { te: "RNE", tz: "RTZ", tp: "RUP", tn: "RDN", ta: "RMM", "-": null };
const filt = new RegExp(process.argv[2] ?? ".");
const mu = await loadMuse(), cf = await loadCft();
const ops = buildOps(mu, cf);
const byM = new Map(ops.map((o) => [o.mname, o]));
const tally = {};     // per op name
let lines = 0, skippedStr = 0, skippedAug = 0, skippedPack = 0, unmapped = new Map();
const files = readdirSync(DIR).filter((f) => f.endsWith(".vec") && filt.test(f));
const T = (name) => (tally[name] ??= { n: 0, museOk: 0, museBad: 0, cftOk: 0, cftNan: 0, cftFlags: 0, cftValue: 0, cftInv: 0, ex: [] });
for (const f of files) {
  for (const ln of readFileSync(`${DIR}/${f}`, "utf8").split("\n")) {
    if (!ln || ln.startsWith("#")) continue;
    const t = ln.split(" ");
    const name = t[0];
    if (name.startsWith("internal.")) { skippedPack++; continue; }
    if (t.some((x) => /^(IN|A|SPEC|OUT|LEN|C)=/.test(x))) { skippedStr++; continue; }
    const arrow = t.indexOf("->");
    const op = byM.get(name);
    if (!op) { unmapped.set(name, (unmapped.get(name) ?? 0) + 1); continue; }
    if (arrow < 0 || t.length - arrow !== 4) { skippedAug++; continue; }                 // pair results (aug) have 2 result fields
    const rm = RMTOK[t[1]];
    let a = t.slice(2, arrow).map((x) => BigInt("0x" + x));
    const want = BigInt("0x" + t[arrow + 1]);
    const wflags = t[arrow + 2] === "--" ? null : parseInt(t[arrow + 2], 16);
    if (/scale_b/.test(name) && Number.isNaN(toNumber(64, a[1]))) continue;               // NaN exponent: no cft equivalent
    const s = T(name); s.n++; lines++;
    // ---- muse side: the descriptor's m() takes n as an INTEGER for scaleB, so call msf_run directly there
    let mres;
    if (/scale_b/.test(name)) mres = mu.run(name, rm ? { RNE: 0, RTZ: 1, RUP: 2, RDN: 3, RMM: 4 }[rm] : -1, a);
    else mres = op.m(rm, a);
    const mv = mres.bits ?? mres.v;
    const wantCmp = op.kind === "num" ? toNumber(64, want) : op.kind === "i" ? want & maskOf(op.w) : want;
    const mvCmp = typeof mv === "number" ? mv : op.kind === "i" ? mv & maskOf(op.w) : mv;
    const mOk = (typeof wantCmp === "number" ? Object.is(wantCmp, mvCmp) : wantCmp === mvCmp) && (wflags === null || mres.flags === wflags);
    mOk ? s.museOk++ : s.museBad++;
    // ---- cft side
    let cres;
    if (/scale_b/.test(name)) {                                                         // n is an F64 encoding in muse; integer in cft
      const nNum = toNumber(64, a[1]);
      const nI = !Number.isFinite(nNum) ? (nNum > 0 ? 1n << 40n : -(1n << 40n)) : Math.abs(nNum) >= 2 ** 62 ? (nNum > 0 ? 1n << 62n : -(1n << 62n)) : BigInt(Math.trunc(nNum));
      cres = op.c(rm, [a[0], nI]);
    } else cres = op.c(rm, a);
    const cmpC = op.kind === "num" ? cres.v : op.kind === "i" ? cres.v & maskOf(op.w) : cres.v;
    const valEq = typeof wantCmp === "number" ? Object.is(wantCmp, cmpC) || (Number.isNaN(wantCmp) && Number.isNaN(cmpC)) : wantCmp === cmpC;
    const flagsEq = wflags === null || cres.flags === wflags;
    if (valEq && flagsEq) s.cftOk++;
    else if (!flagsEq) { s.cftFlags++; if (s.ex.length < 2) s.ex.push(`${t[1]} ${a.map((x) => x.toString(16)).join(",")} want ${t[arrow + 1]}/${t[arrow + 2]} cft ${typeof cmpC === "bigint" ? cmpC.toString(16) : cmpC}/${cres.flags.toString(16)}`); }
    else if (op.kind === "f" && isNaNBits(op.F, wantCmp) && isNaNBits(op.F, cmpC)) s.cftNan++;
    else if (op.kind === "i" && (wflags & FLAG.INVALID)) s.cftInv++;
    else { s.cftValue++; if (s.ex.length < 2) s.ex.push(`${t[1]} ${a.map((x) => x.toString(16)).join(",")} want ${t[arrow + 1]}/${t[arrow + 2]} cft ${typeof cmpC === "bigint" ? cmpC.toString(16) : cmpC}/${cres.flags.toString(16)}`); }
  }
}
const sum = Object.values(tally).reduce((p, s) => { for (const k of ["n", "museOk", "museBad", "cftOk", "cftNan", "cftFlags", "cftValue", "cftInv"]) p[k] += s[k]; return p; }, { n: 0, museOk: 0, museBad: 0, cftOk: 0, cftNan: 0, cftFlags: 0, cftValue: 0, cftInv: 0 });
console.log("files", files.length, "| replayable lines (op mapped on both sides, f32/f64):", lines, JSON.stringify(sum));
console.log("skipped: string-conv lines", skippedStr, "| aug/pair lines", skippedAug, "| internal.pack lines", skippedPack);
const um = [...unmapped].filter(([k]) => /^msf(32|64)_/.test(k)), um16 = [...unmapped].filter(([k]) => /^msf16_/.test(k));
console.log("unmapped f32/f64 op names:", um.length, "lines", um.reduce((p, [, v]) => p + v, 0), "| f16-only names", um16.length, "lines", um16.reduce((p, [, v]) => p + v, 0));
console.log("  e.g. unmapped:", um.slice(0, 12).map(([k, v]) => `${k}:${v}`).join(" "));
for (const [k, s] of Object.entries(tally)) if (s.museBad || s.cftFlags || s.cftValue) console.log("DIFF", k, JSON.stringify({ ...s, ex: undefined }), s.ex.join(" | "));
