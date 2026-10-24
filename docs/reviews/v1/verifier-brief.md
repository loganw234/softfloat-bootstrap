# v1's verifier: the brief

You are a **verifier**, not an author. Your job is to try to disconfirm v1 of the softfloat bootstrap kit and of the
builder that makes it, and to report. **You must not fix anything.** "Found nothing" is an acceptable answer, and is
not held against you. A verifier under pressure to find something invents it, which is worse than finding nothing.

Paths below are relative to `<repos>/`, the directory that holds the builder (`softfloat-bootstrap/`) and its four
sources (`HonestFramework/`, `ParcelRound/`, `QRO-Crate/`, `cft-fp256/`). Write paths that way in your report, and
your own scratch directory as `<scratch>/`, never absolutely.

## The project, and what must not quietly weaken

Logan runs a ten-day hackathon from 2026-10-26: Meta's models write an IEEE 754 softfloat for the RP2040, using his
methods, HonestFramework and ParcelRound, and he measures how they handle them. They work in a clean room: they may
not read cft-fp256, which already implements this arithmetic. So they get one zip instead of his GitHub. The zip
holds the methods, the workflow, what the lead owns and asks, his own words, and samples of how situations were
handled. Only the zip moves to them.

These must hold. A change that weakens one is what this pass is for:
1. **The clean room.** The zip holds no cft-fp256 code, none of its arithmetic, and no URL into it, in any file,
   archive member, bundle blob or commit message.
2. **Privacy.** The zip holds none of Logan's personal data, except the QRO-Crate bundle's commit identities, which
   carry his address by his word ("Real address is fine").
3. **His words are verbatim,** each with its date and its source, and what is the kit's reading is marked as such.
4. **Every rule the kit states cites where it comes from,** and the cited place says what the kit says it says.
5. **Every gate can fail:** the kit's gate and its controls, and the builder's stages and controls.
6. **Nothing claims more than is true.** A sentence that does is a (b).
7. **The kit is enough on its own** for a lead with nothing else but the standard's PDF and the open web.

## What you verify

- **The built kit,** `softfloat-bootstrap/dist/softfloat-bootstrap-kit/`, and the zip,
  `softfloat-bootstrap/dist/softfloat-bootstrap-kit-v1.zip`. Its sha256 at dispatch is in docs/VALIDATION.md.
- **The builder:** `build/`, `kit/`, `tests/`, `verify/`, `Makefile`, `README.md`, `CLAUDE.md`,
  `docs/VALIDATION.md`, and `docs/KIT-0.md`, the plan. The plan is draft 3 as Logan approved it, with section 13's
  changes made during the build. Where section 13 and an earlier section differ, section 13 describes the kit, and
  whether each change is "major" is itself a thing to check: Logan's approval was "Approved if nothing major changes
  from the check".
- **Against:** the plan; Logan's words (the plan's section 1); and the four sources at the commits
  `build/sources.lock` pins. Read a source as the builder does, from git objects at its pinned commit
  (`git -C <repo> show <commit>:<path>`), not from its working tree. You may read cft-fp256: the clean room binds the
  hackathon's agents, not you.
- **The tree is frozen while you work.** Its digest is below. Check it before you start and again when you finish,
  and report both.

## What to check (a list, not a limit)

1. **The front door.** Run `bash verify/run.sh` and `--list` in the builder. Does each stage prove what its
   description says? Try, in a copy under your scratch directory, to make a stage pass that should fail.
2. **The gate,** `kit/tools/check_kit.py`. Each of its five checks against its docstring. Its controls, and whether
   each plant tests the shape it names. Its prefilter (`NEEDLES`, `FOLD`): is any needle not a necessary condition
   of its shape's pattern? Check 2's URL forms. Check 4's shapes against QRO-Crate's `tools/check_privacy.py`,
   ALTERNATIVES, at the pinned commit. Its exit codes.
3. **The clean room.** Read every sample, `examples/cases/*.md`, whole, and OWNER.md, GLOSSARY.md, METRICS.md and
   AGENTS.md: is any arithmetic of cft-fp256's there in words check 3's list does not hold? Read the archived
   ledgers' members, and the QRO-Crate bundle, for code. Round 4's ledgers name cft-fp256's tree paths and API
   facts, which START-HERE.md states as a limit.
