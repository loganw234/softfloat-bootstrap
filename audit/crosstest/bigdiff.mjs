// bigdiff.mjs - large differential run, both wasm modules, worker threads.
//   node bigdiff.mjs <scale> <outprefix>      (scale 1 ~ 30M cases)
// Every (descriptor, rounding attribute) task gets cases from gen.mjs (TestFloat-style); each
// worker loads its own copy of both modules. A deterministic 1-in-SAMPLE subset of cases is
// written with both answers for the exact Python oracle, so agreement is also checked for truth.
import { Worker, isMainThread, parentPort, workerData } from "node:worker_threads";
import { writeFileSync } from "node:fs";
import { basename } from "node:path";

const RMS = ["RNE", "RTZ", "RUP", "RDN", "RMM"];
const SAMPLE = 997;

if (isMainThread) {
  const scale = Number(process.argv[2] ?? 1), out = process.argv[3] ?? "bigdiff";
  const { loadMuse, loadCft } = await import("./xlib.mjs");
  const { buildOps } = await import("./opsmap.mjs");
  const ops = buildOps(await loadMuse(), await loadCft());
  // volume per (descriptor, attribute); the 9.2 functions are the slow ones
  const vol = (o) => {
    const id = o.id;
    if (/^(add|sub|mul|div|fma)@/.test(id)) return 400000;
    if (/^sqrt@/.test(id)) return 200000;
    if (o.slow) return 60000;
    if (/^formatOf_/.test(id)) return 60000;
    if (/^formatOfMixed_/.test(id)) return 15000;
    if (/^convertFormat_/.test(id)) return 200000;
    if (/^(to_|from_|roundToIntegral|remainder|scaleB|logB|next)/.test(id)) return 60000;
    return 20000;
  };
  const tasks = [];
  for (const o of ops) for (const rm of o.rm ? RMS : [null]) tasks.push({ id: o.id, rm, n: Math.max(1, Math.round(vol(o) * scale / (o.rm ? 1 : 2))) });
  tasks.sort((a, b) => b.n - a.n);
  const W = 4, buckets = Array.from({ length: W }, () => ({ load: 0, t: [] }));
  for (const t of tasks) { const b = buckets.reduce((x, y) => (x.load <= y.load ? x : y)); b.t.push(t); b.load += t.n * (/(sin_pi|cos_pi|exp2|log2|hypot|r_sqrt)/.test(t.id) ? 12 : 1); }
  const t0 = Date.now();
  const results = await Promise.all(buckets.map((b, i) => new Promise((res, rej) => {
    const w = new Worker(new URL(import.meta.url), { workerData: { tasks: b.t, seed: 1000 + i } });
    w.on("message", res); w.on("error", rej);
  })));
  const tally = {}, ex = {}, sample = [];
  for (const r of results) {
    for (const [k, n] of Object.entries(r.tally)) tally[k] = (tally[k] ?? 0) + n;
    for (const [k, l] of Object.entries(r.ex)) (ex[k] ??= []).push(...l.slice(0, 3 - (ex[k]?.length ?? 0)));
    sample.push(...r.sample);
  }
  const total = Object.values(tally).reduce((s, n) => s + n, 0);
  const cls = {};
  for (const [k, n] of Object.entries(tally)) { const c = k.split("\t")[2]; cls[c] = (cls[c] ?? 0) + n; }
  let txt = `cases ${total} in ${(Date.now() - t0) / 1000}s over ${tasks.length} tasks\n\nby class:\n`;
  for (const [c, n] of Object.entries(cls).sort((a, b) => b[1] - a[1])) txt += `  ${String(n).padStart(10)}  ${c}\n`;
  txt += "\nnon-ok by descriptor:\n";
  for (const [k, n] of Object.entries(tally).sort()) if (!k.endsWith("\tok")) txt += `  ${String(n).padStart(8)}  ${k.replaceAll("\t", " | ")}\n`;
  txt += "\nexamples:\n";
  for (const [k, l] of Object.entries(ex)) for (const e of l) txt += `  [${k.replaceAll("\t", " | ")}] ${e}\n`;
  writeFileSync(`${out}.txt`, txt);
  writeFileSync(`${out}.sample.jsonl`, sample.map((s) => JSON.stringify(s)).join("\n") + "\n");
  console.log(txt.split("\nnon-ok by descriptor:")[0]);
  console.log(`sample for the oracle: ${sample.length} cases -> ${basename(out)}.sample.jsonl (beside the run's other outputs)`);
} else {
  const { loadMuse, loadCft, flagStr, FLAG } = await import("./xlib.mjs");
  const { buildOps } = await import("./opsmap.mjs");
  const { Rng, operands, operand, FMT } = await import("./gen.mjs");
  const { isNaNBits } = await import("./corpus.mjs");
  const ops = new Map(buildOps(await loadMuse(), await loadCft()).map((o) => [o.id, o]));
  const r = new Rng(workerData.seed);
  const tally = {}, ex = {}, sample = [];
  let counter = 0;
  const intArg = (kind) => {   // integers with structure: boundaries, runs, small, random
    const w = kind.endsWith("32") ? 32 : 64, signed = kind[0] === "i";
    const k = r.below(6);
    let v = k === 0 ? (1n << BigInt(r.below(w))) + BigInt(r.below(5)) - 2n
          : k === 1 ? ((1n << BigInt(1 + r.below(w - 1))) - 1n) << BigInt(r.below(8))
          : k === 2 ? BigInt(r.below(1000)) : r.bits(w);
    v = BigInt.asUintN(w, v);
    return signed ? BigInt.asIntN(w, v) : v;
  };
  const nearInt = (F) => {    // values at and near integer and half-integer boundaries, incl. 2^31, 2^32, 2^63, 2^64
    const f = FMT[F], k = [31, 32, 63, 64, 0, 1, 2, 23, 24, 52, 53][r.below(11)];
    const e = Number(f.bias) + k - (r.below(3) - 1);
    if (e <= 0 || e >= (1 << f.eb) - 1) return operand(r, F);
    let m = r.below(2) ? 0n : ((1n << BigInt(f.p - 1)) - 1n) ^ BigInt(r.below(4));
    if (r.below(3) === 0) m = r.bits(f.p - 1);
    return (BigInt(r.below(2)) << BigInt(f.w - 1)) | (BigInt(e) << BigInt(f.p - 1)) | m;
  };
  const scaleN = () => [0, 1, -1, 2, -2, 127, -126, 128, -149, 150, 1023, -1022, 1024, -1074, 1075, 2000, -2000, 300, -300][r.below(19)] + (r.below(4) ? 0 : r.below(64) - 32);
  for (const t of workerData.tasks) {
    const o = ops.get(t.id);
    const fo = (k) => (o.argFmts ? o.argFmts[k] : o.srcF);
    for (let i = 0; i < t.n; i++) {
      let args;
      if (o.argKinds[0] !== "f") args = [intArg(o.argKinds[0])];
      else if (o.argKinds[1] === "n") args = [operand(r, o.srcF), BigInt(scaleN())];
      else if (/^(to_|roundToIntegral)/.test(o.id) && r.below(2)) args = [nearInt(o.srcF)];
      else if (o.argFmts && new Set(o.argFmts).size > 1) args = o.argFmts.map((F) => operand(r, F));
      else args = operands(r, fo(0), o.argKinds.length, o.id);
      const m = o.m(t.rm, args), c = o.c(t.rm, args);
      if (process.env.MUTANT) {          // positive control: planted wrong answers on the muse side
        if (t.id === "add@32" && t.rm === "RNE" && i % 1000 === 0) m.v ^= 1n;
        if (t.id === "div@64" && t.rm === "RTZ" && i % 1000 === 1 && (m.flags & FLAG.INEXACT)) m.flags &= ~FLAG.INEXACT;
      }
      // judge
      let cat;
      const F = o.F, valEq = m.v === c.v || (typeof m.v === "number" && (Object.is(m.v, c.v) || (Number.isNaN(m.v) && Number.isNaN(c.v))));
      const nan = !valEq && o.kind === "f" && isNaNBits(F, m.v) && isNaNBits(F, c.v);
      if (valEq && m.flags === c.flags) cat = "ok";
      else if (nan && m.flags === c.flags) cat = "nan-payload";
      else if ((valEq || nan) && (m.flags ^ c.flags) === FLAG.INVALID && o.id.includes("fma")) cat = "fma(0,inf,qNaN) invalid";
      else if (o.kind === "i" && !valEq && (m.flags & FLAG.INVALID) && (c.flags & FLAG.INVALID) && m.flags === c.flags) cat = "int invalid delivery";
      else if (valEq || nan) cat = `flags muse ${flagStr(m.flags)} cft ${flagStr(c.flags)}`;
      else cat = "VALUE";
      const key = `${t.id}\t${t.rm ?? "-"}\t${cat}`;
      tally[key] = (tally[key] ?? 0) + 1;
      if (cat !== "ok" && (ex[key] ??= []).length < 3)
        ex[key].push(`${args.map((x) => "0x" + BigInt.asUintN(64, BigInt(x)).toString(16)).join(",")} muse ${typeof m.v === "number" ? m.v : "0x" + m.v.toString(16)}[${flagStr(m.flags)}] cft ${typeof c.v === "number" ? c.v : "0x" + c.v.toString(16)}[${flagStr(c.flags)}]`);
      if (++counter % SAMPLE === 0 && o.kind === "f" && !o.argFmts && o.srcF === o.F)
        sample.push({ id: t.id, rm: t.rm, F, args: args.map((x) => BigInt.asUintN(64, BigInt(x)).toString(16)), m: m.v.toString(16), mf: m.flags, c: c.v.toString(16), cf: c.flags });
    }
  }
  parentPort.postMessage({ tally, ex, sample });
}
