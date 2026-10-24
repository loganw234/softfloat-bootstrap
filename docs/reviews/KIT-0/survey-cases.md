<!-- The read-only surveyor's final report on samples of "how things should be handled" in cft-fp256's
     docs/VALIDATION.md at 39f9801, extracted by script from its transcript's final message, unedited but for
     two absolute paths, written <repos>/ and <scratch>/ here, as round 6's verifier brief has a report write
     its paths: the harness refused its own write of this file. Its scripts and outputs stayed in its scratch
     directory. -->

I found 44 usable samples: 35 come through the kit's filter intact and 9 lose a line or two. Six strong statements are cut whole by a single filter term; they are listed separately as poor. The harness refused to let me write `report.md` ("Subagents should return findings as text, not write report files"), so this message is the only copy of the report. The scripts and outputs are in the scratch directory.

**Source:** `<repos>/cft-fp256` at `39f9801`, working tree clean before and after. `docs/VALIDATION.md` is 23,649 lines in 230 entries, ASCII with LF endings.

**Marks:**
- **MEASURED:** I ran a script. Every cut count, line count, privacy hit and skeleton below is MEASURED.
- **READ:** I read the text. Every "what it shows" is READ.
- **COMPUTED:** arithmetic on a script's output.

**The filter:** implemented exactly as the brief gives it, as `\b(?:<list>)\b` case-insensitive (`filt.py`). It cuts whole lines, and lines here are paragraph-long (median 68 characters, 90th percentile 237, longest 6,623). One hit therefore removes a whole bullet.

