<!-- v1's verifier's fifth re-check, extracted by script from the last hand-back call in its transcript,
     unedited: the verifier wrote its paths as <scratch>/ and <repos>/ itself, and the report holds no
     dotted capital I, so the script replaced nothing. -->

NOT READY: 0 (a), 1 (b), 0 notes (under the loose cap).

The fifth fix round closes all six findings from my fourth re-check, each confirmed by a run. Its new code holds against the faults I picked. One defect blocks under the cap, because a line the builder prints says what is not so:
- `--check` passes a dist/ whose MANIFEST.txt differs byte for byte outside the bundle's line, in its line endings or its final newline.
- It then prints that dist/ "is what the pinned sources and kit/ make", and the rebuild stage prints "byte for byte".
- This is not a regression. The exemption has compared lines with `splitlines()` since it was written, and was rewritten this round without changing that.

Paths are relative to `<repos>/`; "kit:" means `softfloat-bootstrap/dist/softfloat-bootstrap-kit/`. No name of Logan's is written below.

## My fourth re-check's findings, closed or not

| finding | status |
|---|---|
| (a)1, the fence tracker let a typed heading through | **Closed** (MEASURED). All six forms from my last report are refused again, as rounds 2 and 3 refused them. In a fresh comparison of 700 bodies against pandoc's CommonMark reader, no body that CommonMark reads with a top-level level-1 or level-2 heading is accepted. The refusals of fenced `#` lines that follow are stated in the usage text ("errs toward refusing"). |
| (b)1, reads that stopped silently at an unreadable directory | **Closed** (MEASURED, as root without DAC capabilities via `setpriv`). An unreadable directory in the work tree is refused at dispatch ("check cannot read 1 directory of the copy's work tree, secret first") and passes at the reveal, as stated. An unreadable directory in .git is refused in both modes. An unreadable tracked file, an unreadable untracked file, and a directory readable but not searchable are each refused at dispatch. |
| (b)2, a false reason when git refuses a repository | **Closed** (MEASURED). A copy owned by another uid: "git will not read the copy: fatal: detected dubious ownership ...", in both modes. Such a repository given to `make`, to `check --repo` and to `round_metrics.py --repo`: "git will not read ... as a repository: fatal: detected dubious ownership ...". A `--repo` or `--copy` that is a file, or absent, is refused by name. |
| N1, `make`'s fsck sentence and reason | **Closed** (MEASURED). A flagged object outside what the copy holds still lets `make` build, which is what the restated docstring now says. A plant that makes fsck flag `.gitmodules` is refused, with a reason that no longer blames the repository. |
| N2, the MANIFEST exemption | **Closed for the two forms I named** (MEASURED): a bundle line left out, or naming another sha256, is refused by `--check` and by the gate. **The legitimate case still passes** (MEASURED): the bundle repacked into other bytes (12,143,878 against 1,072,660), its manifest line naming it, gives `--check` exit 0. **The exemption is still wider than "the bundle's line alone"**: see (b)1. |
| N3, `ledger.sh` against CommonMark | **Closed:** stated in the usage text. In the 700-body comparison, the 16 bodies accepted with a heading only nested in a quote or list item are of the forms the text says are not refused. |

## New finding

**(b)1. `--check` treats MANIFEST.txt's line endings and final newline as no difference, then says dist/ is what the sources make, byte for byte.**

**Where.**
- softfloat-bootstrap/build/build_kit.py:387-398, `manifest_equal_but_bundle`. It splits both manifests with `splitlines()`, which treats CRLF, a lone CR, U+2028 and a missing final newline as no difference.
- The two printed lines that then say what is not so:
  - `--check`: "check: dist/softfloat-bootstrap-kit is what the pinned sources and kit/ make";
  - verify/run.sh:227, the rebuild stage: "a second build is dist/, byte for byte".
- The function's docstring and KIT-0.md:1309 ("may differ in the bundle's line alone") claim the same. The two new trials change only the bundle line, so nothing tests this.

**Evidence (MEASURED, in copies under `<scratch>/verifier-v1/r5/`).** I took a fresh dist/ and changed only its MANIFEST.txt, three ways:
- every LF made CRLF;
- the final newline removed;
- one line feed replaced by U+2028.

Each time `--check` exits 0 with the line above, and the kit's gate passes too ("VERDICT: PASS, all five checks hold"). In a builder copy with a CRLF MANIFEST.txt (cmp: differs at char 31), `bash verify/run.sh --only rebuild,kit-gate` prints "rebuild ok ... a second build is dist/, byte for byte" and passes both stages.

**How much it matters.**
- It needs dist/'s MANIFEST.txt rewritten after a build, with its content kept, for example by an editor that saves CRLF.
- A full `verify/run.sh` rebuilds dist/ in its first stage, so the full front door cannot be fooled this way. `make check` and `run.sh --only rebuild` can.
- The zip stage would then pack the changed manifest.

**Fix.** Compare the non-bundle lines exactly, for example `read_bytes().split(b"\n")`, and add a trial with a CRLF manifest.

**Reproduce.** Copy build/ and kit/ into a scratch root, build its dist/, convert its MANIFEST.txt to CRLF, then run `python3 -I -B <root>/build/build_kit.py --check --sources <repos>/`. Output is in `<scratch>/verifier-v1/r5/mf-root/check-crlf.out`, `check-nofinal.out` and `check-ls2028.out`.

## Notes

None. The new code's sentences match what it does, as far as I measured. The exemption's docstring and KIT-0's N2 row are the prose side of (b)1.

## What I ran

All runs used -B or PYTHONDONTWRITEBYTECODE=1, and wrote only into `<scratch>/verifier-v1/r5/`.
- **The front door:** `STATEROOT=<scratch>/verifier-v1/r5/gate-state bash verify/run.sh`: 17 of 17 in 6 min 25 s, alongside my other work. Its figures match VALIDATION.md:
  - self-tests: ledger.sh 49, plant.py 125, round_metrics.py 43;
  - mutant stages: 87, 31, and 14 + 3 sites;
  - builder-refusals: 17 trials.
- **The tree:** the digest before and after, dist/ byte for byte, and the zip's sha256.
- **Faults:** routes5.py (A1-A5, D, the non-directory inputs), and my fourth re-check's routes4.py again (C1, C2).
- **ledger.sh:** html_cases2.py on this round's tool and on rounds 2 and 3, and difftest.py (700 bodies against pandoc 3.1.3).
- **The manifest exemption:** drop, rehash, CRLF, no final newline and U+2028 against `--check` and the gate; a repacked bundle; a builder copy through `--only rebuild,kit-gate`.
- **Reading:** the diffs of the code files against my copy of the fourth re-check's code (round 3's tree with round 4's kit/, tests/ and build/ laid over it), and KIT-0 sections 11, 12 (items 57-60) and 13 (items 14, 15, 23), and VALIDATION.md.

## What I did not check

- Windows, Git Bash or macOS.
- gawk or BSD awk.
- A git other than 2.43.
- A real non-root account; I used root without DAC capabilities.
- Python 3.11, the cold read and the samples.

## The tree

Digest before and after: b8ae910f218a9717cc6c797050cad7042caa523197385e48918f8407c8d8811f. The zip is 0c36e7df969ed42967004bc7be9765307ea17a7684996225ba6f83aee0ced364, and dist/ is unchanged byte for byte. There is no new `__pycache__`, and my chowned scratch copies were returned to root.

## What the brief got wrong

Nothing that I found.
