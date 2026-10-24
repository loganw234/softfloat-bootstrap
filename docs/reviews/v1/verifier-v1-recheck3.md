<!-- v1's verifier's third re-check, extracted by script from the last hand-back call in its transcript,
     unedited: the verifier wrote its paths as <scratch>/ and <repos>/ itself, and the report holds no
     dotted capital I, so the script replaced nothing. -->

NOT READY: 0 (a), 1 (b), 5 notes.

The third fix round closes (b)2 and all eight notes. (b)1 is half closed:
- **The reveal:** `check`'s line now says exactly what it reads, and every route from my second re-check is refused where it says or left out where it says it does not read.
- **`--dispatch`:** its line, its docstring and WORKFLOW.md step 2 say "its work tree and index are its commit's" and "holds the copy as make left it". What it actually reads is `git status`, which the copy's own index bits and config can steer, plus the names of the git directory's files. Three copies whose work tree holds the unplanted text pass it.

No regression found. One rule is now stricter than its own comment says (note 4).

Paths are relative to `<repos>/`; "kit:" means `softfloat-bootstrap/dist/softfloat-bootstrap-kit/`. No name of Logan's is written below.

## My second re-check's findings, closed or not

| finding | status |
|---|---|
| (b)1, `check` claims more than it reads | **Reveal: closed** (MEASURED with my old routes, `<scratch>/verifier-v1/r3/oldroutes.out`). The work tree and the key copied in pass at the reveal, as its line says ("its work tree and its git directory's other files were not read"). The unindexed pack, the hand-made `worktrees/w/ORIG_HEAD` and the rewritten object are refused in both modes. **`--dispatch`: not closed**, see (b)1 below. |
| (b)2, `--check`'s comparison | **Closed** (MEASURED). The new trial passes. My earlier mutant (`return diffs` at the top of `compare_trees`) now fails it. builder-mutants takes out 17 sites, each caught. |
| N1, linked worktree | Closed: refused in both modes (MEASURED). |
| N2, wrong base | Closed: stated in plant.py:33-34 and WORKFLOW.md step 2, and `make` prints the parent. |
| N3, setext and level-1 headings | Closed (41 checks, MEASURED). See note 4 for a side effect. |
| N4, builder-mutants with no sources | Closed: the stage now fails, "builder-refusals fails with nothing taken out" (MEASURED, `<scratch>/verifier-v1/r3/bm-vac.out`). |
| N5, section 13 item 15's count | Closed. 10 + 32 + 16 refusals, 21 conditions, 14 + 3 builder sites (COMPUTED; stage logs agree). |
| N6, ROLES.md:11-13 | Closed. One nit: ROLES.md:5 cites Logan's words by name and date, which is none of the three forms the sentence lists. |
| N7, CLEAN-ROOM.md:57 | Closed. |
| N8, the HEAD condition | Closed: it is now an append, and the stage takes it out (79 sites). |

## New findings

**(b)1. `check --dispatch` says it holds the work tree and the git directory; it reads `git status` and file names.**

Where:
- kit: tools/plant.py:30-32 (docstring): "With --dispatch, it also holds the copy as make left it: its work tree and index are its commit's, with no untracked or ignored file, and its git directory holds no file but those make writes".
- kit: tools/plant.py:471, the printed line: "for the dispatch, its work tree and index are its commit's, ...".
- kit: WORKFLOW.md:133-135: "holds the copy as `make` left it: its work tree is its commit's".
- docs/KIT-0.md:1268 ("a changed, untracked or ignored file ... are refused"), :1497-1498 ("also its work tree and every file of its git directory") and :1545-1547 (item 24).

Evidence (MEASURED, dist's plant.py, git 2.43). Setup as before: one plant on src.c, "x <= n" to "x >= n". `check --dispatch` exits 0 and prints the line above on each of these copies:
- **R1.** `git update-index --skip-worktree src.c`, then real_tip's src.c written into the work tree. `git status` is empty; `git ls-files -v` shows `S src.c`; the file holds `return x <= n;`.
- **R2.** The same with `--assume-unchanged`.
- **R3.** `core.worktree` in the copy's config pointed at a clean checkout elsewhere, and the copy directory's own src.c unplanted.
- **R8.** A same-size edit with its mtime put back, under `core.trustctime=false`, which emulates Git for Windows. There st_ctime is the file's creation time (BELIEVED, from git's compat/mingw.c), so an mtime-preserving edit leaves the stat data matching.
- **R4, R5, R7.** These contradict "as make left it", though not the printed line's "no file but those make writes":
  - R4: the unplanted text as a comment in `.git/config`;
  - R5: as the message of an extra HEAD reflog entry from the copy commit to itself;
  - R7: after the id in `.git/HEAD`.

  All three files are ones `make` writes, so all three pass in both modes.

A replaced `.rev` is refused by fsck, as it should be.

R1 to R3 need someone to set git state on purpose, as the rewritten object of my last report did. By the brief's test ("say what it reads, and no more"), the line should say "git status --ignored reports nothing", or `check` should read more: index flags (`git ls-files -v`), the config's content, or a hash of each work-tree file.

Reproduce: `python3 -I -B <scratch>/verifier-v1/r3/scripts/routes3.py <scratch>/verifier-v1/r3/routes` (R1-R7, R9), then `python3 -I -B <scratch>/verifier-v1/r3/scripts/routes3b.py <scratch>/verifier-v1/r3/routes-b` (R8). Output is in `routes3.out` and `routes3b.out` beside them.

## Notes