**Verdicts (my reading, not a script's):**
- **good:** the point survives, and no remaining line refers to a cut one.
- **usable:** the point survives, but the cuts show.
- **poor:** the point goes with the cut (listed under Near misses, not in the table).

## 1. Candidates (44)

All rows are from 2026-10-12 to 2026-10-22 except 12a (2026-09-30), which is the only explicit resume-note case. "Lines" counts the lines in the range; "Cut" counts lines the filter removes, with their numbers.

| # | Sit | Entry (shortened) | Lines in VALIDATION.md | What it shows (READ) | Lines | Cut (MEASURED) | Verdict |
|---|---|---|---|---|---|---|---|
| 1a | 1 | 10-20 coverage wave, closed | 22531-22553 | "What Logan asked, verbatim", one quote a bullet, then "The lead's readings and decisions, reported to Logan as they were made", 1 to 8 | 23 | 4 (22532, 22543, 22548, 22549) | usable: his ten numbered answers and readings 3-4 go |
| 1b | 1 | 10-22 figures refresh (FR) | 23534-23536 | Logan's verbatim words making the header define history; the lead added the sentence, then took it out; his "Go with 1" of "the lead's three ways", given "in the lead's words" | 3 | 0 | good |
| 1c | 1 | 10-13 experiment E1 | 19161-19172 | "Logan's decisions (verbatim)" beside "The lead's recommendation"; the send-back cap reached, "so the merge went to Logan", who waived it | 12 | 0 | usable: 19169 "round-to-odd" slips the filter, cut by hand |
| 2a | 2 | 10-14 second wave, closed | 19757-19762 | Twelve questions via AskUserQuestion: the question verbatim, the answer "Approve all as recommended (Recommended)", the option's own text, question 9 as put | 6 | 1 (19761) | usable |
| 2b | 2 | 10-14 third wave, closed | 20097-20101 | The lead's offer ending "Want me to queue it?", the answer verbatim, then "The lead's own correction of that offer" | 5 | 0 | good |
| 3a | 3 | 10-22 coverage report reads git (RG) | 23585-23599 | "Sent back three times": each (b) measured, fixed and restated in place with earlier figures kept; notes "no change"; a third look finds a check that could not fail | 15 | 0 | good (11.8 KB) |
| 3b | 3 | 10-21 transcendentals story (RM) | 22816-22823 | "A send-back under Logan's rule": the verifier's (b), a second (b) the lead found, notes taken, notes "Left alone, as the lead said", the re-check | 8 | 1 (22819) | usable: 22823 still names the cut note |
| 3c | 3 | 10-22 CI and the runner (P3) | 23177-23185 | "Known limits (Logan's rule: they merge)" stated as costs, then "Sent back once" for a check that passed when its file was missing | 9 | 0 | good |
| 4a | 4 | 10-22 gates that could pass a damaged input (P4) | 23515-23521 | Each limit as what still passes: "It guards accident, not forgery"; a SKIP by name where git cannot say | 7 | 1 (23517) | good |
| 4b | 4 | 10-22 scheduler staged runner (S2) | 23382-23392 | "Nothing here ran on the card, the box, XRT or the network"; "The guard is a look, not a lock"; a verifier's notes "kept as limits" | 11 | 0 | good |
| 5a | 5 | 10-19 side parcels, closed | 21846-21859 | The integration verifier's (b)s, then its re-check's one (b): "The (b) was in its own words, which 6db584a quoted" | 14 | 0 | good |
| 5b | 5 | 10-21 five false statements (P1) | 23106 | A verifier's run under other conditions "neither confirms nor refutes" the figures; its notes added at the merge | 1 | 0 | good |
| 6a | 6 | coverage wave, closed | 22601-22608 | "Twelve of the wave's thirty-eight (b)s were the lead's own words", listed; "The lead's lesson, four times in one day" | 8 | 2 (22602, 22606) | usable: the list no longer sums to twelve; 22603 needs a hand cut |
| 6b | 6 | E1 | 19185-19191 | "The lead's slips, each recorded in the round's ledger" | 7 | 1 (19190) | good |
| 7a | 7 | coverage wave, closed | 22675-22683 | Conduct: a global git config set and removed (checked); an unbundle into the main checkout repaired and checked with `git fsck`; new brief rules ("NEVER change any git configuration"); the lead's own slips | 9 | 0 | good |
| 7b | 7 | side parcels, closed | 21783-21791 | Conduct: a directory deleted that was not the agent's own, "reported it unprompted"; "The rule, restated: ... exact path ..., never by prefix"; a browser-tab rule added | 9 | 0 | good |
| 7c | 7 | 10-12 step 6's leftovers, closed | 18987-18991 | Two agents' slips, each with Logan's verbatim reply; the affected session told; "Every brief now carries both rules"; the lead's repeated slip | 5 | 0 | good |
| 8a | 8 | coverage wave, closed | 22655-22663 | Two failures "not a regression": four fresh clones, tip and base, built and unbuilt; cause read in the code; "The lead's:" part | 9 | 1 (22659) | usable: one A/B arm goes; 22655's "clause-5" slips |
| 8b | 8 | 10-22 stress driver before the nights (P5) | 23413 | A box failure (4 of 869) traced to a frozen test: "The planner and the tally were right; the check was frozen" | 1 | 0 | good |
| 9a | 9 | P5 | 23429; 23461 | Failed once under load, passed alone twice, "MEASURED both ways", carried as "load-sensitive" | 2 | 0 | good |
| 9b | 9 | 10-19 parcel EX | 21590 | "A pre-existing, timing-flaky check ..., not touched"; "reported to the lead, who agreed to record it as a known limit"; "no gate is exposed" | 1 | 0 | good |
| 10a | 10 | coverage wave, closed | 22610-22617 | "Corrections this record owes (a commit message stands as written)"; one "Not amended: DR2 had branched from it" | 8 | 2 (22612, 22615) | good |
| 10b | 10 | 10-22 parcel P2b | 23344-23349 | The lead's merge edits; counts corrected in place; "Two of the lead's own commit messages, which cannot be restated" | 6 | 2 (23345, 23346) | good |
| 11a | 11 | 10-19 seventh wave, closed | 21352-21363 | The VERDICT line; each stage skip by name with its quoted reason; "the same ... as each of waves 1 to 6's gates" | 12 | 1 (21361) | usable: "4 inner skip(s)" no longer adds up |
| 11b | 11 | P5 | 23427 | "VERDICT: PASS with 10 inner skip(s) in cardstress (10)", each skip named with its reason | 1 | 0 | good |
| 12a | 12 | 09-30 steps 5 and 6 round (older) | 16510 | Logan paused the round; every agent committed and wrote a resume note in 9 minutes; each re-dispatched "from its brief and its own ledger's resume note" | 1 | 0 | good |
| 12b | 12 | 10-16 sixth wave; 10-19 seventh wave | 20805; 21277-21279 | "Monday can carry on where this is left off", then "Clear to resume where the round leftoff" | 4 | 0 | good |
| 13a | 13 | coverage wave, closed | 22770 | "The time boxes (reported to Logan on his question)": first passes against boxes, two overruns, size ceilings passed by about 1.2 to ten times | 1 | 0 | good |
| 13b | 13 | 10-21 parcel P6 | 23114 | 1,193 lines against a 700-line mark, "accepted by the lead after the fact" ("the late flag is this parcel's slip") | 1 | 0 | good |
| 14a | 14 | coverage wave, closed | 22685-22698 | "The experiment: Sonnet 5.5 authors, Haiku 5.5 verifiers", as data, with caveats ("not a measured comparison") and "The lead's reading, for Logan" | 14 | 2 (22686, 22689) | usable: the headline bullet goes |
| 14b | 14 | E1 | 19140-19148 | Verdict "with the criteria applied as fixed": "Not met, by the letter" | 9 | 0 | good |
| 14c | 14 | E1 | 19180-19184 | Known limits: "n = 1", the seal "held ... by instruction only", position bias, default effort | 5 | 0 | good |
| 15a | 15 | E1 | 19112-19118 | A verifier's (a) "CONFIRMED by the lead: the test alone fails in 1.25 s" before the send-back | 7 | 0 | good |
| 15b | 15 | side parcels, closed | 21717; 21729-21733 | Logan's "PK has been going for over 4 hours, check in", "answered from its ledger and transcript"; "Briefs now carry a scope ceiling and a time box" | 6 | 0 | good |
| 15c | 15 | 10-21 DR4 (23000) and SR2 (23041) | 23000; 23041 | One parcel's measured collision with another's suite, relayed by the lead; both sides discount overlapping runs ("it is NOT counted") | 2 | 0 | good |
| 16a | 16 | coverage wave, closed | 22619-22638 | Eleven merges, their conflicts "recomputed for this record by `git merge-tree` of each merge's two parents", resolutions, checks | 20 | 2 (22624, 22629) | usable: two table rows go |
| 16b | 16 | 10-22 nightly page (NP) | 23643-23647 | Main merged into the branch; a test failed once; a silent fallback removed: "an error from the report is a failure, not a fallback" | 5 | 0 | good |
| 17a | 17 | coverage wave, closed | 22682 | An empty first clone (a bundle with no HEAD); "SHA, tree and content" asserted on the rerun; later bundles cloned with `-b` | 1 | 0 | good (also a bullet of 7a) |
| 17b | 17 | P2b | 23296 | A card run from a branch clone, "(the SHA and the content asserted apart ...)" | 1 | 0 | good |
| 18a | 18 | 10-19 CI's RTL suite as three jobs | 21023-21036 | "Known limits (the verifiers' other notes, not taken)", each with its reason; "The lead takes the trade" | 14 | 0 | good |
| 18b | 18 | coverage wave, closed | 22783; 22790 | The integration verifier's notes "Not taken", each with its reason | 2 | 0 | good |
| 19a | 19 | 10-20 sweep reorganised (DR2) | 22478-22487 | "What the brief got wrong", the size among it ("The lead accepted the size") | 10 | 0 | good |
| 19b | 19 | RM | 22825-22832 | "Checked and left alone (READ, each with its reason)" | 8 | 2 (22826, 22827) | good: the first two bullets go; mild math-library names remain |
| 19c | 19 | P4 | 23504-23506 | "What only the lead's runs, and CI's next run, will show": claims kept BELIEVED until a run says | 3 | 0 | good |

