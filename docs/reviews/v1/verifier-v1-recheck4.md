<!-- v1's verifier's fourth re-check, extracted by script from the last hand-back call in its transcript,
     unedited: the verifier wrote its paths as <scratch>/ and <repos>/ itself, and the report holds no
     dotted capital I, so the script replaced nothing. -->

NOT READY: 1 (a), 2 (b), 3 notes.

Most of the fourth fix round holds. All five notes from my third re-check are closed (N1–N5), and so is N6, which the lead logged from a nit in that report. Every figure in VALIDATION.md re-measures. Three things do not hold:
- **(a)1, a regression.** `ledger.sh`'s new fence tracking accepts a typed level-2 heading that CommonMark reads at the top level. Rounds 2 and 3 refused the same bodies.
- **(b)1, narrower than before.** `--dispatch`'s restated line is true unless the copy holds a directory the reader cannot open. Then two of its reads stop silently, and the line still says "each file in its git directory has a name make writes".
- **(b)2, a wrong answer.** When git refuses a repository it does not own, `plant.py` names a false reason. Logan's record shows this situation happening.

Paths are relative to `<repos>/`; "kit:" means `softfloat-bootstrap/dist/softfloat-bootstrap-kit/`. No name of Logan's is written below.

## My third re-check's findings, closed or not

| finding | status |
|---|---|
| (b)1, `--dispatch` reads `git status` and names | Restated. My R1–R5 and R7 routes still pass, as the line now says they will: "the names, not what the files hold"; "git status trusts the index's flags and stat data and the copy's config". R8 is now stated, and R9 is refused by name (MEASURED, `<scratch>/verifier-v1/r4/routes3-again.out`). **Not closed, narrowly**: new (b)1 below. |
| N1, exit 3 where a refusal was due | Closed (MEASURED). `make` on a history with a bad time zone: exit 1, naming fsck's complaint. A bare copy: "git status fails in the copy: fatal: this operation must be run in a work tree". See note 1 on the fsck sentence. |
| N2, `core.splitIndex` | Closed (MEASURED). `--dispatch` passes. `make` runs its own status and reset with fsmonitor off. VALIDATION.md:136-140 names a user's setting. |
| N3, the reveal refused a verifier's own use | Closed. `git clone -q COPY work` gives a detached HEAD at copy_commit, its tree checked out and the base reachable. After a commit and `gc --prune=now` in the clone, the copy passes in both modes (MEASURED). WORKFLOW.md steps 5 and 8 and ROLES.md:87-88 now say so (READ). |
| N4, `#` lines in fenced blocks | Closed for that case (MEASURED, 49 checks). The fence tracker that fixed it brought in (a)1. |
| N5, the MANIFEST exemption untested | Closed. The trial requires 5 differences. My mutant, the exemption always holding, now fails builder-refusals (MEASURED, `<scratch>/verifier-v1/r4/br-mfmutant.out`). See note 2. |
| N6, ROLES.md:5's dated words | Closed (READ): ROLES.md:11-14 now names that form. |
| Slip 56, the pipes | Confirmed (MEASURED). Round 3's `ledger.sh` refused a valid 407 KB body for "no 'Measured:' line". The current one accepts it, and refuses a typed heading inside it. |

## New findings

