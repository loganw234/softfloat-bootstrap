<!-- v1's verifier's sixth re-check, extracted by script from the last hand-back call in its transcript,
     unedited: the verifier wrote its paths as <scratch>/ and <repos>/ itself, and the report holds no
     dotted capital I, so the script replaced nothing. -->

READY: 0 (a), 0 (b), 0 notes (under the loose cap, as the brief holds it).

My fifth re-check's one (b) is closed: `--check` now compares the manifests byte for byte. A dist/ that differs from the build in its manifest, or in its bundle's content, is refused, and one that is the same still passes. I found no regression and nothing new.

Paths are relative to `<repos>/`. No name of Logan's is written below.

## My fifth re-check's finding

**(b)1, `--check` treating the manifest's line endings and last line end as no difference: closed.** All MEASURED. I copied build/ and kit/ into `<scratch>/verifier-v1/r6/root`, built a dist/ there, changed it, and ran `--check` and the kit's gate on it (`<scratch>/verifier-v1/r6/cases6.py`, output in `cases6.out`).

**It refuses a dist/ that differs, by its manifest.** Each of these exits 1, "CHECK FAILED: 1 difference(s)":
- CR LF line ends;
- no last line end;
- a U+2028 in place of one line feed;
- the bundle's line moved up one line;
- the bundle's line written twice;
- a CR on the bundle's line alone;
- the bundle's hash in capitals;
- a trailing space on another line;
- a byte-order mark first;
- one more line end at the end.

The kit's gate passes most of these, so `--check` is the stage that holds them.

**It refuses a dist/ that differs, by its bundle.** Each exits 1, with the manifest's line updated to name the changed bundle:
- the same refs with one more object in the pack;
- junk appended after the pack;
- one more ref;
- a prerequisite line added.

**It still passes one that is the same.** Each exits 0:
- the dist/ as built;
- the same objects repacked into other bytes and named so by the manifest, the exemption's purpose;
- a v3 bundle of the same refs and objects, named. The bytes are other but the content the same, which the exemption allows.

**The new controls do what they say:**
- An exemption that never holds (`return False`) fails bundle-compare: "does not pass --check: CHECK: differs: MANIFEST.txt". With the code restored, bundle-compare passes.
- builder-refusals has 19 trials and passes.

## New findings

None.

## Regressions

None found. The full front door passes, and dist/ comes out byte for byte as it was.

## What I ran

All runs used -B or PYTHONDONTWRITEBYTECODE=1, and wrote only into `<scratch>/verifier-v1/r6/`.
- **The front door:** `STATEROOT=<scratch>/verifier-v1/r6/gate-state bash verify/run.sh`: 17 of 17 passed in 6 min 46 s. The stage logs show:
  - bundle-compare with its new control;
  - builder-refusals: 19 trials;
  - builder-mutants: 14 + 3 sites;
  - refusal-mutants: 87 sites;
  - finding-mutants: 31 sites;
  - self-tests: ledger.sh 49, plant.py 125, round_metrics.py 43.
- **The tree:** the digest before and after; dist/ against my snapshot and against the fifth dispatch's (the same); the zip's sha256.
- **The faults:** cases6.py, as above.
- **The never-holding mutant:** bundle-compare in a builder copy, mutated and then restored.
- **Reading:** the diffs of build/build_kit.py, tests/controls.py and verify/run.sh against my copy of the fifth re-check's tree; KIT-0 section 11's new row and section 12, item 61; VALIDATION.md's sixth-round section and its section on the cap.

## What I did not check

- Another git's own bundle bytes. I made "other bytes" by repacking with compression 0, and by bundle format v3.
- Windows or Git Bash.
- Python 3.11.
- The kit itself, which this round did not change: its bytes are the same as at my fifth re-check.

## The tree

Digest before and after: 6e456ad6017f88b7de013c35a4542c8bf730a58f0b2b24ac3ab4feb4435f17a1. The zip is 0c36e7df969ed42967004bc7be9765307ea17a7684996225ba6f83aee0ced364, and dist/ is unchanged byte for byte. There is no new `__pycache__`.

## What the brief got wrong

Its "What changed" leaves out verify/run.sh, whose bundle-compare stage now ends "; a repacked bundle its manifest names passes --check" (run.sh:240). The change matches the new control.
