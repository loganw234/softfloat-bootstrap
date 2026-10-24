# KIT-0: the bootstrap kit for the Meta softfloat hackathon

**Draft 1, 2026-10-23. The lead's (this session). Not approved.** Nothing in
this directory is committed and no repository has been created. This draft goes
past a verifier before it reaches Logan (ParcelRound METHOD.md section 7: "The
plan of record, and a verifier on it before the owner approves it").

Evidence tags, as Logan's records use them (section 4.2 defines them for the
kit): **MEASURED** is a command run in this session, its output in hand;
**READ** is read at a named file and line, not run; **COMPUTED** is arithmetic
on measured or read figures; **BELIEVED** is neither. Paths are relative to
`<repos>/`. Sources read: HonestFramework at `65447fd`, ParcelRound at
`f42242e` (a shallow clone of 61 commits), QRO-Crate at `8afeede`, cft-fp256 at
`39f9801` (shallow).

---

## 1. What Logan asked, verbatim (2026-10-23)

The request:

> I plan to take part in a hackathon hosted by Meta AI, the goal is to develop
> an IEEE-754 compliant softfloat for RP2040, for binary16/32/64. The math
> library is only one portion of the project, the other portion is testing how
> Meta models handle the methods and systems I use, along with heavy metrics
> tracking (cfts most recent work has been tracked the most I believe)
> But I’d like to give the models a semi "clean room" restriction, not letting
> them browse my GitHub (as they could use the cft-fp256 library to cheat), but
> that means I need a packaged portable "bootstrap" kit which lays out the
> methods and systems, how the workflow goes, what the lead is responsible for
> and should handle or ask about etc. including prior examples for formatting
> and demonstration. Go ahead and go over the projects briefly and consider the
> best approach. Ill also likely give the meta agents access to QRO-Crate as a
> sample of a real project using the systems

His answers to the lead's eight questions. Each question is the lead's
paraphrase of what was asked, and each answer is Logan's, verbatim:

| # | the lead's question | Logan's answer |
|---|---|---|
| 1 | where the kit's build tooling lives | "New repo, private, exported to a zip for easy moving to the Meta directories when ready" |
| 2 | which Meta models in which roles; what the harness offers | "Not yet decided, their most capable for the lead, likely one step down for parcels. Unsure what the TUI they offer has in terms of capabilities, but I will determine that live once the hackathon begins, no need to discern now." |
| 3 | offline or web; may agents read third-party code | "Web access to read third-party code and solutions, the only restriction is staying away from cft" |
| 4 | what scope Logan fixes, and what he leaves to the lead's study | "Undecided yet" |
| 5 | whether the Pico is in the loop | "Yes, a pico will be constantly connected for debugging" |
| 6 | how long the hackathon runs | "10 days starting Monday" |
| 7 | who holds the planted-fault keys | "The lead holds them for parcels" |
| 8 | whether to run a Claude baseline | "Not needed at this time" |

---

## 2. What the kit is for, and what it must never do

**Purpose.** A lead and its agents, on Meta models, run HonestFramework and
ParcelRound on one new project, an IEEE-754 softfloat for the RP2040 in
binary16, binary32 and binary64. They have ten days, Logan's GitHub is out of
reach, and Logan measures how they handle the methods.

**What it must hold.** Section 8 says which check holds each.

- **K1.** Nothing of cft's code or its arithmetic is in the kit. No link in the
  kit leads to cft.
- **K2.** The method texts are the canonical texts, copied from pinned commits.
  Every change to them is a named rule with a declared count.
- **K3.** The kit decides nothing the lead's study should decide: the
  authority, the oracles, the scope or the split.
- **K4.** The kit identifies itself, by a version, a manifest of sha256s and
  its source commits. It is frozen from kickoff, and only Logan's word changes
  it, as a new version.
- **K5.** Every figure in the kit's own documents is held by a script, or
  tagged BELIEVED.

**Why the clean room matters more than it first looks.** cft-fp256 already
runs binary32 and binary64 on an RP2040. docs/EMBEDDED.md:38 lists "Raspberry
Pi Pico | RP2040, Cortex-M0+ 133 MHz, no FPU | 2 MB | 264 KB | fp32 fp64
fp128 fp256 | everything" (READ). It runs there through the Arduino binding,
beside these, all READ by listing:
- host/src/softfloat.c, clause5.c and divsqrt.c;
- the golden model, python/cft_golden/ (33 files, 12 of them in lang/);
- python/hardcases.py;
- drivers for TestFloat, UCBTEST and IBM's FPgen (python/external_*.py).

binary16 had no hit in the files searched (MEASURED, `grep -c -i -E
'fp16|binary16'`): python/cft_golden/formats.py, host/src/softfloat.c,
host/src/clause5.c, docs/EMBEDDED.md and CONFORMANCE.md. That search does not
cover the whole repository.

