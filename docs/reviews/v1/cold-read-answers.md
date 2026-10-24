<!-- The cold reader's report on v1, extracted by script from the hand-back call that ends its transcript,
     unedited but for its absolute paths, written <scratch>/ (2) and <repos>/ (2) here, as round 6's
     verifier brief has a report write its paths. -->

## First, a clean-room disclosure

CLEAN-ROOM.md says to disclose this, so it comes before the answers. Before I ran anything, the harness loaded two local files into my context: `<repos>/cft-fp256/CLAUDE.md` and `<repos>/QRO-Crate/CLAUDE.md`. I did not open, list or search either path, or anything else outside my directory. No answer below uses them.

The cft-fp256 file holds that project's working notes: its verification runner and budgets, its build machines, its FPGA build traps, its simulation gates and the role of its golden model. It holds no source code.

CLEAN-ROOM.md's steps for this are: stop, write it in your own ledger, and escalate to the lead, who tells Logan. I have no ledger in this reading, so this report is my escalation. QRO-Crate is not restricted.

Kit files below are cited relative to `<scratch>/coldread/kit/softfloat-bootstrap-kit/`.

## Answers

1. **First step.** Run the kit's gate from the kit's directory: `python3 -I tools/check_kit.py`. It must end `VERDICT: PASS, all five checks hold`. If it does not, stop and tell Logan what it printed, because "the kit you hold is not the one that was built". `--control` shows that each check can fail. Then read CLEAN-ROOM.md. Sources: START-HERE.md, "First, before anything else"; WORKFLOW.md, Phase 0 step 1. The gate's docstring adds: exit 1 is a refusal; exit 2 is bad usage or no git, and then nothing passes; exit 3 means the gate itself failed, which is no verdict. MEASURED here: PASS, 5 of 5 checks, exit 0. `--control`: 59 of 59 plants caught.

2. **The off-limits repository** is Logan's cft-fp256. It counts in any form: on his GitHub account, its pages, raw files, API and archives, and any fork or mirror. It also covers its GitHub Pages site, a copy shown through another repository (such as a submodule's view), and pages of Logan's site that show it. The last is the lead's reading, which Logan may correct. Nothing else of his is restricted. If you opened it: stop, write the URL and what you saw in your own ledger file, and escalate to the lead, who tells Logan. It is judged on whether you disclosed it, and Logan audits the work against fingerprints of cft-fp256 at each wave's close. Source: CLEAN-ROOM.md, "What counts", "If a search lands there" and "The audit".

3. **What sends work back:** only a regression (a) or a wrong answer (b). Everything else merges as a recorded known limit. Sources: OWNER.md rule 1; ROLES.md; GLOSSARY.md, "What a verifier finds".
   - **A false sentence, when nothing else sends the work back:** the lead restates it at the merge, as a very small fix that goes past a verifier. Logan, 2026-10-13: "Lead fixes sentence at merge". If a send-back is going anyway, the author restates it. Sources: GLOSSARY.md, "How a false sentence is handled"; OWNER.md rules 1 and 4.
   - Rule 1 is one of the rules whose application is settled at kickoff.

4. **The ledger.**
   - **Where:** a directory outside every worktree, at a fixed absolute path that every brief states, ignored by version control. The lead makes it with templates/ledger.md as its README.
   - **Who writes what:** one file per author, append only: `P1.md`, `verifier-P2.md`, `lead.md`. Everyone reads every file and writes only their own. A verifier reads `lead.md` first and a parcel's file only after forming its own view. `urgent/` holds one file per message, `<who>-<slug>.md`, written elsewhere and renamed into place. `board.lock` lives there too.
   - **Corrections:** never edit an entry, even your own. Append the correction, and link it from the entry it corrects with a "see <time>" line.
   - **Heading times:** from `date`, never from memory. `tools/ledger.sh append` writes `## 2026-10-02 21:37:58 -0700 - headline`, and refuses a body without Measured:, Believed: and For: lines.
   - **At the round's end:** the ledger is archived with its timestamps and kept.
   - Sources: ParcelRound METHOD.md §4; templates/ledger.md; WORKFLOW.md, Phase 0; BOARD.md; tools/ledger.sh.

5. **When a parcel reads the ledger:** at three moments, which are the floor. Before it starts; before it designs anything that touches a file its brief calls shared or forbidden; and before it writes its report. It also does a full read on resuming after a pause, and whenever its watch dies or expires while it is still working. Sources: ROLES.md; METHOD.md §4; templates/ledger.md; templates/brief.md.

6. **A question only the lead can answer.** The parcel escalates. It writes the question in its own ledger file first, then sends it to the lead at once. It sends it either as an `urgent/` file (`tools/ledger.sh urgent`) or through the harness's messages, then waits for the answer. It does not leave the question in its file for the lead's next read, or hold it for its report. An escalation that turns out to be its own misreading is not penalised. Sources: METHOD.md §4, "Escalation: one rule"; templates/brief.md; START-HERE.md, "Five things", item 3.

