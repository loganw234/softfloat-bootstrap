# KIT-0: the bootstrap kit for the Meta softfloat hackathon

**Draft 2, 2026-10-23. The lead's (this session). Not approved.** Nothing in
this directory is committed and no repository has been created.

Draft 1 went past a verifier, which returned NOT READY with six (a), ten (b)
and eighteen notes. Its report is docs/reviews/KIT-0/draft1-verifier.md.
Section 11 says what draft 2 did with each finding, and section 12 lists the
lead's slips. Draft 2 goes back to that verifier for a scoped re-check before it
reaches Logan (ParcelRound METHOD.md section 7: "The plan of record, and a
verifier on it before the owner approves it").

Evidence tags, as Logan's records use them (GLOSSARY.md, section 4.2):
- **MEASURED**: run in this session, the output in hand;
- **READ**: read at a named place, not run;
- **COMPUTED**: arithmetic on measured or read figures;
- **BELIEVED**: an estimate, an inference, or a claim not checked.

Paths are relative to `<repos>/`. Sources read: HonestFramework at
`65447fd`, ParcelRound at `f42242e` (a shallow clone of 61 commits),
QRO-Crate at `8afeede`, cft-fp256 at `39f9801` (shallow).

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

His answers to the lead's first eight questions. Each question is the lead's
paraphrase, and each answer is Logan's, verbatim:

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

His answers to draft 1's section 10, given the same day:

| # | draft 1's question | Logan's answer |
|---|---|---|
| 1 | the repository's name, `softfloat-bootstrap` | "That name works" |
| 2 | what "cft" covers | "cft-fp256 only, as thats the only project where code could be copied from" |
| 3 | cft-fp256's record excerpts as formatting examples | "Yes, include many samples of "how things should be handled"" |
| 4 | QRO-Crate in the zip, or given separately | "Bundle" |
| 5 | who may use the Pico | "Lead controls hardware access" |
| 6 | which standing rules hold; the verifiers' tier; a remote for the softfloat repository | "List all 8, I will discuss which apply with the Meta model, yes to remote, just create a private repo for now." |
| 7 | the caps | "Same as above, discussed with the model to determine what it thinks would be best for its harness capabilities." |

Then, unasked, the same day:

> It wont be included in the zip as its licensed to me, but I will also be
> giving the Meta lead the real IEEE 754 pdf for reference, so they will have
> the material needed in terms of the contract, but not necessarily how to
> achieve it

---

## 2. What the kit is for, and what it must never do

**Purpose.** A lead and its agents, on Meta models, run HonestFramework and
ParcelRound on one new project: an IEEE-754 softfloat for the RP2040, in
binary16, binary32 and binary64. They have ten days and stay away from
cft-fp256, while Logan measures how they handle the methods.

**What it must hold.** Section 8 says which check holds each.

- **K1.** Nothing of cft-fp256's code or its arithmetic is in the kit. No link
  in the kit leads to cft-fp256. No personal data of Logan's is in it.
- **K2.** The method texts are the canonical texts, copied from pinned
  commits. Every change to them is a named rule with a declared count.
- **K3.** The kit decides nothing the lead's study should decide: the
  authority, the oracles, the scope, P0's contents or the split. Where the kit
  shows a shape, it says it is a proposal.
- **K4.** The kit identifies itself, by a version, a manifest of sha256s and
  its source commits. It is frozen from kickoff. Only Logan's word changes it,
  as a new version, and nothing the agents fill in lives inside it.
- **K5.** Every figure in the kit's own documents is held by a script, or
  tagged BELIEVED.

**Why the clean room matters.** cft-fp256's arithmetic is the same source on
every target, all READ:
- "Nothing was ported. libcft has no floating-point dependence to begin with"
  (docs/EMBEDDED.md:9-10);
- it compiles for the Pico (EMBEDDED.md:251-253 and 450-453);
- its board profile's 168 vector sets match on a host loopback (:602-603).

It has never run on a Pico. "Four boards have not been attached: the Pico, the
Uno, the Nano and the Mega. Everything this document says about them is a
COMPILE result" (EMBEDDED.md:673-677), and "all 168 sets on a Pico" is pending
(:685).

What an agent could copy, all READ by listing:
- host/src/softfloat.c, clause5.c and divsqrt.c;
- the golden model, python/cft_golden/ (33 files, 12 of them in lang/);
- python/hardcases.py and vectors/gen_vectors.py;
- drivers for TestFloat, UCBTEST and IBM's FPgen (python/external_*.py).

binary16 had no hit in the files searched (MEASURED, `grep -c -i -E
'fp16|binary16'`): python/cft_golden/formats.py, host/src/softfloat.c,
host/src/clause5.c, docs/EMBEDDED.md and CONFORMANCE.md. That search does not
cover the whole repository.

**What leaving cft-fp256 out would lose.** Its records are where some of
Logan's newest practice is written. None of the phrases below appears in
ParcelRound's METHOD.md or its templates, or in HonestFramework's documents
and templates. In cft-fp256's docs/VALIDATION.md they have these counts
(MEASURED, `grep -c`):

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

So the kit carries that practice itself (section 4.2), and the samples of
section 4.3 show it in use.

The loose cap is a different case. It is written in QRO-Crate, not in
cft-fp256 (READ, the verifier):
- CLAUDE.md item 6;
- docs/VALIDATION.md:789-792, :1021, :1027, :1781 and :2753;
- docs/reviews/P0.1/round1.md:9.

The kit carries QRO-Crate (section 4.3), and OWNER.md quotes the rule.

---

## 3. Logan's decisions, and what the kit does with each

1. **The repository.** A private repository, `softfloat-bootstrap`, holds the
   builder. `make dist` writes `softfloat-bootstrap-kit-v<N>.zip` and its
   SHA256SUMS. Only the zip moves to the Meta directories, never the
   repository: the builder reads cft-fp256, for section 4.3's samples and
   section 7's audit.

   The zip carries cft-fp256's text only in these places, and check 3 reads
   each of them:
   - `examples/cases/`;
   - the short quotations in OWNER.md, GLOSSARY.md and METRICS.md;
   - the desktop entries in AGENTS.md.
2. **Models and the harness.**
   - **Tiers, not models.** ROLES.md names tiers: the lead on the most capable
     model, parcels one step down. The verifiers' tier is settled at kickoff
     (item 6 below).
   - **HARNESS.md** is a template that maps each mechanism the methods assume
     to the TUI's feature, or to the method's own fallback:
     - worktrees;
     - messages between agents;
     - background watches;
     - resumable agents;
     - transcripts;
     - a usage log.
   - **The fallbacks already exist.** The `urgent/` file channel is in
     ParcelRound METHOD.md section 4. A send-back as a newly briefed agent is
     in section 8.
   - **On day 1** the lead fills in a copy in the softfloat repository
     (docs/HARNESS.md), with Logan, and the kit stays as it was frozen (K4).
     The filled copy is part of the record, because which fallbacks were used
     is a result.
3. **Web access.** CLEAN-ROOM.md says four things:
   - **What is off limits.** The restriction is "cft-fp256 only, as thats the
     only project where code could be copied from" (Logan). That means
     cft-fp256 in any form:
     - its GitHub pages, raw files and API;
     - forks, mirrors and archives;
     - its public site, `loganw234.github.io/cft-fp256` (cft-fp256
       README.md:28, READ);
     - the copy shown through another repository's submodule. One example is
       atlas-film, which pins "cft-fp256's pinned arithmetic" (ParcelRound
       CASE-STUDY-4.md:27-30, READ).

     Logan's site loganw.dev is "a static site generated from the owner's
     other repositories" (CASE-STUDY-5.md:19-21, READ), cft-fp256 among them
     (round 5's briefs/P1.md:72-74). Its pages that show cft-fp256 count as
     cft-fp256. That is the lead's reading of "staying away from cft", for
     Logan to correct. His other projects are not restricted.
   - **What to do when a search lands there.** Do not open it. If it was
     opened, stop, write it in the ledger (the URL and what was seen), and
     escalate. The crossing is judged on disclosure, as ParcelRound section 3
     judges a boundary crossing.
   - **That the output is audited** (section 7).
   - **That third-party sources are open to read**: SoftFloat, TestFloat,
     pico-sdk, MPFR and the literature. Recording their licences is the lead's
     job.

   A search for an RP2040 softfloat could surface cft-fp256's EMBEDDED.md
   (BELIEVED, not tried).
4. **Scope.** PROJECT.md fixes only what Logan has said. It lists the
   questions the lead's study must put to him (section 6), and proposes no
   answers.
5. **The board.** "Lead controls hardware access" (Logan). BOARD.md says:
   - The lead holds the Pico. A parcel asks the lead for board time, and the
     lead runs the job itself or grants a slot, one holder at a time.
   - Every board result names its ELF's sha256, the commit and the flags
     (HonestFramework METHOD.md section 6).
   - Long runs on it are the lead's (OWNER.md rule 2, if it applies).
   - The debug link's details go in the filled copy, docs/BOARD.md in the
     softfloat repository, on day 1.
6. **Ten days from Monday.** That is 2026-10-26 to 2026-11-04 (MEASURED:
   2026-10-23 is a Friday, and Monday plus nine days is Wednesday
   2026-11-04). Reading "10 days" as ten calendar days, Monday included, is the
   lead's (BELIEVED).
   - WORKFLOW.md carries proposed caps and a calendar (section 5.3).
   - They are settled at kickoff, with the lead: "discussed with the model to
     determine what it thinks would be best for its harness capabilities"
     (Logan).
   - So are the standing rules. "List all 8, I will discuss which apply with
     the Meta model" (Logan).
7. **The lead holds the keys.** WORKFLOW.md carries the planted-fault
   protocol, and `tools/plant.py` helps run it (section 4.4). It is round 6's
   practice, ParcelRound archive/round6-ledger.zip (READ), with round 6's own
   pending lessons taken in:
   - **The copy.** A verifier gets a copy of the parcel's work that may hold
     planted faults. The copy is "a fresh repository detached at <copy>, with
     no remote, no branches and no route back to [the parcel's] own tip"
     (round 6's lead.md:488).
   - **The parcel's tip** stays out of the ledger until its verifier reports
     (lead.md:460; ParcelRound ADOPTION.md:143, CS5#8, pending).
   - **The key** is "kept outside every agent's reach" (lead.md:489), in the
     lead's scratch directory, which no agent reads.
   - **At dispatch**, the key's sha256 goes in the ledger.
   - **Into git as well.** Draft 2 proposes the lead also commits the hash to
     the softfloat repository's record before dispatch, so that `git log` shows
     the order, as HonestFramework METHOD.md:696-702 asks. That depends on
     whether Logan lets the lead commit (OWNER.md rule 7). Where it cannot,
     the deviation is stated: round 6 kept the hash in a ledger outside
     version control (METHOD.md:501-506).
   - **The keys stay hidden until the round ends.** "A round's planted-fault
     keys, and any description of their plants, stay out of the ledger until
     every verifier on a planted copy in the round has reported, later waves'
     included" (CASE-STUDY-6.md:346-348; ADOPTION.md:151, CS6#3, pending). This
     comes from round 6's lapse: "The lead revealed keys while a verifier still
     worked" (CASE-STUDY-6.md:171-173).
   - **The design comes last.** A verifier on a planted copy reads the
     parcel's ledger file, which holds its design, only after it has written
     its own view (ADOPTION.md:152, CS6#4, pending). In round 6 each verifier
     "noticed that its two wrong answers were the only places where the copy
     differs from the parcel's own design" (lead.md:560).
   - **Grading is by reading**, as round 6's was. `plant.py` lists each plant
     beside the report, the lead grades it caught or missed, the grading goes
     in the record, and the integration verifier checks it.

   Four consequences, stated in METRICS.md and WORKFLOW.md:
   - A detection rate measures the lead's plants and the verifiers' detection
     together.
   - The verifiers of the lead's own work get no plants, since no one but the
     lead holds keys.
   - The kit itself shows plant shapes: round 6's keys, in the archive. A
     verifier that read them knows those shapes, which is HonestFramework
     METHOD.md:702-711's fourth precaution, a corpus that already holds the
     answers. So the lead plants shapes the kit does not show, and the record
     states the limit.
   - "Three-commit protocol" is round 6's phrase (briefs/_verifier.md:38-42;
     CASE-STUDY-6.md:46; lead.md:487). HonestFramework's protocol rests its
     evidence on `git log`, which is why draft 2 proposes the hash go into
     git.
8. **No baseline.** METRICS.md derives its tables in the shape of cft-fp256's
   records, so a baseline can be added later with the same kit. Until then any
   comparison with cft-fp256's waves is qualitative: a different task, a
   different harness and different models.
9. **The standard.** It goes to the Meta lead outside the zip, and PROJECT.md
   says what it is for (section 6). Check 1 refuses any PDF in the kit.

---

## 4. The kit's contents

### 4.1 `method/`: the method texts, copied by script

Every file is read from git objects at the pinned commit (`git show
<commit>:<path>`), not from a working tree, so an uncommitted edit cannot reach
the kit.

**Included.** Tokens are counted with tiktoken's `o200k_base`, a proxy for a
200K-vocabulary tokenizer (MEASURED):

| from | files | tokens |
|---|---|---:|
| HonestFramework | README.md, METHOD.md, FAILURE-MODES.md, ADOPTING.md, WITH-PARCELROUND.md, CASE-STUDY.md, LICENSE | 22,521, LICENSE aside |
| HonestFramework | templates/: README.md, agent-notes.md, controls.md, ledger.md, manifest.md, gate-runner.sh, check_generated.py | 11,099 |
| HonestFramework | tools/check_claims.py, which passes on the copy with LICENSE present: rc 0, "39 links resolve" (MEASURED by the verifier) | — |
| ParcelRound | README.md, METHOD.md, ADOPTION.md, LICENSE | 30,253, LICENSE aside |
| ParcelRound | templates/: brief.md, verifier.md, ledger.md, checklists.md | 10,418 |
| ParcelRound | CASE-STUDY.md and CASE-STUDY-2.md to -6.md | 64,041 |
| ParcelRound | archive/round6-practice-survey.md | 8,170 |
| ParcelRound | archive/round4-ledger.zip, round4-second-ledger.zip, round5-ledger.zip and round6-ledger.zip, repacked by R4 and R5 with every member's timestamp and order kept | 109,280, 21,693, 106,866 and 152,142, unpacked |

Both LICENSE files are MIT: "The above copyright notice and this permission
notice shall be included in all copies or substantial portions" (LICENSE:12 in
each; READ by the verifier).

**A budget depends on the tokenizer.** Claude Code's Read tool reported
27,193 tokens for the whole of ParcelRound's METHOD.md, 78,786 bytes, where
`o200k_base` counts 19,866 (MEASURED). What the tool counts is not known. With
its line-number prefixes added, `o200k_base` counts 25,529 (MEASURED by the
verifier). The kit states bytes and `o200k_base` tokens, and says which.

**Excluded, with the reason.**
- **archive/round2-ledger.zip and round3-ledger.zip**, cft-fp256's own rounds.
  The counts are word-bounded and MEASURED over each archive's members:
  - round 2: fp32 53, fp64 31, fma 13, overflow 13, underflow 10 and sticky 8;
  - round 3: softfloat 25, fp32 12 and fp64 8.
- **ParcelRound's tools/check_method.py.** It pins all six archives by sha256
  (`ARCHIVE_SHA256`, tools/check_method.py:225-232, READ), and its
  `archive_pins` refuses a missing one: "a pinned record is gone" (:719-735,
  READ by the verifier). It also fails in this shallow clone: "anchors FAIL
  ... ADOPTION.md names commit 868f95e, which is not in HEAD's history"
  (MEASURED, rc 1, 9 of 10 checks hold). That it passes with full history is
  BELIEVED; it was not run. The kit's own gate (section 8) is the runnable
  example of a gate with controls.

**Round 4's ledgers are back in**, by Logan's "cft-fp256 only". Draft 1 left
them out because that round's project is built on libcft (CASE-STUDY-4.md:58).
A scan since found, all MEASURED:
- no URL into cft-fp256;
- no `host/src/` path and no `cft_golden`;
- one call to a `cft_` function, in P1.md.

Their numerics (binary64 82, ulp 34 and binary32 22, word-bounded, in the first
ledger) are that project's, not cft-fp256's code.

**The rules.** Each has its count declared beside it, and the build fails if a
count differs, so a source that moves cannot slip through:

| rule | what it does | count |
|---|---|---:|
| R1 | A Markdown link into `github.com/loganw234/cft-fp256` keeps its text, loses its target, and gains "(cft-fp256's record; not in this kit)". | 12, all in ParcelRound METHOD.md (MEASURED) |
| R2 | A link to `github.com/loganw234/ParcelRound` becomes the kit-relative path. | 3, one each in HonestFramework METHOD.md, FAILURE-MODES.md and WITH-PARCELROUND.md (MEASURED) |
| R3 | A link to a file the kit leaves out keeps its text, loses its target, and gains "(not in this kit)". | 3: CASE-STUDY-2.md:580 and CASE-STUDY-3.md:781, the excluded archives, and README.md:29, tools/check_method.py (MEASURED) |
| R4 | Inside an archived ledger's member, a URL into cft-fp256, in any host form or spelling (the regex-escaped site included), becomes its path as text, marked "(cft-fp256; not in this kit)". | 15. Round 5: P1.md:134, verifier-P1.md:305 and briefs/P1.md:74, the last written `https://loganw234\.github\.io/cft-fp256/`. Round 6: P2.md:153 and :437; P3.md:104, :388, :391, :409 and :412; P4.md:80, :159, :209, :294 and :384 (MEASURED) |
| R5 | Inside an archived ledger's member, a home path's user segment becomes `<user>`, and an address at a personal domain becomes `<address>`. The builder holds the personal domains by sha256 only. | Lines, MEASURED; the build declares the occurrence counts. Round 4: 61 home-path lines, and 4 addresses at Logan's own domain. Round 4's second ledger: 14 home-path lines. Round 5: 42 home-path lines, and 9 addresses at loganw.dev. Round 6: none. |

R4 and R5 rewrite only the members that hold a match. Every member keeps its
timestamp, the zip keeps its members in order, and every other byte stays as it
was.

These addresses are left as they stand:
- example.com, example.invalid and evil.example, which are reserved names;
- amazon.com's public contact, which ParcelRound's own gate also keeps
  (tools/check_method.py, `KNOWN_PRIVACY`);
- noreply@anthropic.com.

The tracked method texts hold no home path and no personal address (MEASURED;
ParcelRound's only ones are in tools/check_method.py, which is excluded).

**Left as it stands:**
- **Prose that names a cft-fp256 file**, as in "docs/VALIDATION.md:16682, at
  `4190a47`". It is the record's citation and carries no code.
- **The two loganw.dev URLs in CASE-STUDY-5.md.** The site is not cft-fp256's
  code. Its pages that show cft-fp256 are off limits by CLEAN-ROOM.md (section
  3, item 3).
- **round6-practice-survey.md:18**, which names the round-4 archives in code
  font, not as a link. They are now included.

**Stated as limits**, in START-HERE.md:
- METHOD.md:22-24 and ADOPTION.md:11 describe tools/check_method.py, which is
  not in the kit.
- METHOD.md:12-18's citation forms point at ledgers archived beside the case
  studies; two of the six are absent.
- ParcelRound's citations of cft-fp256, and QRO-Crate's, dangle.

### 4.2 The layer written for the hackathon

All new, short, and each with its sources cited. The target is 15,000 tokens
for all of it (BELIEVED).

| file | what it holds | built from |
|---|---|---|
| START-HERE.md | The front door: what the kit is; the reading order for each role, with sizes (generated, `--check`); the limits of section 4.1; and the five things that bind from the first minute: the clean room, the ledger, the escalation channel, nothing pushed without Logan's word, and the kit's own gate | HonestFramework METHOD.md section 10 |
| ROLES.md | Owner, lead, parcel, verifier: what each decides, what each asks, what each must never do | ParcelRound sections 3, 6 and 7; templates/checklists.md; OWNER.md |
| WORKFLOW.md | The round, phase by phase, with exit criteria and the template each phase uses (section 5); the planted-fault protocol (section 3, item 7) | ParcelRound sections 1 to 8; HonestFramework sections 1 to 3 and 9 |
| OWNER.md | Logan's words for the hackathon; his standing rules from other projects, verbatim with dates and sources; the rules his leads added; what the lead asks first (below) | as cited below |
| PROJECT.md | The softfloat charter: what is fixed, the standard's place, and the questions for the lead's study (section 6) | Logan's words |
| GLOSSARY.md | The evidence tags; (a), (b) and notes; READY and NOT READY; known limit; send-back; restate; the chain; wave; seam; P0; plant and key | the uses in cft-fp256's and QRO-Crate's records (below) |
| CLEAN-ROOM.md | Section 3, item 3 | Logan's words |
| METRICS.md | Section 7 | cft-fp256's record format; ParcelRound section 7 |
| HARNESS.md | A template, filled on day 1 as docs/HARNESS.md in the softfloat repository | section 3, item 2 |
| BOARD.md | The Pico protocol, a template filled on day 1 as docs/BOARD.md in the softfloat repository | section 3, item 5 |
| AGENTS.md | Seed agent notes for the softfloat repository. The front door is P0's to set. The desktop's traps apply if the agents run on Logan's desktop. Where the agents run is not known until kickoff, so each trap says the condition it holds under. | HonestFramework templates/agent-notes.md; QRO-Crate CLAUDE.md, "What bites" items 1 and 2; cft-fp256 CLAUDE.md's desktop entries (the `\| grep \| head` deadlock; the two MSYS `/tmp`s) |

**OWNER.md's standing rules.** Each is quoted with its date and source, all
READ. All of them are listed, and which apply is settled at kickoff: "List all
8, I will discuss which apply with the Meta model" (Logan). Rule 9 was found by
the verifier after he answered.

1. **2026-09-27, the send-back rule.** "Only a regression or a wrong answer
   sends work back; anything else merges as a recorded known limit, and a
   sentence that claims more than is true is restated at the merge, not left
   standing" (ParcelRound METHOD.md:1125-1127). Logan's words: "Agreed with
   the only regression or wrong answer being send backs"
   (archive/round6-practice-survey.md:115, B3).
2. **2026-09-29, long runs.** "dont have the individual agents all run the
   full suites, have them hand back large runs to you to monitor rather than
   them, but they should still verify and test as much as they can quickly"
   (METHOD.md:1236-1239).
3. **2026-10-12, tiers.** "For 'simpler' level tasks, you may also utilize
   Sonnet for the Parcels and Haiku for the verifier. But only when its not a
   'challenging' task" (cft-fp256 docs/VALIDATION.md:20101).
4. **2026-10-13, small fixes.** "Go ahead and handle the two task chips first
   before we move on, with a Sonnet parcel and verifier for each. Unless they
   are very small fixes, in which case you can handle them and utilize a
   verifier to check" (VALIDATION.md:19293).
5. **2026-10-15, models in QRO-Crate's round.** "Use Sonnet models for the
   parcels in this round, as well as for the verifiers. ... Difficult parcels
   still get opus, though most of this work is not "difficult" so to speak"
   (QRO-Crate docs/VALIDATION.md:1167-1171).
6. **2026-10-15, the loose cap.** "If the last rounds have just been semantic
   changes and nothing related to code directly, round 6 can be the last, with
   the verifier instructed not to hold it back for prose only issues"
   (QRO-Crate docs/VALIDATION.md:789-792), as QRO-Crate CLAUDE.md:105 states
   it (item 6).
7. **Commits and pushes by Logan's word.**
   - "Nothing is committed or pushed without Logan's word" (QRO-Crate
     CLAUDE.md:104, item 5).
   - His words of 2026-10-14: "Go ahead with the first commit once P0 is
     READY, you can also make a remote repo to push to as well" (QRO-Crate
     VALIDATION.md:922-924).
   - His words of 2026-10-16: "You are clear to commit and push when ready"
     (VALIDATION.md:2473-2474).
   - For the softfloat repository, 2026-10-23: "yes to remote, just create a
     private repo for now".
8. **2026-09-30, the pause.** "Go ahead and instruct agents to wrap up for
   now to take a pause, commit where they are and leave a resume note for
   themselves incase context is lost in the downtime" (cft-fp256
   VALIDATION.md:16510; ParcelRound METHOD.md:542-544 quotes its second half).
9. **2026-09-25, load.** "Logan, 2026-09-25: no agent loads the machine on
   purpose" (cft-fp256 VALIDATION.md:15443). These are the record's words, not
   a quotation of his. The record carries the rule as "Logan's rule" at :15797,
   and as "Nothing loaded either machine on purpose" at :16664, :16840 and
   :17030 (READ by the verifier). It matters if the agents share Logan's
   desktop.

**The leads' brief rules.** These are not Logan's words. They are kept apart
from his and marked as the leads':
- a time box and a scope ceiling in every brief (cft-fp256
  VALIDATION.md:21733). Logan on them, 2026-10-20: "If needed it can have more
  time, though how have the time bounds been working so far? I noticed you
  started giving the agents them, good choice" (VALIDATION.md:22537);
- "NEVER change any git configuration" (:22676);
- "wait on one quiet event; do not report a wait" (:22681).

**Reading the tiers.** Rules 3, 4 and 5 name Claude models. For the hackathon,
OWNER.md reads "Opus" as the most capable tier and "Sonnet" as one step down,
and nothing in Logan's words places "Haiku". That reading is the lead's, marked
as such, for the kickoff discussion.

**What the lead asks first, and records the answer.** Each item is marked with
its source:
- **The method's three** (ParcelRound METHOD.md:1372-1377): "a push that
  deploys, a remote branch deleted, a change to how results are counted".
- **Logan's:**
  - every commit and push (rule 7);
  - models and tiers (rules 3 and 5 are his);
  - scope (his "Undecided yet", and PROJECT.md's questions);
  - the standard's PDF (his licence, section 6).
- **The lead's own additions**, marked as such:
  - any exception to a standing rule;
  - any suspected contact with cft-fp256;
  - anything that would put Logan's name, address or data in front of a third
    party.

Board time is not on the list, because "Lead controls hardware access"
(Logan). Everything else the lead decides by the standards: unattended, it
merges, verifies, diagnoses and records within the project's rules, and puts
the owner's questions in the ledger (METHOD.md:1364-1370). Logan's words are
recorded with their dates, and the lead's reading goes beside them, marked as
the lead's (METHOD.md:1379-1386).

**GLOSSARY.md.** It sets each tag out as the records use it, sampled by the
verifier (READ), and marks where two records differ:
- **MEASURED**: run, the output in hand. cft-fp256 names who ran it and where
  ("MEASURED by RT at 949e56c", VALIDATION.md:18913).
- **READ**: read, not run. That covers a file and line, a report, a page or a
  search ("(READ, by VCI)" :20929; "(READ, the project's page)" :21941;
  QRO-Crate's "(READ, a search of its tree)").
- **COMPUTED**: arithmetic on measured or read figures. cft-fp256 does not
  always show the arithmetic ("(COMPUTED)" :18110), and the kit asks that it
  be shown. QRO-Crate's documents never use the tag: 0 lines, against 589 for
  MEASURED, 228 for READ and 105 for BELIEVED (MEASURED by the verifier).
- **BELIEVED**: an estimate, an inference, or a claim not checked ("BELIEVED
  where a word was not checked" :18253).
- **(a) and (b)** are cft-fp256's classes: "Only a regression "(a)" or a wrong
  answer "(b)" sends a parcel back. Everything else merges as a recorded limit,
  with its false sentences restated at the merge" (VALIDATION.md:15854).
  - A false sentence has been classed (b): "(b)2, a sentence the merges made
    false" (:17961).
  - The record handles one both ways. "P1 was sent back a second time for it"
    (:15903). "no: the lead fixed the wording three times" (:22587).
  - So GLOSSARY.md says what rule 1 says: a false sentence is restated at the
    merge. The author restates it when a send-back is going anyway. The lead
    restates it as a very small fix past a verifier (rule 4) when nothing else
    sends the work back.
- **QRO-Crate's split** is the other practice. It separates "a defect in what
  the code does" from prose (CLAUDE.md:105-109).

### 4.3 `examples/`: prior work, each with a provenance header

`examples/README.md` is an index, not a second copy. It points into what the
kit already carries, by path and purpose.

**Rounds 4, 5 and 6** (method/parcelround/archive/).

Round 6 holds:
- a common brief, `briefs/_common.md`;
- the parcel briefs;
- a verifier brief for a planted copy, `briefs/_verifier.md`;
- an integration verifier's brief;
- the keys (`keys/*.json`), whose limit is stated in section 3, item 7;
- the ledger's README;
- the lead's ledger;
- the verifiers' ledgers.

Round 5 holds its urgent messages and its seam verifier's brief. Round 4 holds
three parcel briefs, and a verifier on the lead's P0 that went at least five
passes (CASE-STUDY-4.md:118, READ).

Some lines name Claude Code's tools. Round 6's verifier brief, for one, says to
message the lead with "SendMessage; load it with ToolSearch". The index labels
each such line as that harness's.

**QRO-Crate**, in the zip ("Bundle", Logan), in this form:
- **A snapshot of its tree at `8afeede`** (`git archive`), and **a history
  file**: its six commits' hashes, dates, subjects and messages.
- **No git bundle.** Every one of its six commits carries Logan's email
  address as author and committer (MEASURED, `git log --format`, read by
  domain), and a bundle would take that address into the Meta directories.
  That is the lead's reading of K1 and of "licensed to me"'s spirit, for
  Logan to correct (section 10, Q4).
- **No URL into cft-fp256** in any commit's tree or message (MEASURED, a `git
  grep` of every commit, and of every message).

What it shows:
- its plan of record, and its verifiers' reports on twelve drafts
  (docs/studies/QRO-0.md and docs/reviews/QRO-0/);
- its lead's P0, past verifiers six times (docs/reviews/P0/);
- P0.1 to P0.5, past verifiers 4, 4, 2, 4 and 4 times (docs/VALIDATION.md's
  headings, MEASURED);
- its record entries, its agent notes (CLAUDE.md), its front door
  (verify/run.sh), a generated vocabulary with `--check`, and plants
  (controls/).

Three cautions go with it:
- **It shows no parallel parcels yet.** Its pace was six verifier rounds on
  one P0, which a ten-day round cannot afford, so the caps of section 5.3 are
  for the kickoff discussion.
- **52 of its lines name cft-fp256** (MEASURED, `git grep -c -i cft-fp256`).
  - 43 are in documents, about the certificate format and the number
    spelling.
  - 9 are in code, tests and tools: qro/ 5, tests/ 2 and tools/ 2 (MEASURED
    by the verifier).
  - The code follows cft-fp256's documented rules, and its docstrings say
    so, all READ:
    - qro/spelling.py:70-71 writes "A binary64's exact decimal, in
      cft-fp256's one spelling", on Python's `Decimal`;
    - tests/format/test_spelling.py:17-21 holds nine values of cft-fp256's
      spelling;
    - qro/reader.py:4 is "cft-fp256's strict reader, docs/CERTIFICATES.md:
      852-899, READ, adapted to JSON-LD";
    - tools/check_docs.py:21 and :34 list cft-fp256 among the foreign
      repositories whose paths are their own.
  - Whether any line was copied from cft-fp256 is not checked.
  - An exact decimal is not a correctly rounded conversion. That it gives the
    softfloat no real help is BELIEVED, and keeping these files is Logan's
    call (section 10, Q5).
- **In the kit, those citations dangle**, by design.

**`examples/cases/`: "many samples of "how things should be handled""**
(Logan). These are verbatim passages from cft-fp256's record, one situation
each. A read-only surveyor of that record is finding candidates; its report
becomes docs/reviews/KIT-0/survey-cases.md. Build step 4 (section 9) chooses
the samples from its table, and v1's verifier checks the choice.

Each sample's header gives:
- the entry and its line range;
- what the passage shows;
- every cut and its reason;
- the licence: cft-fp256 is Apache-2.0, "Copyright 2026 Logan W." (cft-fp256
  NOTICE, READ). The kit does not copy the NOTICE file, which holds a URL
  into cft-fp256.

Beside the samples goes the skeleton of a closed-wave entry: the section
order of the most recent closed entries, as the survey measures it. With it go
whole process sections of the coverage wave's close (cft-fp256
docs/VALIDATION.md:22529-22790):
- "What Logan asked, verbatim";
- "The chain";
- "Conduct";
- "The experiment";
- "Time and tokens", with its method line;
- "Corrections this record owes".

The case studies have per-agent cost tables of their own (CASE-STUDY-3.md:541,
-4.md:248, -5.md:290 and -6.md:293, READ by the verifier). What the record's
samples add is minutes per pass against time boxes, and (a) and (b) per pass.

### 4.4 `tools/`: what the agents run

- **`ledger.sh`.** `append <file> <headline>` writes a heading stamped from
  `date`, with the Measured, Believed and For lines. That is ParcelRound
  section 4's stamp rule, made mechanical. `urgent <author> <slug>` composes a
  message elsewhere and renames it into place.
- **The watcher.** It is a snippet in the ledger's README to paste inline, not
  a script file. ParcelRound METHOD.md:677-686 says why: "Arm the watcher from
  an inline command, not a script file".
- **`plant.py`.**
  - `make` builds a verifier's copy as a fresh one-commit repository with no
    remote, no branches and no route back to the parcel's tip. It applies the
    plants from a key in round 6's format: `real_tip`, `copy_commit`, and
    `plants[]` of `file`, `old`, `new` and `shape`. Then it prints the key's
    sha256.
  - `list` shows each plant beside the verifier's report, for the lead to
    grade by reading. It does not grade.
  - Each refusal is planted in its self-test: a plant whose `old` text is not
    found, a plant found twice, and a copy that still holds the parcel's tip in
    its history.
- **`round_metrics.py`.** Section 7's tables, from section 7's sources. It has
  a usage-log adapter for a generic JSONL, and a manual fallback whose rows are
  marked as transcribed. Its self-test has fixtures and plants.
- **`check_kit.py`.** The kit's gate (section 8). The agents run it first, on
  day 1.

The runner and the generate-and-check pattern are HonestFramework's, in
method/honest/templates/, for the softfloat repository's P0 to adopt if its
study chooses them.

### 4.5 `MANIFEST.txt`

The kit's version, the builder's commit, the source commits, the rules' counts,
and the sha256 of every file. `check_kit.py` verifies it. Every table
METRICS.md derives names the kit's version in its header.

---

## 5. The workflow WORKFLOW.md lays out

### 5.1 Phases, and what ends each

0. **Day 1.**
   - Read START-HERE.md, then run `tools/check_kit.py`.
   - Make the softfloat repository, with its private remote ("yes to remote,
     just create a private repo for now", Logan).
   - Fill docs/HARNESS.md and docs/BOARD.md there from the kit's templates,
     with Logan.
   - Settle the standing rules, the caps and the verifiers' tier with Logan.
   - Make the ledger outside every worktree.
   - Arm the escalation channel and test it: "A test escalation at dispatch
     must reach the lead" (ParcelRound section 4).
1. **The survey.** Read-only surveyors read the ground, and report facts with
   their sources, each tagged (ParcelRound section 1, "Survey the tree before
   the plan, read-only"). The ground:
   - the standard, Logan's PDF, given to the lead and not in the kit;
   - the RP2040's datasheet;
   - pico-sdk's float support;
   - SoftFloat and TestFloat;
   - published hard cases.
2. **The study, SF-0, the plan of record**, in the softfloat repository. It
   covers:
   - its proposed answers to section 6's questions, put to Logan as
     questions;
   - the authority and the oracles (HonestFramework section 1);
   - refusals (section 2);
   - the gates, with their negative controls (section 3);
   - P0;
   - the parcels and the waves;
   - how the metrics are captured.

   It ends when a verifier's re-check finds no (a) or (b), or the draft cap
   is reached with the open findings listed, and Logan approves.
3. **P0, the lead's.** In a new repository, P0 is the seam, not a refactor. A
   proposal for what it might hold, which the study decides (K3):
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
   - each parcel's verifier works on a planted copy (section 3, item 7);
   - send-backs follow OWNER.md's rule 1, if it applies: a regression or a
     wrong answer goes back, and a false sentence is restated at the merge;
   - the lead merges serially, with the gate after each merge;
   - an integration verifier checks the lead's merges and record;
   - the lead writes a closing record entry, whose tables `round_metrics.py`
     makes.

   The keys are revealed only after every planted verifier in the round has
   reported.
5. **Board sessions**, by docs/BOARD.md.
6. **The close.**
   - The keys revealed, and the grading recorded.
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

These are proposals for the kickoff discussion, where Logan settles them with
the lead to fit the harness (section 3, item 6). As evidence beside them:
QRO-Crate's study went twelve drafts, and its P0 six verifier rounds (section
4.3).

- **The study:** at most three drafts and two re-checks, then it goes to
  Logan with its open findings listed.
- **Verifier passes:** the loose cap (OWNER.md rule 6), if it applies. After
  three NOT READY verdicts whose reasons grow more menial, only a defect in
  what the code does blocks.
- **Every brief:** a time box and a scope ceiling.
- **The calendar:**

  | days | dates | what |
  |---|---|---|
  | 1 | Mon 10-26 | setup and the survey |
  | 2 | Tue 10-27 | the study, its verifier, and Logan |
  | 3 | Wed 10-28 | P0 |
  | 4 | Thu 10-29 | P0's verifier; the first wave dispatched |
  | 5 to 8 | to Mon 11-02 | two or three waves |
  | 9 | Tue 11-03 | integration, and the board's conformance runs |
  | 10 | Wed 11-04 | the keys, the record, the metrics and the summary |

  The lead plans around Logan's hours. Decisions wait for him in the ledger
  (ParcelRound section 7, unattended).

---

## 6. PROJECT.md: the softfloat charter

**Fixed, by Logan's words:**
- "an IEEE-754 compliant softfloat for RP2040, for binary16/32/64";
- a Pico "constantly connected for debugging", whose access the lead controls;
- web access to third-party code, with "the only restriction ... staying away
  from cft", meaning cft-fp256.

**The standard.** "It wont be included in the zip as its licensed to me, but
I will also be giving the Meta lead the real IEEE 754 pdf for reference, so
they will have the material needed in terms of the contract, but not
necessarily how to achieve it" (Logan). So PROJECT.md says:
- **The standard is the contract**: what conformance requires.
- **It is not the authority** of HonestFramework METHOD.md section 1. The
  study names an executable authority and its oracles, and Logan approves
  them.
- **The PDF is Logan's**, under his licence. It goes in no repository and no
  zip, and the record cites it by clause. That last rule is the lead's
  reading of "licensed to me", for Logan to confirm at kickoff.
- **Who besides the lead reads it** is the lead's decision.

**The questions.** The lead's study puts these to Logan, each with its own
proposal, and the kit proposes no answers. The lead's statements about the
standard are from memory, so they are BELIEVED until the lead reads the PDF.

1. **The edition.** IEEE 754-2019 or 2008. The edition changes the required
   set. In 2008, minNum and maxNum are in clause 5; in 2019, the minimum and
   maximum operations are recommended ones in clause 9 (BELIEVED, the
   verifier's reading).
2. **The formats.** Each of binary16, binary32 and binary64 is either an
   arithmetic format or an interchange format only (BELIEVED: binary16 can be
   either). An arithmetic format takes all of clause 5's operations (BELIEVED:
   section 5.1 of the standard), the conversions to and from decimal
   character sequences among them, and they are a large piece. Clause 9's
   recommended operations (exp, log and the rest): in or out.
3. **Rounding.** roundTiesToEven and the three directed attributes are
   required. roundTiesToAway is required only for decimal formats. In or out
   here?
4. **Exceptions.**
   - Default handling, and the five flags.
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
9. **The authority and the oracles.** The study proposes, and Logan approves.

---

## 7. METRICS.md: which source each figure comes from

Six of these rows rest on what agents write. For each, the table names its
cross-check. Draft 1's title, "every figure from a source the agents don't
write", was false (the verifier's B5).

| figure | source | does an agent write it? | cross-check |
|---|---|---|---|
| Tokens (output, input, cached), messages, the model per message | The TUI's usage log, or the API's, whichever docs/HARNESS.md finds on day 1. Failing both, the TUI's own counters, transcribed and marked as such. | no; a transcription is marked | the sums against the TUI's totals |
| Tool uses | The transcript | no | — |
| Minutes per pass | The transcript's stamps, from each prompt of the lead's to the pass's last line (cft-fp256 docs/VALIDATION.md:22742, READ) | no | — |
| Commits; diff size against the scope ceiling; files outside the ownership list | git | no | — |
| Gate runs | The runner's JSONL record | no | the log read against it |
| Findings, and their classes | The verifier's report, each confirmed or rejected by the lead in the ledger | yes | the integration verifier reads both |
| Plants caught | The lead's grading of each report against its key | yes | the key's hash, recorded before dispatch; the integration verifier |
| Brief corrections | The report's "what this brief got wrong", counted, with the lead's acceptance | yes | — |
| Escalation latency | The ledger's stamps, written by `ledger.sh` from `date` | yes, by tool | the transcript's stamps |
| Conduct, and the lead's slips | The record's lists | yes | git, the filesystem, and the integration verifier |
| Logan's words | The record, verbatim, with dates | yes, a transcription | the TUI's conversation log, where it keeps one |

`round_metrics.py` makes these tables, per wave and for the hackathon:
- the chain: work, author, the verifier's passes with (a) and (b) per pass, and
  send-backs;
- time and tokens: agent, model, passes, minutes for the first pass and in
  all, tool uses, output tokens, input tokens;
- each brief's time box and scope ceiling against the actual;
- plants;
- brief corrections;
- escalations.

cft-fp256's coverage wave measured tokens as "output tokens summed from the
last line of each response" (VALIDATION.md:22742, READ). The adapter states its
own method beside its figures.

**Comparisons.** Tokens read depend on a harness's caching. Across harnesses,
compare output tokens and minutes; compare tokens read only within one harness.

**The audit**, Logan's tool. It lives in the builder repository and is never in
the zip.
- **What it holds:** fingerprints of cft-fp256's arithmetic sources, as hashed
  k-grams of normalized tokens. The files are:
  - host/src/ and python/cft_golden/;
  - python/hardcases.py, python/external_*.py and vectors/gen_vectors.py.

  Any other file is outside its reach, and that is stated.
- **When it runs:** against the softfloat repository, at each wave's close and
  at the end.
- **Its self-test,** run in the builder: real cft-fp256 functions, which it
  must flag, and Berkeley SoftFloat 3e functions, which it must not.
- **Its false-alarm rate** is measured and stated (HonestFramework METHOD.md
  section 3: "A signal's rank ... is set by its measured false-alarm rate").

The agents know from CLEAN-ROOM.md that the audit exists, and never see its
data. It is not needed at kickoff, so it is built after v1 (section 9).

---

## 8. The kit's gate, and its controls

`check_kit.py` runs these checks on the unpacked zip. **It reads inside every
zip archive the kit carries, and inside the QRO-Crate snapshot.**

1. **The manifest.**
   - Every file's sha256 matches.
   - No file is outside the manifest, and none the manifest lists is missing.
   - The manifest names the source commits and the rules' counts.
   - The kit holds no PDF. The standard is Logan's, and nothing the kit
     carries is a PDF (the archived ledgers' members are .md, .py, .out and
     .json, MEASURED).
2. **Links.**
   - Every relative link resolves inside the kit.
   - No URL leads to cft-fp256, in any spelling, the regex-escaped included:
     not `github.com/loganw234/cft-fp256`, not its raw, API or archive hosts,
     and not `loganw234.github.io/cft-fp256`.
3. **Arithmetic.** This check covers every place in section 3, item 1 that
   carries cft-fp256's text. No line there may hold a term from the list: the
   draft 1 list, extended by the survey's terms (section 4.3).
   - **This is a stated limit, not a guarantee** (ParcelRound METHOD.md:920-927,
     "A gate that reads source text is a stated limit, not a guarantee"). The
     list catches a line that names a listed term. It cannot see arithmetic
     described in other words, and the verifier found four such lines in the
     coverage wave's sections alone: VALIDATION.md:22600, :22603, :22614 and
     :22689.
   - **So a reading backs it.** The lead reads every sample whole against the
     criterion "no arithmetic method or implementation detail", and so does
     v1's verifier. The list is the backstop.
   - **It also over-fires.** It fires on the round 5 and 6 ledgers, which
     hold binary64 7 times and overflow twice (MEASURED) and carry no
     arithmetic. So a cut is not evidence of arithmetic, and each sample's
     header lists its cuts.
4. **Privacy.**
   - No home path, no email address but the kept ones of section 4.1, and no
     key or token of the shapes in QRO-Crate's tools/check_privacy.py.
   - No private-range IPv4 address (10/8, 172.16/12, 192.168/16), and no
     user@host that names a machine. The template's `<ssh user@addr>`
     placeholder (HonestFramework templates/agent-notes.md) is not one.
   - What passes: round 4's one IPv4-shaped string, `5.15.153.1`, BELIEVED a
     version number; round 5's 127.0.0.1; and round 5's three public
     addresses, BELIEVED to be hosting services' (all MEASURED, a scan of every
     member).
   - Personal domains are held by sha256, so the gate never names them.
   - A fixture shaped like any of these is built in pieces at run time, as
     QRO-Crate's plants are (its CLAUDE.md, "What bites" item 3).
5. **Generated files.** The reading table in START-HERE.md and the examples
   index match their generators (`--check`).

In the builder, `build_kit.py --check` also re-derives `method/` and the
repacked archives from the pinned sources, and compares them byte for byte.
The zip carries no sources, so check 1's hashes stand in for that there.

**Controls.** `--control` plants each fault in a copy and confirms the matching
check fails and names it. Each plant restores the bytes it planted over exactly
(ParcelRound section 5). There is one plant for each shape the checks refuse:
- a changed byte;
- an extra file;
- a missing file;
- a PDF;
- a broken relative link;
- each cft-fp256 host form, and the regex-escaped spelling, inside a file and
  inside a zip member;
- an arithmetic term in a sample;
- each home-path shape;
- an address at a personal domain;
- an IP address;
- a user@host;
- a stale reading table.

---

## 9. The builder, and the order of the build

These steps follow Logan's approval of this plan.

```
softfloat-bootstrap/          (private)
  README.md, CLAUDE.md        what this is; the front door; what bites
  docs/KIT-0.md               this plan
  docs/VALIDATION.md          the record
  docs/reviews/               every verifier's and surveyor's report
  kit/                        the layer of section 4.2, and the tools of 4.4
  build/sources.lock          each source: repository, commit, paths
  build/build_kit.py          copy, rules with counts, --check, dist
  audit/                      section 7's audit; reads cft-fp256; never in the zip
  tests/                      the builder's tests; the gate's controls
  verify/run.sh               the front door, after HonestFramework's gate-runner.sh
  dist/                       ignored: the zip and its SHA256SUMS
```

1. The skeleton, the runner, and this repository's agent notes.
2. `build_kit.py`, the rules with their counts, and `method/` derived, with
   `--check`.
3. The layer of section 4.2: Logan's words verbatim, and every rule with its
   source.
4. `examples/`: the index, the samples (each read whole against check 3's
   criterion) and the skeleton.
5. `tools/`, each tool with its self-test and plants.
6. `check_kit.py` and its controls.
7. `make dist`.
8. **A cold read.** A fresh agent with only the zip, in an empty directory,
   answers a fixed list of questions about the roles, the ledger, the
   send-back rule, the clean room and the first day. Its answers are scored
   against a key written before it runs, in the three steps of HonestFramework
   METHOD.md:696-700. This shows the kit works for a reader who has nothing
   else.
9. **A verifier** on the built kit and on the builder (ParcelRound section 7:
   the lead's work goes past a verifier).
10. **Logan's word.** Then the private repository is created, the work is
    committed and pushed, and the zip is exported.

v1 by Sunday 2026-10-25 (BELIEVED feasible). The audit follows, before the
first wave closes.

---

## 10. Questions for Logan

Each has the plan's proposal beside it.

1. **This plan.** Do you approve it as the plan of record?
2. **The last step of section 9.** May the lead create the private repository
   `softfloat-bootstrap` and push v1 once v1's verifier finds it READY, or do
   you want to see v1 first? Proposal: create and push on the verifier's
   READY, and send you the zip.
3. **The softfloat repository's remote.** On "just create a private repo for
   now": is that one for the lead to create now, and under what name, or at
   kickoff, by you or the Meta lead? Proposal: at kickoff (section 5.1, phase
   0).
4. **QRO-Crate's history.** Is a tree snapshot plus a history file enough, or
   do you want the real git history in the zip, which carries your email
   address in all six commits? Proposal: the snapshot.
5. **QRO-Crate's code that follows cft-fp256's documented rules** (section
   4.3): keep it, or leave those files out? Proposal: keep it.
6. **Personal data in the archives.** R5 replaces home paths' user segments
   and personal addresses in the ledgers of rounds 4 and 5. Proposal: as R5
   says.

---

## 11. Draft 1's findings, and what draft 2 did with each

The findings are the verifier's (docs/reviews/KIT-0/draft1-verifier.md). The
lead checked each finding that changes the plan or corrects a claim before
acting on it (ParcelRound METHOD.md:781-785, "Verify an escalation like any
other report"). MEASURED or READ again by the lead, this session:
- B2's EMBEDDED.md:673-677 and :685;
- A3's QRO-Crate lines;
- A5's citations in CASE-STUDY-6.md, ADOPTION.md and round 6's lead.md;
- A1's privacy counts, extended to rounds 4 and 6;
- N1's :15443 and N2's :16505 and :16510;
- B10's :789-792;
- the escaped spelling at round 5's briefs/P1.md:74.

| finding | what draft 2 does |
|---|---|
| A1, cft links and private data inside the archives | R4 (15 URLs, the escaped one included) and R5. Check 2 and check 4 read inside every zip. QRO-Crate goes in as a snapshot, not an opaque bundle. |
| A2, three dangling links; both MIT notices lost | Both LICENSE files are included, and check_claims.py with them. R3 takes README.md:29's link to check_method.py. |
| A3, QRO-Crate's code that follows cft-fp256's documented rules | Section 4.3 states it, with its lines, and puts it to Logan (Q5). The false sentence about the 52 lines is restated. |
| A4, check 3's list misses arithmetic described in other words | Section 8 states the limit, by the behaviour it concedes. A whole reading of every sample, by the lead and by v1's verifier, backs the list, and the survey's terms extend it. |
| A5, the keys revealed per report; round 6's conditions missing | Section 3, item 7: CS6#3, CS6#4 and CS5#8 taken in; round 6's copy conditions; grading by reading; the hash proposed into git. |
| A6, HARNESS.md and BOARD.md filled inside a frozen kit | They are templates. The filled copies live in the softfloat repository. |
| B1, the token figure | Restated: 27,193 is the whole file's count, by Claude Code's Read tool, whose method is unknown. |
| B2, cft-fp256 has not run on a Pico | Restated (section 2), and listed in section 12. |
| B3, a third repository carrying cft-fp256 | By Logan's answer, the restriction is cft-fp256 in any form, a submodule's view of it included. Atlas-film is named as the example. |
| B4, loganw.dev "not cft" | Restated: the site is built partly from cft-fp256, and its pages showing cft-fp256 are off limits. |
| B5, section 7's title | Retitled. Each row now says whether an agent writes it, and names its cross-check. |
| B6, "the only examples of the per-agent tables" | Restated: the case studies have per-agent cost tables. |
| B7, the send-back rule without its restate clause | Rule 1 quotes the clause, and GLOSSARY.md and phase 4 follow it. |
| B8, the ask-first list attributed wholly to METHOD.md:1372-1377 | Each item is marked: the method's three, Logan's, and the lead's own. Board time is off the list, by Logan's answer. |
| B9, the loose cap "only in CLAUDE.md"; "excluding cft drops it" | Restated (section 2). |
| B10, rule 6's lines | 789-792. |
| N1, the load rule | Rule 9. |
| N2, rule 8's date | 2026-09-30, with Logan's whole words. |
| N3, rule 4 names a Claude model | "Rules 3, 4 and 5". |
| N4, "not letting them browse my GitHub" against "cft-fp256 only" | Logan's later answer settles it: only cft-fp256 is restricted. |
| N5, check 2's list | It is cft-fp256's forms alone, by Logan's answer. |
| N6, cft-fp256 text outside check 3's directory | Section 3, item 1 lists every place, and check 3 reads them all. |
| N7, the GLOSSARY nuances | Taken in (section 4.2). |
| N8, the watcher | An inline snippet, not a script file. |
| N9, R3's target | R3 drops the target. |
| N10, carried text pointing at things left out | Stated as limits in START-HERE.md (section 4.1). |
| N11, no transcripts row in HARNESS.md | Added. |
| N12, `plant.py score` | Replaced by `list`, with grading by reading. |
| N13, the audit's reach | Widened, and its limit stated. |
| N14, P0's contents fixed by the kit | Marked as a proposal (K3). |
| N15, controls thinner than the checks | One plant for each shape (section 8). |
| N16, the protocol's evidence outside git | Stated, and the hash proposed into git (section 3, item 7). |
| N17, round 6's keys in the kit | Stated as a limit, and the lead plants shapes the kit does not show. |
| N18, the standard's points; where the agents run | Taken into section 6's questions 1 and 2. AGENTS.md's traps each state their condition. |

---

## 12. The lead's slips

Each is recorded in the order it was found.

1. **"cft-fp256 already runs binary32 and binary64 on an RP2040."** It does
   not: the Pico has never been attached (B2). The lead told Logan this in its
   first reply, and in draft 1.
2. **Draft 1's URL count read only the files git tracks.** It missed the 15
   URLs inside the round 5 and 6 archives' members: 14 found by the lead after
   the freeze, and the escaped one by the verifier.
3. **The token figure.** The lead read the Read tool's whole-file count as a
   count of the lines it showed (B1).
4. **"The loose cap is written only in QRO-Crate's CLAUDE.md"** (B9).
5. **The send-back rule quoted without its restate clause** (B7).
6. **Eight ask-first items cited to three lines of METHOD.md** (B8).
7. **"The only examples of the per-agent tables"** (B6).
8. **Section 7's title** (B5).
9. **The 52 lines called documentation only.** Nine are code, tests and tools
   (A3).
10. **Rule 6's line range** (B10).
11. **A key reveal that repeats round 6's recorded lapse** (A5).
12. **HARNESS.md and BOARD.md filled inside a frozen kit** (A6).
13. **"loganw.dev is not cft"** (B4).
14. **A git bundle of QRO-Crate**, which would carry Logan's address in its
    commits. Found by the lead after Logan's "Bundle", before any build.
15. **Personal data in the archives.** Round 5's was found by the verifier.
    Round 4's, the lead's own domain among it, was found by the lead.