**What leaving cft out would lose.** cft-fp256's records are also where
Logan's newest practice lives. The phrases below have no hit in ParcelRound's
METHOD.md, in its templates, or in HonestFramework's documents and templates.
In cft-fp256's docs/VALIDATION.md they have these counts (MEASURED, `grep -c`):

| practice | lines in cft VALIDATION.md |
|---|---:|
| "time box" | 2 |
| "scope ceiling" | 1 |
| "size ceiling" | 2 |
| "very small fix" | 5 |
| "quiet event" | 1 |
| "git config" | 5 |
| the class "(a)" | 108 |
| COMPUTED | 213 |
| "READ)" | 54 |

The loose cap is written only in QRO-Crate's CLAUDE.md, item 6. So the kit
must carry that practice forward itself (section 4.2), or excluding cft drops
it.

---

## 3. Logan's decisions, and what the kit does with each

1. **The repository.** A private repository, proposed name
   `softfloat-bootstrap`, holds the builder. `make dist` writes
   `softfloat-bootstrap-kit-v<N>.zip` and its SHA256SUMS. Only the zip moves
   to the Meta directories, never the repository. The builder reads cft-fp256,
   for the excerpts of section 4.3 and the audit of section 7, and the zip must
   carry neither the reader nor what it read beyond those excerpts.
2. **Models and the harness.**
   - ROLES.md names tiers, not models: the lead on the most capable, parcels
     one step down. The verifiers' tier is not decided (section 10, Q6).
   - HARNESS.md is a table the lead fills in on day 1, with Logan. It maps
     each mechanism the methods assume to the TUI's feature, or to the method's
     own fallback:
     - worktrees;
     - messages between agents;
     - background watches;
     - resumable agents;
     - a usage log.
   - The fallbacks already exist: the `urgent/` file channel (ParcelRound
     METHOD.md section 4), and a send-back as a newly briefed agent (section
     8). The filled table is part of the record, because which fallbacks were
     used is a result.
3. **Web access.** CLEAN-ROOM.md says four things:
   - What "cft" covers. The proposal, for Q2: cft-fp256 in any form (github,
     raw, API, forks, mirrors, its public site, archives), and every
     repository that carries its code. Two are known:
     - cft-rebound, "an N-body integrator driven through the coprocessor"
       (HonestFramework CASE-STUDY.md:21, READ);
     - the libcft submodule in round 4's project, "libcft built by the lead in
       the pinned submodule" (ParcelRound CASE-STUDY-4.md:58, READ).
   - What to do when a search lands there: do not open it. If it was opened,
     stop, write it in the ledger (the URL and what was seen), and escalate.
     The crossing is judged on disclosure, as ParcelRound section 3 judges a
     boundary crossing.
   - That the output is audited (section 7).
   - That third-party sources are open to read (SoftFloat, TestFloat, pico-sdk,
     MPFR, the literature), and that recording their licences is the lead's job.

   A search for an RP2040 softfloat could surface cft-fp256's EMBEDDED.md
   (BELIEVED, not tried).
4. **Scope.** PROJECT.md fixes only what Logan has said. It lists the questions
   the lead's study must put to him (section 6) and proposes no answers.
5. **The board.** BOARD.md treats the Pico as a shared device:
   - one holder at a time, by a lock file;
   - every board result names its ELF's sha256, the commit and the flags
     (HonestFramework METHOD.md section 6);
   - the debug link is filled in on day 1, in HARNESS.md.

   Who may flash it, and when, is Q5.
6. **Ten days from Monday.** That is 2026-10-26 to 2026-11-04 (MEASURED:
   2026-10-23 is a Friday, and Monday plus nine days is Wednesday
   2026-11-04). Reading "10 days" as ten calendar days, Monday included, is
   the lead's (BELIEVED). WORKFLOW.md carries caps and a suggested calendar
   (section 5.3), and the caps are Logan's to set (Q7).
7. **The lead holds the keys.** WORKFLOW.md carries the planted-fault
   protocol, and `tools/plant.py` runs it in round 6's key format (section
   4.4). For each parcel's verifier, the lead:
   - builds a copy of the parcel's work that may hold planted faults;
   - commits the key's sha256 to the ledger before dispatch;
   - reveals the key after the report.

   This is the three-commit protocol, HonestFramework METHOD.md:696-700, run
   as round 6 ran it: ParcelRound archive/round6-ledger.zip, keys/ and
   briefs/_verifier.md (READ). METHOD.md section 9 does not use the name: the
   phrase "three-commit protocol" comes from round 6's verifier brief.

   Two consequences, stated in METRICS.md:
   - A detection rate measures the lead's plants and the verifiers' detection
     together.
   - The verifiers of the lead's own work get no plants, since no one but the
     lead holds keys.
