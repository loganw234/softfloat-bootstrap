# KIT-0: the bootstrap kit for the Meta softfloat hackathon

**Draft 3, 2026-10-23. The lead's (this session). The plan of record, by
Logan's word: "Approved if nothing major changes from the check".** Nothing in
this directory is committed yet, and no repository has been created.

- **Draft 1** went past a verifier: NOT READY, with six (a), ten (b) and
  eighteen notes (docs/reviews/KIT-0/draft1-verifier.md).
- **Draft 2** answered them, and went back to that verifier for a scoped
  re-check: NOT READY, with one (a), four (b) and nine notes
  (docs/reviews/KIT-0/draft2-recheck.md).
- **Draft 3** takes in the re-check. Section 11 says what each draft did with
  each finding, and section 12 lists the lead's slips.
- **The build** (v1) changed the kit from draft 3 where building it found
  something. Section 13 lists each change, with its reason, for v1's verifier
  to check and Logan to overrule. Draft 3's text stands as approved; where
  section 13 and an earlier section differ, section 13 is the kit.

The lead's reading of "nothing major": none of the re-check's findings changes
the kit's shape, its contents or one of Logan's decisions. The one (a) is the
gate's specification, which build step 6 tests and v1's verifier checks
(section 9). That reading is the lead's, and it is in the lead's report to
Logan, for him to overrule.

Evidence tags, as Logan's records use them (GLOSSARY.md, section 4.2):
- **MEASURED**: run in this session, the output in hand;
- **READ**: read at a named place, not run;
- **COMPUTED**: arithmetic on measured or read figures;
- **BELIEVED**: an estimate, an inference, or a claim not checked.

Paths are relative to `<repos>/`, the directory that holds the four source repositories. Sources read: HonestFramework at
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

His answers to draft 2's section 10, the same day:

