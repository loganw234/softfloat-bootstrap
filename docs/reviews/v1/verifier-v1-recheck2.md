<!-- v1's verifier's second re-check, extracted by script from the last hand-back call in its transcript,
     unedited: the verifier wrote its paths as <scratch>/ and <repos>/ itself, and the report holds no
     dotted capital I, so the script replaced nothing. -->

NOT READY: 0 (a), 2 (b), 8 notes.

The second fix round closes the two routes my re-check named, and every figure in VALIDATION.md re-measures. Two (b) remain.
- **(b)1.** The fix for my re-check's (b)1 is restated wider than the code: "`check` refuses a copy that holds a planted file's text at real_tip by any route". `check` reads the copy's objects by id only. A copy whose work tree, an unindexed pack, or a rewritten loose object holds the unplanted text passes it.
- **(b)2.** One refusal of the builder is outside both new stages and has no control: `--check`'s comparison of dist/. With that comparison disabled, all 17 stages pass.

No regression found.

Paths are relative to `<repos>/`. "kit:" means `softfloat-bootstrap/dist/softfloat-bootstrap-kit/`. No name of Logan's is written below.

## My re-check's findings, closed or not

| finding | status |
|---|---|
| (b)1, a copy holds the unplanted text through the base's history | **Closed for that route.** `make` now refuses my cases B (file restored), C (moved unchanged) and D (left as the base had it), naming "text at real_tip is in the base's history", and leaves no copy (MEASURED). The new `check` refuses the three copies the old tool made: "holds the unplanted text of x.md, as blob 3eaab481…" (MEASURED). **The restatement claims more** than `check` does: new (b)1. |
| (b)2, the mutant stages' reach | **Closed for the forms named.** refusal-mutants: 71 sites, each caught (MEASURED). Each of the 14 `raise BuildError(` sites, taken out alone, fails its own trial and no other trial (MEASURED, `<scratch>/verifier-v1/r2/bmap.out`). **Not closed** for one builder refusal written another way: new (b)2. |
| (b)3, ROLES.md:9 | Closed in substance: lines that cite nothing are now called the kit's summary. The new sentence is nearly true: note 6. |
| (b)4, CLEAN-ROOM's code inventory | Closed (READ). I listed every code span the kit quotes from cft-fp256's record that is longer than 18 characters or holds an operator. Each is a file, function or command name, a short test or runner expression, a tb Makefile line, or a tool's output. None is arithmetic. |
| (b)5, 4b | Closed (READ). Record lines 23382-23392 are "4. Known limits", and 23392 is that section's last line; the entry runs on to 23397. |
| N1 | Closed: kept, and stated in KIT-0. By hash (USER_NAMES), the token before "@" at round 4's verifier-P0.md:391 is his first name, and no domain follows (MEASURED). |
| N2 | Closed. A tools/`__pycache__` in a kit copy gives check 1 three findings and check 4 five, as START-HERE.md:105-107 now says (MEASURED). |
| N3 | Closed for its spellings (self-test 36 checks, MEASURED). A setext heading still passes: note 3. |
| N4 | Closed at the git directory's top level only: note 1. |
| N5 | Closed (READ). ROLES.md:5-8 quotes OWNER.md:13's sentence whole and marks the reading as the kit's. |
| N6 | Restated; nearly true: note 7. |
| N7 | Closed (READ): kit: tools/check_kit.py:24-27 and CLEAN-ROOM.md:64-66. |

## New findings

**(b)1. `check` claims more than it reads.**
- **Where.**
  - softfloat-bootstrap/docs/KIT-0.md:1244: "check refuses a copy that holds a planted file's text at real_tip by any route".
  - KIT-0.md:1451-1454, section 13 item 14: "check refuses one that holds more".
  - kit: tools/plant.py:403-405, the line `check` prints: "...differs from real_tip only by the plants; ... and no planted file's text at real_tip".
  - kit: WORKFLOW.md:146-148, step 8: "the copy differs from the parcel's tip only by the plants".