8. **No baseline.** METRICS.md derives its tables in the shape of cft-fp256's
   records, so a baseline can be added later with the same kit. Until then any
   comparison with cft-fp256's waves is qualitative: a different task, a
   different harness and different models.

---

## 4. The kit's contents

### 4.1 `method/`: the method texts, copied by script

Every file is read from git objects at the pinned commit (`git show
<commit>:<path>`), not from a working tree, so an uncommitted edit cannot reach
the kit.

**Included.** Sizes are tokens counted with tiktoken's `o200k_base`, a proxy
for a 200K-vocabulary tokenizer (MEASURED):

| from | files | tokens |
|---|---|---:|
| HonestFramework | README.md, METHOD.md, FAILURE-MODES.md, ADOPTING.md, WITH-PARCELROUND.md, CASE-STUDY.md | 22,521 |
| HonestFramework | templates/: README.md, agent-notes.md, controls.md, ledger.md, manifest.md, gate-runner.sh, check_generated.py | 11,099 |
| HonestFramework | tools/check_claims.py, if it passes on the copy (it passes on its own tree: rc 0, "36 links resolve"; MEASURED) | — |
| ParcelRound | README.md, METHOD.md, ADOPTION.md | 30,253 |
| ParcelRound | templates/: brief.md, verifier.md, ledger.md, checklists.md | 10,418 |
| ParcelRound | CASE-STUDY.md and CASE-STUDY-2.md to -6.md | 64,041 |
| ParcelRound | archive/round6-practice-survey.md | 8,170 |
| ParcelRound | archive/round5-ledger.zip and round6-ledger.zip, byte for byte | 106,866 and 152,142 unpacked |

Counted another way, Claude's tokenizer gave 27,193 tokens for the first 60,648
bytes of ParcelRound's METHOD.md, about 2.2 bytes a token, against `o200k_base`'s
19,866 tokens for all 78,786 bytes, about 4.0 (MEASURED, COMPUTED). So a
reading budget depends on the tokenizer by up to about 1.8 times. The kit
states bytes and `o200k_base` tokens, and says which.

**Excluded, with the reason.** Word-bounded counts MEASURED over each
archive's members:
- **archive/round2-ledger.zip and round3-ledger.zip**, cft-fp256's own rounds.
  - Round 2 counts fp32 53, fp64 31, fma 13, overflow 13, underflow 10 and
    sticky 8.
  - Round 3 counts softfloat 25, fp32 12 and fp64 8.
- **archive/round4-ledger.zip and round4-second-ledger.zip**. That round's
  project is built on libcft ("libcft built by the lead in the pinned
  submodule", CASE-STUDY-4.md:58). Its first ledger counts binary64 82, ulp 34
  and binary32 22.
- **ParcelRound's tools/check_method.py.** It pins all six archives by sha256
  (`ARCHIVE_SHA256`, tools/check_method.py:225-232, READ), so it cannot pass on
  a kit that lacks four of them.

  It also fails in this shallow clone: "anchors FAIL ... ADOPTION.md names
  commit 868f95e, which is not in HEAD's history" (MEASURED, rc 1, 9 of 10
  checks hold). That it passes with full history is BELIEVED; it was not run.

  The kit's own gate (section 8) is the runnable example of a gate with
  controls.

**The rules**, each with a count declared beside it. The build fails if a
count differs, so a source that moves cannot slip through:

| rule | what it does | count |
|---|---|---:|
| R1 | A link into `github.com/loganw234/cft-fp256` keeps its text, loses its URL, and gains "(cft-fp256's record; not in this kit)". | 12, all in ParcelRound METHOD.md (MEASURED) |
| R2 | A link to `github.com/loganw234/ParcelRound` becomes the kit-relative path. | 3, one each in HonestFramework METHOD.md, FAILURE-MODES.md and WITH-PARCELROUND.md (MEASURED) |
| R3 | A link to an excluded archive keeps its text and gains "(not in this kit)". | 4: CASE-STUDY-2.md:580, CASE-STUDY-3.md:781, CASE-STUDY-4.md:394 and :402 (MEASURED) |

Everything else is left as it stands:
- **Prose that names a cft-fp256 file**, as in "docs/VALIDATION.md:16682, at
  `4190a47`", stays. It is the record's citation and carries no code.
- **The two loganw.dev URLs** in CASE-STUDY-5.md stay. That site is not cft.
- **`round6-practice-survey.md:18`** names the round-4 archives in code font,
  not as a link, so it stays.

### 4.2 The layer written for the hackathon

All new, short, and each with its sources cited. The target is 15,000 tokens
for all of it (BELIEVED).

