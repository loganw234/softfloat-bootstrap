# The cold read of v1: the grading

**The order of the three steps.**
1. The key, [cold-read-key.md](cold-read-key.md), was stamped in docs/VALIDATION.md before the reader was
   dispatched: sha256 `d54936304912183183b6d2648231afd12751c37c4cbfd894a71be5858ebe4fe2`, at 2026-10-23
   21:42:02 +0000.
2. The reader worked from 21:44:47 to 21:52:13 +0000, by its own `date -u`. Its report is
   [cold-read-answers.md](cold-read-answers.md).
3. The key was revealed at 21:56:13 +0000, and hashed to the recorded value (MEASURED).

Nothing was committed, so this order rests on the stamps and the transcripts, not on git (KIT-0, section 13,
item 13).

## The grades, by the key

The lead graded by reading. Every claim an answer made beyond the key was checked against the kit, and is listed
where it was not the key's own words.

| question | grade | what was checked beyond the key |
|---|---|---|
| 1 | right | It ran the gate: PASS, and `--control` 59 of 59. The exit codes it gives are the gate's docstring's. |
| 2 | right | |
| 3 | right | |
| 4 | right, 4 of 4 | "a fixed absolute path that every brief states, ignored by version control": ParcelRound METHOD.md:500 and the ledger's README. |
| 5 | right | The full read on resuming and when a watch dies: the ledger's README. |
| 6 | right | "not penalised": the README's "costs nothing". |
| 7 | right | "day 10 in the proposed calendar": WORKFLOW.md's calendar. |
| 8 | right | |
| 9 | right | "NOTICE.md says so": NOTICE.md:19. |
| 10 | right | "Commit inside your worktree only": templates/brief.md:183-184. |
| 11 | right | |
| 12 | right | |
| 13 | right, 4 of 4 | "Scope and PROJECT.md's questions go to him in the study on day 2": WORKFLOW.md, phase 2 and the calendar. |
| 14 | right | |
| 15 | right | "READY waits until the limit is restated": METHOD.md:1108-1115. "confirmed, defect or not determined": templates/verifier.md:179. |

**15 of 15 right, none partly right, and no invention.** The kit told a reader with nothing else these fifteen
things, in 7 minutes 26 seconds of reading, by the reader's own count (MEASURED, by the reader).

## What that does not show

- **The reader did not have quite nothing else.** Before it began, this harness loaded two agent-notes files into
  its context: cft-fp256's CLAUDE.md and QRO-Crate's. It disclosed this first, as CLEAN-ROOM.md asks.
  QRO-Crate's notes hold two of the things the questions touch: item 5, "Nothing is committed or pushed without
  Logan's word", and item 6, the loose cap. Its answers cite the kit for each, and the kit holds each. cft-fp256's
  notes hold its working notes and no code, and no answer uses them.
- **It is an agent of the harness that built the kit,** not one of Meta's models.
- **The questions are the lead's,** and so is the kit. They measure what the lead thought to ask.

## The reader's findings, and the lead's rulings

The reader's last section, "Unclear, contradictory, or missing on day 1", is the cold read's "what this brief got
wrong". The lead checked each one against the kit before ruling (ParcelRound METHOD.md, "Verify an escalation
like any other report"). The tree was frozen for v1's verifier, so these are taken in after it reports. A ruling of
(b) means a sentence of the kit's that claims more than is true.

| finding | the lead's ruling |
|---|---|
| A, the clean room and the harness | **Accepted, and the most important.** This harness loaded cft-fp256's agent notes into an agent's context because cft-fp256 was attached to the session. A Meta harness on Logan's desktop could do the same. CLEAN-ROOM.md gains a rule: no clone of cft-fp256 in, under, or beside any directory an agent or its harness is given, and none among what a harness loads on its own. HARNESS.md gains a row: what the harness puts in an agent's context by itself. And a (b): CLEAN-ROOM.md's list of what the kit carries of cft-fp256 leaves out AGENTS.md's two quotations of its agent notes, and the quotations of its record in OWNER.md, GLOSSARY.md and METRICS.md. |
| B, commits | **Accepted, as a kickoff question.** The method has parcels commit in their worktrees (templates/brief.md:183-184), and `plant.py` needs a parcel's commit. Rule 7, as written, would forbid both. OWNER.md and WORKFLOW.md's phase 0 put it to Logan: does rule 7 cover a parcel's commits in its own worktree, or the main branch and pushes only? And where does "a private repo" live? |
| C, which rules bind before kickoff | **Accepted, (b).** ROLES.md cites rules 1 and 2 as binding. Both gain "if it applies", as elsewhere. The count of ten, and rule 9's being the record's words rather than his, are stated in OWNER.md already. |
| D, ROLES.md line 5 | **Accepted, (b).** Logan's words are "Not yet decided" and "likely". ROLES.md quotes them, and states nothing beyond them. |
| E, rule 10 and HonestFramework section 7 | **Accepted.** Rule 10 restates an entry in place until a push. HonestFramework section 7 has the record append only. OWNER.md's reading of rule 10 names the conflict: Logan's later rule governs his own records where it applies, which is settled at kickoff. GLOSSARY.md says which "ledger" is which: ParcelRound's round ledger; HonestFramework's templates/ledger.md, a template for the record; and cft-fp256's record, whose header calls it a ledger. |
| F, correcting a ledger entry | **Accepted in part.** `ledger.sh`'s header says that a "see <time>" line beneath an older entry is written by hand, which the README allows, and that its heading's hyphen is the archived ledgers', where the template has a dash. |
| G, absolute paths | **Accepted.** WORKFLOW.md's phase 0: the brief gives the ledger's absolute path (METHOD.md section 4), and entries and reports write places by roots each dispatch defines, such as `<repos>/` (round 6's practice; CS6#7, pending in ADOPTION.md:155). |
| H, how a false sentence is classed | **Accepted.** GLOSSARY.md says how Logan's chain tables count one: as a (b), with the lead's restates named in the "sent back" column (examples/cases/20-record-skeleton.md, 20a). Round 6 kept "restate" as a class of its own. The study picks one, and the record says which. |
| I, plants per wave | **Accepted, (b).** METRICS.md has every wave's entry carry a plants table, but plants are graded only at the reveal. The plants table is made at the reveal. WORKFLOW.md states the kit's proposal that the ten days are one round. |
| J, blinding | **Accepted.** HARNESS.md gains a row: whether an agent can read another agent's scratch directory, the lead's included. Where it can, the blinding rests on the instruction and on disclosure, and the record says so. |
| K, the kit's provenance | **Accepted, (b).** START-HERE.md's first step reads as though a PASS shows the kit is the one that was built. Check 1 compares the kit with its own manifest, which a changed kit could carry changed with it. What shows the kit is the one built is the zip's sha256, which Logan has from the builder's record. START-HERE.md says so, and asks the lead to confirm the hash with him. |
| L, a stale figure | **Accepted, (b).** START-HERE.md's 78,786 bytes and 27,193 Read-tool tokens were measured on ParcelRound's METHOD.md before the rules changed it. The kit's copy is 78,224 bytes (MEASURED). The sentence is restated on the kit's copy, as a ratio, which does not go stale with the reading table. |
| M, not in the kit | **Accepted in part.** PROJECT.md says the PDF may sit in a directory the lead gives a reader, outside every repository. ROLES.md's "the ledger's own file", the method's phrase (METHOD.md:1235), is said plainly: the ledger's README, "the ledger directory's own README.md" (templates/ledger.md). The harness, where the agents run, the board's details and Logan's hours are day 1's, and HARNESS.md, BOARD.md and WORKFLOW.md's phase 0 say so already. |