- **Evidence (MEASURED, with dist's plant.py).**
  - Setup: a repository with a base, a parcel commit adding `return x <= n;`, and a tip that changes another line of src.c. One plant on src.c: "x <= n" to "x >= n". Each copy comes from `make` with the right base, then has the fault applied, then `check --key --repo --copy`.
  - Each of these exits 0 and prints the sentence above:
    1. **The copy's work tree holds src.c as real_tip has it, uncommitted.** `git status` shows ` M src.c`; the file hashes to real_tip's blob (15c03bdf…); `git diff` shows `-  return x >= n;` and `+  return x <= n;`.
    2. **The key itself is copied, untracked, into the copy** (`?? notes.json`).
    3. **A pack of the unplanted blob sits in `.git/objects/pack/` with no `.idx`.** A fresh repository's `git index-pack --stdin` recovers the text from that file. `git count-objects -v` says garbage 1; fsck exits 0, with a warning.
    4. **The planted blob's loose object is rewritten to hold real_tip's text under the planted id.** `git show HEAD:src.c` in the copy prints `return x <= n;`. `git fsck --full` refuses it ("hash-path mismatch").
- **Why it matters.** Routes 1 and 2 are what a verifier reads first. A verifier may change its own work tree before it reports, so `check` cannot hold the work tree. Its printed sentence and section 11 should say what it does read.
- **Reproduce.** `python3 -I -B <scratch>/verifier-v1/r2/scripts/routes.py <scratch>/verifier-v1/r2/routes` (cases F1a, F1b, F2; output in `<scratch>/verifier-v1/r2/routes.out`). Then `python3 -I -B <scratch>/verifier-v1/r2/scripts/swap.py <scratch>/verifier-v1/r2/routes`.

**(b)2. The builder's `--check` comparison is outside builder-refusals and builder-mutants, and nothing watches it fail.**
- **Where.**
  - softfloat-bootstrap/build/build_kit.py:346-363 (`compare_trees`) and :424-429 ("CHECK FAILED", exit 1). The module docstring counts this exit as one of the builder's own ("1 when ... a check disagrees").
  - verify/run.sh:257-262: both new stages say "each refusal of the builder".
  - KIT-0.md:1245: "Each of the builder's 14 refusals has a trial".
- **Evidence (MEASURED).**
  - I copied the builder to `<scratch>/verifier-v1/r2/ct-builder` and added `return diffs` after `compare_trees`'s `diffs = []` (line 349). `bash verify/run.sh` there, with SOURCES=`<repos>/`, gives passed 17, failed 0 (`<scratch>/verifier-v1/r2/ct-run.out`).
  - With build_kit.py restored and one byte appended to the copy's dist ROLES.md, `--check` prints "CHECK: differs: ROLES.md" and "CHECK FAILED: 1 difference(s)", exit 1. So the code is right, but the rebuild stage has only ever been seen to pass. bundle-compare covers only the bundle's comparison.
  - This is the class of my re-check's (b)2: the line-count guard that no stage watched.
- **CLAUDE.md item 7, as asked.** True as worded. The forms it names are exactly what the stages find (COMPUTED from the sources, MEASURED in the stage logs):
  - ledger.sh: 9 `die "`;
  - `raise Refused(`: 31 in plant.py and 16 in round_metrics.py;
  - plant.py's copy-condition appends: 15 (71 in all with the above);
  - check_kit.py's finding sites: 31;
  - the builder's `raise BuildError(`: 14.

  It says a refusal written another way is not found. Two existing ones are written another way: this one, which is untested, and plant.py's first copy condition (note 8), which is tested.

## Notes

1. **N4 is closed at the top level only.** `check` globs `*_HEAD` and reads `logs/refs/` only directly in the git directory (kit: tools/plant.py:250, :253). A linked worktree's `.git/worktrees/w/ORIG_HEAD` and `.git/worktrees/w/logs/HEAD`, each naming the parcel's tip, pass `check` (MEASURED, routes.py F3). KIT-0.md:1252's "any *_HEAD ..., and any reflog of a ref" reads wider than that.
2. **A copy made on the wrong base passes `check`.** `make` accepts any ancestor of real_tip as `--base`. With the parcel's own first commit given as the base, `check` passes, though the copy holds that parcel commit and its src.c holds the unplanted line (MEASURED, F4). `check` finds "the parcel's own commits" from the copy's own parent (plant.py:214), and the key holds no base. So the docstring's "none of the parcel's own commits" (plant.py:23) is only relative to whatever base was given, and nothing says so. Also measured: the copy takes real_tip's message by default (stated), and here that message names the unplanted text (F5). That is what a real defect against its message looks like, so I do not count it as a leak.
3. **ledger.sh misses setext headings.** A body line followed by `---` (or `===`) is a heading as Markdown reads one, and ledger.sh appends it (MEASURED, exit 0, `<scratch>/verifier-v1/r2/ledger/case1.md`). kit: tools/ledger.sh:54-55 says it refuses "a level-2 heading as Markdown reads one". ATX level-1 headings also pass; level 3 is allowed on purpose.
4. **builder-mutants runs no unmutated baseline and needs only an exit code** (tests/controls.py:369). refusal-mutants and finding-mutants also require FAIL or MISSED in the output (:426, :449). With SOURCES an empty directory, `verify/run.sh --only builder-mutants` passes in 0 s, saying "14 refusals ... each time builder-refusals failed" (MEASURED, `<scratch>/verifier-v1/r2/bm-vac.out`). builder-refusals fails unmutated in that state. A full run is not fooled, because builder-refusals fails first.
5. **Section 13 item 15 is stale.** KIT-0.md:1459 still says "the tools' 55 refusals". The tools now hold 56 refusals (the base-history refusal is new) plus 15 copy conditions, 71 in all. VALIDATION.md:74 has 71 right.
6. **ROLES.md:11-13 is nearly true.** ROLES.md:34 cites BOARD.md, not OWNER.md, for Logan's "Lead controls hardware access"; OWNER.md:17 also has it. Lines 30, 31, 35, 36, 38, 92 and 98 point to other kit pages, which is neither form the sentence names.
7. **CLEAN-ROOM.md:57's "each cited by its line" is nearly true.** METRICS.md:46-48 and GLOSSARY.md:38-40 cite samples (20b, 20a), and OWNER.md:73-75 cites the record's header rather than a line.
8. **refusal-mutants' description overstates its reach by one.** It says "each of plant.py's copy conditions" (run.sh:243), but never takes out the first: the HEAD condition is a `return [` (plant.py:234). Taken out by hand, the self-test fails ("not the key's copy_commit"; MEASURED, `<scratch>/verifier-v1/r2/mut-head/out.txt`). CLAUDE.md's "each copy condition plant.py's check appends" is exact.

## The brief's other questions

- **3. Regressions.** None found. I diffed all 13 changed files and ran the full front door. On a legitimate plant, `make` and `check` pass. The `load_sources` change makes "is not a commit" reachable, and its trial shows it.
- **4. Section 13 item 20, as restated.** It now says what is true (MEASURED, by name built from pieces at run time):
  - 21 occurrences: 7 of one name and 14 of the other.
  - One is in a bundle blob: docs/reviews/P0/round5.md at 8afeede.
  - The other 20: 4 in samples 03, 07 and 17, 1 in CASE-STUDY-3.md, and 15 in round 4's archived ledger.
- **VALIDATION.md's figures all re-measure:**
  - 17 of 17 stages, in 3 min 54 s here; the mutant stages took 93, 93 and 10 s.
  - The mutant stages' sites: 71, 31 and 14.
  - Self-tests: 36, 93 and 42 checks.
  - The build: 73 files, each rule's count as declared, and METHOD.md at 1,448 lines, as its source has.
  - The gate's controls: 80 of 80 plants and 96 of 96 spellings.

## What I ran

All of it with PYTHONDONTWRITEBYTECODE=1 or -B, and all writes in `<scratch>/verifier-v1/r2/`.
- The full front door: `STATEROOT=<scratch>/verifier-v1/r2/gate-state bash verify/run.sh`. Afterwards I checked dist/ byte for byte against my dispatch snapshot, and the zip's sha256.
- builder-refusals unmutated, in a copy holding only build/, kit/ and tests/ (passes), and with no sources (fails).
- `bmap.py`: each builder refusal site's mutant.
- The disabled-comparison builder copy, and builder-mutants alone with no sources.
- `routes.py` and `swap.py`, plus fsck and count-objects on their copies.
- My re-check's cases B, C and D through the new `make`, and its old copies through the new `check`.
- The HEAD-condition mutant.
- Six heading spellings through ledger.sh.
- The gate on a kit copy with a `__pycache__` written on purpose.
- `machines.py`, and the hash check at round 4's verifier-P0.md:391.
- Reading: KIT-0 sections 11, 12 (items 42-46) and 13 (items 14, 15, 20, 22); VALIDATION.md; the restated kit texts; and the record's lines 23376-23400.

## What I did not check

- Python 3.11, Windows and Git Bash, or git other than 2.43.
- The cold read.
- Sample texts other than 4b.
- Whether each tool mutant fails for its intended reason; I checked only that the stage passes.
- Other files in a copy's .git: rebase-*, sequencer/, rr-cache/, MERGE_MSG. I BELIEVE `check` reads none of them.
- Who could realistically write each route.

## The tree

Digest before and after: 189820e695cdefd034080f8ef669006e92d042b394e69d5c28ed0061c92e75fa. The zip is 1fb81970a679dcdb506cb43c5748254e56e4595a39a6c8ef62d5842a2eb8563c before and after, and dist/ is unchanged byte for byte.

`kit/tools/__pycache__/` and `build/__pycache__/` hold .pyc files dated 22:52 to 23:41 UTC, before dispatch, so they are not mine. They are outside the digest by .gitignore.

## What the brief got wrong

"Every file but those under docs/reviews/v1/" leaves out that ignored files (dist/, .gate-state/, `__pycache__/`) are excluded too. "Taken as before" covers it.