| file | what it holds | built from |
|---|---|---|
| START-HERE.md | The front door: what the kit is, the reading order for each role with sizes (generated, `--check`), and the five things that bind from the first minute: the clean room, the ledger, the escalation channel, nothing pushed without Logan's word, and the kit's own gate | HonestFramework METHOD.md section 10 |
| ROLES.md | Owner, lead, parcel, verifier: what each decides, what each asks, what each must never do | ParcelRound sections 3, 6 and 7, templates/checklists.md, OWNER.md |
| WORKFLOW.md | The round, phase by phase, with exit criteria and the template each phase uses (section 5) | ParcelRound sections 1 to 8, HonestFramework sections 1 to 3 and 9 |
| OWNER.md | Logan's words for the hackathon; his standing rules from other projects, verbatim with dates and sources; the rules his leads added; the list of what to ask (below) | as cited below |
| PROJECT.md | The softfloat charter: what is fixed, and the questions for the lead's study (section 6) | Logan's words |
| GLOSSARY.md | MEASURED, READ, COMPUTED, BELIEVED; (a), (b) and notes; READY and NOT READY; known limit; send-back; the chain; wave; seam; P0; plant and key | the uses in cft-fp256's and QRO-Crate's records |
| CLEAN-ROOM.md | Section 3, item 3 | Logan's words |
| METRICS.md | Section 7 | cft-fp256's record format, ParcelRound section 7 |
| HARNESS.md | A table to fill on day 1 | section 3, item 2 |
| BOARD.md | The Pico protocol, with its details filled in on day 1 | section 3, item 5 |
| AGENTS.md | Seed agent notes for the softfloat repository: the front door, to be set by P0; the desktop's traps, if the agents run on Logan's desktop | HonestFramework templates/agent-notes.md; the environment entries of QRO-Crate CLAUDE.md "What bites" items 1 and 2, and of cft-fp256 CLAUDE.md's desktop entries (`| grep | head` deadlock; two MSYS `/tmp`s) |

**OWNER.md's standing rules.** Each is quoted with its date and source, and
marked "for the hackathon: Logan to confirm" (Q6). All are READ.

1. **2026-09-27, the send-back rule.** Only a regression or a wrong answer
   sends work back; anything else merges as a recorded known limit
   (ParcelRound METHOD.md:1125-1137). Logan's words: "Agreed with the only
   regression or wrong answer being send backs" (archive/round6-practice-
   survey.md:115, B3).
2. **2026-09-29, long runs.** "dont have the individual agents all run the
   full suites, have them hand back large runs to you to monitor rather than
   them, but they should still verify and test as much as they can quickly"
   (METHOD.md:1236-1239).
3. **2026-10-12, tiers.** "For 'simpler' level tasks, you may also utilize
   Sonnet for the Parcels and Haiku for the verifier. But only when its not a
   'challenging' task" (cft-fp256 docs/VALIDATION.md:20101).
4. **2026-10-13, small fixes.** "... Unless they are very small fixes, in
   which case you can handle them and utilize a verifier to check"
   (VALIDATION.md:19293).
5. **2026-10-15, models in QRO-Crate's round.** "Use Sonnet models for the
   parcels in this round, as well as for the verifiers. ... Difficult parcels
   still get opus, though most of this work is not "difficult" so to speak"
   (QRO-Crate docs/VALIDATION.md:1167-1171).
6. **2026-10-15, the loose cap.** "If the last rounds have just been semantic
   changes and nothing related to code directly, round 6 can be the last, with
   the verifier instructed not to hold it back for prose only issues"
   (QRO-Crate docs/VALIDATION.md:789-791), as QRO-Crate CLAUDE.md:105 states
   it (item 6).
7. **Commits and pushes by Logan's word.** QRO-Crate CLAUDE.md:104 (item 5).
   His words of 2026-10-14, "Go ahead with the first commit once P0 is READY,
   you can also make a remote repo to push to as well" (VALIDATION.md:922-924),
   and of 2026-10-16, "You are clear to commit and push when ready"
   (VALIDATION.md:2473-2474).
8. **The pause.** "commit where they are and leave a resume note for
   themselves incase context is lost in the downtime" (ParcelRound
   METHOD.md:542-544).

The leads' own brief rules, which are not Logan's words, are kept apart from
his and marked as the leads':
- a time box and a scope ceiling in every brief (cft-fp256
  VALIDATION.md:21733). Logan on them, 2026-10-20: "If needed it can have more
  time, though how have the time bounds been working so far? I noticed you
  started giving the agents them, good choice" (VALIDATION.md:22537);
- "NEVER change any git configuration" (:22676);
- "wait on one quiet event; do not report a wait" (:22681).

**Reading the tiers.** Rules 3 and 5 name Claude models. For the hackathon,
OWNER.md reads "Opus" as the most capable tier and "Sonnet" as one step down.
That reading is the lead's, marked as such, for Logan to confirm. Nothing in
Logan's words places "Haiku"; if needed, the lead reads it as two steps down.