1. **Two inputs end in exit 3, "the tool failed", where a refusal by name is due.** Both MEASURED, routes3b FR1 and routes3 R9.
   - **A parcel repository whose history `git fsck` flags.** I used a base commit with a bad time zone, as some imported histories have. `make` exits 3: "ToolFailed: the copy is not what it should be: git fsck --full refuses the copy's objects: ... badTimezone". No copy can be made, and nothing states this. Logan's four source repositories are fsck-clean (MEASURED, read-only).
   - **A copy whose config sets `core.bare=true`.** `check --dispatch` exits 3, because `git status` fails.
2. **A user's git setting can make `--dispatch` refuse a copy exactly as `make` left it.** Under `core.splitIndex=true`, `make`'s git writes `sharedindex.<id>`, and `--dispatch` refuses it as "a file make does not write" (MEASURED). VALIDATION.md's new limit names "another git, or Windows"; a setting does it too. The failure is in the safe direction.
   - No false refusal (MEASURED): `core.autocrlf=true`, `core.eol=crlf` with LF, CRLF and mixed files, untracked cache, index v4, `pack.writeReverseIndex=false`, `core.logAllRefUpdates=false`, `gc.auto=1`.
   - Untested: `core.fsmonitor=true` on macOS or Windows. `make`'s own `git status` runs without `-c core.fsmonitor=false`, so it would start the daemon there (BELIEVED).
3. **At the reveal, `check` refuses a copy its verifier used in ordinary ways** (MEASURED, `<scratch>/verifier-v1/r3/vuse.out`):
   - a linked worktree for a clean build, a refusal that is new this round;
   - `git add` of an edit, then undone (an object HEAD does not reach);
   - `git stash` then pop;
   - a checkout of the base and back (the reflog).

   ROLES.md:86 asks the verifier to "re-run the gate from a clean build". Nothing in WORKFLOW.md or ROLES.md tells it to leave the copy's git state alone, so step 8's check will often refuse for the verifier's own work. Read-only use, and output files, pass.
4. **ledger.sh's level-1 rule refuses a fenced shell comment.** A body holding a fenced block whose line begins "# the gate" is refused as a heading. The second round's ledger.sh accepted it. The rule's comment (ledger.sh:55) says it refuses "a level-1 or level-2 heading as Markdown reads one". Its stated over-refusal is the setext rule's (:61), and the message gives no way round (indent the block four spaces).

   None of the 510 entries in the kit's archived ledgers would be refused by either rule (MEASURED, `<scratch>/verifier-v1/r3/scan_ledgers.py`). Headings inside a blockquote, inside a list item, or as HTML `<h2>` pass (MEASURED). That is outside the docstring's "either of Markdown's spellings". mawk passes the self-test here; the script is POSIX awk, so I BELIEVE gawk and BSD awk behave alike.
5. **`--check`'s MANIFEST.txt exemption has no control.** In a builder copy, I made `manifest_equal_but_bundle` return True: all 17 stages pass (MEASURED, `<scratch>/verifier-v1/r3/mf-run.out`). Under that mutant, a dist/ whose MANIFEST.txt names another ParcelRound commit passes `--check`. The real code refuses it ("CHECK: differs: MANIFEST.txt", MEASURED). The new trial changes three files but never MANIFEST.txt. This is a test gap where the code is right.

## What I ran

All runs used -B or PYTHONDONTWRITEBYTECODE=1, and wrote only into `<scratch>/verifier-v1/r3/`.
- **The front door:** `STATEROOT=<scratch>/verifier-v1/r3/gate-state bash verify/run.sh`: 17 of 17 passed, in 5 min 14 s alongside my other work. Its figures match VALIDATION.md:
  - self-tests: ledger.sh 41, plant.py 112, round_metrics.py 42;
  - mutant stages: 79, 31, and 14 + 3 sites;
  - builder-refusals: 15 trials;
  - the gate's controls: 80 and 96.
- **The tree:** the digest before and after, dist/ byte for byte, and the zip's sha256.
- **The fault scripts:** routes3.py, routes3b.py, oldroutes.py, verifier_use.py and crlf.py.
- **ledger.sh:** six heading cases on both versions, and the archive scan.
- **Builder mutants:** my old `return diffs` mutant through builder-refusals; builder-mutants with no sources; the widened MANIFEST exemption, with a full run.
- **Read-only:** `git fsck` on the four source repositories.
- **Reading:** the diffs of the 11 changed files against my copy of the last tree (its digest re-measures 189820e6…); KIT-0 sections 11, 12 (items 47-51) and 13 (items 7, 14, 15, 22-24); and VALIDATION.md.

## What I did not check

- Windows or Git Bash, macOS, gawk, BSD awk, or a git other than 2.43.
- The fsck checks a newer git adds.
- `core.fsmonitor` on macOS or Windows.
- Python 3.11.
- The cold read and the samples.
- Other places to hide bytes in files `make` writes, such as an index extension.

## The tree

Digest before and after: 938eecf38ff85a696cbc6dcc1a996dfc2c71a270e8e08512890af3a0bca5cccb. The zip is b4e5471884bb54ccefe27cadee03bd7ae016c788af9ae7633cc16eceee0fa113, and dist/ is unchanged byte for byte. No `__pycache__` is newer than my dispatch snapshot.

## What the brief got wrong

Nothing that I found. Its "What changed" names where the round is described. The tree's diff also touches README.md (one line), CLAUDE.md, verify/run.sh, tests/controls.py and five kit files, each consistent with section 11.