7. **Planted-fault keys.**
   - **Who holds them:** the lead, for parcels: "The lead holds them for parcels" (Logan, 2026-10-23).
   - **Before dispatch:** the lead drafts the key in its own scratch directory, and `plant.py make` builds the copy. The key's sha256 goes in the ledger before the verifier is dispatched.
   - **The reveal:** once every verifier on a planted copy in the round has reported, later waves' included. That is day 10 in the proposed calendar. The lead then grades each plant caught or missed by reading. The integration verifier checks the grading with `plant.py check`.
   - **A suspected plant:** the verifier treats everything it finds as real and reports it. Round 6's verifier brief says: "The lead separates planted from real after your report." The verifier forms its view before reading the parcel's design, and never reads the lead's scratch directory.
   - Sources: OWNER.md; ROLES.md; WORKFLOW.md, "The planted-fault protocol" items 1 to 8 and Phase 6; method/parcelround/archive/round6-ledger.zip, `briefs/_verifier.md`.

8. **The Pico.** The lead controls it: "Lead controls hardware access" (Logan). A parcel asks for board time by the escalation channel. The lead runs the job itself, or grants a slot by name and by time, one holder at a time.
   - The lock is `<ledger>/board.lock`, holding the holder, the job and the time from `date`. You take it before touching the board and remove it by its exact path.
   - Each board result must name the ELF's sha256, the commit it was built from, the build flags and the board's id.
   - Sources: BOARD.md, "The protocol"; OWNER.md, "Not on the list: the board"; WORKFLOW.md, Phase 5.

9. **The IEEE 754 standard** is not in the kit. NOTICE.md says so, and the gate's check 1 refuses any PDF. Logan gives the lead the PDF outside the kit, licensed to him. It is the contract, meaning what conformance requires. It is not the authority the gates compare against: the study names an executable authority and its oracles, and Logan approves them. The kit's reading, for Logan to confirm, is that the PDF goes in no repository or zip and the record cites it by clause. Who else reads it is the lead's decision. Sources: CLEAN-ROOM.md, "The standard"; PROJECT.md; ROLES.md.

10. **Commits and pushes.**
    - **A parcel** never pushes, merges or rebases, and never commits to main. The brief template says "Commit inside your worktree only". Sources: ROLES.md; templates/brief.md.
    - **The lead** commits and pushes only on Logan's word, "until he says otherwise at kickoff", and Logan approves each push. Sources: START-HERE.md, item 4; OWNER.md rule 7; ROLES.md.
    - See issue B below: these two do not fully agree.

11. **The full suite.** No, a parcel should not run it. It tests as much as it can quickly and hands long runs to the lead to monitor (Logan, 2026-09-29, rule 2). The lead runs the full suite after merges, and on the tip before main moves. Sources: OWNER.md rule 2; ROLES.md; METHOD.md §7.

12. **The four evidence tags** (GLOSSARY.md, "The evidence tags"):
    - **MEASURED:** run in this round, with the output in hand.
    - **READ:** read, not run: a file and line, a commit, a report, a page or a search.
    - **COMPUTED:** arithmetic on figures that were measured or read, with the arithmetic shown.
    - **BELIEVED:** an estimate, an inference, or a claim not checked.

13. **What the lead settles with Logan on day 1, before the first dispatch:**
    - which standing rules apply;
    - the caps and the calendar (WORKFLOW.md proposes both);
    - the verifiers' tier;
    - the project repository and its private remote;
    - filling docs/HARNESS.md and docs/BOARD.md together;
    - recording his answers verbatim, with their date.

    The "ask first" list adds every commit and push, and how the PDF is held. Scope and PROJECT.md's questions go to him in the study on day 2. Sources: OWNER.md, "So, at kickoff" and "What the lead asks first"; WORKFLOW.md, Phase 0 step 2.

14. **The filled templates** go in the project repository, as docs/HARNESS.md and docs/BOARD.md. The kit is frozen: a changed file fails the gate's check 1, which compares every file's sha256 against MANIFEST.txt. The filled HARNESS.md is also part of the record, because which fallbacks were used is one of the results. Sources: START-HERE.md, item 5; HARNESS.md; BOARD.md.

15. **Verdicts:** READY or NOT READY. `round_metrics.py` accepts only those two. READY means "a gate, or a stated limit": every property of the work is held by a gate, or stated as a limit. A limit is tested by building a fault that passes every gate: if the fault lands outside the limit, READY waits until the limit is restated. Each numbered item in a verifier's report is marked confirmed, defect or not determined, and "found nothing" is an acceptable answer. Sources: GLOSSARY.md; METHOD.md §3 and §6; templates/verifier.md.

## Unclear, contradictory, or missing on day 1