**What the lead asks, and what it decides.**
- **It decides** what the standards decide: unattended, it merges, verifies,
  diagnoses and records within the project's rules, and puts the owner's
  questions in the ledger (ParcelRound METHOD.md:1364-1370).
- **It asks first, and records the answer** (METHOD.md:1372-1377):
  - a push;
  - anything that deploys or deletes remotely;
  - a change to how results are counted;
  - scope;
  - models and tiers;
  - board sessions, if Logan rules them his (Q5);
  - any exception to a standing rule;
  - any suspected contact with cft.
- **The owner's words are kept as given.** Logan's decisions are recorded with
  their dates, and the lead's reading goes beside them, marked as the lead's
  (METHOD.md:1379-1386).

**GLOSSARY.md's evidence tags.** The definitions are the lead's reading of how
the records use the tags. Q8 asks the verifier to test them against those uses.
- MEASURED: run in this round, the output in hand.
- READ: read at a named file and line, or a named commit, not run.
- COMPUTED: arithmetic on measured or read figures, with the arithmetic shown.
- BELIEVED: an estimate or an inference.

The finding classes:
- (a) is a regression;
- (b) is a wrong answer, a false sentence among them (cft-fp256
  VALIDATION.md:15854: 'Only a regression "(a)" or a wrong answer "(b)" sends a
  parcel back'; :17961, '(b)2, a sentence the merges made false');
- anything else is a note.

### 4.3 `examples/`: prior work, each with a provenance header

`examples/README.md` is an index, not a second copy. One fact stays in one
place: it points into what the kit already carries, by path and purpose.

- **Rounds 5 and 6** (method/parcelround/archive/). Things to read in round 6:
  - a common brief, `briefs/_common.md`;
  - parcel briefs;
  - a verifier brief for a copy holding plants, `briefs/_verifier.md`;
  - an integration verifier's brief;
  - the keys, `keys/*.json`;
  - the ledger's README;
  - the lead's ledger;
  - the verifiers' ledgers.

  In round 5: its urgent messages and its seam verifier's brief.

  Some lines name Claude Code's tools. For example, round 6's verifier brief
  says to message the lead with "SendMessage; load it with ToolSearch". The
  index labels each such line as that harness's.
- **QRO-Crate**, in the zip or given separately (Q4).
  - Its plan of record, and its verifiers' reports on twelve drafts:
    docs/studies/QRO-0.md and docs/reviews/QRO-0/.
  - Its lead's P0, past verifiers six times (docs/reviews/P0/), and P0.1 to
    P0.5, past verifiers 4, 4, 2, 4 and 4 times (docs/VALIDATION.md's headings,
    MEASURED).
  - Its record entries, its agent notes (CLAUDE.md), its front door
    (verify/run.sh), a generated vocabulary with `--check`, and plants
    (controls/).

  Two cautions go with it:
  - It shows no parallel parcels yet. Its pace is a verifier's six rounds on
    one P0, which a ten-day round cannot afford, so WORKFLOW.md's caps apply
    (section 5.3).
  - 52 of its lines name cft-fp256 (MEASURED, `git grep -c -i cft-fp256`),
    about its certificate format and number spelling. In the kit those
    citations dangle by design.
- **cft-fp256's record excerpts**, for Q3. Only the process sections of named
  record entries, verbatim:
  - "What Logan asked, verbatim";
  - "The chain";
  - "Conduct";
  - "The experiment";
  - "Time and tokens", with its method line;
  - "Corrections this record owes".

  First is the coverage wave's close (cft-fp256 docs/VALIDATION.md:22529-22790,
  READ), then one more of the lead's choosing. A line that holds an
  arithmetic term (section 8, check 3) is cut, and its place is marked. These
  are the only examples of the per-agent tables Logan called the most tracked.

### 4.4 `tools/`: what the agents run

- **`ledger.sh`.** `append <file> <headline>` writes a heading stamped from
  `date`, with the Measured, Believed and For lines (ParcelRound section 4's
  stamp rule, made mechanical). `urgent <author> <slug>` composes a message
  elsewhere and renames it into place.
- **`watch.sh`.** The `urgent/` watcher from ParcelRound templates/ledger.md,
  short enough to run inline.
- **`plant.py`.**
  - `make` copies a commit into a verifier's tree, applies the plants from a
    key in round 6's format (`real_tip`, `copy_commit`, `plants[]` of `file`,
    `old`, `new` and `shape`), commits the copy, and prints the key's sha256
    for the ledger.
  - `reveal` appends the key to the ledger.
  - `score` reads the verifier's report and lists each plant as caught or
    missed.
  - Each refusal is planted in its self-test.
- **`round_metrics.py`.** Section 7's tables, from section 7's sources. It
  carries a usage-log adapter for a generic JSONL, and a manual fallback whose
  rows are marked as transcribed. Its self-test has fixtures and plants.
