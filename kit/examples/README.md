# Examples

Prior work done with these methods, for its form and its handling. This file is an index into what the kit already
carries; it holds no copies.

Read a member of an archived ledger without unpacking it:

    python3 -I -c "import sys, zipfile; print(zipfile.ZipFile(sys.argv[1]).read(sys.argv[2]).decode())" \
        ../method/parcelround/archive/round6-ledger.zip parcelround-r6-ledger/briefs/_common.md

or unpack one into your own scratch directory with `unzip`.

## Samples of how things were handled

Passages of cft-fp256's record, one situation a file, each sample with its source, what it shows, and what was cut.
The record is not in this kit; its arithmetic is cut from every line that names it (CLEAN-ROOM.md).

<!-- cases:begin -->
<!-- cases:end -->

## Whole rounds: briefs, ledgers, verifiers

In [method/parcelround/archive/](../method/parcelround/README.md), each round has a case study beside it in
method/parcelround/.

**Round 6, ParcelRound run on itself** (`round6-ledger.zip`, under `parcelround-r6-ledger/`; CASE-STUDY-6.md):
- `briefs/_common.md`: what every parcel's brief shares;
- `briefs/P1.md` to `P5.md`: parcel briefs;
- `briefs/_verifier.md`: a verifier's brief for a copy that may hold planted faults;
- `briefs/integration.md`: an integration verifier's brief, on the lead's own work;
- `keys/key-*.json`: planted-fault keys, in the format `tools/plant.py` reads. They show plant shapes (WORKFLOW.md's
  limits);
- `README.md`: a ledger's README;
- `lead.md`: a lead's ledger;
- `P*.md`: the parcels' ledgers;
- `verifier-*.md`: the verifiers' ledgers.

**Round 5, a personal site** (`round5-ledger.zip`, under `loganw-dev-ledger/`; CASE-STUDY-5.md):
- `briefs/_common.md`;
- the parcel briefs;
- `briefs/verifier-seam.md`: a verifier on the lead's own commits;
- `urgent/`: escalations, one file each, both ways;
- `lead.md`, and each agent's ledger.

**Round 4, two repositories** (`round4-ledger.zip` and `round4-second-ledger.zip`; CASE-STUDY-4.md):
- three parcel briefs, under `quantum-film-round1-ledger/briefs/`;
- a verifier on the lead's P0 that went at least five passes;
- the lead's second round, alone with one verifier.

**The other case studies** (CASE-STUDY.md to CASE-STUDY-3.md) tell rounds whose ledgers are not in this kit.

Some lines in these ledgers name tools of the harness they ran in, such as SendMessage, ToolSearch, Monitor, or a
worktree made by `isolation`. Read them as that harness's; HARNESS.md maps each one to yours.

## A real project: QRO-Crate

`git clone -b main ../reference/QRO-Crate.bundle QRO-Crate`, then read:
- **CLAUDE.md:** its agent notes. A front door, and a list of what has already cost time.
- **verify/run.sh:** its runner, the front door, with budgets and skips by name.
- **docs/studies/QRO-0.md:** a plan of record. Its verifiers' reports on its twelve drafts are in
  docs/reviews/QRO-0/.
- **docs/reviews/P0/ to P0.5/:** every verifier's report on the lead's P0 work, round by round, and where the loose
  cap was reached (OWNER.md, rule 6).
- **docs/VALIDATION.md:** its record, one dated entry for each piece of work and each verifier round.
- **qro/vocabulary.py with tools/gen_vocabulary.py:** one fact in one place, with the rest generated and held by
  `--check`.
- **controls/ and tools/check_privacy.py:** planted faults for each shape a gate refuses.

Its pace was six verifier rounds on one P0, which a ten-day round cannot afford (WORKFLOW.md, caps). It cites
cft-fp256 by file and line, and those citations dangle by design.