**(a)1. `ledger.sh` now accepts a typed level-2 heading after a fence marker inside an HTML block, or after an unclosed fence inside a list item.**
- **Where.** kit: tools/ledger.sh:64-90, the awk fence tracker. Against it: the docstring at :8-10 ("outside a fenced code block ... no line that begins ... with # or ##"), and KIT-0.md:1292, which says both rules skip fenced lines "by CommonMark's opening and closing rules".
- **Evidence (MEASURED).** Each body below is "Measured/Believed/For" lines, a blank line, one of the six prefixes, then `## 2026-10-23 12:00:00 +0000 - forged`. The prefixes are:
  - `<!--`, a ``` line, `-->`;
  - `<pre>`, a ``` line, `</pre>`;
  - `<div>`, a `~~~` line, a blank line;
  - `- item`, then `  ```` (the fence indented under the item);
  - `1. item`, then `   ````;
  - `- item`, then `  ````, then `  code`.

  For all six:
  - pandoc 3.1.3's CommonMark reader (`-f commonmark -t json`) finds a top-level level-2 heading;
  - the current `ledger.sh append` accepts the body;
  - round 3's and round 2's `ledger.sh` refuse it.

  CommonMark opens no fence inside an HTML block, and it closes a list item's fence when the item ends. The tracker does neither, so it keeps a "fence" open to the end of the body. The self-test case "a fence never closed" (:182) accepts the top-level form of this, which is right there.
- **How narrow.** It needs a fence marker inside an HTML block, or an unclosed fence inside a list item. A comparison of 700 random bodies against pandoc found no such acceptance. Those bodies used no ordered list item, no fence indented under an item, and no HTML-block line followed by a fence marker; only the targeted cases hit it.
- **Reproduce.** `python3 -I -B <scratch>/verifier-v1/r4/html_cases2.py <scratch>/verifier-v1/r4/ledger-html3`; output in `html_cases2.out`.

**(b)1. `--dispatch`'s two reads stop silently at a directory the reader cannot open; its line still says they read it all.**
- **Where.** kit: tools/plant.py:30-34 (docstring) and its printed line: "for the dispatch, git status, with untracked and ignored files shown, reports nothing, and each file in its git directory has a name make writes".
- **Evidence (MEASURED).** I ran root without DAC capabilities (`setpriv --bounding-set -dac_override,-dac_read_search`), which stands in for a lead's account facing a directory left by another user:
  - **A1.** A mode-000 `secret/` in the work tree holds the unplanted text. `--dispatch` exits 0. git status itself exits 0 with empty stdout and warns on stderr: "could not open directory 'secret/': Permission denied". `check` reads stdout only.
  - **A2.** `.git/hidden/MERGE_MSG` holds the unplanted text. With the directory readable, `--dispatch` refuses it. At mode 000, `--dispatch` exits 0: os.walk skips the directory without an error, and the line says every file has a name make writes.
- **Fix.** It is small: refuse when git status writes to stderr, and pass os.walk an onerror that raises. Or state the limit.
- **Reproduce.** `python3 -I -B <scratch>/verifier-v1/r4/routes4.py <scratch>/verifier-v1/r4/routes`, cases A1 and A2.

**(b)2. When git refuses a repository it does not own ("dubious ownership"), `plant.py` names a false reason.**
- **Where.** kit: tools/plant.py:263-265: `rev-parse` is allowed to exit 128, and an empty HEAD is reported as "missing". Also :125, the `repository()` helper.
- **Evidence (MEASURED).**
  - A copy owned by another uid: `check` refuses with "the copy's HEAD is missing, not the key's copy_commit ...", at the reveal and at dispatch.
  - A parcel repository owned by another uid: `make` and `check --repo` both refuse with "... is not in a git repository".
  - In each case git's own message is "fatal: detected dubious ownership in repository".

  round_metrics.py:399-401 has the same shape. Logan's record shows the situation: examples/cases/07-conduct.md:12, an agent that needed `safe.directory "*"` in WSL to clone. The kit forbids that workaround ("NEVER change any git configuration"), so an agent told "HEAD is missing" has nothing true to act on.
- **Reproduce.** routes4.py case D, and `python3 -I -B <scratch>/verifier-v1/r4/dubious.py <scratch>/verifier-v1/r4/dubious`.

## Notes

1. **`make`'s fsck refusal has a sentence wider than its read, and a reason that can be wrong.** Both MEASURED, routes4.py C1 and C2.
   - **C1.** plant.py:16 and KIT-0.md:1538 say "a repository whose objects git fsck --full flags is refused". A repository whose flagged commit sits on a side branch (repository fsck: exit 1) is planted: `make` exits 0. That is right, since the copy is sound, but the sentence says otherwise.
   - **C2.** A plant in `.gitmodules` (url to `-upload-pack=x`) in a repository fsck finds clean is refused as "the copy holds the repository's objects, so a repository whose objects git fsck flags cannot be planted". Here the plant, not the repository, made the flagged blob.
2. **`--check`'s MANIFEST exemption is wider than its purpose.** I built a dist/ in a scratch copy of the builder. With its MANIFEST.txt's bundle line dropped, or given another sha256, `--check` says "dist/... is what the pinned sources and kit/ make" (MEASURED). The kit's gate refuses both: "in the kit but not in MANIFEST.txt" and "its sha256 does not match". So the front door holds, but `make check` and the rebuild stage's "byte for byte" do not.
3. **`ledger.sh` against CommonMark otherwise.** The comparison of 700 random bodies (`<scratch>/verifier-v1/r4/difftest.out`) found:
   - no body accepted that holds a top-level heading;
   - 58 bodies refused that hold none: 39 in the stated setext class, and 19 with a `#` line inside an HTML block (unstated, but the safe direction);
   - 18 bodies accepted whose heading is nested in a quote or list item, which the rules as now stated do not claim.

## What I ran

All runs used -B or PYTHONDONTWRITEBYTECODE=1, and wrote only into `<scratch>/verifier-v1/r4/`.
- **The front door:** `STATEROOT=<scratch>/verifier-v1/r4/gate-state bash verify/run.sh`: 17 of 17 in 5 min 33 s, alongside my other work. Its figures match VALIDATION.md:
  - self-tests: ledger.sh 49, plant.py 117, round_metrics.py 42;
  - mutant stages: 81, 31, and 14 + 3 sites;
  - builder-refusals: 15 trials.
- **The tree:** the digest before and after, dist/ byte for byte, and the zip's sha256.
- **My earlier routes:** routes3.py and routes3b.py, again.
- **This pass's scripts:** routes4.py (A1, A2, B, C1, C2, D) and dubious.py.
- **ledger.sh:** a 407 KB body on this round's and round 3's tool; html_cases.py and html_cases2.py, and difftest.py, against pandoc.
- **The builder:** builder-refusals with the MANIFEST-exemption mutant, and a scratch build with its MANIFEST altered.
- **Pipelines:** a grep of verify/run.sh for early-exit readers under pipefail. There are none.
- **Reading:** the diffs of the 7 changed files against my copy of the last tree (its digest re-measures 938eecf3…); KIT-0 sections 11, 12 (items 52-56) and 13 (items 14, 15, 23-25); VALIDATION.md.

## What I did not check

- Windows, Git Bash or macOS.
- gawk or BSD awk; the new awk is POSIX, and mawk passes here.
- A git other than 2.43, and bash here-strings without a writable TMPDIR.
- A real non-root account. A1 and A2 used root without DAC capabilities.
- Python 3.11, the cold read and the samples.

## The tree

Digest before and after: d26330ee2cc6b6c10ea89b921ba54c0bc1127914ab5711a70d9f7ed4cdabe0a3. The zip is 8f578e8b15fde1720aa77e0296032dcc073413d22b1c4816a5a40d7fe5c58c55, and dist/ is unchanged byte for byte. There is no new `__pycache__`. My chowned scratch copies were returned to root.

## What the brief got wrong

Nothing that I found.