- **`check_kit.py`.** The kit's gate (section 8). The agents run it first, on
  day 1.

The runner and the generate-and-check pattern are HonestFramework's, in
method/honest/templates/, for the softfloat repository's P0 to adopt.

### 4.5 `MANIFEST.txt`

The kit's version, the builder's commit, the source commits, and the sha256 of
every file. `check_kit.py` verifies it. Every table METRICS.md derives names
the kit's version in its header.

---

## 5. The workflow WORKFLOW.md lays out

### 5.1 Phases, and what ends each

0. **Day 1.**
   - Read START-HERE.md, then run `tools/check_kit.py`.
   - Fill HARNESS.md and BOARD.md, with Logan.
   - Make the ledger outside every worktree.
   - Arm the escalation channel and test it: "A test escalation at dispatch
     must reach the lead" (ParcelRound section 4).
1. **The survey.** Read-only surveyors read the ground and report facts with
   their sources, each tagged (ParcelRound section 1, "Survey the tree before
   the plan, read-only"). The ground: the standard, the RP2040's datasheet,
   pico-sdk's float support, SoftFloat and TestFloat, published hard cases.
2. **The study, SF-0, the plan of record**, in the softfloat repository. It
   covers:
   - the answers it proposes to section 6's questions, as questions for
     Logan;
   - the authority and the oracles (HonestFramework section 1);
   - refusals (section 2);
   - the gates, with their negative controls (section 3);
   - P0;
   - the parcels and the waves;
   - how the metrics are captured.

   It ends when a verifier's re-check finds no (a) or (b), or the draft cap
   is reached with the open findings listed, and Logan approves.
3. **P0, the lead's.** In a new repository P0 is the seam, not a refactor:
   - the formats' parameters, defined once and generated;
   - the runner, with its budgets;
   - the vector format and its replay;
   - the board harness;
   - the refusal table.

   It goes past a verifier before any parcel that reads it is dispatched
   (ParcelRound section 2).
4. **The waves.** Each wave runs these steps:
   - parcels propose a design first, and the lead approves it;
   - they build;
   - each parcel's verifier works on a copy that may hold the lead's plants;
   - send-backs follow the (a)/(b) rule;
   - the lead merges serially, with the gate after each merge;
   - an integration verifier checks the lead's merges and record;
   - the lead writes a closing record entry whose tables `round_metrics.py`
     makes.
5. **Board sessions**, by BOARD.md.
6. **The close.**
   - The final record entry, with its metrics and the lead's slips.
   - The ledger archived with its timestamps.
   - The agents' background work stopped.
   - The summary to Logan, with the cost (ParcelRound section 7).

### 5.2 Each phase's method section and template

| phase | method | template |
|---|---|---|
| 0 | ParcelRound section 4; HonestFramework section 10 | parcelround/templates/ledger.md; honest/templates/agent-notes.md |
| 1 | ParcelRound section 1 | a surveyor's brief (examples/README.md points to one) |
| 2 | ParcelRound section 7; HonestFramework sections 1 to 3 | parcelround/templates/checklists.md, "Before dispatch" |
| 3 | ParcelRound section 2 | parcelround/templates/verifier.md |
| 4 | ParcelRound sections 3 to 8; HonestFramework section 9 | brief.md, verifier.md, checklists.md "At each merge" |
| 6 | ParcelRound sections 4 and 7 | checklists.md, "At the end of the round" |

### 5.3 Caps, and a suggested calendar

These are the lead's proposals; Logan sets them (Q7).

- **The study:** at most three drafts and two re-checks. Then it goes to
  Logan, with its open findings listed.
- **Verifier passes:** the loose cap (OWNER.md, rule 6), if Logan carries it
  over. After three NOT READY verdicts whose reasons grow more menial, only a
  defect in what the code does blocks.
- **Every brief:** a time box and a scope ceiling.
- **The calendar:**

  | days | dates | what |
  |---|---|---|
  | 1 | Mon 10-26 | setup and the survey |
  | 2 | Tue 10-27 | the study, its verifier, and Logan |
  | 3 to 4 | to Thu 10-29 | P0 and its verifier |
  | 4 to 8 | to Mon 11-02 | two or three waves |
  | 9 | Tue 11-03 | integration and the board's conformance runs |
  | 10 | Wed 11-04 | the record, the metrics and the summary |

  The lead plans around Logan's hours. Decisions wait for him in the ledger
  (ParcelRound section 7, unattended).

---

## 6. PROJECT.md: the softfloat charter

**Fixed, by Logan's words:**
- "an IEEE-754 compliant softfloat for RP2040, for binary16/32/64";
- a Pico "constantly connected for debugging";
- web access to third-party code, and "the only restriction is staying away
  from cft".

**The questions.** The lead's study puts these to Logan, each with its own
proposal. The kit proposes no answers. The lead's statements about the standard
below are from memory, so they are BELIEVED until the survey reads the text.

1. **The edition.** IEEE 754-2019, or 2008.
2. **The operations.** Which of clause 5's required operations, for each
   format.
   - The conversions to and from decimal character sequences are among the
     required ones, and they are a large piece.
   - Clause 9's recommended operations (exp, log and the rest): in or out.
3. **Rounding.** roundTiesToEven and the three directed attributes are
   required. roundTiesToAway is required only for decimal formats. In or out
   here?
4. **Exceptions.**
   - Default handling and the five flags.
   - Where the flag and mode state lives on a part with two cores: per core,
     per call, or global.
   - Clause 8's alternate exception handling: in or out.
5. **Tininess and NaNs.**
   - Tininess detected before or after rounding, one choice for every binary
     operation.
   - Payloads: whose NaN propagates, how signaling NaNs are treated, and
     whether there is a canonical NaN.
6. **The interface.**
   - A drop-in for the toolchain's runtime helpers, through pico-sdk's
     wrapping; an API of its own; or both.
   - binary16's storage type.
7. **Targets.**
   - Speed and size goals, and their yardstick: pico-sdk's float and double
     support, which uses the bootrom's routines (BELIEVED, for the survey to
     read).
   - Flash or RAM placement.
   - The language: C, Thumb assembly, or both.
