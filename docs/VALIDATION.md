# The record

Each entry is dated, and each claim carries its tag: MEASURED, run in this repository with the output in hand;
READ, read at a named place; COMPUTED, arithmetic on those; BELIEVED, an estimate or a claim not checked.

History is what has been pushed: until then an entry is restated in place when a verifier sends its work back,
keeping each pass's figures beside the new ones (Logan's rule of 2026-10-22, in cft-fp256's record; the kit's
OWNER.md, rule 10). Nothing here has been pushed yet.

## 2026-10-23 to 2026-10-24: v1 built; its cold read; its verifier's first pass and six re-checks, the sixth READY; six fix rounds

### What Logan asked, verbatim

His first request and every answer since are in [KIT-0.md](KIT-0.md), section 1. These are the words this entry
acts on, all of 2026-10-23 but the last:
- on the plan's draft 3: "Approved if nothing major changes from the check";
- on the push: "Go ahead once it passes", meaning once v1's verifier finds it READY;
- on the project repository: "Kickoff";
- on the QRO-Crate bundle's commits: "Real address is fine";
- on QRO-Crate's code that follows cft-fp256's documented rules: "Keep";
- on stripping an archive's personal data: "Okay to strip, not vital however";
- on the loose cap, 2026-10-24, after v1's fourth re-check had reported: "Go ahead and apply rule 6 for this pass".

### The chain

| work | author | verifier's passes, (a), (b) | sent back |
|---|---|---|---|
| KIT-0, draft 1 | the lead | the plan verifier 6, 10 | once |
| KIT-0, draft 2 | the lead | the plan verifier, re-check: 1, 4 | once |
| KIT-0, draft 3 | the lead | none: Logan approved it on the condition above | no |
| the samples' candidates | a read-only surveyor | none: the lead read every candidate whole, and v1's verifier read every sample | no |
| v1: the kit and this builder | the lead | v1's verifier 0, 12, with 15 notes; 0, 5, with 7 notes; 0, 2, with 8 notes; 0, 1, with 5 notes; 1, 2, with 3 notes; under the loose cap, 0, 1, with no note, and then READY: 0, 0, with no note | six times |
| the cold read of v1 | a cold reader, with only the zip | none: graded by the lead against a key written first | no |

The reports are in [reviews/KIT-0/](reviews/KIT-0/README.md), with the drafts they read, and in
[reviews/v1/](reviews/v1/verifier-v1.md).

### The cold read (MEASURED, its three steps by `date`)

- **The key** was stamped here before the reader was dispatched: sha256
  `d54936304912183183b6d2648231afd12751c37c4cbfd894a71be5858ebe4fe2`, at 2026-10-23 21:42:02 +0000.
- **The reader** worked from 21:44:47 to 21:52:13 +0000, on the zip of sha256 `59d3a1d9...` alone.
- **The reveal,** at 21:56:13 +0000: the key hashed to the value stamped.
- **The grade:** 15 of 15 right, none partly, no invention
  ([reviews/v1/cold-read-grading.md](reviews/v1/cold-read-grading.md)).
- **The blinding is the record's, not git's.** Nothing could be committed before v1's verifier passed, so the order
  of the three steps rests on these stamps and the agents' transcripts (KIT-0, section 13, item 13).
- **The reader did not have quite nothing else:** this harness loaded cft-fp256's and QRO-Crate's agent notes into
  its context, because those repositories were attached to this session. It disclosed this first. That became the
  kit's new clean-room rule, "A copy on the machine" (its finding A).
- **Its findings A to M** are ruled in the grading; six were sentences of the kit that claimed more than was true.

### v1's verifier, first pass: NOT READY, 0 (a), 12 (b), 15 notes

The report is [reviews/v1/verifier-v1.md](reviews/v1/verifier-v1.md). The lead reproduced the four heaviest findings
before acting (MEASURED): a copy made by `plant.py` held a planted file's original blob; a bundle cut to its header
passed the gate; a dotted capital I took a path past the prefilter; the kit's METHOD.md had 1,436 lines against its
source's 1,448. KIT-0, section 11, gives each finding and what the fix round did with it, and section 12 the lead's
slips the round found (29 to 41).

### v1's verifier, its re-check: NOT READY, 0 (a), 5 (b), 7 notes

The report is [reviews/v1/verifier-v1-recheck.md](reviews/v1/verifier-v1-recheck.md). Its first pass's findings
closed, but two; the five new (b) are a copy that could still hold the unplanted text through the base's history, a
mutant stage that claimed more reach than it had, and three sentences that claimed more than was true. KIT-0,
section 11, gives each and what the second fix round did, and section 12 the slips (42 to 46).

### v1's verifier, its second re-check: NOT READY, 0 (a), 2 (b), 8 notes

