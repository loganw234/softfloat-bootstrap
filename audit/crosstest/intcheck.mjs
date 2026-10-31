// Out-of-range finite and infinite operands of every convertToInteger descriptor: do the delivered values differ?
import { loadMuse, loadCft, FLAG } from "./xlib.mjs";
import { buildOps } from "./opsmap.mjs";
import { Rng, pack, FMT } from "./gen.mjs";
const ops = buildOps(await loadMuse(), await loadCft()).filter((o) => o.id.startsWith("to_"));
const r = new Rng(5); let n = 0, differ = 0, inval = 0; const ex = [];
for (const o of ops) {
  const F = o.srcF, f = FMT[F], E = (1 << f.eb) - 1, bias = Number(f.bias);
  const xs = [pack(F, 0, E, 0n), pack(F, 1, E, 0n)];                                   // +-inf
  for (let k = 0; k < 400; k++) {                                                        // |x| >= 2^31 .. max finite, both signs
    const e = bias + 31 + r.below(E - 1 - bias - 31 + 1);
    xs.push(pack(F, r.below(2), Math.min(e, E - 1), r.bits(f.p - 1)));
  }
  for (const x of xs) {
    const m = o.m(null, [x]), c = o.c(null, [x]); n++;
    if ((m.flags & FLAG.INVALID) && (c.flags & FLAG.INVALID)) inval++;
    if (m.v !== c.v || m.flags !== c.flags) { differ++; if (ex.length < 5) ex.push(`${o.id} 0x${x.toString(16)} muse 0x${m.v.toString(16)}/${m.flags} cft 0x${c.v.toString(16)}/${c.flags}`); }
  }
}
console.log(`out-of-range/inf operands: ${n} cases over ${ops.length} descriptors, both-invalid ${inval}, any difference ${differ}`);
console.log(ex.join("\n"));
