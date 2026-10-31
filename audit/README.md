# The audit of the project repository

The kit's clean room ends with an audit: "Logan checks the project repository against fingerprints of
cft-fp256's sources ... A match decides nothing by itself; it opens a question, and the record answers it"
([kit/CLEAN-ROOM.md](../kit/CLEAN-ROOM.md), "The audit"). This directory is that audit's tooling, and a
cross-test of the two libraries that uses each one's tests on the other. Its first run, of 2026-10-31, and what
it found are in [docs/AUDIT-1.md](../docs/AUDIT-1.md).

**Clean room: nothing here goes to the project repository or into the kit.** The tools and their results
describe cft-fp256's code, which is exactly what the clean room keeps from the project's agents. Nothing in
`audit/` is in `kit/` or `build/`, so the kit the builder makes is unchanged by it.

## Run it

```
bash audit/setup.sh          # pinned inputs into dist/audit/: 25 s here, the network once
bash audit/run.sh            # every step: 10 min 48 s on 4 cores, 2026-10-31
bash audit/run.sh --quick    # every step at a small fraction of the volume: a few minutes
```

- **What it needs:** git, Python 3 with venv, Node 22, gcc, make, curl and unzip.
- **The repositories:** muse-softfloat and cft-fp256, each with its whole history (`git fetch --unshallow`), beside
  this one, as the builder's sources are.
- **The variables:**
  - `SOURCES` (default: this repository's parent directory);
  - `MUSE_REPO` and `CFT_REPO`, to name a repository elsewhere;
  - `MUSE_REV` and `CFT_REV` (default `HEAD`), to audit another commit;
  - `AUDIT_WORK` (default `dist/audit/`, which git ignores).
- **Git objects, not working trees.** Every tool reads the repositories as git objects at named revisions, as
  the builder does: the fingerprints read every blob of every ref, and the cross-test runs trees `setup.sh`
  exports with `git archive`.
- **Where the outputs go:** each step's whole output goes to `dist/audit/results/<step>.txt`, and
  `SUMMARY.txt` gathers their last lines.
- **The controls are steps too.** A control that does not hold fails its step:
  - 17 planted copies of cft-fp256 functions must be caught at their planted lines;
  - planted wrong answers must be caught;
  - each library's own corpus must pass through its own side;
  - the exact arbiter must agree with the x86 SSE unit and with Berkeley SoftFloat 3e.

## What is where

| path | what it is |
|---|---|
| [setup.sh](setup.sh) | pinned Python (numpy, mpmath, gmpy2); Berkeley SoftFloat/TestFloat 3e by sha256; both trees from git objects; the native builds; cft-fp256's fp32/fp64 vector sets regenerated, each checked against its `vectors/SHA256SUMS` |
| [run.sh](run.sh) | every step below, in order, with the controls' own checks |
| [fingerprint/fp.py](fingerprint/fp.py) | the tokenizer (C-like, Python, shell), k-gram hashing, reading git blobs |
| [fingerprint/run_fp.py](fingerprint/run_fp.py) | every k-gram of every muse-softfloat blob, on every ref and with its copy of the kit left out, against every cft-fp256 blob; exact (k = 24) and normalised (k = 40); baseline: Berkeley 3e and the kit; plants the 17 controls |
| [fingerprint/analyze.py](fingerprint/analyze.py) | the controls by planted-line overlap; each muse path's strongest cft-only overlap and its complexity; the longest runs, side by side |
| [fingerprint/features.py](fingerprint/features.py) | shared high-entropy constants, identifiers, string literals and comment phrases, minus the baseline and the kit's prose |
| [fingerprint/vecfp.py](fingerprint/vecfp.py) | high-entropy hex words of muse's test data that occur anywhere in cft-fp256, decoded |
| [crosstest/xlib.mjs](crosstest/xlib.mjs) | adapters over the two WebAssembly modules, as shipped: muse's `site/msf.wasm`, cft's `bindings/node/cft_node.wasm` |
| [crosstest/opsmap.mjs](crosstest/opsmap.mjs) | 324 descriptors, one per operation and format both libraries have, with the call on each side |
| [crosstest/corpus.mjs](crosstest/corpus.mjs), [crosstest/gen.mjs](crosstest/gen.mjs) | bit helpers and operand pools; the TestFloat-style generator |
| [crosstest/smoke.mjs](crosstest/smoke.mjs) | both modules loaded, a few operations each |
| [crosstest/replay_cft_full.mjs](crosstest/replay_cft_full.mjs) | cft-fp256's published corpus through both modules: cft's own is the control, muse's the test |
| [crosstest/replay_muse_vec.mjs](crosstest/replay_muse_vec.mjs) | muse-softfloat's committed vectors through both modules, the other way round |
| [crosstest/bigdiff.mjs](crosstest/bigdiff.mjs) | the random differential on four workers. `MUTANT=1` plants wrong answers. It writes a 1-in-997 sample for the arbiter |
| [crosstest/check_sample.py](crosstest/check_sample.py) | that sample against the exact arbiter: are both libraries right, not only agreed |
| [crosstest/intcheck.mjs](crosstest/intcheck.mjs) | integer conversions of out-of-range and infinite operands |
| [crosstest/oracle.py](crosstest/oracle.py) | the exact arbiter for the basic operations: rationals, five attributes, tininess either way, five flags |
| [crosstest/oracle_math.py](crosstest/oracle_math.py) | the eight shared 9.2 functions: exact for rSqrt and hypot, an MPFR Ziv loop for the rest |
| [crosstest/validate_oracle.py](crosstest/validate_oracle.py), [hostref.c](crosstest/hostref.c), [sfref.c](crosstest/sfref.c) | the arbiter checked against the x86 SSE unit and against Berkeley SoftFloat 3e |
| [native/xnative.c](native/xnative.c) | one program linking both libraries at their revisions: augmented pairs and character conversions, which msf.wasm does not run |
| [native/native_replay.py](native/native_replay.py) | both corpora's augmented and character records through it, each with its control |
| [native/classes.py](native/classes.py) | each documented-policy class that replay reports, checked case by case to be what it claims |
| [native/dense.c](native/dense.c) | the eight shared functions over contiguous binary32 ranges |
| [native/exp2m1_probe.c](native/exp2m1_probe.c) | the cft-fp256 exp2m1 defect at emax+1: every attribute, its four formats, and muse's two |
| [results/2026-10-31/](results/2026-10-31/REVS.txt) | the first run's outputs, as `run.sh` wrote them |