**Where the record's wording differs from the brief:**
- **Situation 3:** the rule is "Logan's rule of 2026-09-27", first quoted at 15277 and restated at 15854: 'Only a regression "(a)" or a wrong answer "(b)" sends a parcel back.' Recent entries cite it as "Logan's rule" and head their limits "Known limits (Logan's rule: they merge)".
- **Situation 8:** the rule "never call a failure a defect or a false alarm until a clean re-run says which" is not written in those words in VALIDATION.md or CLAUDE.md (MEASURED by grep). The nearest statements are 22475 (cut whole, below), 22553 (inside 1a), 23429, 23131 and 23413.
- **Situation 15:** in this record "escalation" is an arithmetic term (43 lines, the precision-escalation path). The rows are findings or questions that reached the lead and were checked before acting.

**Near misses (poor): cut whole by one term**

| Lines | What it says | Term |
|---|---|---|
| 23552 | Situation 2's best case: the question verbatim plus the text of the option Logan chose | `scaleb32`, inside the option's text |
| 22475 | Failures under load "none chased", "not as defects found" | `cvtto32`, `rne` |
| 22599-22600 | "Three of the verifiers' own supporting statements were wrong, each corrected by its verifier" (restated at 22686, also cut) | `clause5` |
| 22814 | "A correction at the lead's word (... after this entry's first report, which had flagged the count)" | `rounding` |
| 23210 | A stage stopped by PID, "recorded `golden.fail` for that stop and for nothing else" | `fma` |
| 22703 | "The flake list" | `cvtto32` |