| # | draft 2's question | Logan's answer |
|---|---|---|
| 1 | approve the plan | "Approved if nothing major changes from the check" |
| 2 | create the private repository and push v1 on its verifier's READY | "Go ahead once it passes" |
| 3 | the softfloat repository: now or at kickoff | "Kickoff" |
| 4 | QRO-Crate: a snapshot, or the real git history with his address in its commits | "Real address is fine" |
| 5 | QRO-Crate's code that follows cft-fp256's documented rules | "Keep" |
| 6 | strip personal data from the archived ledgers (R5) | "Okay to strip, not vital however" |

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

   The builder writes cft-fp256's text into these places, and check 3 reads
   each of them:
   - `examples/cases/` and the record skeleton;
   - the short quotations in OWNER.md, GLOSSARY.md and METRICS.md;
   - the desktop entries in AGENTS.md.

   The carried sources also quote cft-fp256, as they were published. None of
   it is arithmetic (READ by the verifier):
   - ParcelRound's texts cite and quote its record throughout;
   - QRO-Crate's docs/studies/QRO-0.md:292-295 quotes its CERT-V2.md;
   - round 5's briefs/P1.md:77-78 quotes its README.md:319;
   - round 4's ledgers name its tree paths and API facts, but carry no code
     (section 4.1's limits).

   Check 3 does not filter these. They are the sources' own text (K2).
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
       Quantum-Film's `vendor/cft-fp256`, "submodule 7d7285d" (round 4's
       lead.md:9-11 and briefs/P1.md:66; CASE-STUDY-4.md:55; READ by the
       verifier).

     Logan's site loganw.dev is "a static site generated from the owner's
     other repositories" (CASE-STUDY-5.md:19-21, READ), cft-fp256 among them
     (round 5's briefs/P1.md:72-74). Its pages that show cft-fp256 count as
     cft-fp256. That is the lead's reading of "staying away from cft", for
     Logan to correct. So the kit carries the site's address as text, not as a
     link (R6). His other projects are not restricted.
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
   - **Rulings wait too.** A ruling on a finding that touches only the copy
     describes a plant, so it waits for the reveal, with the keys. That is
     observation 6's other path: "The lead's entries that graded wave 1
     described each plant in prose" (CASE-STUDY-6.md:180-182, READ by the
     verifier).
   - **The copy goes out of reach.** Once its verifier reports, the lead moves
     the copy into its own scratch directory. A copy diffed against the merged
     real tip would give the key back early.

   Four consequences, stated in METRICS.md and WORKFLOW.md:
   - A detection rate measures the lead's plants and the verifiers' detection
     together.
   - The verifiers of the lead's own work get no plants, since no one but the
     lead holds keys.
   - The kit itself shows plant shapes: round 6's keys, round 4's
     `verifier-P0-work/plant_*.py`, and QRO-Crate's controls/. A verifier that
     read them knows those shapes, which is HonestFramework
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
| R5 | Inside an archived ledger's member, a home path's user segment becomes `<user>` where it is Logan's user name, and an address at a personal domain becomes `<address>`. The builder holds the name and the domains by sha256 only. | MEASURED occurrences. The user name: 121 (round 4 65, round 4's second ledger 14, round 5 42). Addresses: 13 (round 4 4, at the domain ParcelRound's `KNOWN_PRIVACY` holds by hash; round 5 9, at loganw.dev). Round 6: none. Round 4's three `/c/Users/.../` paths hold no name, and stay (the verifier's B12). |
| R6 | A URL to loganw.dev becomes text (section 3, item 3), in the texts and inside the archived ledgers' members. | 5 (MEASURED): CASE-STUDY-5.md 2; round 5's briefs/verifier-seam.md 2 and lead.md 1, found by the lead at the build, after draft 3 |

R5 is by Logan's word: "Okay to strip, not vital however" (draft 2's Q6).

R4 and R5 rewrite only the members that hold a match. Every member keeps its
timestamp, the zip keeps its members in order, and every unchanged member's
bytes stay as they were. The zip files themselves differ, since their CRCs,
sizes and offsets change. At deflate level 6, the originals' level, every
unchanged member re-compresses to its original bytes (MEASURED by the
verifier).

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
- **round6-practice-survey.md:18**, which names the round-4 archives in code
  font, not as a link. They are now included.

**Stated as limits**, in START-HERE.md:
- METHOD.md:22-24 and ADOPTION.md:11 describe tools/check_method.py, which is
  not in the kit.
- METHOD.md:12-18's citation forms point at ledgers archived beside the case
  studies; two of the six are absent.
- ParcelRound's citations of cft-fp256, and QRO-Crate's, dangle.
- CASE-STUDY-6.md:383-388 says its archive is "checked byte for byte" and
  that "The gate pins the archive's SHA-256"; CASE-STUDY-4.md:126 says
  "checked byte for byte". That is false of the kit's repacked copies.
- Round 4's ledgers name cft-fp256's tree paths and API facts, but carry no
  code (briefs/P2.md:22-25, :46, :71 and :99, READ by the verifier). Among
  them: `bindings/python/cftmpfr`, `host/cft.dll`, ABI 0.14, "libcft's
  correctly rounded functions", and two per-element timings.
- The archives' token counts above are from before the rewrite.

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
- **A git bundle of `main` at `8afeede`**, all six of its commits.
- **Logan's address goes with it.** Every one of those commits carries his
  email address as author and committer (MEASURED, `git log --format`, read
  by domain). He has allowed it: "Real address is fine" (draft 2's Q4). That
  is the one place in the kit where his address may stand, and check 4 allows
  it there, in the commits' identity fields, and nowhere else.
- **No URL into cft-fp256** in any commit's tree or message (MEASURED, a `git
  grep` of every commit, and of every message).
- **A bundle is opaque to a text search** (the verifier's A1). So the gate
  clones it into a temporary repository and reads every commit's tree and
  message, as it reads a zip's members.

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
      852-899, READ, adapted to JSON-LD".
  - tools/check_docs.py:21 and :34 only name cft-fp256, among the foreign
    repositories whose paths are their own.
  - Whether any line was copied from cft-fp256 is not checked.
  - An exact decimal is not a correctly rounded conversion. That it gives the
    softfloat no real help is BELIEVED. Logan keeps the files: "Keep" (draft
    2's Q5).
- **In the kit, those citations dangle**, by design.

**`examples/cases/`: "many samples of "how things should be handled""**
(Logan). These are verbatim passages from cft-fp256's record, one situation
each. A read-only surveyor of that record found the candidates. Its report is
docs/reviews/KIT-0/survey-cases.md, and its cut counts are MEASURED by its
scripts:
- 44 candidates across nineteen situations, all but one from 2026-10-12 to
  2026-10-22;
- 35 of them pass check 3's draft 1 list whole, and 9 lose a line or two;
- six more lose their point to a single term, and are left out.

Build step 4 (section 9) chooses the samples from that table, and v1's verifier
checks the choice.

Each sample's header gives:
- the entry and its line range;
- what the passage shows;
- every cut and its reason;
- the licence: cft-fp256 is Apache-2.0, "Copyright 2026 Logan W." (cft-fp256
  NOTICE, READ).

The kit does not copy the NOTICE file, which holds a URL into cft-fp256.
Apache-2.0 asks for the licence text and the NOTICE's attributions (sections
4(a) and 4(d)). The kit's NOTICE.md gives the attribution in words, without
the URL. That Logan, as the copyright holder, is not bound by his own licence
is BELIEVED, so how much of it the kit carries is his choice.

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
zip archive the kit carries, and every commit of the QRO-Crate bundle.**

1. **The manifest.**
   - Every file's sha256 matches.
   - No file is outside the manifest, and none the manifest lists is missing.
   - The manifest names the source commits and the rules' counts.
   - The kit holds no PDF. The standard is Logan's, and nothing the kit
     carries is a PDF (the archived ledgers' members are .md, .py, .out and
     .json, MEASURED).
2. **Links.**
   - Every relative link in a file the kit carries as a file resolves inside
     the kit.
   - Inside an archive member or a commit of the QRO-Crate bundle, only URLs
     are read. Relative links there belong to the record, written from their
     source repository's root, and are not resolved. There are 13 such links
     in rounds 5 and 6, round 6's P2.md:98 among them (MEASURED by the
     verifier).
   - No URL leads to cft-fp256, in any spelling, the regex-escaped included:
     not `github.com/loganw234/cft-fp256`, not its raw, API or archive hosts,
     and not `loganw234.github.io/cft-fp256`.
3. **Arithmetic.** This check covers every place in section 3, item 1 that
   carries cft-fp256's text. No line there may hold a term from the list.
   - **The list** is draft 1's, extended by the survey's section 3 (MEASURED
     by its scripts):
     - spellings the old list could not reach: `clause-5`, `conv32to64`,
       `cvtto` and `cvtfrom` without digits, and `f32_` and `f64_` names;
     - operation names: `divsqrt`, `divfull`, `rsqrt`, division, square
       root, reciprocal, Newton, Goldschmidt, and `scaleB`, `rint`,
       `nextup`, `nextdown` and `logb` without digits;
     - inflections that the closing `\b` blocked: overflows, underflows,
       exponents, rounded and rounds;
     - technique terms: round-to-odd, round-to-nearest, binade, enclosure,
       cancellation, limbs, inexact, signed zero, fused multiply-add,
       widening, narrowing, augmented, and the precision escalation;
     - "modular inverse";
     - transcendental names;
     - the oracle and test-source names (MPFR, mpmath, gmpy2, UCBTEST,
       FPgen, CORE-MATH, "golden model"). These are on the list because a
       sample naming cft-fp256's oracles would steer the study's choice of
       its own (K3).
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
   - No home path that holds Logan's user name.
   - No email address but the kept ones:
     - the reserved names, as a class (RFC 2606 and RFC 6761): `example`,
       `example.com`, `example.net` and `example.org` with their subdomains,
       and `.invalid`, `.test` and `.localhost`;
     - noreply@anthropic.com;
     - amazon.com's public contact.

     QRO-Crate's bundle holds 5 addresses at example.org and 1 at
     x.example.com (MEASURED by the verifier), and the class covers them.
   - No key or token of the shapes in QRO-Crate's tools/check_privacy.py.
   - No private-range IPv4 address (10/8, 172.16/12, 192.168/16).
   - No user@host whose user or host is one of Logan's names: his user name
     and his machines' names, held by sha256. A user@host shape that names
     none of them passes. That covers:
     - QRO-Crate's IRI test strings: "a@b/c" (tests/format/test_sweep.py:172),
       and "a@b" and "#a/b?c:d@e" (tests/format/test_spelling.py:162);
     - the template's `<ssh user@addr>` placeholder (HonestFramework
       templates/agent-notes.md).
   - What passes: round 4's one IPv4-shaped string, `5.15.153.1`, BELIEVED a
     version number; round 5's 127.0.0.1; and round 5's three public
     addresses, BELIEVED to be hosting services' (all MEASURED, a scan of every
     member).
   - Personal domains are held by sha256, so the gate never names them.
   - The one exception is the QRO-Crate bundle's commit identities, which may
     carry Logan's address by his word (section 4.3). A commit message or a
     file in it may not.
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
- an address at a personal domain, and one at a domain that is neither
  personal nor kept;
- each key and token shape of QRO-Crate's `ALTERNATIVES`, about twenty
  (tools/check_privacy.py:94-115);
- each private IPv4 range;
- a user@host that names one of Logan's names;
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

None is open. Every question the drafts asked is answered (section 1).

---

## 11. The verifiers' findings, and what each draft did

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

**The re-check of draft 2** (docs/reviews/KIT-0/draft2-recheck.md), and what
draft 3 does:

| finding | what draft 3 does |
|---|---|
| A7, checks 2 and 4 not re-derived against the archives' and the bundle's contents | Check 2 reads only URLs inside a member or a commit. Check 4 keeps the reserved names as a class, and refuses a user@host only where it names one of Logan's names. |
| B11, "the zip carries cft-fp256's text only in these places" | Restated (section 3, item 1): where the builder writes that text, and what the carried sources quote as published. |
| B12, round 4's 61 home-path lines | R5 declares occurrences: the user name 121 times, addresses 13. The three nameless paths stay. |
| B13, atlas-film as the example | Quantum-Film's `vendor/cft-fp256`. |
| B14, "one plant for each shape" | One plant per key and token shape, and per private range. |
| N19, rulings on copy-only findings in the ledger | They wait for the reveal, and each copy goes out of reach once its verifier reports. |
| N20, "every other byte" | Restated: every unchanged member's bytes. |
| N21, two carried claims of byte-for-byte archives | Added to the limits. |
| N22, round 4's cft-fp256 paths and API facts | Stated (section 3, item 1; section 4.1's limits). |
| N23, live links to Logan's site | R6: as text. |
| N24, R5's deferred counts; the archives' token counts | R5's occurrences declared; the token counts marked as before the rewrite. |
| N25, Apache-2.0's licence text and NOTICE | Stated, as Logan's choice (section 4.3). |
| N26, check_docs.py grouped with the code that follows cft-fp256's rules | Regrouped. |
| N27, the snapshot form | Moot: Logan chose the bundle, and check 4 reads every commit of it. |

**v1's verifier** (docs/reviews/v1/verifier-v1.md): NOT READY, 0 (a), 12 (b),
15 notes. The lead reproduced (b)1, (b)3, (b)4 and (b)6 before acting on them
(MEASURED). What the fix round does:

| finding | what the fix round does |
|---|---|
| (b)1, `plant.py`'s copy holds the unplanted text of every planted file, and `check` passes it | (Not whole: the re-check found the text could still come through the base's history; see its table below.) `make` leaves each planted file's original blob out, and refuses a plant in a file whose text another file of the tree shares. `check` refuses any object the copy's HEAD does not reach, alternates, a shallow file, a FETCH_HEAD and a reflog that names another commit. The self-test has a case for each: 84 checks. |
| (b)2, two of check 4's refusals never watched to fail | A plant for a bundle identity that is neither kept nor Logan's. Every plant counts only when the finding that names it appears. A plant for every finding the five checks give: 80. The builder's finding-mutants stage takes each of the gate's 31 finding sites out alone, and `--control` misses a plant each time (MEASURED). |
| (b)3, the gate passes a bundle git cannot read | A finding of checks 2 and 4, with a plant for each. |
| (b)4, the prefilter skips eight shapes on a dotted capital I | The text is folded as `re` folds, its four letters, before it is lowered. `--control` writes each privacy sample with each of them, 96 spellings, and requires each found. With the old fold, 15 of them are missed (MEASURED). |
| (b)5, the kit holds two of Logan's machines' names, 21 times; the builder's own privacy claims | Kept, and stated. MACHINE_NAMES holds his desktop's name. His Linux machine's name and his WSL distro's are in texts he published, and the QRO-Crate bundle's history holds one of them, which cannot be rewritten (section 13). The README and the agent notes restate what is held by hash, and say that his user name is his first name in lower case. |
| (b)6, R1 joins lines, so OWNER.md's five METHOD.md citations land on other text | R1 writes the line ends of the target it removes into its marker. The build refuses any rule that changes a file's line count, in the method texts and in every archive member. The kit's METHOD.md has 1,448 lines, as its source does, and each of the five citations lands on its text (MEASURED). |
| (b)7, the self-tests do not run "each refusal" | Each of the twelve is tested. The builder's refusal-mutants stage takes each of the tools' 55 refusals out alone, and that tool's self-test fails each time (MEASURED). |
| (b)8, the rebuild compares the bundle by its heads | By its heads and every object it holds. The bundle-compare stage holds the comparison: equal to itself, and unequal to its header alone and to one more commit. |
| (b)9, check 2's "in any spelling" | Its forms now hold git's scp-like remote, any fork on GitHub, and percent-encoding undone. codeload's alternative is dropped, because github's holds it. Each form is planted in a file and in an archive member. The claim is restated to the forms it lists, and a mirror on another host is stated as outside them. |
| (b)10, ROLES.md attributes every line to METHOD.md | Restated, and the two leads' rules cited to OWNER.md. |
| (b)11, AGENTS.md drops words from its quotation | Quoted whole. |
| (b)12, two samples' "What it shows" | Restated. |
| N1, fragments of Logan's identifiers the gate does not see | R5 replaces his email domain's name and an account id's prefix, by hash: 7 in two archives (MEASURED). Check 4 refuses each, with a control plant for each. |
| N2, "None of its code" | Restated: but for two statements of its test harness that its record quotes (3a). |
| N3, "roundeven" | On the list, with 33 more operation names. It cut sample 4b's last line, and 4b's title and "What it shows" are restated. |
| N4, the must-fail stage inverts any failure | It needs its REFUSED line in its output, or it fails. With no build, it now fails (MEASURED). |
| N5, "about 80 seconds" | Restated. |
| N6, "line 15443" | Lines 15443-15444. |
| N7, "follow whole" | Restated. |
| N8, the site's address "carried as text" | Restated, as R6 has it. |
| N9, three protocol steps are pending lessons; a rule cited to no source | WORKFLOW.md names CS5#8, CS6#4 and CS6#3 as pending in ADOPTION.md. "The fix goes back to the verifier that found it" cites CASE-STUDY-4.md, observation 7. |
| N10, codeload redundant; zip-member plants | As (b)9. |
| N11, a stray `__pycache__` | The controls' samples are built at run time, so a .pyc holds none whole. START-HERE.md says to run the tools as commands, and to delete a `__pycache__` by its exact path. |
| N12, removal on Windows | The tools remove read-only files as they go. That this works on Windows is BELIEVED: it was not run there. |
| N13, K5 | Each figure no script holds is tagged with its evidence. K5's wording is in section 13. |
| N14, a typed heading in a body | `ledger.sh` refuses a heading line in the body and a headline of more than one line. |
| N15, section 13's own list | R1's and R4's markers, and K5, are listed there. |
| What the brief got wrong, 1 to 3 | The lead's: listed in section 12. |

**The cold read of v1** (docs/reviews/v1/cold-read-grading.md): 15 of 15
right, no invention. Its findings A to M are ruled there, and the fix round
takes each in.

**v1's verifier, its re-check** (docs/reviews/v1/verifier-v1-recheck.md):
NOT READY, 0 (a), 5 (b), 7 notes. Of its first pass's findings, every one
closed but (b)10, not closed (its new (b)3), and N2, restated wrongly (its new
(b)4). What the second fix round does:

| finding | what the second fix round does |
|---|---|
| (b)1, a copy holds the unplanted text through the base's history: a file restored, or moved unchanged | `make` refuses a plant whose file's text at real_tip is in the base's history, a file left as the base had it among them, which it made before with a note. `check` refuses a copy whose objects, read by id, hold a planted file's text at real_tip. The self-test has 93 checks. (Not whole: the second re-check found routes `check` does not read, and the "by any route" this row first said; see its table below.) |
| (b)2, refusal-mutants finds only `raise` and `die`; the builder's line-count refusal has no control | The stage also takes out each copy condition of plant.py's check: 71 sites, each caught (MEASURED). Each of the builder's 14 refusals has a trial (builder-refusals), and builder-mutants takes each out alone: each caught (MEASURED). One trial found the builder's "is not a commit" refusal unreachable: a missing commit gave git's own error first. Fixed. CLAUDE.md now says which forms the stages find. (Not whole: the builder's `--check` comparison had no trial; see the second re-check's table.) |
| (b)3, ROLES.md:9, "Each line cites its source" | Restated: a line that cites nothing is the kit's summary of the role. |
| (b)4, CLEAN-ROOM.md's inventory of quoted code, incomplete | Restated as a class, with three examples (3a, 9b and 18a) and no count. |
| (b)5, 4b's "the entry's last line" | "The section's last line." |
| N1, the pattern of his address's local part at round 4's verifier-P0.md:391 | Kept, and stated here: it is his first name, without a domain. |
| N2, a `__pycache__` trips check 4 too | START-HERE.md says so. |
| N3, a heading with spaces before it, a tab after it, or after a lone CR; a headline with a CR | Each refused, with a case: 36 checks. |
| N4, an ORIG_HEAD or a ref's reflog naming the tip passes `check` | `check` refuses any *_HEAD at the git directory's top naming another commit, and any reflog of a ref. (A linked worktree's passed: the second re-check's note 1.) |
| N5, ROLES.md:6's reading, unmarked | Logan's whole sentence, and the reading marked as the kit's. |
| N6, CLEAN-ROOM.md's list of GLOSSARY.md's quotations | As (b)4: "short quotations of its record, each cited by its line". |
| N7, a renamed fork and a submodule's view pass check 2 | Stated among check 2's exceptions, in check_kit.py and CLEAN-ROOM.md. |
| Section 13, items 18 and 20 | Item 20 restated: only the bundle's one occurrence cannot be rewritten; the other 20 could be, by a rule like R5, so keeping them is a choice, put to Logan. |

**v1's verifier, its second re-check** (docs/reviews/v1/verifier-v1-recheck2.md):
NOT READY, 0 (a), 2 (b), 8 notes, and no regression. Its re-check's findings
closed for the routes and forms they named; two fixes claimed more than they
did. This was v1's third NOT READY. The loose cap's condition (OWNER.md, rule
6) is met, but which standing rules apply is Logan's to decide (ROLES.md), and
he has not applied it here, so the third re-check runs without it
(docs/VALIDATION.md). What the third fix round does:

| finding | what the third fix round does |
|---|---|
| (b)1, `check` claims more than it reads: a copy whose work tree, an unindexed pack or a rewritten loose object holds the unplanted text passes it | `check`'s docstring and its printed line now say what it reads, and what it does not: the copy's work tree and its git directory's other files, which `--dispatch` reads, run just before dispatch (WORKFLOW.md, step 2), and any place but the key, the copy and the parcel's repository. It reads more as well: `git fsck --full`, which refuses the rewritten object, and `git count-objects`, whose garbage count refuses the unindexed pack. With `--dispatch`, what `git status` reports (a changed, untracked or ignored file) and any file of the git directory whose name `make` does not write are refused; `make` now leaves out git init's template files. (Not whole: `--dispatch`'s sentences said it held the work tree, where it reads what `git status` reports, which the index's flags and the copy's config can steer; see the third re-check's table.) Restating it, the lead found two reads narrower than their sentences, each now whole: a *_HEAD read by its first word, and HEAD's reflog by the commit each entry moved to and not from. And one sentence wider than its read, "each old text is in real_tip once", where the tool holds it once when it is applied: restated. The self-test has a case for each route: 112 checks. Each of plant.py's 53 sites, taken out alone, fails it (MEASURED). |
| (b)2, the builder's `--check` comparison is outside both builder stages | A trial runs `--check` on a dist/ with a file changed, one taken away and one added, and requires each named, CHECK FAILED and exit 1. builder-mutants also takes out each of the 3 places the comparison records a difference: 17 sites, each caught (MEASURED). The verifier's mutant, `return diffs` at the comparison's top, fails the trial (MEASURED). |
| N1, a linked worktree's ORIG_HEAD and reflog pass `check` | `check` refuses a linked worktree, and `--dispatch` any file `make` does not write. |
| N2, a copy made on the wrong base passes `check` | Stated: `check` holds the copy to its own parent, and cannot tell a wrong base. The base is the lead's to give, and `make` prints it for the ledger (the docstring; WORKFLOW.md, step 2). |
| N3, a setext heading, or a level-1 one, passes `ledger.sh` | Both refused, with cases: 41 checks. The setext rule also refuses some lines Markdown reads otherwise, such as `---` under a list, and says to put a blank line above. |
| N4, builder-mutants passes with no sources | It runs builder-refusals with nothing taken out first, and fails if that fails; each mutant must then make it name a failed trial. With no sources it now fails (MEASURED). refusal-mutants and finding-mutants run their check unmutated first too. |
| N5, section 13, item 15's "55" | Restated, with this round's counts. |
| N6, ROLES.md:11-13 | Restated to the forms its lines use: the method by section, a rule by OWNER.md or the kit page that carries it, details by a kit page or template. |
| N7, CLEAN-ROOM.md:57 | "Each cited by its line, sample or header." |
| N8, refusal-mutants' "each of plant.py's copy conditions" | The HEAD condition is now an append, which the stage takes out: the self-test fails (MEASURED). |
| What the brief got wrong | The digest leaves out what .gitignore excludes as well: the next brief says so, and it is in section 12. |

**v1's verifier, its third re-check** (docs/reviews/v1/verifier-v1-recheck3.md):
NOT READY, 0 (a), 1 (b), 5 notes, and no regression. Its second re-check's
(b)2 and eight notes closed, and (b)1 closed for the reveal. This was v1's
fourth NOT READY, and the fourth re-check runs without the loose cap too, as
Logan has not applied it (docs/VALIDATION.md). What the fourth fix round does:

| finding | what the fourth fix round does |
|---|---|
| (b)1, `--dispatch` says it holds the work tree and the copy "as make left it"; it reads what `git status` reports and the names of the git directory's files. Index flags (skip-worktree, assume-unchanged), `core.worktree`, or an edit with its stat data put back pass it, and so does text hidden in a file `make` writes | Restated to what it reads, in plant.py's docstring and printed line, WORKFLOW.md, step 2, and section 13: `git status`, with untracked and ignored files shown, must report nothing, and each file of the git directory must have a name `make` writes; the names, not what the files hold. It is stated as the lead's check against a slip, not a defense against a copy built to pass it, since `git status` trusts the index's flags and stat data and the copy's config. |
| N1, two inputs end in exit 3 where a refusal by name is due | `make` refuses a repository whose objects `git fsck --full` flags, naming fsck's first complaint, and the docstring says so. A `git status` that fails in the copy is a refusal by name. A case for each: the self-test has 117 checks, and each of plant.py's 55 sites, taken out alone, fails it (MEASURED). |
| N2, under `core.splitIndex`, `--dispatch` refuses the copy `make` left | Its shared index is on the list of files `make` writes, with a case. `make`'s own `git status` and `reset` run with `core.fsmonitor` off. The limit in docs/VALIDATION.md names a user's setting as well as another git. |
| N3, the reveal's `check` refuses a copy its verifier used in ordinary ways | WORKFLOW.md, step 5, and ROLES.md tell the verifier to build in a clone of the copy, which leaves the copy's git state as it was sent (MEASURED: a clone of a copy, then `check --dispatch` on the copy, passes). Step 8 says what the lead does when `check` refuses a copy for its verifier's own use. |
| N4, the level-1 rule refuses a `#` line in a fenced block | Both heading rules now skip lines inside a fenced block, by CommonMark's opening and closing rules, and the docstring states each rule as it is read: a line that begins, up to three spaces in, with `#` or `##` and then a space, a tab or its end, and a line of `-` or `=` right under a line that holds text and is not a fence, outside a fenced block. Cases for each: 49 checks. Making it, the lead found the tool read its body through pipes, which a large body turned round (section 12, item 56). (A regression: the fourth re-check found a fence marker in an HTML block, or an unclosed fence in a list item, held the tracker open past a typed heading. Reverted: see its table.) |
| N5, `--check`'s MANIFEST.txt exemption has no control | The trial also gives the manifest another ParcelRound commit and cuts the bundle to its header, and requires each named: 5 differences. The verifier's mutant, the manifest's exemption always holding, and the same for the bundle's, each fail the trial (MEASURED). |
| N6, ROLES.md:5, Logan's words by name and date | ROLES.md's sentence names that form too. |

**v1's verifier, its fourth re-check** (docs/reviews/v1/verifier-v1-recheck4.md):
NOT READY, 1 (a), 2 (b), 3 notes. Its third re-check's findings closed, and
the fourth fix round's fence tracker was a regression. Logan applied the loose
cap to the next pass, the fifth, on 2026-10-24: "Go ahead and apply rule 6 for
this pass". Each of the three findings below is a defect in what the code does,
so each would block under the cap too. What the fifth fix round does:

| finding | what the fifth fix round does |
|---|---|
| (a)1, `ledger.sh`'s fence tracker accepts a typed level-2 heading that CommonMark reads at the top level, after a fence marker in an HTML block or an unclosed fence in a list item | Reverted to the rule of rounds 2 and 3, which reads each line wherever it is, a fenced block included, and errs toward refusing: only a full parser reads Markdown's blocks right, and a partial one let a heading through. The usage text says so, says how to keep a code block's `#` lines (indent the block four spaces), and states what is not refused: a heading that follows `>` or a list item's marker on its line, or that is written in HTML. Two of the verifier's six forms are cases: 49 checks. The fourth round's here-strings stay. |
| (b)1, `--dispatch`'s two reads stop silently at a directory the reader cannot open, under a line that says they read it all | `check` walks the copy's git directory always, and with `--dispatch` its work tree, and refuses a directory it cannot read, by name; the docstring and the printed line say so. The self-test makes `os.scandir` fail on two directories, in-process, as it does for a user who cannot read them: root reads every one, so a real unreadable directory was not made here. |
| (b)2, a false reason when git refuses a repository it does not own | Where git will not read REPO or the copy as a repository, the refusal gives git's own first line, "detected dubious ownership" among them, in plant.py and round_metrics.py alike. A `--repo` or `--copy` that is no directory, which ended in exit 3, is now refused by name: the lead found those three, mending the rest. The self-test reaches git's refusal through a copy whose config git cannot parse, as a copy another user owns needs root to make: 125 checks, and round_metrics.py's 43. Each of plant.py's 60 sites, taken out alone, fails its self-test (MEASURED). |
| N1, `make`'s fsck sentence wider than its read, and a reason that can be wrong | Restated: a copy one of whose objects `git fsck --full` flags, from the base's history, real_tip's tree or a plant, is refused, and the refusal says which three it holds. |
| N2, `--check`'s MANIFEST exemption wider than its purpose | Two manifests may differ in the bundle's line alone, and each must name its own tree's bundle by sha256. Two trials give a manifest alone a bundle line left out or naming another bundle, and require MANIFEST.txt alone named; the old exemption passes both (MEASURED). builder-refusals has 17 trials. (Not whole: the comparison was of lines, not bytes; see the fifth re-check's table.) |
| N3, `ledger.sh` against CommonMark otherwise | Stated in its usage text, as (a)1's row says. |

**v1's verifier, its fifth re-check** (docs/reviews/v1/verifier-v1-recheck5.md),
under the loose cap: NOT READY, 0 (a), 1 (b), 0 notes. Its fourth re-check's
six findings closed. Its one (b) blocks under the cap, as a line the builder
prints said what was not so. Logan's word applied the cap to the fifth pass;
the lead holds it for the sixth, which checks this round's one fix
(docs/VALIDATION.md says why). What the sixth fix round does:

| finding | what the sixth fix round does |
|---|---|
| (b)1, `--check` treats MANIFEST.txt's line endings and last line end as no difference, then prints that dist/ is what the sources make, and the rebuild stage "byte for byte" | The exemption compares the manifests' bytes: equal, but for the bundle's one line at the same place in each, which must name its own tree's bundle by sha256. Two more trials give the manifest alone CR LF line ends, or no last line end, and require MANIFEST.txt named; the old comparison passes both (MEASURED). builder-refusals has 19 trials. The exemption's purpose, a bundle repacked into other bytes and named so by its manifest, now has a control of its own in bundle-compare, which an exemption that never holds fails (MEASURED). |

**v1's verifier, its sixth re-check** (docs/reviews/v1/verifier-v1-recheck6.md),
under the loose cap: READY, 0 (a), 0 (b), 0 notes. Its fifth re-check's one
finding closed, and it found no regression. With no note, it is READY without
the cap as well.

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
16. **The verifier's B3 taken without a check.** Atlas-film was the wrong
    example. That was the verifier's inference, which the lead put in draft 2
    without reading round 4's briefs (B13).
17. **Round 4's 61 home-path lines.** One holds no user name (B12).
18. **"The zip carries cft-fp256's text only in these places"** (B11).
19. **"One plant for each shape"** (B14).
20. **Checks 2 and 4 written for files, then made to read archives and a
    bundle**, without re-deriving what they let pass (A7).
21. **The plan's own account of round 6's copies.** Draft 3 said `plant.py`
    builds "a fresh one-commit repository". Round 6's copies were "detached at
    9c306e9 (parent a30aca5)": one commit on the parcel's base, with the base's
    history. Found by the lead reading round 6's lead.md:824 to write the tool.
22. **A self-test plant the plan promised and the first self-test lacked:** a
    copy that holds the parcel's own commits. Found by the lead re-reading
    section 4.4.
23. **Two "softfloat repository"s left after the rename**, in ROLES.md and
    WORKFLOW.md, which check 3 does not read. Found by grep.
24. **A stored report quoting one of Logan's addresses, and three files holding
    a home path**: the draft 1 verifier's report, the re-check, the survey's
    report and this plan. Found by the builder's self-privacy stage, before any
    commit.
25. **The first gate-refuses control** planted its URL in WORKFLOW.md, whose
    size the reading table states, so two checks refused and the control could
    not show check 2 alone. Found by running it.
26. **The first metrics mutant made the tool crash (exit 3)** rather than let the
    fault through, so it showed a self-test catching a crash, not a silent
    acceptance. Found by reading the control's output.
27. **The ledger tool's first self-test** cleaned up through a variable that had
    gone out of scope, and so exited 1 after passing. Found by running it.
28. **The metrics tables summed "0 output tokens"** for agents with no usage
    recorded. Found by reading its output.

29. **`plant.py`'s copy packed the unplanted blobs.** Its filter left out the
    planted blobs, which were never in the parcel's repository, instead of the
    originals, and its self-test never listed the copy's objects. Found by v1's
    verifier, (b)1.
30. **Two of check 4's findings had no plant of their own,** the x-api-key lesson
    again, for the findings no shape names. Found by v1's verifier, (b)2.
31. **"A gate that cannot read the bundle does not pass it."** It passed one.
    Found by v1's verifier, (b)3.
32. **The fold held two of the four letters `re` folds,** written from memory
    of its behaviour, not from its documentation. Found by v1's verifier, (b)4.
33. **"None of his machines' names", and "nothing here spells them",** where the
    kit holds two machines' names, and his user name is his first name. Found by
    v1's verifier, (b)5, and by the lead.
34. **R1 joined lines,** so that five of OWNER.md's citations landed elsewhere.
    Found by v1's verifier, (b)6.
35. **"Each refusal"**, claimed by three self-tests that did not run twelve of
    them. Found by v1's verifier, (b)7.
36. **"Byte for byte"**, for a bundle compared by its heads. Found by v1's
    verifier, (b)8.
37. **"In any spelling."** Found by v1's verifier, (b)9.
38. **ROLES.md's attribution, AGENTS.md's dropped words, and two samples'
    "What it shows".** Found by v1's verifier, (b)10 to (b)12.
39. **v1's verifier's brief** told it never to write Logan's personal domains,
    where the plan has the kit carry his site's domain 81 times. It said "his
    machines' names" for one machine's. And it asked for `verify/run.sh`, which
    rewrites `dist/`, while saying to edit nothing there. Found by that
    verifier.
40. **Six sentences of the kit claimed more than was true:** ROLES.md's models
    and its unconditioned rules 1 and 2, CLEAN-ROOM.md's list of what the kit
    carries, METRICS.md's plants table per wave, and START-HERE.md's "the kit
    you hold is not the one that was built" and its METHOD.md figures. Found by
    the cold read.
41. **In the fix round itself:** the first spelling control tested a list's
    membership for a substring, and called every spelling missed; the first
    reading-table plant edited the prose above the table; and an f-string held
    a backslash inside its braces, which Python before 3.12 refuses. Each was
    found by running it.

42. **The fix for (b)1 claimed more than it did:** a copy held the unplanted
    text where the base's history held it. Found by the re-check, (b)1.
43. **"A new refusal without its own case fails the run"**, from a stage that
    found two forms of refusal. Found by the re-check, (b)2.
44. **A refusal of the builder unreachable as written:** `load_sources` asked
    git first, through a call that raised on the same failure, so a missing
    commit never reached "is not a commit". Found by the new builder-refusals
    trial.
45. **Two inventories that claimed to be whole,** ROLES.md's citations and
    CLEAN-ROOM.md's quoted code, **and 4b's "the entry's last line".** Found by
    the re-check, (b)3 to (b)5.
46. **In the second fix round:** a trial passed a tuple as a keyword; the
    line-joining trial's expected text was loose enough for the archives'
    refusal to satisfy it, which builder-mutants found; and a self-test case
    ran before its body file was written. Each was found by running it.

47. **"By any route"**, for a check that reads a copy's objects by id. Found by
    the second re-check, (b)1. Restating it, the lead found two more reads
    narrower than their sentences, and one sentence wider than its read
    (section 11).
48. **A refusal of the builder that no stage watched fail**, its `--check`
    comparison: slip 43's class again. Found by the second re-check, (b)2.
49. **Four statements of reach, each nearly true:** refusal-mutants' "each copy
    condition", where the HEAD condition was a return; ROLES.md's two citation
    forms; CLEAN-ROOM.md's "each cited by its line"; and section 13, item 15's
    count. Found by the second re-check, notes 5 to 8.
50. **The second re-check's brief** gave the digest as every file but those
    under docs/reviews/v1/, where it also leaves out what .gitignore excludes.
    Found by that verifier. And the report's header, as first filed, said its
    paths had been replaced "(0)" times, where the verifier wrote them so
    itself. Found by the lead, reading the filed report.
51. **In the third fix round:** the first case of the forms `ledger.sh` allows
    put `===` under dashes four spaces in, which the new rule refuses, as it
    should. Found by running it.

52. **`--dispatch`'s "its work tree and index are its commit's" and "as make
    left it",** for a check that reads what `git status` reports and the names
    of the git directory's files: slip 47's class, in the sentence that mended
    it. Found by the third re-check, (b)1.
53. **Two inputs that ended in exit 3, "the tool failed", where a refusal by
    name was due:** a history `git fsck` flags, and a copy `git status` cannot
    read. Found by the third re-check, note 1.
54. **A new rule stricter than its comment,** `ledger.sh`'s level-1 rule, which
    refused a `#` line in a fenced block; **and the `--check` trial, which left
    the comparison's two exemptions untested.** Found by the third re-check,
    notes 4 and 5.
55. **A reveal check that a verifier's ordinary work fails,** where nothing told
    the verifier to leave the copy's git state alone. Found by the third
    re-check, note 3.
56. **`ledger.sh` read its body through pipes that a reader may leave early.**
    Under pipefail, a body larger than a pipe's buffer was refused for lacking
    a label it held; with that mended, a typed heading in such a body passed
    (MEASURED, with a 236 KB body). It was so since the tool was written. Found
    by the lead, making the heading rules skip fenced blocks.

57. **A fence tracker that let a typed heading through,** where the rule it
    replaced refused it: v1's first regression in its own checks. "By
    CommonMark's opening and closing rules" claimed a parser the tracker was
    not. Found by the fourth re-check, (a)1.
58. **Two reads that stopped silently at a directory they could not open,**
    under a line that said they read it all. Found by the fourth re-check,
    (b)1.
59. **"HEAD is missing" and "not in a git repository",** where git said
    "dubious ownership"; and a `--repo` or `--copy` that is no directory,
    which ended in exit 3, slip 53's class. Found by the fourth re-check, (b)2,
    and the last by the lead, mending it.
60. **`make`'s fsck sentence and `--check`'s MANIFEST exemption, each wider
    than what it reads.** Found by the fourth re-check, notes 1 and 2.

61. **A comparison of lines, under a sentence about bytes.** `--check`'s
    manifest exemption split both files by `splitlines()`, so line endings and
    a last line end were no difference, and the rebuild stage still said "byte
    for byte". It was so since it was written, and stayed so when the fifth
    round rewrote it. Found by the fifth re-check, (b)1.
62. **The sixth re-check's brief** left verify/run.sh out of its "What
    changed", though the round changed the bundle-compare stage's line there.
    Found by that verifier.

## 13. What the build changed from draft 3

The lead's reading of "Approved if nothing major changes from the check": none
of these changes the kit's shape, the kinds of thing it holds, or one of Logan's
decisions. The largest is item 7, where draft 3 misdescribed round 6, and the
tool follows round 6. That reading is the lead's, for Logan to overrule.

1. **OWNER.md has ten standing rules, not nine.** The tenth is Logan's of
   2026-10-22, the header of cft-fp256's record: "History is what has been
   pushed: until then an entry is restated in place when a verifier sends its
   work back" (sample 1b). Found while the samples were cut. Rule 1 also carries
   his "Lead fixes sentence at merge" (2026-10-13, cft-fp256 VALIDATION.md:19166).
2. **The leads' rules** in OWNER.md add three to section 4.2's list, each with
   its line in the record: delete only what the run created and stop only its
   own processes, by PID (:18990); scratch in a shared directory deleted by its
   exact path (:21789); a browser tab of one's own, acted on by its id (:21790).
3. **Check 3's list.**
   - `escalat\w*` is off it: the methods use "escalation" for the urgent
     channel, and the record's other sense, a path to more digits, is caught by
     "precision".
   - The repository's own name is stripped before matching, since
     "cft-fp256" ends in a listed term.
4. **Check 4.**
   - QRO-Crate's `named:x-api-key` shape is left out: `named:api-key` matches
     inside every x-api-key, so its plant tested nothing of its own. A privacy
     plant now counts as caught only by its own shape's name.
   - A prefilter runs each shape only on a text holding a literal that the
     shape cannot match without. With one batch read of the bundle, that cut
     the gate from 12 seconds to 2.6, and its controls from 19 to 5.8
     (MEASURED in this container, with 56 plants). Its folds (a long s, a dotless i, which `re`
     matches for s and i) and the `\u0040` escape have plants of their own:
     59 plants, every one caught. Without the folds, two are missed (MEASURED).
   - A crash inside the gate exits 3, never 1: no verdict (HonestFramework
     section 5).
5. **"The project repository."** "softfloat" is on check 3's list, so the kit
   calls the work's repository "the project repository", and START-HERE.md
   defines the term. This plan still says "the softfloat repository".
6. **The samples:** 45 in 20 files (build/cases.json gives each one's lines and
   why). The skeleton carries "The chain" and "Time and tokens" whole. The rest
   of the coverage wave's entry that section 4.3 lists ("What Logan asked",
   "Conduct", "The experiment", "Corrections this record owes") is quoted by
   samples under their own situations, and the skeleton's opening lists them in
   the entry's order.
