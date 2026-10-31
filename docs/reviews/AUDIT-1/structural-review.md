<!-- The structural reviewer's report (an unanchored expert read of both libraries' code), extracted by script from
     the hand-back call that ends its transcript, unedited. Its redactions (<user>, <address>, <domain>, <Logan's
     site>) are its own, as its brief asked. Paths into the session's scratch directory name files that were not
     kept, but for the ones audit/ now holds. -->

## Verdict: weak similarities that common sources explain

Nothing I read in muse-softfloat's library code looks copied from cft-fp256, translated from it, or closely paraphrased. The parallels I found sit at the level of the standard's own definitions and textbook algorithms. Where IEEE 754 leaves a choice to the implementation, muse usually chose differently from cft, and in one case it deliberately took the opposite reading.

Every claim below is READ unless it is marked INFERRED. Line citations give muse first, then cft.

## Evidence table

| # | Similarity | muse | cft | Explained by |
|---|---|---|---|---|
| 1 | Values are decoded to sign, class, an integer significand and the exponent of its lowest bit. Subnormals are left un-normalised at emin−t. | msf_decode.h:40-70 | softfloat.c:75-116 | The (s, q, c) representation in IEEE §3.3. muse's own plan, SF-0 §3.2, also requires this decode. |
| 2 | One rounding kernel takes (sign, exponent, significand, sticky, mode). Both describe its input as "(sig + f)·2^e, with f in [0,1) and non-zero exactly when sticky is set". | msf_internal.h:74-84; msf_roundpack.c:9-25 | softfloat.c:158-164, 189-191 | Berkeley's `softfloat_roundPackToF64(sign, exp, sig)` (internals.h:135) and its "jam" sticky convention. muse puts the arguments in Berkeley's order (exponent before significand), not cft's (m, e). |
| 3 | Tininess is decided by rounding a second time as if the exponent range were unbounded. | msf_roundpack.c:136-158 | softfloat.c:206-212 | The wording of IEEE §7.5. muse's first version (P0) got this wrong. The fix (commit 53acb1a) came from disagreements with Berkeley, not from cft. |
| 4 | An internal sixth rounding direction, roundTiesTowardZero, is given a value outside the public range, and the augmented-operations file is its only caller. The two comments are the closest wording I found ("exact tie keeps… smaller magnitude", "strictly above the midpoint"). | msf_internal.h:20-26; msf_roundpack.c:60-64 | softfloat.h:64-76; softfloat.c:126-130 | The text of IEEE §9.5 ("the one with smaller magnitude") plus the only correct increment rule. muse worked out the value 5 in its own ledger (audit-bundle/ledger/parcel-w5aug.md:24-33). |
| 5 | Flag bits are ordered invalid=1, divide-by-zero=2, overflow=4, underflow=8, inexact=16. | muse_softfloat.h:86-90 | softfloat.h:51-55 | The order Clause 7 lists them (7.2 to 7.6), which x86 also follows; Berkeley uses the reverse. The rounding-mode numbers differ: muse has toward +∞=2 and toward −∞=3, cft uses RISC-V's RDN=2, RUP=3. |
| 6 | Augmented addition has a "far" branch that returns the larger operand as the head and the smaller as the tail. Both prove it with the same half-grid-step lemma and the same p+2 bound. | msf_aug.c:222-245; docs/WIDTHS.md:43-60 | augmented.c:31-47, 287-298 | The mathematics of 2Sum and §9.5, and standard near/far adder terminology. muse's branch actually triggers when the operands span more than 127 bits (its 128-bit window), not at p+2. |
| 7 | Decimal input outside the format's range is answered by packing one representative value from inside the overflow or underflow band. | msf_string.c:455-461, 588-601 | chars.c:66-88, 586-604 | The usual strtod idiom (musl returns LDBL_MAX*LDBL_MAX for overflow; INFERRED from memory). The band tests differ (muse: a per-format table of decimal magnitudes; cft: rational bounds on log2(10)), and so do the representatives. |
| 8 | sinPi and cosPi are shown to be exact only at integers and half-integers using Niven's theorem; a dyadic argument cannot give ±1/2. | msf_math.c:27-31 | transcend.c:3270-3278 | A standard result that every correctly rounded sinPi relies on to terminate. muse's studies argue it themselves. |
| 9 | Ziv's test: round both interval endpoints through the pack and accept only if bits and flags both agree. | msf_math.c:546-579 | transcend.c:28-35 | Ziv's method as in the literature (e.g. Muller's handbook). Comparing flags is needed for underflow cases. |
| 10 | log: recentre by an exact test of m² ≥ 2, then sum the atanh((m−1)/(m+1)) series. | msf_math.c:1213-1227, 1404-1425 | transcend.c:877-920 | The classic logarithm reduction. |
| 11 | rSqrt(−0) = −∞ with divide-by-zero, and both note that MPFR disagrees. | msf_alg.c:26-35 | transcend.c:4303-4306 | The §9.2.1 table. The MPFR manual itself documents that its rec_sqrt returns +Inf for −0 (INFERRED from memory). |
| 12 | hypot's special cases in the order: signaling NaN, then infinity beats quiet NaN, then zeros. | msf_alg.c:46-50 | transcend.c:2958-2975 | §9.2.1 and §6.2. |
| 13 | Constants are generated by a script from mpmath, truncated, stored as little-endian 32-bit limb arrays with an exponent, and regenerated byte-identically. | msf_trig_tables.h:1-4; gen_trig_tables.py:1-20 | mp_consts.h:1-25; gen_mp_consts.py:1-40 | Generic practice plus the owner's shared method. The layouts differ: muse uses 384 bits, a top-bit exponent and stored Taylor coefficients; cft uses 1088 bits, a lowest-bit exponent and computes its series terms at run time. |
| 14 | remainder uses bit-serial division and the parity of the last quotient bit to break ties. | msf64.c:502-582; msf32.c:407-470 | clause5.c:1254-1345 | The textbook fmod/remquo approach. |

A light pass over shared comment word sequences (computed, comments only) found three generic 6-word phrases and about 25 five-word ones. All are clause numbers or phrases from the standard, such as "the exponent range were unbounded". None of cft's identifiers or vocabulary (round_pack, steer, lane, cls_of, K_*, scaffolding, contract flags) appears in muse's library code, and cft has no jam or clz helpers while muse uses both.

## Strongest differences against derivation

- **NaNs:** muse propagates payloads (the first signaling NaN, quieted, otherwise the first quiet NaN; msf_decode.h:11-24, 102-127). cft only ever produces its one canonical quiet NaN (softfloat.c:50-56, 312-322). For fma(0, ∞, quiet NaN), muse signals invalid (msf64.c:295-297) and cft does not (softfloat.c:336-337).
- **Add, subtract, multiply:** cft routes all three through one FMA by substituting operands (softfloat.c:430-468). muse has separate kernels (msf64.c:90-181).
- **Operand alignment:** cft computes the near case exactly and handles the far case with FAR = 2p+4 and a sticky-and-decrement trick (softfloat.c:263-310, 381-401). muse aligns into a fixed 118-bit window with jam shifts (msf64.c:67-128).
- **Division and square root:** cft uses Markstein-style Newton iteration from 2^9-entry seed tables (divsqrt.c:22-37, 81-91). muse uses restoring division and a bit-by-bit root search (msf64.c:183-271).
- **roundToIntegral:** cft computes (x + C) − C with C = 2^(p−1) as device passes (clause5.c:281-330). muse rounds the integer significand directly (msf64.c:339-397).
- **Integer conversion of NaN:** muse returns 0 (muse_softfloat.h:22-26); cft returns the maximum (clause5.c:755-757, 779-783).
- **Augmented operations:** cft raises underflow for an exact tiny tail, including in the far branch (augmented.c:213-232, 295-296). muse ships the opposite reading, which the owner pinned, and keeps cft's behaviour only as a test mutant labelled "R1" (msf_aug.c:15-26, 161-183).
- **Character conversions:**
  - cft parses whole strings only, with no digit limit, exact default output, a "(0x…)" payload suffix, and subnormal hex normalised to 0x1… (chars.c:850-1000, 1208-1240, 1390-1430).
  - muse parses the longest valid prefix, limits significant digits to H=20 with the §5.12.2 two-step route beyond that, emits Pmin digits by default with fixed and scientific styles, prints no payload, and writes subnormals as 0x0… (msf_string.c:11-23, 964-1140).
- **Transcendentals:**
  - cft runs one general Ziv loop over a multiprecision float that tracks its error at run time. It escalates precision from 2p+40 up to 8p+128 and returns CFT_ERR_INTERNAL if it reaches the cap (transcend.c:62-84, 150-193).
  - muse writes a fixed-point kernel per function with three fixed stages (160/256/384 bits), error bounds proven offline by the generator, and a fallback that returns the lower endpoint (msf_math.c:16-26, 685-686).
  - muse computes rSqrt and hypot exactly in integers (msf_alg.c:7-50); cft goes through the Ziv loop (transcend.c:2166-2178, 4317-4359).
- **Infrastructure:** cft passes a run-time format descriptor and a variable-length bignum by pointer (softfloat.c:10-16; bigint.h:52-60). muse generates per-format constants, instantiates per-format code by macro token-pasting (msf_performat.inc:12-16), and uses a fixed four-limb value type (msf_internal.h:37-54).

## History

- **Branches:** muse has 185 commits, and every branch is contained in HEAD.
- **No deletions:** no file was ever deleted (835 additions, 471 modifications, one rename, of a video file).
- **Additive growth:** the library grew by addition from P0 on 2026-10-26.
- **Only real rewrites:** msf_roundpack.c's generalisation (de2d48c) and its tininess fix (53acb1a). Its early version was further from cft, because it judged tininess on the delivered value.
- **No earlier drafts:** msf_aug.c and the transcendental code arrived complete in one to three commits, with nothing earlier to compare.

## Limits of this review

- **Not read in cft:** most of transcend.c (about 5,200 lines), mpfloat.c, reduce.c, program.c, device.c and the backends, conformance.c, the body of formatof.c, and the golden model beyond softfloat.py's rounding, division and square root.
- **Not read in muse:** the exp2 core (msf_math.c:1024-1210), most of msf16.c and msf32.c (sampled against msf64.c), hex input, compat/msf_wrap.c, the body of the generated header, and tests/.
- **No full literal matching:** I did no token fingerprinting beyond the comment pass; that is left to the separate run.
- **The clean room was enforced by rule and disclosure only:**
  - No mechanical fence existed (docs/KICKOFF.md:111-115).
  - The owner waived the fingerprint audit (docs/KICKOFF.md:196-198).
  - The shared owner approved muse's plans and its decision pins, which could carry design intent but not code (INFERRED).
- **From memory, not checked:** the claims about MPFR's manual and musl are from my own knowledge, not verified against those sources.

The only file written was a scratch script, /tmp/claude-0/-home-user/a5ed6180-6e84-5c9f-9e43-f754d57c15fd/scratchpad/structure/ngrams.py. Neither repository was modified.