**Alternates (good, not in the table):**
- 20924 and 18963: answers to recommendations.
- 22951-22958: scheduler limits.
- 20997-20998: a verifier's caveat on its own (b).
- 20986-20987, 22683 and 22789: the lead's slips.
- 18310-18313: a failure read as "not a defect".
- 23131: "BELIEVED a load flake".
- 20902-20904, 20123-20126 and 21369-21383: messages that stand as written.
- 20886-20888: a gate's skips by name.
- 21412-21416: "Beside the wave, not in this push".
- 22883, 23577 and 22480: size overruns.
- 20127-20135: merge checks.
- 22571 and 21355: clones asserted.
- 21101: notes taken except one.
- 22864-22869, 22206-22211, 23466 and 22862: what the brief or the author's own drafts got wrong, and findings the brief did not ask for.

## 2. Closed-entry skeleton (MEASURED by `skeleton.py`)

**Method:** 15 headings contain "closed". A section is a `### ` line or a paragraph-level `**` lead-in. None of these six has a `###` heading; the record's 170 all end by line 11223. "[n]" counts the bulleted bold lead-ins inside a section.

**Caveat:** 21989 is a single parcel's entry (FX), not a wave close. The seventh newest, 20554, is the alternative.

- **20802-20921** (sixth wave, 10-16):
  - 20804 What Logan asked
  - 20810 The lead's readings and decisions [5]
  - 20822 The chain [6]
  - 20858 Time and tokens [3]
  - 20868 The census at the small tasks' commit [3]
  - 20876 The card [8]
  - 20886 The gate [6]
  - 20902 The merge messages, restated [2]
  - 20906 Known limits carried [4]
  - 20917 Records