The report is [reviews/v1/verifier-v1-recheck2.md](reviews/v1/verifier-v1-recheck2.md). It found no regression, and
every figure the second fix round recorded here re-measured. Its re-check's findings closed for the routes and forms
they named. Its two new (b) are claims wider than the code: `plant.py check`'s "by any route", where it read a copy's
objects by id, and "each refusal of the builder", where `--check`'s comparison had no trial. The verifier measured
both. The lead did not re-run them on the old tools; it ran each route against the new `check`, which refuses each
(its self-test's cases), and the verifier's mutant of the comparison against the new trial, which then fails
(MEASURED).
KIT-0, section 11, gives each finding and what the third fix round did, and section 12 the slips (47 to 51).

### v1's verifier, its third re-check: NOT READY, 0 (a), 1 (b), 5 notes

The report is [reviews/v1/verifier-v1-recheck3.md](reviews/v1/verifier-v1-recheck3.md). It found no regression, and
every figure the third fix round recorded here re-measured. Its second re-check's findings closed, but for (b)1 in
`--dispatch`, whose sentences said it held the work tree where it reads what `git status` reports, which the index's
flags and the copy's config can steer. The lead reproduced its note 1's first case before acting (MEASURED: `make`
exited 3 on a history whose base commit has a bad time zone). KIT-0, section 11, gives each finding and what the
fourth fix round did, and section 12 the slips (52 to 56). Slip 56 is the lead's own find in this round: `ledger.sh`
turned a large body's answer round, in both directions, since it was written.

### v1's verifier, its fourth re-check: NOT READY, 1 (a), 2 (b), 3 notes

The report is [reviews/v1/verifier-v1-recheck4.md](reviews/v1/verifier-v1-recheck4.md). Every figure the fourth fix
round recorded here re-measured, and its third re-check's findings closed. Its (a) is the fourth round's own: the
fence tracker `ledger.sh` gained let a typed level-2 heading through, which rounds 2 and 3 refused. Its two (b) are a
read that stopped silently at a directory it could not open, and a false reason when git refused a repository it
did not own. KIT-0, section 11, gives each finding and what the fifth fix round did, and section 12 the slips (57 to
60).

### v1's verifier, its fifth re-check, under the loose cap: NOT READY, 0 (a), 1 (b), 0 notes

The report is [reviews/v1/verifier-v1-recheck5.md](reviews/v1/verifier-v1-recheck5.md). Its fourth re-check's six
findings closed, each by a run, and every figure re-measured. Its one (b) blocks under the cap, as a line the builder
prints said what was not so: `--check`'s manifest exemption compared lines, not bytes, so a MANIFEST.txt with CR LF
line ends or no last line end passed, and the rebuild stage said "byte for byte". The lead reproduced it before acting
(MEASURED: the two new trials, run on the old comparison, exit 0). KIT-0, section 11, gives what the sixth fix round
did, and section 12 the slip (61).

### v1's verifier, its sixth re-check, under the loose cap: READY, 0 (a), 0 (b), 0 notes

The report is [reviews/v1/verifier-v1-recheck6.md](reviews/v1/verifier-v1-recheck6.md). Its fifth re-check's one (b)
closed, measured on ten manifests and four bundles that differ from the build, each refused, and three that are the
same, each passed; it found no regression and nothing new. With no note, the verdict is READY without the cap as
well, so it does not rest on the lead's reading of the cap's scope. The brief's "What changed" left out verify/run.sh,
whose bundle-compare line the round changed (KIT-0, section 12, item 62). This is Logan's condition for the push, "Go
ahead once it passes".

### The loose cap, not applied to the third and fourth passes, applied to the fifth and sixth

This was v1's third NOT READY, and the reasons have narrowed: from a copy that leaked the unplanted text and a gate
that passed an unreadable bundle, to a claim wider than its code and a test gap where the code is right. So the
condition of Logan's loose cap (the kit's OWNER.md, rule 6; QRO-Crate's CLAUDE.md, item 6) is met. But which
standing rules apply is his to decide (the kit's ROLES.md), and he has not applied this one to the kit's own
verification: the second re-check's brief said the lead would consider it "if Logan applies it". So the third and
fourth re-checks ran without the cap, and the lead put the choice to him after the second.

After the fourth re-check had reported, he applied it: "Go ahead and apply rule 6 for this pass" (2026-10-24). The
lead reads "this pass" as the next one, the fifth, as the fourth had reported when his word came. Its brief tells the
verifier that only a defect in what the code does blocks; prose, test gaps where the shipped code is right, and other
non-code findings become notes, which the lead takes in before the commit. The fourth re-check's own three findings
would have blocked under the cap too: an accepted typed heading, a printed claim of a read that did not happen, and
a false reason for a refusal are each a defect in what the code does.

The fifth re-check found one such defect, and no note. The sixth checks only the fix for it, and the lead holds the
cap for it too: Logan's word was for "this pass", the fifth, but he gave it to stop the send-backs over prose, and
the sixth pass closes the fifth's one finding. That reading is the lead's, for him to overrule.

### v1 after the sixth fix round (MEASURED, in this container, on the uncommitted tree)

Each figure stands beside the ones it replaced: at dispatch, then after the first five fix rounds.

- **`bash verify/run.sh`:** 17 of 17 stages passed, nothing skipped, in 6 minutes 37 seconds (run 20261024-023330;
  its id reads `nogit`, as nothing is committed). At dispatch, 13 of 13 in 23 seconds; after the first fix round,
  15 of 15 in 3 minutes 4 seconds; after the second to the fifth, 17 of 17 in 3 minutes 57 seconds, 5 minutes 23
  seconds, 5 minutes 36 seconds and 6 minutes 17 seconds. The mutant stages take 187, 113 and 48 seconds of it (185,
  112 and 35 after the fifth round).
- **The mutant stages:** each of 87 sites of the agent tools, which are ledger.sh's 10 refusals, plant.py's 35 and its
  25 copy conditions, and round_metrics.py's 17 (81 after the fourth round, 79 after the third, 71 after the second,
  55 after the first, which missed the copy conditions); each of the gate's 31 finding sites; and each of the
  builder's 14 refusals and the 3 differences its `--check` records (14 after the second round, which missed the
  comparison). Each, taken out alone, fails its self-test, the gate's `--control` or builder-refusals, and each of
  those first passes with nothing taken out (since the third round). builder-refusals has 19 trials (17 after the
  fifth round, 15 after the third and fourth, 14 after the second), and bundle-compare holds the comparison's
  exemption from both sides: a bundle repacked into other bytes, its manifest naming it, passes `--check` (new).