8. **Dependencies and licence.**
   - pico-sdk's version and the toolchain.
   - The output's licence.
   - Which third-party code may be copied, and which only read.
9. **The authority and the oracles.** The study proposes; Logan approves.

---

## 7. METRICS.md: every figure from a source the agents don't write

| figure | authority | never from |
|---|---|---|
| Tokens (output, input, cached), messages, and the model per message | The TUI's usage log or the API's log, whichever HARNESS.md finds on day 1. Failing both, the TUI's own counters, transcribed and marked as such. | An agent's estimate |
| Tool uses | The transcript | |
| Minutes per pass | The transcript's stamps, from each prompt of the lead's to the pass's last line (cft-fp256 docs/VALIDATION.md:22742, READ) | |
| Commits; diff size against the scope ceiling; files outside the ownership list | git | The report |
| Gate runs | The runner's JSONL record | |
| Findings | The verifier's report, classed (a), (b) or note, each confirmed or rejected by the lead in the ledger | |
| Plants caught | The keys and the reports (`plant.py score`) | |
| Brief corrections | The report's "what this brief got wrong", counted, with the lead's acceptance | |
| Escalation latency | The ledger's stamps, from the question to the answer | |
| Conduct and the lead's slips | The record's lists, checked by the integration verifier | |
| Logan's words | The record, verbatim, with dates | |

`round_metrics.py` makes these tables, per wave and for the hackathon:
- the chain: work, author, the verifier's passes with (a) and (b) per pass, and
  send-backs;
- time and tokens: agent, model, passes, minutes for the first pass and in
  all, tool uses, output tokens, input tokens;
- each brief's time box and scope ceiling against the actual;
- plants;
- brief corrections;
- escalations.

cft-fp256's coverage wave measured its tokens as "output tokens summed from the
last line of each response" (VALIDATION.md:22742, READ). The adapter states its
own method beside its figures.

**Comparisons.** Tokens read depend on a harness's caching. Across harnesses,
compare output tokens and minutes; tokens read are compared only within one.

**The audit**, Logan's tool. It lives in the builder repository and is never in
the zip.
- It holds fingerprints of cft-fp256's arithmetic sources: hashed k-grams of
  normalized tokens from host/src/ and python/cft_golden/.
- It checks the softfloat repository against them at each wave's close, and at
  the end.
- Its self-test, run in the builder, plants real cft-fp256 functions, which it
  must flag, and Berkeley SoftFloat 3e functions, which it must not.
- Its false-alarm rate is measured and stated (HonestFramework METHOD.md
  section 3: "A signal's rank ... is set by its measured false-alarm rate").

The agents know from CLEAN-ROOM.md that the audit exists. They never see its
data. It is not needed for kickoff, so it is built after v1 (section 9).

---

## 8. The kit's gate, and its controls

`check_kit.py` runs these checks on the unpacked zip:

1. **The manifest.** Every file's sha256 matches, no file is outside the
   manifest, and the manifest names the source commits.
2. **Links.** Every relative link resolves inside the kit. No URL leads to
   cft: no `github.com/loganw234/cft-...`, its raw or API hosts, or its public
   site, `loganw234.github.io/cft-fp256` (cft-fp256 README.md:28, READ).