7. **`plant.py`** builds round 6's copy: a fresh repository detached at one
   commit whose parent is the parcel's base, holding the base's history, so the
   verifier can diff the work against its base, with no remote, no refs and none
   of the parcel's own commits. The lead writes a draft of the key without
   `copy_commit`; `make` adds it and prints the key's sha256. `check` is new:
   with `--dispatch` just before dispatch, and without it at the reveal, it
   confirms the key's hash, each plant's text, and the copy's git state as its
   docstring lists it (item 14). `make` refuses a shallow source, whose copy
   would lose history.
8. **`ledger.sh`'s interface** is `append LEDGER AUTHOR "headline" < body` and
   `urgent LEDGER AUTHOR SLUG "headline" < body`. Its heading takes the
   archived ledgers' shape ("## 2026-10-02 21:37:58 -0700 - ..."); round 5's
   verifier-P4.md has a heading whose stamp is empty, which the tool cannot
   write.
9. **`round_metrics.py`** reads six JSONL files whose fields `--help` gives, and
   refuses a field it does not know. The adapter from a harness's own usage log
   is day 1's work, in docs/HARNESS.md, because that log's format is not known
   until kickoff. A transcribed row is marked in its table.
10. **START-HERE.md is not in its own reading table**, which cannot give the
    size of the file that holds it. The sample table is written before the
    reading table, which gives examples/README.md's size.