- **The build:** 73 files, as before. The rules' counts: R1 12, R2 3, R3 3, R4 15, R5's names 121, addresses 13 and
  fragments 7, R6 5, as before. Each equals its declaration, and no rule changes a file's line count: the kit's
  ParcelRound METHOD.md has 1,448 lines, as its source does (at dispatch, 1,436).
- **The kit's gate:** `VERDICT: PASS, all five checks hold`. Its controls: 80 of 80 plants caught, each by the finding
  that names it (at dispatch, 59 of 59, eight of them by any finding), and 96 of 96 spellings with a letter `re` folds
  found (since the first round). With the old fold, 15 of those are missed.
- **The tools' self-tests:** `ledger.sh` 49 checks (21 at dispatch, then 31, 36, 41, 49 and 49 after the first five
  rounds), `plant.py` 125 (41, 84, 93, 112, 117, 125), `round_metrics.py` 43 (33, 42, 42, 42, 42, 43), none failed.
- **Under Python 3.11:** the build's check, the gate, its controls, the three self-tests, builder-refusals and
  bundle-compare pass.
  Python 3.9 and 3.10 are not installed here, so the builder's "3.9 or later" is BELIEVED for them; the code parses
  under 3.11, and holds no feature newer than 3.7 that the lead knows of.
- **The zip, before its sixth re-check:** 1,973,893 bytes, sha256
  `0c36e7df969ed42967004bc7be9765307ea17a7684996225ba6f83aee0ced364`, as after the fifth round, as the sixth changed
  no file of the kit (after the fourth round, `8f578e8b...`; after
  the third, `b4e54718...`; after the second, `1fb81970...`; after the first, `20958f28...`). Its manifest's builder
  line still reads "no commit yet". The zip Logan receives is rebuilt after the first commit, whose hash that line
  then names, and the run that builds it is recorded here.

### Known limits carried

- **Check 3's term list** is a stated limit: it cannot see arithmetic described in other words. The lead read every
  sample whole, and v1's verifier read them again.
- **The kit's tools ran in this container, on Linux,** with git 2.43, Python 3.13 and 3.11, and mawk as `awk`. On
  Logan's Windows desktop, under Git Bash, they are BELIEVED to run: they use only bash, coreutils, POSIX awk, git and
  Python's standard library, and they remove read-only files as they go, as git on Windows needs.
- **`plant.py check --dispatch` holds the list of files `make` writes** into a copy's git directory as git 2.43 wrote
  them here. Under another git, another of the user's git settings, or on Windows, it is BELIEVED to be the same:
  `core.splitIndex` was one such setting, found by v1's third re-check, and its shared index is now on the list. A
  git or a setting that wrote another file there would have `check --dispatch` refuse the copy, naming that file,
  not pass it.
- **`--dispatch` is the lead's check against a slip,** not a defense against a copy built to pass it: `git status`
  trusts the index's flags and stat data and the copy's config, and a file's name, not what it holds, is what
  `--dispatch` reads of the git directory.
- **Two of Logan's machines' names** are in the kit, as his published texts spell them (KIT-0, section 13, item 20).
- **The cold reader is an agent of the harness that built the kit.** What it shows is that the kit tells a reader
  with nothing else the fifteen things the questions ask. It shows nothing about how Meta's models will read it.
- **The scratch directories** of the surveyor, the plan's verifier and v1's verifier, with their scripts, were in
  this container and are not kept. Their reports say what they ran.