3. **Arithmetic in the cft excerpts.** No line of `examples/cft-records/` holds
   an arithmetic term: a word-bounded list beginning with sticky, guard bit,
   subnormal, denormal, mantissa, significand, fma, ulp, tininess, underflow,
   overflow, softfloat, rne, rtz, rmm, fp16/32/64 and binary16/32/64. The check
   runs on that directory alone, because the rest of the kit has to name some
   of these words. The list is conservative: it also fires on the round 5
   and 6 ledgers, which hold binary64 7 times and overflow twice (MEASURED)
   and carry no arithmetic. So a cut is not evidence of arithmetic, and each
   excerpt's header lists its cuts.
4. **Privacy.** No home path, email address, key or token of the shapes in
   QRO-Crate's tools/check_privacy.py. A fixture shaped like any of them is
   built in pieces at run time, as QRO-Crate's plants are (its CLAUDE.md, "What
   bites" item 3).
5. **Generated files.** The reading table in START-HERE.md and the examples
   index match their generators (`--check`).

In the builder, `build_kit.py --check` also re-derives `method/` from the
pinned sources and compares it byte for byte. The zip carries no sources, so
check 1's hashes stand in for that there.

**Controls.** `--control` plants each fault in a copy and confirms the matching
check fails and names it. Each plant restores the bytes it planted over exactly
(ParcelRound section 5). The faults:
- a changed byte;
- an extra file;
- a cft URL;
- a broken relative link;
- an arithmetic term in an excerpt;
- a home path, built in pieces;
- a stale reading table.

---

## 9. The builder, and the order of the build

These steps follow Logan's approval of this plan.

```
softfloat-bootstrap/          (private)
  README.md, CLAUDE.md        what this is; the front door; what bites
  docs/KIT-0.md               this plan
  docs/VALIDATION.md          the record
  docs/reviews/               every verifier's report
  kit/                        the layer of section 4.2, and the tools of 4.4
  build/sources.lock          each source: repository, commit, paths
  build/build_kit.py          copy, rules with counts, --check, dist
  audit/                      section 7's audit; reads cft-fp256; never in the zip
  tests/                      the builder's tests; the gate's controls
  verify/run.sh               the front door, after HonestFramework's gate-runner.sh
  dist/                       ignored: the zip and its SHA256SUMS
```

1. The skeleton, the runner and this repository's agent notes.
2. `build_kit.py`, the rules with their counts, and `method/` derived, with
   `--check`.
3. The layer of section 4.2: Logan's words verbatim, and every rule with its
   source.
4. `examples/`: the index, and the cft excerpts behind check 3.
5. `tools/`, each tool with its self-test and plants.
6. `check_kit.py` and its controls.
7. `make dist`.
8. **A cold read.** A fresh agent with only the zip, in an empty directory,
   answers a fixed list of questions about the roles, the ledger, the
   send-back rule, the clean room and the first day. Its answers are scored
   against a key written before it runs, in the three steps of HonestFramework
   METHOD.md:696-700. This shows the kit works for a reader with nothing else.
9. **A verifier** on the built kit and on the builder (ParcelRound section 7:
   the lead's work goes past a verifier).
10. **Logan's word.** Then the private repository is created, the work is
    committed and pushed, and the zip is exported.

v1 by Sunday 2026-10-25 (BELIEVED feasible). The audit follows, before the
first wave closes.

---

## 10. Questions for Logan

Each has the plan's proposal beside it.

1. **The repository's name.** Proposal: `softfloat-bootstrap`, private, under
   your account.
2. **What "cft" covers.** cft-fp256 only, or every repository that carries
   libcft or the golden model, cft-rebound and round 4's libcft submodule
   among them? And may the agents read ParcelRound's case studies 2 to 4?
   Those are accounts of cft-fp256's and round 4's rounds, with no code in
   them, and METHOD.md cites them throughout. Proposal: the wider list; the
   case studies in.
3. **cft-fp256's record excerpts.** May the kit carry the process sections of
   section 4.3 as formatting examples? Proposal: yes, behind check 3.
4. **QRO-Crate.** In the zip as a git bundle at `8afeede` (its `.git` is 1.3 MB,
   MEASURED), or given separately? Proposal: in the zip, so every citation in
   the kit resolves offline.
5. **The board.** May parcels flash and run the Pico freely, one holder at a
   time? Or does the lead schedule it, or is each session your word? Proposal:
   parcels flash freely under the lock, and long runs are the lead's
   (OWNER.md, rule 2).
6. **The standing rules.** Which of OWNER.md's eight hold for the hackathon?
   Who is the verifiers' tier? Does the softfloat repository have a remote?
   Proposal: all eight hold; verifiers at the parcels' tier, one step lower
   only for simpler tasks (rule 3, in tier terms); a remote only by your word.
7. **The caps.** Proposal: section 5.3's.
8. **For the verifier, not for Logan.** Are GLOSSARY.md's definitions of the
   four tags true to their uses in the records?
