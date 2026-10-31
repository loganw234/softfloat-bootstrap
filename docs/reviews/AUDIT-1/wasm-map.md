<!-- The WebAssembly mapper's report (both modules' interfaces, the operation table, the first differential runs),
     extracted by script from the hand-back call that ends its transcript, unedited. Its redactions (<user>,
     <address>, <domain>, <Logan's site>) are its own, as its brief asked. Paths into the session's scratch
     directory name files that were not kept, but for the ones audit/ now holds. -->

# muse-softfloat vs cft-fp256 (wasm, Node 22.23.4): verified mapping, smoke, disagreements

V = I ran it. R = read from code or docs only. Both repos untouched (git status empty, no __pycache__ in either).
Scratch dir `X` = /tmp/claude-0/-home-user/a5ed6180-6e84-5c9f-9e43-f754d57c15fd/scratchpad/xtest/
`X`RUN_TRANSCRIPTS.txt holds the terminal output of every run below (copied, not re-run).

## 0. Traps that will bite a harness (all V)
1. **Rounding numbers 2 and 3 are swapped.** muse 2 = toward +inf, 3 = toward -inf. cft 2 = RDN (-inf), 3 = RUP (+inf). 0, 1 and 4 agree.
2. **cft ADD and SUB read operands a and c (b ignored).** MUL reads a and b. FMA reads a, b, c.
3. muse accepts an out-of-range `rm` silently (5 acted like RNE, -1 like RTZ). cft returns status 1 for rnd outside 0..4.
4. **logB:** muse returns a binary64 encoding for both formats. cft returns the operand's own format.
5. **class() numbering differs:** cft = (muse + 8) % 10 (tables in the op table).
6. cft compare, totalOrder and min/max predicates return 1.0 or +0.0 in the operand format. muse returns 0 or 1.
7. **NaN results:** cft always returns the canonical +qNaN. muse propagates the first NaN operand, quieted, keeping sign and payload.
8. `WebAssembly.instantiate(bytes, imports)` returns `{instance, module}`. `instantiate(Module, imports)` returns an Instance.
9. cft: `M.HEAPU8` and DataViews detach when memory grows, so re-fetch after any call or malloc.

## 1. Module facts

| facet | muse `site/msf.wasm` (770,233 B) | cft `bindings/node/cft_node.wasm` (276,303 B) + `cft_node.js` (CJS emscripten loader) |
|---|---|---|
| imports (V) | none | 10: env.{__syscall_openat, __syscall_fcntl64, __syscall_ioctl, emscripten_resize_heap}; wasi_snapshot_preview1.{fd_write, fd_read, fd_close, environ_sizes_get, environ_get, fd_seek} |
| exports (V) | memory, msf_op_count, msf_run (arity 8), msf_result_lo, msf_result_hi, msf_result_flags, msf_result_ok | 149: memory, __indirect_function_table, and 147 functions (141 `cftw_*`, malloc, free, __wasm_call_ctors, 3 emscripten stack helpers). ABI 0.18 |
| memory (V) | defined and exported, 17 pages (1,114,112 B), no max. You never need to touch it | defined and exported, 259 pages (16,973,824 B), max 32,768 pages, grows via the `emscripten_resize_heap` import |
| instantiate (V) | `(await WebAssembly.instantiate(readFileSync(p), {})).instance.exports`. No ctors, no start | Easiest: `import {loadModule} from ".../bindings/node/lib.mjs"; const {M,C}=await loadModule()`. M is the emscripten Module (_malloc, _free, HEAPU8, HEAPU32, FS); C holds 141 cwrap'd `cftw_*`. `loadModule` also audits cft.h opcode numbers against the module. High level: `Context.open(32\|64, "rne")` from `index.mjs`. Raw (`X`raw_cft.mjs, V): compile, instantiate with 10 stubs (fd_* return errno or 0, resize_heap = memory.grow), call `__wasm_call_ctors()`. I never triggered memory growth in the raw path |
| operands | by value: `msf_run(idx, rm, a_lo, a_hi, b_lo, b_hi, c_lo, c_hi)`. binary32 uses the low word. Signed ints are two's complement in the low bits. `idx` is the position in `site/ops.json` (849 entries, 822 runnable); resolve by name. Examples in this build: msf32_add 46, sub 73, mul 100, div 127, sqrt 145, fma 190 | through the heap: dense little-endian, 4 or 8 bytes per element, pointers from `malloc`, `n` elements. dev handle from `cftw_open_software(&dev)`. fmt 0 = fp32, 1 = fp64. int64 args are split lo/hi (scaleb). Int arrays and strings live in the heap |
| results | `msf_result_lo/hi` (64-bit slot, to-int results arrive sign-extended, so mask to `retw`), `msf_result_flags()`, `msf_result_ok()` (0 = entry not runnable; bad idx also gives 0). State is global, so not re-entrant | written to the output buffer. Returns status 0 = OK, 1 = invalid argument. `flags_out` may be NULL |
| rounding | `rm` 0 RNE, 1 RTZ, 2 toward +inf, 3 toward -inf, 4 TiesToAway; -1 or anything for ops without an attribute | `rnd` 0 RNE, 1 RTZ, **2 RDN (-inf), 3 RUP (+inf)**, 4 RMM (TiesToAway). Names "rne rtz rdn rup rmm" in Context and jsonl |
| flags | per-call delta (V: `msf_run` resets every call). 0x01 invalid, 0x02 divByZero, 0x04 overflow, 0x08 underflow, 0x10 inexact. The `msf_*_flags` ops are not runnable | same bits. Per-call `flags_out` is overwritten (V: preset 0x1f became 0). Sticky device word: `cftw_save_all_flags(dev)` reads it, `cftw_lower_flags(dev, mask)` is the only clear, plus raise/test/restore/test_saved. `cftw_flags_all()` = 0x1f. Context: `ctx.lastFlags` (last call), `ctx.flags` (sticky), `clearFlags()` |
| tininess | after rounding (R: header, SF-0 2.5, `MSF_TININESS_AFTER_ROUNDING`=1). V: f32 `0x00800001 * 0x3f7ffffe` and f64 `0x0010000000000001 * 0x3feffffffffffffe` give min-normal plus inexact only on both | after rounding (R: CAPABILITIES.md:111, softfloat.py:36). Same V probes agree |
| NaN | SF-0 2.5 matrix (R, V): no NaN input gives default +qNaN. An sNaN input signals invalid and returns that operand quieted. Otherwise the first NaN operand is returned, sign and payload kept. fma(0, inf, qNaN) signals invalid and delivers the addend | any NaN in arithmetic, min/max, formatOf, etc. gives canonical +qNaN, and an sNaN raises invalid (R: DETERMINISM.md, V). abs, neg, copysign, select, payload ops and char conversions preserve payload. fma(0, inf, qNaN): the NaN wins and invalid is NOT raised (documented deviation) |
| accuracy (R) | correct rounding is promised for every rounded op (SF-0 2.3), gated against Berkeley TestFloat 3e, MPFR or exact references (COVERAGE.tsv). The 9.2 functions are "correctly rounded" (README, authority mpfr-exact). binary32 exp2 and log2 were exhaustively checked once; binary64 is by hardest-case and seeded vectors. Decimal output is correct for 1..H = 20 digits | cft.h: every rounded op is correctly rounded in all 5 modes. All 39 table-9.1 functions are "CORRECTLY ROUNDED ... not accurate to an ulp". Decimal conversions are exact with H unbounded |

## 2. Operation table
`{F}` = 32 or 64. "muse" = name for `msf_run`. "cft" = `C.<name>` over export `cftw_*`; common prefix `(dev, fmt, rnd, ...ptrs, n, flags*)`. V rows: both sides executed on the same corpora; counts are in section 5.

| operation | muse | cft | |
|---|---|---|---|
| add / sub / mul | `msf{F}_add\|sub\|mul` (a,b; rm) | `cftw_run` op 1 ADD (a+c), 2 SUB (a-c), 3 MUL (a*b) | V |
| fma | `msf{F}_fma` (a,b,c) | `cftw_run` op 0 | V, class B |
| div / sqrt | `msf{F}_div\|sqrt` | `cftw_div(dev,fmt,rnd,a,b,d,n,fl,bus)` / `cftw_sqrt(dev,fmt,rnd,a,d,n,fl,bus)` | V |
| remainder | `msf{F}_remainder` (exact, no rm) | `cftw_rem(dev,fmt,a,b,d,n,fl)` | V |
| roundToIntegral x5 | `msf{F}_round_to_integral_{ties_to_even\|ties_to_away\|toward_zero\|toward_positive\|toward_negative}` (no rm) | `cftw_rint(dev,fmt,rnd,0,a,d,n,fl,bus)` with rnd = RNE, RMM, RTZ, RUP, RDN | V |
| roundToIntegralExact | `msf{F}_round_to_integral_exact` (rm) | `cftw_rint(...,rnd,1,...)` | V |
| nextUp / nextDown | `msf{F}_next_up\|next_down` | `cftw_next_up\|next_down(dev,fmt,a,d,n,fl)` | V |
| minimum, maximum, minimumNumber, maximumNumber | `msf{F}_minimum\|maximum\|minimum_number\|maximum_number` | `cftw_run` op 7 MIN, 8 MAX, 9 MINNUM, 10 MAXNUM (a,b) | V |
| the 4 magnitude forms | `msf{F}_minimum_magnitude\|maximum_magnitude\|minimum_magnitude_number\|maximum_magnitude_number` | `cftw_min_mag\|max_mag\|minnum_mag\|maxnum_mag(dev,fmt,a,b,d,n,fl)` | V |
| scaleB | `msf{F}_scale_b` (a, n = binary64 ENCODING of an integral value, truncated toward 0; rm) | `cftw_scaleb(dev,fmt,rnd,a,n_lo,n_hi,d,n,fl,bus)` | V for integral n; a NaN n exists only in muse (R) |
| logB | `msf{F}_log_b`, result binary64 for both F | `cftw_logb(dev,fmt,a,d,n,fl)`, result in operand format | V (compare numerically) |
| convertFormat | `msf32_from_f64`, `msf64_from_f32`, and same-format `msf32_from_f32`, `msf64_from_f64` (rm) | `cftw_convert(dev,sfmt,dfmt,rnd,a,d,n,fl)` | V |
| convertFromInt | `msf{F}_from_{i32,u32,i64,u64}` (also i8,u8,i16,u16) | `cftw_cvt_from_{i32,u32,i64,u64}(dev,fmt,rnd,src*,d,n,fl)` | V |
| convertToInteger | `msf{F}_to_{i32,u32,i64,u64}_{ties_to_even\|ties_to_away\|toward_zero\|toward_positive\|toward_negative}` and the `_exact_` forms (no rm; also i8..u16) | `cftw_cvt_to_{i32,u32,i64,u64}(dev,fmt,rnd,exact,a,dst*,n,fl)` | V, class C |
| compare quiet and signaling | `msf{F}_compare_quiet_{equal,not_equal,greater,greater_equal,less,less_equal,not_greater,not_less,less_unordered,greater_unordered,unordered,ordered}` and `_signaling_` (same minus unordered/ordered). Mixed-format forms carry a `_f64` or `_f32` suffix | quiet: `cftw_run` op 12 CMPLT, 13 CMPLE, 14 CMPEQ (unordered = false). Signaling: `cftw_cmp_sig(dev,cmp,fmt,a,b,d,n,fl,bus)`. The rest are exact compositions, flags OR-ed: gt = lt(b,a), ge = le(b,a), ne = !eq, ngt = !lt(b,a), nlt = !lt(a,b), lu = !le(b,a), gu = !le(a,b), unordered = !le(a,b) && !le(b,a), ordered = le(a,b) \|\| le(b,a). Mixed forms: widen the binary32 side with `cftw_convert`, OR its flags, compare in fp64 | V, 88 descriptors |
| totalOrder / Mag | `msf{F}_total_order\|total_order_mag` | `cftw_total_order\|total_order_mag(dev,fmt,a,b,d,n)` | V |
| class and predicates | `msf{F}_class`: 0 sNaN, 1 qNaN, 2 -inf, 3 -norm, 4 -sub, 5 -0, 6 +0, 7 +sub, 8 +norm, 9 +inf. Also `_is_{normal,finite,zero,subnormal,infinite,nan,signaling,sign_minus,canonical}`, `_radix` | `cftw_class(dev,fmt,a,u8*,n)`: 0 -inf, 1 -norm, 2 -sub, 3 -0, 4 +0, 5 +sub, 6 +norm, 7 +inf, 8 sNaN, 9 qNaN. Predicates are subset tests; isSignMinus = top bit; canonical is always true; radix is 2 | V |
| abs / negate / copySign | `msf{F}_abs\|negate\|copy_sign` (`_copy` is muse only) | `cftw_run` op 4 ABS, 5 NEG, 6 COPYSIGN (magnitude a, sign b) | V, bit-exact |
| payload (9.7) | `msf{F}_get_payload\|set_payload\|set_payload_signaling` | `cftw_get_payload\|set_payload\|set_payload_signaling(dev,fmt,a,d,n)` | V, bit-exact |
| sinPi, cosPi, rSqrt, hypot, exp2, exp2m1, log2, log2p1 | `msf{F}_sin_pi\|cos_pi\|r_sqrt\|hypot(a,b)\|exp2\|exp2m1\|log2\|log2p1` (rm) | `cftw_sinpi\|cospi\|rsqrt\|hypot\|exp2\|exp2m1\|log2\|log2p1(dev,fmt,rnd,a[,b],d,n,fl)` | V, class D |
| formatOf, same-source operands | `msf{D}_{add,sub,mul,div}_f{S}_f{S}`, `msf{D}_sqrt_f{S}`, `msf{D}_fma_f{S}_f{S}_f{S}` | `cftw_formatof_{add,sub,mul,div,sqrt,fma}(dev,sfmt,dfmt,rnd,...,d,n,fl,bus)` | V |
| formatOf, mixed-source (e.g. `msf32_add_f32_f64`) | native | no single call. Widen each narrow operand with `cftw_convert` (exact) and OR its flags (an sNaN's invalid comes from there), then formatOf(64 to D) | V as a recipe |
| decimal and hex char conversions | C only: `msf{F}_from_decimal(s,&consumed,rm,fl)`, `_to_decimal(a,&{precision,style,min_digits},buf,size,rm,fl)`, `_from_hex`, `_to_hex(a,&{precision},...)`. **Not runnable in msf.wasm (ok=0)** | `cftw_from_decimal_char(dev,fmt,rnd,char**,d,n,bad_idx*,fl)`, `cftw_to_decimal_char(dev,fmt,rnd,a,digits,out,cap,len*,fl)`, `cftw_from_hex_char`, `cftw_to_hex_char(dev,fmt,a,out,cap,len*)`. Context: `fromDecimal`, `toDecimal(x,{digits})`, `fromHex`, `toHex` | cft V via Context, muse R |
| augmented (9.5) | C only: `msf{F}_augmented_{add,sub,mul}(a,b,fl)` returning {head,tail}. **ok=0 in wasm** | `cftw_augmented_{add,sub,mul}(dev,fmt,a,b,r*,e*,n,fl)`; `ctx.augmentedAdd(x,y)` returns {r,e}. Both fix roundTiesTowardZero | cft V, muse R |
| flag ops and 5.7.1 | `msf_{lower,raise,test,restore,save_all,test_saved}_flags` have ok=0; `msf_is754version*` runnable | `cftw_{lower,raise,test,save_all,restore,test_saved}_flags`, `cftw_is754version*` (V: 2019 = 1, 2008 = 0, 1985 = 0) | |

Only on one side at binary32/64:
- **muse only:** all f16; 8/16-bit int conversions; `copy`; directly named compare, is* and mixed-operand ops (cft composes or widens).
- **cft only:** the other 31 of the 39 table-9.1 functions (exp, expm1, log, log1p, log10, pow, tanPi, asin, acos, atan, the Pi forms, atan2, atan2Pi, sin, cos, tan, the hyperbolics, exp10, exp10m1, log10p1, powr, pown, compound, rootn).
- **also cft only:** reductions (sum, dot, sumsq, sumabs, maxall, scaled products), SELECT (11), integer ops 16-23 and 30, seeds 26/27, fp128/fp256, programs, sha256. Opcodes 15 and 32+ return canonical qNaN with invalid.

## 3. Smoke script
`X`smoke.mjs is standalone. Run it with `node X smoke.mjs`. It loads both modules and runs 1+2 and 1/3 (RNE, plus RTZ, RUP, RDN, RMM). `X`xlib.mjs holds the reusable adapters.
```
== binary32 ==
1 + 2  RNE           muse 0x40400000 [-        ]  cft 0x40400000 [-        ]  SAME  (3)
1 / 3  RNE           muse 0x3eaaaaab [inexact  ]  cft 0x3eaaaaab [inexact  ]  SAME  (0.3333333432674408)
1 / 3  RTZ           muse 0x3eaaaaaa [inexact  ]  cft 0x3eaaaaaa [inexact  ]  SAME  (0.3333333134651184)
1 / 3  RUP(+inf)     muse 0x3eaaaaab ...  cft 0x3eaaaaab ...  SAME      RDN(-inf)  0x3eaaaaaa both  SAME     RMM 0x3eaaaaab both  SAME
  trap: rounding number 2 => muse +inf 0x3eaaaaab, cft -inf 0x3eaaaaaa (cft +inf is 3: 0x3eaaaaab)
== binary64 ==
1 + 2  RNE           muse 0x4008000000000000 [-        ]  cft 0x4008000000000000 [-        ]  SAME  (3)
1 / 3  RNE           muse 0x3fd5555555555555 [inexact  ]  cft 0x3fd5555555555555 [inexact  ]  SAME  (0.3333333333333333)
1 / 3  RTZ           muse 0x3fd5555555555555 [inexact  ]  cft 0x3fd5555555555555 [inexact  ]  SAME  (0.3333333333333333)
1 / 3  RUP(+inf)     0x3fd5555555555556 both  SAME     RDN 0x3fd5555555555555 both  SAME     RMM 0x3fd5555555555555 both  SAME
  trap: rounding number 2 => muse +inf 0x3fd5555555555556, cft -inf 0x3fd5555555555555 (cft +inf is 3: 0x3fd5555555555556)
flag bits (both): invalid=1 divByZero=2 overflow=4 underflow=8 inexact=16
```
Full lines are in RUN_TRANSCRIPTS.txt section 1.

## 4. Vector formats
**muse `tests/vectors/*.vec`** (R: `tests/VECTORS.md`; V census: 51 files, 411,213 vector lines, matching the README)
- Line: `<op> <rm> <args...> -> <result> <flags> <provenance>`. `#` starts a comment.
- `<op>` is the API name, e.g. `msf32_add`. `<rm>` is te, tz, tp (toward +inf), tn (toward -inf) or ta, or `-`.
- Args and result are lowercase hex with no `0x`, leading zeros trimmed, at the operand's width. scaleB's n is a binary64 encoding.
- Flags are two hex digits in muse's layout, or `--` for ops without flags. Provenance is the last token.
- Augmented pairs: `<op> - a b -> head tail flags prov`. String ops use `IN=...`, `A=...`, `SPEC=...`, `OUT=...`, `LEN=...`, `C=<consumed>`. There are also `internal.pack{16,32,64}` lines. `# compare=<mode>` directives are allowed but none are present.
- Counts per file (V), f32/f64-relevant:

| files | lines |
|---|---|
| arith-f32 / arith-f64 | 4,240 / 4,355 |
| arith-xf (cross-format) | 6,959 |
| fma-sqrt-f32 / fma-sqrt-xf | 1,172 / 3,566 |
| compare-f32 / compare-f64 / compare-xf | 2,362 / 2,302 / 1,980 |
| conv-f64 / conv-int-f32 / conv-xf | 3,480 / 1,115 / 460 |
| toint-f32, rint-misc-f32 | 2,640, 1,143 |
| misc-f64, nan-f64 | 1,467, 285 |
| encodings-f32 / f64 | 2,352 each |
| minmax-f32 / f64 | 5,832 each |
| payload-f32 / f64 | 102 each |
| alg-f32 / f64 | 3,700 each |
| explog-f32 / explog-f64 | 29,175 / 32,050 |
| trig-f32 / trig-f64 | 17,800 / 22,610 |
| aug-f32 / aug-f64 | 46,146 each |
| copysign (3 formats) | 4,336 |
| from-decimal, to-decimal, from-hex, to-hex (strings) | 4,290, 7,506, 1,959, 2,661 |
| pack32 / pack64 | 6,160 / 6,270 |

- f16 files mirror these.
- 145,448 f32/f64 lines have an op on both sides in my map and were replayed on both. The remaining lines are f16, 8/16-bit ints, strings, augmented pairs and internal.pack*; the ones with no cft op (including the strings and augmented lines) are not runnable in msf.wasm.

**cft vectors** (R: `vectors/gen_vectors.py` docstring, plus V on generated files)
- `vectors/` holds only `gen_vectors.py` and `SHA256SUMS`; the sets are generated.
- `make vectors` writes into the repo (`vectors/out`) for all four formats. Instead call the generator directly: `PYTHONDONTWRITEBYTECODE=1 python3 -B vectors/gen_vectors.py --out <scratch> --formats fp32 fp64 --rounding rne rtz rdn rup rmm --directed 3000 --random 4000 --simple 200 --jobs 4`. It imports `python/cft_golden` and needs mpmath. I used the scratchpad venv.
- **Time (V): 5.6 s wall, 19.8 s CPU on 4 vCPU. Output: 64 sets, 59 MB. All 64 SHA-256 match `vectors/SHA256SUMS`.** The rne column alone took 4.7 s serial. The docs quote 404 s for 5 attributes x 4 formats on the author's desktop (R).
- Already generated at `X`cftvec_f32f64/ (64 sets + SHA256SUMS + MODEL), log in `X`cftvec_f32f64.log. You can reuse it.
- rne column counts (V): fp32.jsonl 11,800; transcend 22,139 (fp64 34,830); minmaxmag 2,432; augmented 54,048 (fp64 11,856); reduce 512; character 854; formatof 960 / 912 / 4,275 / 1,008.
- Schemas, one JSON object per line, hex fixed width (8 or 16 digits), flags a decimal int in the cft bit layout:
  - opcode sets `fp32.jsonl`, `fp32-rtz`, `-rdn`, `-rup`, `-rmm`: `{"op","rnd","a","b","c","d","flags"}`. ADD and SUB use a and c, with b present but ignored. cmp* gives d = 1.0 or +0.
  - `fp32-transcend[-rXX]`: `{"fn","rnd","a",["b"],["n" signed decimal],"d","flags"}`.
  - `fp32-augmented`: `{"fn":"augmentedAddition","a","b","r","e","flags"}`, no rnd.
  - `fp32-reduce[-rXX]`: `{"fn","rnd","n","a":[...],["b":[...]],"d"|("pr","sf"),"flags"}`.
  - `fp32-character[-rXX]`: `{"fn","rnd","s",...,"flags"}`, with `"refuse":1` marking sequences that must be rejected.
  - `fp32-minmaxmag`: `{"fn","a","b","d","flags"}`, no rnd.
  - `fp64-to-fp32-formatof[-rXX]`: `{"fn","sfmt","dfmt","rnd","a","b","c","d","flags"}`.
- **conformance.html sample (V, extracted to `X`cft_embedded_sample/*.jsonl):** a JS object `CFT_SAMPLE` (file name to jsonl text) plus `CFT_BUILD`.
  - It holds 20 files, the opcode sets only (4 formats x 5 attributes), 4,015 cases: fp32 sets 200 each, fp64 202 each, fp128 201, fp256 200.
  - Rule: every 59th line (0-based) of each 11,800-case set, plus the first line of any opcode the stride missed.
  - The generator command is in `CFT_BUILD.gen_command`.
  - There are 28 op names, with no transcendentals, augmented, reduce, character, minmaxmag or formatOf sets.
- **Feeding arbitrary vectors to `cft_conformance` (R only; I did not execute it):**
  - Call `cftw_conformance(dev, dirPtr, reportPtr, reportSize, casesLoPtr, casesHiPtr)`. It returns 0 on all-match, ERR_INTERNAL on the first disagreement, and ERR_ARTIFACT if no set is found. The report text names the failing case.
  - `dir` is a directory in the module's MEMFS: `M.FS.mkdir`, `M.FS.writeFile`, as `bindings/node/conformance.mjs` does.
  - It probes fixed file names only (`fp32.jsonl`, `fp32-rtz.jsonl`, ..., `fp32-transcend*.jsonl`, `-augmented`, `-reduce*`, `-character*`, `-minmaxmag`, `A-to-B-formatof*`) and replays each set twice, per element and as arrays.
  - So muse vectors must be converted to cft's schema, saved under one of those names, and given cft-canonical NaN results.
  - Each line's `rnd` should equal the file's attribute. The JS driver enforces this; I did not check the C side.

## 5. Runs I did (scripts in `X`)
- **xlib.mjs, corpus.mjs, opsmap.mjs, diff_all.mjs.** The adapters and the op table as 324 executable descriptors, driven by `node diff_all.mjs 1 --json out.json`.
  - corpus.mjs: specials (zeros, subnormals, 1 +/- ulp, max, inf, qNaN, sNaN with payloads, integer-boundary values) plus xorshift32 randoms; the 3-operand fma cross also includes a 9-value NaN matrix.
  - Compares value and flags for the same operation and rounding on both sides.
  - Raw: `X`diff_scale1.txt, `X`diff_scale1.json, `X`diff_scale1.time. This run was 280 descriptors, 5,929,853 cases, 31 s.
  - Result: identical 5,613,644; NaN-payload-only 313,961; flags 1,288; finite-value mismatches 0; NaN-to-int 960.
  - `X`diff_cmp.json: the 88 compare descriptors (44 added later, mixed-format), 2,191,992 cases, 0 non-identical.
  - `X`diff_scale0.3.* is an older, superseded run.
- **diff_math.mjs 6000** (stdout only). The 8 shared 9.2 functions x 2 formats x 6,000 random inputs x 5 modes: 480,000 cases, 0 mismatches, 280 NaN-payload-only.
- **nan_matrix.mjs** (stdout only). 9 special values crossed, with RNE and RTZ: only class A everywhere, plus class B in fma.
- **fma_flag_pattern.mjs** (stdout only). 2,380,800 fma-family cases: 64 flag mismatches, all exactly class B, 0 unexplained.
- **replay_muse_vec.mjs.** Muse's committed `.vec` lines to msf.wasm and to cft. This run predates the mixed-compare ops.
  - 145,448 replayable lines. msf.wasm reproduced all of them (0 bad).
  - cft: exact 139,081; NaN-payload-only 6,119; flags 88; value 0; NaN-to-int 160.
  - The 88 flag lines are 4 exp2m1 (class D) and 84 in the fma family; the examples I printed were all class B.
- **replay_cft_sample.mjs.** cft's embedded fp32/fp64 sample to muse: 1,520 mappable lines, exact 1,415, NaN-payload-only 105, other 0. Integer, select, seed and reserved ops (about 500 lines) have no muse equivalent.
- **exp2m1_edge.mjs, misc_checks.mjs, explore_*.mjs, inspect_*.mjs, raw_cft.mjs** (stdout only, in the transcripts). Also `muse_vec_census.py`, `extract_conf_sample.py`, `list_unmapped.mjs`.
- I did **not** run muse's own `site/replay.mjs` (R: its log says 1,620 vectors, 0 mismatches). My own replay above covers far more.

### Disagreement classes (all four seen; no finite-value mismatch in about 6.6M cases)
- **A. NaN result payload and sign** (cft canonicalises; muse propagates).
  - `add` binary32 RNE a=0x00000000, b=0x7fc00005: muse 0x7fc00005 flags 0; cft 0x7fc00000 flags 0.
  - `fma` binary32 RNE a=0, b=0, c=0xffa00000: muse 0xffe00000 [invalid]; cft 0x7fc00000 [invalid].
  - abs, neg, copysign, payload ops, compares and class are bit-exact.
- **B. fma(+-0, +-inf, quiet NaN).** muse raises invalid; cft does not (documented in DETERMINISM.md as a deliberate deviation).
  - `fma` binary32 RNE 0x00000000, 0x7f800000, 0x7fc00000: both 0x7fc00000; muse flags 0x01, cft 0x00.
  - `fma` binary64 RNE 0x0000000000000000, 0x7ff0000000000000, 0x7ff8000000000000: both 0x7ff8000000000000; muse 0x01, cft 0x00.
  - Also seen in formatOf fma and the mixed forms.
- **C. NaN to integer.** The delivered value differs; invalid is raised on both.
  - `to_i32` (any direction, exact or not) binary32 0x7fc00000: muse 0 [invalid]; cft 0x7fffffff [invalid].
  - u32 gives 0xffffffff, i64 0x7fffffffffffffff, u64 0xffffffffffffffff; binary64 behaves the same. All 960 cases are NaN inputs.
- **D. exp2m1 at x = emax+1 under RTZ and RDN: overflow flag.**
  - binary32 x=0x43000000 (128), RTZ: both 0x7f7fffff; muse flags 0x10 (inexact); cft 0x14 (overflow|inexact). RDN is the same.
  - binary64 x=0x4090000000000000 (1024), RTZ and RDN: both 0x7fefffffffffffff; muse 0x10; cft 0x14.
  - By my reading of 754-2019 7.4, muse is right: RTZ(2^128-1) with unbounded exponent is exactly maxFinite, so overflow does not occur. Muse's MPFR-derived vector agrees. exp2(128) agrees on both sides.
  - Random sampling (480k) missed it; only muse's vectors found it (4 lines). Cross-test with both vector sets.
- **E. Harness-side issue, fixed.** The mixed-source formatOf recipe lost the widening conversion's invalid flag. Example: `msf32_add_f32_f64`, RNE, a=0x7f800001 (binary32 sNaN), b=0: muse 0x7fc00001 [invalid]; the recipe without conversion flags gave 0x7fc00000 [-]. Fix: OR the conversion flags (done in opsmap.mjs).

## 6. Not verified
- `cft_conformance` fed with converted muse lines (R only).
- cft heap growth in the raw instantiate.
- muse `is754version*` values (R: true for 2019).
- Mixed-compare ops are covered by diff_cmp.json but were not added to the vector replay.
- Muse scaleB with fractional n versus cft (R: truncation toward zero).
- Per-call cost with my adapters, from diff_scale1.json: muse about 0.7 to 6 us. cft about 1.7 to 17 us for arithmetic, 14 to 104 us for the 9.2 functions.