- **A. The clean room and the harness (most urgent).** CLEAN-ROOM.md never mentions a local copy of cft-fp256 on the machine the agents use, or a harness that loads its agent notes on its own, which is what happened to me. HARNESS.md's only row on this is "a network policy". Separately, AGENTS.md quotes cft-fp256's agent notes (items 3 and 4), which CLEAN-ROOM.md's list of what the kit carries leaves out.
- **B. Commits.** Rule 7 says "nothing is committed" without Logan's word. But the brief template tells parcels to commit in their worktree, HARNESS.md's fallback is "local commits only", and `plant.py make` refuses a parcel with no commit of its own. So the planted-fault protocol cannot run until Logan rules on commits. Also unclear: whether "yes to remote" means he allows pushes, and on which host or account the private repository goes.
- **C. Which rules bind before kickoff.** ROLES.md states rules 1 and 2 as binding, while WORKFLOW.md and BOARD.md say "if it applies". Logan asked to "list all 8"; the kit lists 10, and rule 9 is not in his words.
- **D. ROLES.md line 5 claims more than is true.** It says the lead "runs on Meta's most capable model". Logan's words in OWNER.md begin "Not yet decided" and say "likely". The tier rules also name Claude models, and the kit cannot place Haiku.
- **E. The project's record.** Rule 10 lets an entry be restated in place until a push. HonestFramework (METHOD.md §7, README item 6, templates/ledger.md) says the record is append only, and never to edit a past entry's numbers. The kit's own reading applies rule 10 to exactly the file HonestFramework governs. "Ledger" also names three different things across the kit.
- **F. Correcting a ledger entry.** The method wants a "see <time>" line beneath the corrected entry. `ledger.sh` can only append at the end of the file, so under an older entry that line would be an insertion mid-file. The heading separator also differs: an em dash in the template, a hyphen in `ledger.sh`.
- **G. Absolute paths.** METHOD.md §4 says the ledger is at "a fixed absolute path". Round 6's verifier brief says never to write one, and that proposal (CS6#7) is still pending in ADOPTION.md. WORKFLOW.md takes in other pending round 6 lessons but is silent on this one, while the kit's gate refuses home paths that carry a name.
- **H. How a false sentence is classed.** GLOSSARY.md counts it as a (b), which normally sends work back. Round 6's brief makes "restated at the merge" a separate class. Which one is used changes the chain table's (b) counts and its send-back counts.
- **I. Plant tables per wave.** Plants are graded only at the reveal (day 10), yet each wave's record entry is meant to carry the plants table. The kit also never says outright that the ten days are one round (BELIEVED).
- **J. Blinding.** Nothing maps whether an agent can actually read the lead's scratch directory, where the keys are. Blinding rests on instruction only (BELIEVED).
- **K. The kit's provenance.** The gate checks files against a MANIFEST.txt inside the same zip, so a kit changed together with its manifest still passes. The manifest also says "builder ... no commit yet". Confirm these hashes with Logan out of band:
  - zip sha256: `59d3a1d994562933de1bda9787d71776a8308fabc0778b3579e0382b8e7c3a00`
  - MANIFEST.txt sha256: `124df9fba16faa0237aefd909ca0b225f473c65d5184757a380416aab940fa64`
- **L. A stale figure in START-HERE.md.** It says ParcelRound's METHOD.md is 78,786 bytes and 27,193 Read-tool tokens. The kit's copy is 78,224 bytes (by its own table and by `wc -c`), and my Read reported 26,833 tokens for it. The figures were MEASURED on another version.
- **M. Not in the kit.** The PDF, and how to share it with surveyors when it may go in no directory. The harness's capabilities, which Logan is determining live. Where the agents run; AGENTS.md assumes his Windows desktop (BELIEVED). The board's details. Logan's hours. Also, what "the ledger's own file" means in ROLES.md is unclear: BELIEVED to be its README.

## What I ran, and how long it took

Everything ran inside my directory, with `TMPDIR`, `HOME` and `GIT_CONFIG_NOSYSTEM` pointed there. Python 3.13.17, git 2.43.0.
- `unzip -l` and `sha256sum` on the zip, then `unzip -q -d kit`.
- `python3 -I tools/check_kit.py`: PASS, 2.6 s.
- `python3 -I tools/check_kit.py --control`: 59 of 59 caught, 5.1 s.
- The tools' self-tests: `bash tools/ledger.sh selftest` (21 checks), `python3 -I tools/plant.py selftest` (41), `python3 -I tools/round_metrics.py --selftest` (33). All passed with 0 failures.
- `unzip -l` and `unzip -p` on round6-ledger.zip, to read `briefs/_verifier.md`.
- Read and Grep on kit files.

I did not clone the QRO-Crate bundle, read the other archives, or read ParcelRound's case studies 1 to 5.

**Time (MEASURED, `date -u`):** 21:44:47Z to 21:52:13Z, so 7 min 26 s for everything. In that time I read about 470 KB, in whole or in part: every file on the everyone's and lead's lists, plus AGENTS.md, NOTICE.md, the tools, all 20 cases, WITH-PARCELROUND.md, HonestFramework's ledger template, parts of CASE-STUDY-6.md and the round 6 archive. The lead's prescribed reading is 245,966 bytes, about 61K tokens (COMPUTED from START-HERE.md's table).

**Files I left** in `<scratch>/coldread/`:
- `kit/`, the unpacked kit
- `control.out`, the `--control` output
- `metrics-selftest.out`
- `tmp/` and `home/`, both empty
