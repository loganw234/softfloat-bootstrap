# The cold read of v1: the key

Written by the lead before the reader was dispatched. Each answer gives what the kit says, its source in the kit, and
what earns "right", "partly" and "wrong". An answer that adds a claim the kit does not make is marked as an invention,
whatever its grade. "Not found in the kit", where the kit does say it, is "wrong" for that question, and counts
against the kit's findability, not against the reader.

1. Run the kit's gate from the kit's directory, `python3 -I tools/check_kit.py` (or `python` / `py -3` on Windows).
   It must end `VERDICT: PASS, all five checks hold`. If it does not, stop and tell Logan what it printed.
   (START-HERE.md, "First, before anything else", item 1.)
   Right: the gate, the PASS line, and stop-and-tell-Logan. Partly: two of the three.
2. cft-fp256 only. It counts in any form: its pages, raw files, API, archives, forks and mirrors; its project site
   on GitHub Pages; a copy shown through another repository, such as a submodule's view; pages of Logan's site that
   show it (the lead's reading). If opened: stop; write the URL and what you saw in your own ledger file; escalate to
   the lead, who tells Logan. It is judged on disclosure. (CLEAN-ROOM.md.)
   Right: cft-fp256 alone, at least three of the forms, and stop, write and escalate. Partly: the repository and
   either the forms or the steps.
3. Only a regression, (a), or a wrong answer, (b). Everything else merges as a recorded known limit. A sentence that
   claims more than is true is restated at the merge: by the lead, as a very small fix past a verifier, when nothing
   else sends the work back. (OWNER.md, rule 1; GLOSSARY.md, "What a verifier finds".)
   Right: (a) and (b) only, and the restatement at the merge. Partly: one of the two.
4. Outside every worktree. One file per author, append only, and each writes only its own. An entry is never edited:
   a correction is a new entry, which names the one it corrects. A heading's time comes from `date`, never from
   memory (`tools/ledger.sh` writes it). (START-HERE.md, "Five things", item 2; the ledger's README in
   method/parcelround/templates/ledger.md; GLOSSARY.md; tools/ledger.sh.)
   Right: at least three of the four. Partly: two.
5. At three moments: before it starts anything; before it designs anything that touches a file its brief calls
   shared or forbidden; and before it writes its final report. (ROLES.md, "A parcel"; the ledger's README.)
   Right: all three. Partly: two.
6. It escalates at once rather than holding the question for its report: it writes the question in its own ledger
   file first, then sends it by the escalation channel (a file renamed into `urgent/`, with a `For:` line, or the
   harness's messages), and waits for the answer. (START-HERE.md, "Five things", item 3; WORKFLOW.md, phase 0,
   step 4; the ledger's README.)
   Right: at once, the ledger first, and the channel. Partly: two of the three.
7. The lead ("The lead holds them for parcels"). The key's sha256 goes in the ledger before dispatch. The keys are
   revealed once every verifier on a planted copy in the round has reported, later waves' included. The verifier
   treats everything it finds as real, and reports it. (WORKFLOW.md, "The planted-fault protocol".)
   Right: the lead, the reveal after every planted verifier has reported, and treat-as-real. Partly: two.
8. The lead: "Lead controls hardware access". A parcel asks the lead by the escalation channel; the lead runs the job
   itself or grants a slot by name and by time; one holder at a time, by a lock file, `<ledger>/board.lock`.
   (BOARD.md, "The protocol".)
   Right: the lead, and asking the lead. Partly: one of the two.
9. No. Logan gives the lead the PDF, outside the kit; it is licensed to him, and goes in no repository and no zip.
   It is the contract, what conformance requires, and not the authority the gates compare against, which the study
   names. Who else reads it is the lead's decision. (PROJECT.md, "The standard"; CLEAN-ROOM.md, "The standard".)
   Right: not in the kit, from Logan, and the contract, not the authority. Partly: two of the three.
10. A parcel never pushes, merges, rebases or commits to the main branch (ROLES.md). Nothing is committed or pushed
    without Logan's word (OWNER.md, rule 7), until he says otherwise at kickoff, so the lead asks first
    (START-HERE.md, "Five things", item 4).
    Right: both halves. Partly: one.
11. No. It hands large runs back to the lead to monitor, and still verifies and tests as much as it can quickly
    (OWNER.md, rule 2, if it applies; ROLES.md, "A parcel").
    Right: hand back, and test quickly. Partly: one.
12. MEASURED: run, with the output in hand. READ: read at a named place, not run. COMPUTED: arithmetic on measured or
    read figures. BELIEVED: an estimate, an inference, or a claim not checked. (GLOSSARY.md, "The evidence tags".)
    Right: all four with their meanings. Partly: the four names, or three with meanings.
13. Which of the standing rules apply; the caps; the verifiers' tier; the project repository and its private remote
    (OWNER.md, "So, at kickoff"). WORKFLOW.md's phase 0 adds: fill docs/HARNESS.md and docs/BOARD.md in the project
    repository, and record his answers verbatim with their date.
    Right: three of OWNER.md's four. Partly: two.
14. In the project repository, as docs/HARNESS.md and docs/BOARD.md. The kit is frozen: a changed file fails the
    gate's check 1 (START-HERE.md, "Five things", item 5; HARNESS.md; BOARD.md).
    Right: the project repository, and why. Partly: one.
15. READY or NOT READY. READY means every property of the work is held by a gate, or stated as a limit (GLOSSARY.md,
    "Verdicts and limits"; ROLES.md, "A verifier").
    Right: both verdicts, and READY's meaning. Partly: one.

The score is the count of right answers, with the partly-right and the inventions counted beside it. What this
measures is whether the kit tells a reader with nothing else what these fifteen things are. The reader is an agent
of the harness that built the kit, not one of Meta's models, so it does not measure how Meta's models will read it.