- **21042-21102** (the card's long stress run, 10-19):
  - 21044 What Logan asked
  - 21046 The sources
  - 21054 The run [4]
  - 21060 The legs [5]
  - 21074 The sweep [7]
  - 21087 Telemetry [3]
  - 21094 Uptime
  - 21096 Known limits [3]
  - 21101 Who ran it
- **21275-21431** (seventh wave, 10-19):
  - 21277 What Logan asked
  - 21283 main's first CI run of the split [4]
  - 21295 The lead's readings and decisions [3]
  - 21304 The chain [18]
  - 21334 The box and the card [10]
  - 21352 The gate [5]
  - 21369 The entries above, restated [2]
  - 21385 Known limits carried [4]
  - 21412 Beside the wave, not in this push [4]
  - 21418 Time and tokens [3]
  - 21426 Records [1]
- **21711-21860** (side parcels, 10-19):
  - 21713 What Logan asked
  - 21722 The lead's readings and decisions
  - 21736 The chain [2]
  - 21752 Found at the merges [7]
  - 21761 The box [8]
  - 21783 Conduct [5]
  - 21793 Known limits carried [4]
  - 21816 The follow-ups
  - 21823 Wave 7's entry, restated
  - 21829 Time and tokens [2]
  - 21842 Records [5]
- **21989-22064** (FX, 10-20):
  - 21991 What Logan asked
  - 21993 The hazard, shown [5]
  - 22002 The choice [3]
  - 22010 What changed [3]
  - 22026 Evidence [6]
  - 22046 Known limits [7]
  - 22060 Conduct
- **22529-22791** (coverage wave, 10-20):
  - 22531 What Logan asked
  - 22545 The lead's readings and decisions
  - 22555 The pass-size experiment [6]
  - 22563 The overnight run [5]
  - 22571 The card smoke ...
  - 22583 The chain [2]
  - 22610 Corrections this record owes
  - 22619 The merges [4]
  - 22640 The box [18]
  - 22675 Conduct [8]
  - 22685 The experiment ... [8]
  - 22700 Known limits carried [14]
  - 22733 The follow-ups [7]
  - 22742 Time and tokens [2]
  - 22772 Records [6]
- **Alternative, 20554-20675** (fifth wave, 10-16):
  - 20556 What Logan asked [3]
  - 20561 The lead's decisions during the parcel
  - 20575 The chain [5]
  - 20607 Time and tokens [2]
  - 20614 MC's runs on amd-arc-box [3]
  - 20629 The gate [5]
  - 20645 The merge's message, restated [3]
  - 20650 Known limits carried [5]
  - 20670 Records

**Recurrence across the six** (COMPUTED by `skelsum.py`; position 0 is first, 1 is last):

| Section | Entries (of 6) | Mean position |
|---|---|---|
| What Logan asked | 6 | 0.00 |
| The lead's readings and decisions | 4 | 0.12 |
| The chain | 4 | 0.27 |
| Box, card or gate runs | 5 | 0.44 |
| Merge messages restated | 2 | 0.64 |
| Conduct | 3 | 0.71 |
| Time and tokens | 4 | 0.77 |
| Known limits | 6 | 0.78 |
| Follow-ups | 2 | 0.78 |
| Records | 4 | 1.00 |

## 3. Arithmetic terms the list misses (MEASURED: `missed.py`, `missed2.py`)

"Lines" counts lines of the whole file containing the term; "not cut" counts those the filter lets through.
- **Spellings the list cannot reach:**
  - `clause-5` with a hyphen: 16 lines, 10 not cut; 22655 (8a), 21413.
  - `conv32to64` / `conv64to32`: 36 lines, 4 not cut. The `\b` after the digits fails before "to".
  - `cvtto` / `cvtfrom` with no digits: 26 lines, 8 not cut; 22614 (10a).
  - `f32_` / `f64_` names: 4 lines, 1 not cut.
- **Operation names missing from the list:**
  - `divsqrt`, `divfull`, `rsqrt`: 107 lines, 48 not cut.
  - `scaleB` / `rint` / `nextup` with no digits: 51 lines, 17 not cut.
  - `nextdown`, `logb`, `class32`: 21 lines, 7 not cut.
  - division / divide: 111 lines, 64 not cut. Square root: 43, 20. Reciprocal / `RECIP_`: 15, 7. Newton / Goldschmidt: 20, 14.
- **Inflections the closing `\b` blocks:**
  - overflows / overflowed / underflows: 20 lines, 12 not cut.
  - exponents: 23, 7. Normalized: 12, 4 (some English).
  - rounded / rounds / "round to": 130, 73 ("correctly rounded" 27, 16).
- **Technique and format terms:**
  - round-to-odd, round-to-nearest, "directed": 67 lines, 13 not cut; 19169 (1c).
  - binade(s): 23, 5. Powers `2^-N`: 85, 27. Encodings: 96, 49.
  - precision: 61, 43. Enclosure: 39, 21. Cancellation: 17, 9. Truncat*: 48, 35. Limbs: 35, 24.
  - `mpfloat` / `cft_mp_`: 23, 15. `Bv`, `bound_half`, `bound_double`: 71, 8.
  - inexact: 65, 36. Invalid: 35, 11. Signed zero / +0 / -0: 79, 48.
  - "fused multiply-add": 10, 6. Widening / narrowing: 25, 20. Augmented: 49, 26.
  - escalat* (the precision path): 43, 38.
- **Hard-case construction:** "modular inverse": 3 lines, 1 not cut, and it is **22603, inside 6a: cut it by hand**.
- **Transcendentals:** transcend*: 244 lines, 154 not cut. exp2 / expm1 / log1p / log2: 320, 105. Payne-Hanek, 2/pi: 6, 2. ln2: 49, 8.
- **Oracle and test-source names:** MPFR: 141, 111. mpmath / gmpy2: 201, 154. UCBTEST, FPgen, CORE-MATH: 17, 6. "golden model": 97, 56. These are mostly tool names and versions, the mildest kind.
- **Standard references:** "table 9.1", "clause 9": 14, 7.
- **False positives checked by eye:** "log" (a log file), "exp" in branch and file names, "ties" (23095), "quiet" (a quiet desktop), "the remainder of this week".

## 4. Privacy shapes inside candidates (MEASURED; classification READ)

- **Inside the 44:** no email, IP address, user@host, home or personal path, or key or token shape. Two false-positive shapes:
  - 21355 (11a): two 40-hex git object ids, key-shaped but not secrets.
  - 19187 (6b): the word "token", meaning model output tokens.
- **Outside the ranges, to keep out of excerpts:**
  - 23532 and 23575: the personal-path scan's own pattern list; 23575 includes the owner's bare user name followed by "@" and a Windows host-name prefix.
  - 22358: root's git config path in WSL.
  - 18955-18956: a box home directory written with `~`.
  - 33 older lines (238 to 11968): a full Windows desktop host name.
  - 19920, 21132, 21661, 22220, 23080, 23235 and 23641: IPv4 shapes that are loopback addresses, a library version and a C-standard clause.

## What I did not do

- **Not read all 23,649 lines.** I read in full or near full the low-arithmetic entries from 2026-10-12 on: every closed entry from 18943 on, the 10-21 and 10-22 entries, E1, the CI split and the RETIMING decisions. Everything else I located by keyword.
  - Unsurveyed in depth: 18996-19068, 19422-19547, 19644-19752, 19885-20094, 20211-20326, 20444-20553, 21432-21710, 21861-22064, 22253-22361, 22495-22528, and everything before 10-12 except 16505-16516 and 18300-18322.
  - Long lines were read truncated on a first pass. For 23585, 23413 and 23643-23647 the descriptions rest on their first 600 to 1,500 characters.
- **Verdicts are judgement;** only the cut counts are measured. I verified no claim of the record itself.
- **Grep only** on CLAUDE.md and CARDDAY.md. The privacy scan is my own regexes, not the kit's gate.
- **Nothing changed:** no git command that writes (read-only ones used `GIT_OPTIONAL_LOCKS=0`), nothing edited in either repository, no background process started.
- **Time:** about 21 minutes of the 60-minute box.

Files are in `<scratch>/surveyor-cases/`:
- `filt.py`
- `measure.py`
- `final.tsv` (the 44 ranges)
- `final.txt` (each cut line and the terms that cut it)
- `skeleton.py`, `skeleton.txt`
- `skelsum.py`
- `missed.py`, `missed.txt`, `missed2.py`
- `density.tsv` (lines and cut lines for every entry)