11. **The builder.**
    - Its controls are `tests/controls.py`, eight of them, each a stage of
      `verify/run.sh` (13 stages in all).
    - The manifest's builder line names the last commit that changed `build/`
      or `kit/`, so a commit to `docs/` alone leaves the manifest as it was.
    - `audit/` is not in v1. It follows before the first wave closes, as
      section 9 says.
12. **This repository's own privacy.** The draft 1 verifier's report quoted one
    of Logan's addresses (now `<address>`). Two reports, this plan and both
    frozen drafts held this container's home path (now `<repos>/`). The drafts
    are kept in docs/reviews/KIT-0/ with both hashes, as read and as kept, and
    every line number still holds.
13. **The cold read** (section 9, step 8) is blinded by the record, not by git,
    since nothing is committed before v1's verifier passes. Its key's sha256 is
    in docs/VALIDATION.md before the reader is dispatched, and the key is
    revealed after the reader reports. That is WORKFLOW.md's step 3 where Logan
    does not let the lead commit.
14. **`plant.py`'s copy holds only the objects its HEAD reaches, and no planted
    file's text at real_tip, and its git directory only the files `make`
    writes.** `check` reads what its docstring lists: the copy's objects by id,
    its refs, remotes and reflogs, the files of its git directory it names,
    every directory of that git directory, `git fsck --full` and `git
    count-objects`; with `--dispatch`, also what `git status` reports, the name
    of each file in its git directory, and every directory of its work tree. It
    refuses a directory it cannot read, and where git will not read a
    repository, it gives git's own reason (v1's verifier, (b)1; its re-checks'
    (b)1; the fourth's (b)2). At the reveal it does not read the work tree,
    which a verifier may change, and it reads no place but the key, the copy
    and the parcel's repository. A plant whose file's text at real_tip is in
    the base's history is refused, and so is a copy one of whose objects `git
    fsck --full` flags. A wrong base passes: the base is the lead's to give.
15. **The gate's controls plant every finding the checks can give,** 80 plants,
    each caught only by the finding that names it, and they write each privacy
    sample with each letter `re` folds, 96 spellings. Section 8 promised one
    plant for each shape. The builder takes out alone each of the gate's 31
    findings; each of the tools' 62 refusals and plant.py's 25 copy conditions,
    87 in all; and each of its own 14 refusals and the 3 differences its
    `--check` records. Each time the control fails, having passed with nothing
    taken out.
16. **R5 removes two fragments as well,** Logan's email domain's name and an
    account id's prefix, by hash, and check 4 refuses each.
17. **R1's and R4's markers.** Section 4.1 has R1 gain "(cft-fp256's record;
    not in this kit)" and R4 mark a URL "(cft-fp256; not in this kit)". The
    build writes ", cft-fp256's record, not in this kit" for a link, and
    "[cft-fp256 URL removed]" for a bare URL, whose path stays. R1 keeps each
    file's line count, so its marker can carry a line end.
18. **K5's wording.** "Every figure in the kit's own documents is held by a
    script, or tagged with its evidence: MEASURED or READ, saying by whom or
    where, or BELIEVED." Section 2's wording, "or tagged BELIEVED", is stricter
    than Logan's own records, which tag each figure with its evidence.
19. **Check 2's forms,** after v1's verifier's (b)9: github.com's form takes any
    owner and git's scp-like separator, and holds codeload's; percent-encoding
    is undone. A mirror on another host is stated as outside its list.
20. **Two of Logan's machines' names stay in the kit:** his Linux machine's and
    his WSL distro's, 21 times (MEASURED by v1's verifier). They are in texts he
    published (ParcelRound's CASE-STUDY-3.md, cft-fp256's record). One of them
    is in a blob of the QRO-Crate bundle, whose history cannot be rewritten; the
    other 20 could be replaced by a rule like R5, so keeping them is a choice.
    It departs from section 8's "his machines' names, held by sha256" and from
    K1. The gate holds his desktop's name only. This is the lead's reading of
    his word on personal data, "Okay to strip, not vital however", put to him
    to overrule.
21. **The term list gains 34 operation names** in 32 patterns, lrint and llrint,
    and lround and llround, each sharing one (COMPUTED), after v1's verifier's
    N3. One of them cut sample 4b's last line.
22. **The builder's runner has 17 stages.** bundle-compare, refusal-mutants,
    finding-mutants, builder-refusals and builder-mutants are new, tool-mutants
    is gone, the must-fail stage needs the gate's REFUSED line, and each mutant
    stage runs its check with nothing taken out first.
23. **`ledger.sh` refuses a level-1 heading and a setext one** as well as a
    level-2 one (v1's second re-check, note 3), wherever the line is, a fenced
    code block included: a code block's lines are kept by indenting it four
    spaces. The fourth round's fence tracker let a heading through and is gone
    (section 12, item 57). It reads its body from here-strings, not pipes (item
    56).
24. **`plant.py check --dispatch`**, run just before dispatch (WORKFLOW.md, step
    2), reads what the reveal cannot: what `git status` reports of the copy,
    and the name of each file in its git directory. It is the lead's check
    against a slip, not a defense against a copy built to pass it. `make`
    leaves out git init's template files, so that each file's name in the
    copy's git directory is one it writes.
25. **The verifier on a planted copy builds in a clone of it** (WORKFLOW.md,
    step 5; ROLES.md), so that the reveal's `check` reads the copy as it was
    sent. Where it did not, step 8 says what the lead records.
