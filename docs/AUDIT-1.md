# AUDIT-1: the project repository against cft-fp256, and the two libraries against each other

2026-10-31. This is the audit the kit's clean room ends with ([kit/CLEAN-ROOM.md](../kit/CLEAN-ROOM.md), "The
audit"). muse-softfloat's kickoff record says it was waived at the start, "because the fingerprint tooling was not
finished before the hackathon began", and that "the record must keep saying so" (its docs/KICKOFF.md:196-198).

After the audit, the two libraries were cross-tested: each one's tests run through the other, and both side by
side.
- **Nothing was changed in either repository.**
- **The tooling is [audit/](../audit/README.md).** One run of it, `bash audit/setup.sh && bash audit/run.sh`, wrote
  [audit/results/2026-10-31/](../audit/results/2026-10-31/SUMMARY.txt).
- **The three agents' reports** are in [reviews/AUDIT-1/](reviews/AUDIT-1/README.md).
- **The one defect found** is reported at [loganw234/cft-fp256#1](https://github.com/loganw234/cft-fp256/issues/1).

Tags as in [VALIDATION.md](VALIDATION.md): MEASURED, READ, COMPUTED, BELIEVED.

| repository | commit | history read |
|---|---|---|
| muse-softfloat | `a2241fc`, its HEAD | all 185 commits, every ref: main, wave6-ci, wave6-examples, wave6-sanitize, claude/sweet-dirac-dv44dp |
| cft-fp256 | `f68c630`, its HEAD | all 2,101 commits, every ref |
| softfloat-bootstrap | `a23a0ff` | the kit muse received, as the baseline |

## Verdict

**The audit finds no sign that muse-softfloat took code from cft-fp256.** Four independent checks found nothing:
1. A token-level search over both full histories. It caught every copy planted to test it.
2. A comparison of constants, identifiers, comments, strings and test data.
3. An expert structural read by an agent not told what the lead suspected.
4. A review of muse's own record.

What the two projects share traces to IEEE 754, Berkeley SoftFloat 3e, standard algorithms, mathematical constants
and well-known random generators. Where 754 leaves a choice, muse often made the opposite one.

**On their shared surface (binary32 and binary64), the two libraries never disagree on a result value.** That covers:
- 44.46 million random cases;
- cft's published corpus run through muse;
- muse's committed corpus run through cft;
- 16.8 million contiguous inputs of the eight functions both have.

Every disagreement is either a choice one project documents, or one defect, in cft-fp256. exp2m1 raises a spurious
overflow at x = emax+1 under roundTowardZero and roundTowardNegative, in all four of its formats. Its golden model
carries the same error, so its own conformance gate cannot see it. muse's vectors exposed it.

## Part 1: the audit

### What was compared (MEASURED)

- **The suspect:** every code blob ever committed to muse-softfloat, on any ref, with its copy of the kit left out:
  466 blobs.
- **The source:** every code blob ever committed to cft-fp256: 3,430 blobs of C, headers, C++, Arduino, JS, MJS,
  Python, shell and HTML.
- **The baseline of permitted common sources:** a match also found there does not count. It holds 649 files:
  - Berkeley SoftFloat 3e and TestFloat 3e, fetched from jhauser.us (sha256 `21130ce8…` and `6d4bdf00…`);
  - the kit's code as muse received it.

### Results (MEASURED)

| check | result |
|---|---|
| token k-grams, every k-gram, exact (k = 24) and identifier/number-normalised (k = 40) | No muse library file (src/, include/, compat/, site/) has an exact cft-only run of 50 tokens or more, in any version. The longest is 28 tokens (site/index.html), and 26 in src/. Normalised runs of 80 tokens or more in library code are all repetitive tables or macro lists: complexity under 0.1, where copied code scores 0.34 to 0.64. |
| the same, anywhere in muse | 3 code-like runs, all in tests: SplitMix64 (Vigna's public-domain reference code); the FIPS 180-4 round loop in a test-only SHA-256; a hand-written lexer loop (hex in muse, decimal in cft) |
| positive controls | 17 of 17 planted cft functions caught at their planted lines: 5 C functions verbatim, renamed, and renamed and reflowed; 2 Python functions renamed |
| high-entropy numeric constants | 60 shared and not in the baseline. All are 32-bit words of ln 2, log2(e) or π; PRNG or hash constants (SplitMix64, the golden ratio, xorshift*, Knuth's MMIX, FNV); or plain values (powers of ten, 0.1f, √2, a date seed) |
| identifiers | The shared multi-part names in library code are 754 operation names, Web APIs and generic field names. Two helper names collide (`u64_bitlen`, `set_payload_core`) with unrelated bodies: a loop against a binary search; scalar decoding against device lanes over bignums |
| comments | 0 shared 8-word phrases (a planted cft comment is found, as 11). At 6 words, 12 generic phrases |
| string literals of 18 or more characters | 28 shared, all generic: 754 operation names, the NIST SHA-256 message, DBL_MAX, π's digits, HTML boilerplate |
| test data | 54 of muse's 33,468 high-entropy hex words (0.16%) occur anywhere in cft. All are famous values (1/3, 0.1, √2, e, π, 2^(k/8), 2^24 + 1); none is a random operand |
| structural read ([its report](reviews/AUDIT-1/structural-review.md)) | Weak similarities that common sources explain: 14 parallels, each traced to 754, Berkeley or the literature. The architectures differ throughout. cft routes add, sub and mul through one FMA, divides by Newton iteration from seed tables, and evaluates its transcendentals in one generic bignum Ziv loop. muse has separate kernels, restoring division, and per-function fixed-point kernels with error bounds proven offline. No cft identifier or vocabulary appears in muse's library code |
| muse's own record ([its report](reviews/AUDIT-1/record-review.md)) | 178 lines in 154 files mention cft outside the kit. Each restates the rule, attests non-access, or is the lead's day-1 disclosure. The fetch log holds 5 archive fetches (Berkeley, REBOUND, KissFFT, CORE-MATH) and no URL to cft-fp256, its Pages site, a mirror or a fork. No near-miss and no use is recorded |

### What the audit cannot rule out

- **Reading without copying.** Token and feature checks find copied text. A translation from cft's Python golden
  model into C would show only to the structural read, and that read covered the core files, not all 5,200 lines of
  cft's transcend.c. (READ, its report's limits.)
- **There was no fence.** The clean room was a rule and disclosure. On day 1 the lead listed the names of cft-named
  clones beside the workspace. No removal is recorded, and the audit was waived until now. (READ, muse
  docs/KICKOFF.md:111-115 and 196-198.)
- **The raw transcripts are not in the record.** The session transcripts are the only place an open or a fetch would
  show, and they are not in muse's repository or its audit bundle. Wave 6 has no ledgers. (READ, the record review.)
- **Two of muse's statements claim more than is true.** Its final audit says "zero cft mentions in history/tree",
  which holds only for paths and commit messages. Its bundle builder drops cft-named paths without counting them.
  (READ, the record review.)

## Part 2: the cross-test

### Surfaces and controls (MEASURED)

- **The shipped WebAssembly:**
  - muse's `site/msf.wasm`, which runs 822 of its 849 operations, and has had only comment changes since it was
    built;
  - cft's `bindings/node/cft_node.wasm`, built at `ba03b1d7` (2026-10-05).

  324 descriptors cover the binary32 and binary64 operations both have
  ([opsmap.mjs](../audit/crosstest/opsmap.mjs)).
- **Native builds of both at HEAD, linked into one program.** It runs what msf.wasm cannot: the augmented pairs and
  the character conversions. It also runs the dense sweeps, and checks findings against current source.
- **The exact arbiter.** Rationals for the basic operations, an MPFR (gmpy2) Ziv loop for the eight functions, and
  an exact integer square root for rSqrt and hypot. It was checked first against 72,000 x86 SSE cases and 120,000
  Berkeley SoftFloat 3e cases, roundTiesToAway and both tininess modes among them: 0 disagreements in bits or in
  any of the five flags.
- **Each library's own corpus through its own side,** which validates the adapters:
  - cft: 163,412 of 163,412 in WebAssembly, and every one of its native augmented and character records;
  - muse: 146,907 of 146,907, and every one of its own.
- **Planted wrong answers:** 20 of 20 value plants and 19 of 19 flag plants caught.

### Results (MEASURED)

| run | cases | identical | documented-policy differences | value differences | other |
|---|---:|---:|---|---:|---|
| cft corpus through muse, WebAssembly: the 64 published fp32/fp64 sets, regenerated, all 64 equal to cft's SHA256SUMS | 163,412 | 154,774 | NaN payload 8,624; fma(0,∞,qNaN) 10 | **0** | 4: cft's own record wrong (the exp2m1 defect) |
| cft corpus, augmented pairs, native | 65,904 | 60,872 | NaN payload 1,089; exact tiny tail's underflow 3,943 | **0** | |
| cft corpus, character conversions, native | 6,780 | 5,853 | input only one side's grammar accepts 510; more than H = 20 decimal digits 417 | **0** within H | |
| muse corpus through cft, WebAssembly: its committed f32/f64 lines | 146,907 | 140,540 | NaN payload 6,119; a NaN's integer conversion 160; fma(0,∞,qNaN) 84 | **0** | 4: the exp2m1 defect |
| muse corpus, augmented pairs, native | 92,292 | 73,894 | NaN payload 10,077; exact tiny tail's underflow 8,321 | **0** | |
| muse corpus, character conversions, native | 6,752 | 6,125 | grammar 486; more than H digits 141 | **0** within H | |
| random differential, TestFloat-style generator, WebAssembly, 660 tasks | 44,460,000 | 44,143,795 | NaN payload 308,963; a NaN's integer conversion 7,221 | **0** | 21: the exp2m1 defect, found at random |
| a 1-in-997 sample of that run, against the exact arbiter | 31,128 answers a library | all correct on both sides | | | |
| dense sweeps, native: the eight shared functions, 2^20 consecutive binary32 inputs under RNE and 2^18 under each other attribute, from each function's core range | 16,777,216 | 16,777,216 | none | **0** | |

Each policy class above was checked to be what it claims, case by case
([classes.py](../audit/native/classes.py), [intcheck.mjs](../audit/crosstest/intcheck.mjs)):
- **A NaN's integer conversion is the only integer class.** 32,160 out-of-range and infinite operands across all
  80 integer-conversion descriptors show no difference.
- **Decimal input beyond H.** All 175 differing inputs of more than 20 digits follow muse's documented two-step
  rule exactly, bits and flags, and cft is exactly correct on all 175.
- **Decimal output beyond H.** In all 383 differing outputs, muse's answer is the correctly rounded 20 digits and
  zeros after them, and cft's is correctly rounded to every digit asked for.
- **Augmented underflow.** All 12,264 augmented flag differences are muse 0x00 against cft 0x08, on equal results
  whose tail is exact, nonzero and subnormal.
- **Refusals.** cft refuses exactly the 390 records its own corpus marks `refuse`. No string muse accepts whole is
  refused by cft.
- **fma.** The fma class is fma(0, ∞, quiet NaN) alone.

### The documented policy differences: neither side is wrong (READ, both sources)

| choice | muse | cft | the standard |
|---|---|---|---|
| NaN result payload | propagates the first NaN, quieted | always the canonical +qNaN | 6.2.3 *should* preserve a payload; not required |
| fma(0, ∞, quiet NaN) | signals invalid | does not | 7.2(c): implementation-defined |
| a NaN's conversion to integer: the value delivered | 0 | the maximum | 5.8: invalid is signaled; the value is not specified |
| augmented operations, an exact tiny tail | underflow signaled, no flag raised (its pin P1 = R2, after 7.5's default handling) | underflow flag raised, "underflow WITHOUT inexact" | a reading of 9.5 against 7.5; each project records its ruling |
| more than H decimal digits, in or out | H = 20, the least 5.12.2 allows beside binary64: rounds to H digits under the attribute first; pads output with zeros | no limit; exact | 5.12.2 |
| character grammar | the longest valid prefix; no payload syntax | whole strings only; `nan(0x…)` payloads | the implementation's syntax |
| rounding-direction numbers | toward +∞ = 2, toward −∞ = 3 | RDN = 2, RUP = 3 | an encoding, not a semantic |

### The cft-fp256 defect: exp2m1 at emax+1 (MEASURED, reported at [loganw234/cft-fp256#1](https://github.com/loganw234/cft-fp256/issues/1))

- **The defect:** under roundTowardZero and roundTowardNegative, exp2m1(emax+1) returns maxFinite, which is
  correct, but raises overflow and inexact (0x14) where inexact alone (0x10) is correct.
  - Affected arguments: binary32 x = 128, binary64 x = 1024, binary128 x = 16384, binary256 x = 262144.
  - Shown in the golden model, in native libcft at HEAD, and in the published module.
- **Why it is wrong:** 754-2019 7.4 signals overflow only when the result, rounded as though the exponent range were
  unbounded, exceeds maxFinite. RTZ(2^(emax+1) − 1) is exactly maxFinite.
- **The cause** is the same shortcut in the golden model and the C: `python/cft_golden/transcend.py:2250` and
  `host/src/transcend.c:3992` treat `n > emax` as overflowing under every attribute.
  - At n = emax+1, 2^n − 1 lies just below 2^n. It overflows under RNE, RNA and RUP, but rounds to maxFinite without
    overflow under RTZ and RDN.
  - exp2's branch at transcend.c:2483 is right, because 2^n itself overflows under every attribute.
- **Why cft's gate passes:** its published vectors are generated from the golden model, so they carry the same flag.
  `fp32-transcend-rtz.jsonl` expects `"flags": 20`, and cft's conformance passes.
- **Found three ways:**
  - muse's MPFR-derived vectors (its `tests/vectors/explog-f32.vec` and `explog-f64.vec`) replayed through cft;
  - cft's own corpus replayed through muse;
  - the random differential.
- **The arbiter sides with muse.** [exp2m1_probe.c](../audit/native/exp2m1_probe.c) shows the defect at every
  attribute and in all four formats.
- **No counterpart in muse.** muse has no finding against it: it passed cft's whole corpus, but for the documented
  choices.

### Limits

- **What could not be tested:** binary16, which cft lacks; cft's other 31 functions, its reductions and its
  binary128 and binary256 formats, which muse lacks.
- **cft's module is older than its source:** cft_node.wasm predates 14 commits to host/src. The defect was shown on
  a native build of HEAD as well.
- **Neither method is exhaustive.** Random testing does not cover the input space, and the dense sweeps cover
  contiguous binary32 ranges, not all 2^32 inputs.