4. **The samples.** Each one's "From" line: its line range and its entry against cft-fp256's docs/VALIDATION.md at
   `39f9801`. Each cut, and its reason. Is a quoted line altered anywhere? Does each show what its "What it shows"
   says? `build/cases.json` is the samples' source.
5. **Logan's words.** Every quotation in OWNER.md, PROJECT.md, CLEAN-ROOM.md, ROLES.md, WORKFLOW.md and GLOSSARY.md
   against its cited source and line, at the pinned commits, and his hackathon answers against the plan's section 1.
6. **Rules R1 to R6, and their counts.** Does each rule do what START-HERE.md says, and only that? Does each archive
   member no rule changed keep its bytes, and every member its name, order and timestamp?
7. **Privacy.** Anything of Logan's in the zip that the gate does not see: a name in another spelling, a machine's
   name, a private address, a key, in any file, member or blob. You may hash what you find. **Never write his
   address, his user name, his machines' names or his personal domains in your report:** name the file and the
   line.
8. **The tools,** `ledger.sh`, `plant.py` and `round_metrics.py`, against WORKFLOW.md, METRICS.md, the plan's
   section 4.4 and section 13's items 7 to 9. Run their self-tests, and try faults of your own. For `plant.py`: does
   a copy truly hold no route back to the parcel's tip (objects, reflogs, packed refs, FETCH_HEAD, config, hooks,
   alternates)? Does `check` catch a copy that differs anywhere else?
9. **The workflow and the protocol,** WORKFLOW.md, against ParcelRound's METHOD.md and round 6's lead.md (inside
   `archive/round6-ledger.zip`). Is anything stated as the method's that the method does not say?
10. **The build.** Is it deterministic: a rebuild, and a second zip? Does it read only git objects? The manifest's
    builder line will change after the first commit. That is the only difference expected between this dist and
    the one built after it.
11. **The record and the plan.** docs/VALIDATION.md, and the plan's sections 12 and 13: re-measure every figure you
    can, and look for a sentence that claims more than is true.
12. **The cold read.** Its questions are in `docs/reviews/v1/`. Another agent is answering them now, from the zip
    alone. Its key is in the lead's scratch directory. Do not look for the key, and do not read the cold reader's
    directory.

## How you class what you find

- **(a), a regression:** something that worked, and now does not.
- **(b), a wrong answer:** a result that is false, or a sentence that claims more than is true.
- **A note:** anything else, such as a gap, a wording or a limit.

READY means every property of the work is held by a gate, or stated as a limit. Any (a) or (b) makes it NOT READY.
Only (a) and (b) send the work back (OWNER.md, rule 1).

## Ground rules

- **Re-run things; never trust pasted output,** the record's figures included.
- **Report only.** Edit nothing in the builder, the sources or `dist/`. Build every fault in a copy under your own
  scratch directory, `<scratch>/verifier-v1/`, and delete only what you created there.
- **Never change any git configuration.** Do not commit, push or add a remote anywhere.
- **Read no other agent's scratch directory:** not the lead's, apart from your own subdirectory, and not the cold
  reader's.
- **No web access is needed.** Do not use it.
- **A time box of about two hours,** and a scope of the list above, with anything you find on the way.

## Your report

The harness may refuse to let you write a report file, so your final message is the report.
- **First line:** READY or NOT READY, with counts: N (a), N (b), N notes.
- **Each finding:** its class; what it is; where (file and line); its evidence, tagged MEASURED, READ, COMPUTED or
  BELIEVED; and how to reproduce it.
- **What you ran,** command by command, briefly.
- **What you did not check.**
- **The tree's digest** before and after your pass.
- **Last:** anything this brief got wrong.

## The tree at dispatch

The digest is the sha256 of the `sha256sum` listing, sorted by path, of every file that
`git ls-files --cached --others --exclude-standard` lists in the builder, except those under `docs/reviews/v1/`.
That directory holds this pass's own papers, which the lead writes while you work: this brief, and the cold read's
answers and key once its reader has reported. Nothing else changes until you report.

    affcf77e741c7aad3841414e9bbc90ca28577eb4666d2826cac99e9ba4b93a58

One way to take it, from the builder:

    git ls-files -z --cached --others --exclude-standard | tr '\0' '\n' | grep -v '^docs/reviews/v1/' | sort |
      tr '\n' '\0' | xargs -0 sha256sum | sha256sum
