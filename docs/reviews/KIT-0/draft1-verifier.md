<!-- The verifier's final report on KIT-0 draft 1 (sha256 91a3972c...), extracted by script from its
     transcript's final message, unedited but for one address at Logan's personal domain, written <address>
     here, and its scratch directory's absolute path, written <scratch>/: the harness refused its own write of
     this file. -->

# Verifier report on KIT-0 draft 1

**NOT READY: 6 (a), 10 (b), 18 notes.**

The harness refused to let me write `verifier-KIT0/report.md` ("Subagents should return findings as text, not write report files"), so this message is the only copy of the report.

The draft's sha256 matched before my pass and still matched after it:
`91a3972cebadd2f066092e887f5f8e4a7074d92fd4bcdd97650ea909658bca87` (MEASURED, `sha256sum`, at 19:49 and 20:17 UTC).

All four source repositories were clean before and after my pass, at `65447fd`, `f42242e`, `8afeede` and `39f9801`: `git status --porcelain` printed 0 lines in each (MEASURED). I wrote only under `<scratch>/verifier-KIT0/`:
- `src/hf`, `src/pr`: every tracked file, taken with `git show <commit>:<path>`. Each one `cmp`s equal to its working-tree copy (MEASURED).
- `arch/<round>`: the six archives, unpacked.
- `kitsim`: the planned `method/` layout (section 4.1's 30 files). `kitsim3` is that layout with R1 to R3 applied.
- `cftx/excerpt.md`: the six named sections of cft-fp256 docs/VALIDATION.md:22529-22791.
- `prcopy`, `qrocopy`: copies to run tools in. `qro-8afeede.bundle` is a test bundle.
- `scripts/`: tok.py, terms.py, links.py, rules.py.

I started no background process.

Tags: MEASURED means I ran it and have the output. READ means I read it at the cited place. BELIEVED is neither.

---

## Findings that send the draft back

### (a) Design defects

**A1. The round 5 and 6 archives carry cft links and private data that no rule or check reaches (K1).** Section 4.1 copies both "byte for byte", and no rule can touch a zip. MEASURED, `grep -o` over the unpacked members:
- **round6-ledger.zip** holds 12 full `https://github.com/loganw234/cft-fp256/...` URLs: P2.md:153 and :437; P3.md:104, :388, :391, :409 and :412; P4.md:80, :159, :209, :294 and :384. P3.md:104 is the bare repository URL.
- **round5-ledger.zip** holds two truncated repository URLs, `https://github.com/loganw234/cft-fp256/blob/77b8440.../`, at P1.md:134 and verifier-P1.md:305.
- It also holds the public site written as a regex, `https://loganw234\.github\.io/cft-fp256/`, at briefs/P1.md:74. A check matching the host literally would miss that spelling.
- **round5 also fails check 4's shapes:**
  - 42 lines hold home paths (`C:\Users\<name>`, `C:/Users/<name>`, `/c/Users/<name>`);
  - 9 lines hold a personal address (lead.md:1160 among them);
  - QRO-Crate's ALTERNATIVES refuse both shapes (tools/check_privacy.py:72, :74 and :92, READ).

The draft's R1 counts "12, all in ParcelRound METHOD.md". That count holds for the texts, but it leaves out these 15 links. The two archives are about 64% of the method material by `o200k_base` tokens (259,008 of 405,510; COMPUTED).

Checks 2 and 4 do not say whether they read zip members, so the outcome depends on that:
- **If they do,** the gate catches this, and the planned kit cannot pass, because no rule removes the links.
- **If they do not,** the gate passes a kit that carries cft links.

The proposed QRO-Crate bundle (Q4) is just as opaque. A bundle made at `8afeede` holds 0 grep hits for `cft-fp256`. Unbundled, `git grep` finds all 52 lines (MEASURED).

**A2. The planned layout leaves three relative links dangling, so check 2 fails and both MIT notices are lost.**
- **Dangling links (MEASURED).** I applied R1 to R3 to the 30 planned files with a regex. The counts came out at the declared 12, 3 and 4, and 3 of the 97 relative links did not resolve:
  - `honest/README.md:130` `[LICENSE](LICENSE)`;
  - `parcelround/README.md:29` `[tools/check_method.py](tools/check_method.py)`;
  - `parcelround/README.md:99` `[LICENSE](LICENSE)`.
- **check_claims.py fails on the copy (MEASURED).** HonestFramework's tools/check_claims.py, run on the planned copy, gives rc 1: "README.md: broken link LICENSE".
  - With LICENSE added and R2 applied, it passes: rc 0, "39 links resolve".
  - The control holds. A wrong-case target, `../ParcelRound/README.md`, gives rc 1 with three broken links.
  - So section 4.1's "if it passes on the copy" resolves to no, as planned. Dropping the tool would also break README.md:44 and templates/README.md:39, which both link to it.
- **Licences (READ).** Both LICENSE files are MIT: "The above copyright notice and this permission notice shall be included in all copies or substantial portions" (LICENSE:12 in each).

The plan has this wrong, but the gate would catch it: check 2 fails at step 6 of section 9. Passing would need an unnamed change, which K2 forbids, or files the plan does not list.

**A3. QRO-Crate, proposed for the zip in Q4, carries code and values taken from cft-fp256's specification, not only citations.** READ:
- qro/spelling.py:70-82, `exact_decimal`: "A binary64's exact decimal, in cft-fp256's one spelling".
- qro/vocabulary.py:70-71: the binary64 spelling "in cft-fp256's spelling ([-]D[.DDD]e[+-]X; 0, -0, inf, -inf)".
- tests/format/test_spelling.py:17-21 holds nine values, which tests/format/test_sweep.py:17 calls "nine values of cft-fp256's".
- qro/reader.py:4: "cft-fp256's strict reader, docs/CERTIFICATES.md:852-899, READ, adapted to JSON-LD".
- qro/spelling.py:3-4 states a "Departure from cft-fp256".

A binary64-to-decimal writer is one of the conversions the draft's own section 6 lists among clause 5's required operations (BELIEVED, for the standard).

The draft's text, "52 of its lines name cft-fp256 ... about its certificate format and number spelling. In the kit those citations dangle by design", is wrong on two counts:
- 9 of the 52 lines are in code or tests: qro/ 5, tests/ 2, tools/ 2.
- tools/check_docs.py:21 and :34 are about neither the certificate format nor number spelling (MEASURED, `git grep -c -i cft-fp256 8afeede`).

The code is QRO-Crate's own, built on Python's `Decimal` to follow a spelling cft-fp256 documents. Whether that breaches K1 is Logan's call, and Q4 has to put it to him. No planned check catches it: check 3 reads only examples/cft-records/, and a bundle is opaque (A1).

**A4. Check 3's term list lets through arithmetic-method content in the very sections the plan names, and the plan states no limit for it.** I ran the stated list over the six named sections (104 lines), word-bounded and case-insensitive (MEASURED). It cuts 5 lines: 22543, 22593 and 22606 for fma; 22602 for softfloat; and 22612 for overflow and fp32. It passes these:
- VALIDATION.md:22603: "'shares no arithmetic with the builders' (false: the modular inverse is shared) and a paraphrase of UCBTEST's README". That describes how cft-fp256 builds its hard cases.
- :22614: "still planted cvtfrom_int", a cft-fp256 conversion routine.
- :22689: "a traceback on an Infinity".
- :22600: "clause5's objects with the define differ on 16.1".

ParcelRound says that a gate written as a list of forbidden spellings is "a stated limit, not a guarantee" (METHOD.md:920-927, READ). The draft calls the list "conservative", which says it fires too often. It does not say the list also misses things.

**A5. The planned key reveal repeats round 6's recorded lapse, against a rule the kit itself carries as pending.** The draft says "reveals the key after the report" and "`reveal` appends the key to the ledger". READ:
- CASE-STUDY-6.md:171-185 is observation 6: "The lead revealed keys while a verifier still worked". The shapes also reached wave 2 through the lead's prose (:180-185).
- Its proposal at :346-348: "A round's planted-fault keys, and any description of their plants, stay out of the ledger until every verifier on a planted copy in the round has reported, later waves' included". ADOPTION.md:151 lists it as CS6#3, pending.
- Round 6's lead.md:588 records "The lapse", and :596 makes the proposal.

With two or three waves in a row, revealing each key in a ledger every agent reads hands later verifiers the shapes of earlier plants. The draft follows CASE-STUDY-6.md:44-47's summary ("the key itself after the report") and drops that case study's lesson.

Round 6's conditions are also missing from `plant.py make`:
- "a fresh repository detached at <copy>, with no remote, no branches and no route back to P3's own tip" (lead.md:488);
- the key "kept outside every agent's reach" (:489);
- each parcel's tip kept out of the ledger until its verifier reports (lead.md:460; ADOPTION.md:143, CS5#8);
- the verifier forming its view before it reads the parcel's file. Design-first leaves a reference copy there: "Each of the three noticed that its two wrong answers were the only places where the copy differs from the parcel's own design" (lead.md:560; CASE-STUDY-6.md:160-165; CS6#4).

If `make` commits the plants on top of the real tip, `git show` reveals them (BELIEVED, since the mechanism is unstated). No check covers any of this, and "Plants caught" would measure nothing.

**A6. Filling HARNESS.md and BOARD.md on day 1 contradicts the freeze.** Section 3, item 2 says "HARNESS.md is a table the lead fills in on day 1", and section 5.1, phase 0 says "Fill HARNESS.md and BOARD.md, with Logan". But K4 says "frozen from kickoff, and only Logan's word changes it, as a new version", and check 1 requires "Every file's sha256 matches".
- **If they are filled inside the kit,** check 1 fails on day 1 and K4 is broken. Check 1 would catch it.
- **If filled copies live in the softfloat repository,** the plan has to say so. That one sentence fixes it.

### (b) Wrong answers

**B1. Wrong token figure: 27,193 counts the whole file, not its first 60,648 bytes.** Section 4.1 says "Claude's tokenizer gave 27,193 tokens for the first 60,648 bytes ... about 2.2 bytes a token ... up to about 1.8 times". MEASURED:
- Reading ParcelRound METHOD.md with the Read tool prints "showing lines 1-1132 of 1449 total (27193 tokens, cap 25000)".
- Lines 1-1132 are exactly 60,648 bytes.
- I wrote those same 1132 lines to a scratch file. The tool read them whole under the same 25,000 cap, with and without offset and limit.

So 27,193 is the count for all 78,786 bytes. Corrected (COMPUTED):
- about 2.9 bytes a token, a factor of about 1.37 against `o200k_base`'s 19,866;
- if the tool also counts its own line-number prefixes (BELIEVED possible), the comparable `o200k_base` count is 25,529 (MEASURED), and the factor is about 1.07.

Nothing supports "1.8". Calling the Read tool's count "Claude's tokenizer" is itself BELIEVED.

**B2. cft-fp256 has not run on a Pico.** Section 2 says "cft-fp256 already runs binary32 and binary64 on an RP2040 ... It runs there through the Arduino binding". READ:
- docs/EMBEDDED.md:673-677: "Four boards have not been attached: the Pico, the Uno, the Nano and the Mega. Everything this document says about them is a COMPILE result".
- :685 lists "all 168 sets on a Pico" as pending.
- docs/VALIDATION.md:10570-10571: "The Pico, the Uno, the Nano and the Mega are still unattached".

What is true: it compiles for the RP2040 (EMBEDDED.md:251-253 and 450-453), and the board profile's 168 sets match on a host loopback (:602-603). The case for a clean room still stands (BELIEVED).

**B3. "Two are known" leaves out a third.** CLEAN-ROOM says "every repository that carries its code. Two are known". The kit's own CASE-STUDY-4.md:27-30 says "P2 moves atlas-film ... onto cft-fp256's pinned arithmetic", and :56 and :125 say the same (READ). That makes atlas-film a third.

**B4. Calling loganw.dev "not cft" overreaches.** Section 4.1 says "The two loganw.dev URLs in CASE-STUDY-5.md stay. That site is not cft." READ:
- CASE-STUDY-5.md:19-21: "a static site generated from the owner's other repositories".
- Round 5's briefs/P1.md:72-74: the Home page's Verify checks run "at the cft-fp256 pin", one of them reading cft-fp256's README link to `loganw234.github.io/cft-fp256`.

The site is not the cft-fp256 repository, but by the kit's own record it is built from it, so it cannot be the reason those URLs meet K1. Q2 should name it.

**B5. Section 7's title is false for at least six of its rows.** It promises "every figure from a source the agents don't write". Rows that agents write:
- Findings and Brief corrections both come from reports.
- Escalation latency comes from ledger stamps. Typed stamps ran 3 to 90 minutes off in round 2 (ParcelRound METHOD.md:560-564). The coverage wave's lead wrote ten headings as estimates, 10 to 40 minutes late (VALIDATION.md:22683).
- Conduct and the lead's slips come from the lead's own record: item 8's "self-report in disguise".
- Logan's words come from the lead's transcription.
- Plants caught are scored from reports.

**B6. The excerpt is not the kit's only per-agent table.** Section 4.3 says these "are the only examples of the per-agent tables Logan called the most tracked". But CASE-STUDY-3.md:541, -4.md:248, -5.md:290 and -6.md:293 each have a "Cost of the round(s) (measured from the transcripts)" with a row per agent, for example CASE-STUDY-4.md:269 (READ). What may be unique to the excerpt is its minutes-per-pass column against time boxes (BELIEVED).

**B7. OWNER.md's send-back rule drops the method's restate clause.** Rule 1 reads "Only a regression or a wrong answer sends work back; anything else merges as a recorded known limit (ParcelRound METHOD.md:1125-1137)". The cited lines go on: "and a sentence that claims more than is true is restated at the merge, not left standing" (:1126-1127). cft-fp256 carries the same clause at VALIDATION.md:15854.

The kit's other pieces then turn this into a stricter rule: GLOSSARY says "(b) is a wrong answer, a false sentence among them", and section 5.1 says "send-backs follow the (a)/(b) rule". Together they send back what the method restates at the merge. The coverage wave fixed its wording (b)s without a send-back ("no: the lead fixed the wording three times", VALIDATION.md:22587).

**B8. The cited lines hold three of the eight things the lead asks first.** Section 4.2 gives eight items "(METHOD.md:1372-1377)". Those lines name three: "a push that deploys, a remote branch deleted, a change to how results are counted". The other five are the lead's, and nothing marks them:
- scope;
- models and tiers;
- board sessions;
- exceptions to a standing rule;
- contact with cft.

The plain "a push" is QRO-Crate's CLAUDE.md:104. This sits in a plan that cites :1379-1380 for keeping the lead's reading "marked as the lead's".

**B9. The loose cap is not only in CLAUDE.md, and leaving cft out cannot drop it.** Section 2 says "The loose cap is written only in QRO-Crate's CLAUDE.md, item 6. ... or excluding cft drops it."
- **It is written in other QRO-Crate files too (READ):** docs/VALIDATION.md:789-792, :1021, :1027, :1781 and :2753, and docs/reviews/P0.1/round1.md:9.
- **It is in no cft file (MEASURED):** there are no hits in cft-fp256's CLAUDE.md or docs/.

What would drop it is QRO-Crate's absence.

**B10. Rule 6's line range is one short.** It cites "QRO-Crate docs/VALIDATION.md:789-791", but the quotation ends on line 792: "it back for prose only issues." (READ).

---

## Notes (do not send back)

- **N1. A standing rule is missing:** "Logan, 2026-09-25: no agent loads the machine on purpose" (cft-fp256 VALIDATION.md:15443). It is carried as "Logan's rule" at :15797, and as "Nothing loaded either machine on purpose" at :16664, :16840 and :17030 (READ). The record paraphrases it rather than quoting it. It matters if the agents share Logan's desktop.
- **N2. Rule 8 has no date,** though the plan says each rule has its date and source. The record dates it 2026-09-30 (VALIDATION.md:16505 heading, :16510 words, at `39f9801`; READ).
- **N3. Rule 4 also names a Claude model.** "Rules 3 and 5 name Claude models", but rule 4's elided opening says "with a Sonnet parcel and verifier for each" (VALIDATION.md:19293).
- **N4. Logan's boundary needs asking, not inferring.** The request says "not letting them browse my GitHub", while answer 3 says "the only restriction is staying away from cft". Q2 asks only how wide "cft" is.
  - The kit already names `github.com/loganw234/Quantum-Film` (CASE-STUDY-4.md:13), `/loganw.dev` (CASE-STUDY-5.md:19) and `/ParcelRound` (CASE-STUDY-6.md:20) in plain text.
  - If QRO-Crate is given "separately" through GitHub, the agents will be on Logan's GitHub.
- **N5. Check 2's host list covers cft-fp256 alone, but Q2 proposes the wider list.** Under the wider list, CASE-STUDY-4.md:13's Quantum-Film would pass check 2, though it has cft-fp256 as a pinned submodule (CASE-STUDY-4.md:55; QRO-0.md:102 says moth-quantum holds it). The check should take its list from Q2's answer.
- **N6. Some cft-fp256 text sits outside check 3's directory:**
  - OWNER.md: VALIDATION.md:20101, 19293, 21733, 22537, 22676 and 22681;
  - GLOSSARY: 15854 and 17961;
  - METRICS: 22742;
  - AGENTS.md: cft-fp256 CLAUDE.md's desktop entries.

  So section 3.1's "neither the reader nor what it read beyond those excerpts" does not hold for these lines. None of the ones I read holds arithmetic.
- **N7. Q8 answered: the GLOSSARY definitions are roughly true to the records (READ, sampled).** The nuances:
  - **MEASURED:** in cft, it names who ran it and where ("MEASURED by RT at 949e56c", :18913).
  - **READ:** it covers reports, pages and searches as well as file:line ("(READ, by VCI)" :20929; "(READ, the project's page)" :21941; QRO-Crate's "(READ, a search of its tree)").
  - **COMPUTED:**
    - it does not always show its arithmetic ("(COMPUTED)" :18110);
    - QRO-Crate's docs never use it: 0 lines against 589 for MEASURED, 228 for READ and 105 for BELIEVED (MEASURED, `grep -r -w`).
  - **BELIEVED:**
    - it also covers unchecked claims ("BELIEVED where a word was not checked" :18253; "BELIEVED mine and unverified" :21446);
    - the preamble's "BELIEVED is neither" and GLOSSARY's "an estimate or an inference" differ.
  - **(a)/(b):** these classes are cft-fp256's alone. QRO-Crate splits "a defect in what the code does" from prose instead (CLAUDE.md:105-109).
- **N8. Run `watch.sh` inline.** ParcelRound METHOD.md:677-686 says "Arm the watcher from an inline command, not a script file". The plan should say watch.sh is pasted inline, or run under the agent's own name.
- **N9. R3 does not say the link target goes,** as R1 does. If it stays, check 2 fails on those four links.
- **N10. Some carried text points at things the kit leaves out.**
  - METHOD.md:22-24 and ADOPTION.md:11 describe `tools/check_method.py`, which is excluded.
  - METHOD.md:12-18's citation forms point at ledgers "archived beside" the case studies, and four of the six are absent.

  The plan should state both as limits, beside the cft citations.
- **N11. HARNESS has no row for transcripts,** which METRICS names as the source for tool uses and minutes.
- **N12. `plant.py score`'s rule for matching plants to findings is unstated,** and so is its false-alarm rate. Round 6 graded by reading (lead.md:556-560). HonestFramework METHOD.md:333-335, which the draft itself cites, asks for that rate.
- **N13. The audit's reach is narrower than section 2's list.** It fingerprints only host/src/ and python/cft_golden/, and leaves out python/hardcases.py, python/external_*.py and vectors/gen_vectors.py. The plan should state that limit.
- **N14. Section 5.1, phase 3 fixes what P0 contains,** while K3 says the kit decides nothing of "the split". Mark the P0 list as a proposal.
- **N15. The controls are thinner than the checks:**
  - one "cft URL" plant serves the four host forms check 2 refuses;
  - no plant covers a file missing from the manifest;
  - none covers the escaped spelling at round 5's briefs/P1.md:74.

  QRO-Crate plants one control for each shape (tools/check_privacy.py:320-335 and :384).
- **N16. "three-commit protocol" is round 6's phrase.** It also appears in CASE-STUDY-6.md:46, which is at the kit's top level, and in round 6's lead.md:487. HonestFramework's protocol rests its evidence on `git log` (METHOD.md:696-702). Round 6 and this plan keep the hash and the reveal in a ledger that ParcelRound keeps out of version control (METHOD.md:501-506). The plan should state that deviation.
- **N17. The kit hands every verifier round 6's keys,** which are plant shapes. HonestFramework METHOD.md:702-711's fourth precaution applies: the corpus already holds the answers.
- **N18. On IEEE (BELIEVED, from memory), the statements look right.** Two points would sharpen Q2:
  - Section 5.1 of the standard requires clause 5's operations for every supported arithmetic format, so "which of clause 5's required operations" sits awkwardly beside a fixed "compliant".
  - binary16 can be supported either as an arithmetic format or as an interchange format only.

  The edition also changes the required set: 2008 has minNum and maxNum in 5.3.1, and 2019 moves min/max to 9.6, as recommended operations. A question is missing too: where the agents run, which decides AGENTS.md before the freeze.

---

## The numbered items

**1. Figures and citations. Confirmed, except B1, B10, B8 and B9.**
Commands:
- `scripts/tok.py`: `tiktoken` `o200k_base` over `git show` blobs and unpacked zips.
- `grep -c -F` for each phrase, on cft-fp256 docs/VALIDATION.md and the method files.
- `scripts/terms.py`: word-bounded, case-insensitive counts per archive.
- `git grep -c -i cft-fp256 8afeede`, `ls docs/reviews/*`, `du -sh .git`.
- `sed -n` on every cited `file:line`.

Re-derived exactly (MEASURED):
- **Tokens:** 22,521; 11,099; 30,253; 10,418; 64,041; 8,170; 106,866; 152,142. METHOD.md's 19,866 for 78,786 bytes.
- **Phrase counts:** 2, 1, 2, 5, 1, 5, 108, 213 and 54. None hits ParcelRound's METHOD.md or templates, or HonestFramework's documents or templates.
- **Archive term counts (occurrences):**
  - round 2: fp32 53, fp64 31, fma 13, overflow 13, underflow 10, sticky 8;
  - round 3: softfloat 25, fp32 12, fp64 8;
  - round 4: binary64 82, ulp 34, binary32 22;
  - rounds 5 and 6: binary64 7, overflow 2.
- **Rules:** R1 12, R2 3, R3 4, at the stated lines.
- **QRO-Crate:** 52 lines; 6 P0 rounds; 4, 4, 2, 4, 4; 12 drafts; `.git` 1.3M.
- **cft-fp256:** 33 golden-model files, 12 of them in lang/; binary16 has 0 hits in the 5 files.
- **ParcelRound:** 61 commits; ARCHIVE_SHA256 at tools/check_method.py:225-232.

**2. Quotations. Confirmed verbatim, except B7, B10 and N2.**
Checked with `sed -n` at each cited place, all READ and all verbatim:
- ParcelRound METHOD.md:1187-1188, 618-619, 1236-1239 and 542-544;
- survey:115 (B3, Logan's words, recorded at "ODE lead:1057");
- cft VALIDATION.md:20101 (2026-10-12), 19293 (2026-10-13), 22537 (2026-10-20), 21733, 22676, 22681, 15854, 17961 and 22742;
- QRO-Crate VALIDATION.md:1167-1171 (2026-10-15), 922-924 (2026-10-14), 2473-2474 (2026-10-16), and CLAUDE.md:104 and :105;
- HonestFramework METHOD.md:333-334;
- EMBEDDED.md:38; HonestFramework CASE-STUDY.md:21; CASE-STUDY-4.md:58;
- round 6's _verifier.md:70-71.

Who said each, and when, is as the draft states. The leads' rules are indeed the leads': "Briefs now carry", "The briefs since say" and "later Haiku briefs say". Logan's 2026-10-20 words confirm he did not start the time boxes: "I noticed you started giving the agents them".

**3. K1 leaks. Defect: A1, A3, A4, B4.**
Commands:
- `grep -rnoI 'https?://'` over the method texts and the unpacked round 5 and 6 members;
- a cft-link-shape grep;
- email and home-path greps;
- `git grep` and `git log --all -p` on QRO-Crate (0 cft URLs in its history);
- `scripts/terms.py` over the excerpt.

Clean, as far as I checked:
- The method texts hold no cft URL after R1 (MEASURED).
- Case studies 2 to 4 have no code blocks.
- HonestFramework's texts mention cft-fp256 only at a high level.
- The excerpt has no URLs.

**4. K2 and the rules. Defect: A2. Note: N9, N10.**
- **Byte for byte.** R1 to R3, applied by regex, change only the seven files that hold the declared links: 50 diff lines, and nothing else (MEASURED).
- **Links outside the plan's count.** The 3 dangling relative links in A2. The 15 cft links inside the zips in A1. Bare `github.com/loganw234/...` mentions in CASE-STUDY-4, -5 and -6, which are not cft and not links.
- **check_claims.py after R2.** It passes only with HonestFramework's LICENSE present (MEASURED, A2).
- **check_method.py.** Excluding it is justified.
  - `archive_pins` refuses a missing pinned archive: "a pinned record is gone" (tools/check_method.py:719-735, READ).
  - In a copy of the clone it gives rc 1, "anchors FAIL ... ADOPTION.md names commit 868f95e, which is not in HEAD's history", and "FAIL: 9 of 10 checks hold" (MEASURED).
  - The exclusion leaves README.md:29's link dangling.

**5. Standing rules. Defect: B7, B8, B10. Note: N1, N2, N3.**
- **Dates.** Rules 1 to 7 are dated correctly against their sources.
- **The leads' rules.** All three are the leads' own, not Logan's.
- **Rules 1 and 2.** Both are carried in ParcelRound METHOD.md:1388-1395.

**6. GLOSSARY. Note: N7, and defect B7, about how (b) feeds the send-back rule.**
Commands: `grep -o '(MEASURED|READ|COMPUTED|BELIEVED[^)]*)'`, sampled every 25th to 40th hit, in cft-fp256's and QRO-Crate's docs.

**7. The workflow against the methods. Confirmed, except B7. Note: N8, N14.**
- **Section citations.** Every phase's section is right: ParcelRound sections 1, 2, 4, 7, 3 to 8, and 4 and 7; HonestFramework sections 10, 1 to 3, and 9.
- **Templates.** checklists.md's "Before dispatch", "At each merge" and "At the end of the round" exist (lines 15, 167, 222).
- **Rules carried right:**
  - P0 goes past a verifier before dispatch;
  - the plan goes past a verifier before Logan sees it;
  - an integration verifier re-checks the merges.

**8. Metrics. Defect: B5. Note: N11, N12.**
The "Minutes per pass" and output-token method lines are right at VALIDATION.md:22742 (READ). HonestFramework's runner writes a JSONL record (templates/gate-runner.sh:22 and :143, READ).

**9. Planted faults. Defect: A5. Note: N16, N17.**
- **Key format.** Round 6's key format is as stated, checked in keys/key-db08fdc.json (READ).
- **The phrase.** Its attribution to round 6's verifier brief is right: briefs/_verifier.md:38-42 has it. It is not the only source (N16).

**10. Dates, caps and the calendar. Confirmed.**
- **Dates (MEASURED, `date -d`).** 2026-10-23 is a Friday. 10-26 plus 9 days is 11-04, a Wednesday. 10-25 is a Sunday.
- **Calendar.** Days 3-4 and 4-8 overlap on day 4.
- **Study cap.** Three drafts and two re-checks fit inside day 2. QRO-0 took twelve drafts.

Both of those last points are the lead's proposals.

**11. Section 10's questions. Defect, by what they leave out: A1, A3, B4. Note: N4, N5, N18.**
- **A1** means Q2 or Q3 has to cover the round 5 and 6 archives, and Q4 has to disclose QRO-Crate's derived code (A3).
- **Already answered?** No question is fully answered by the sources. Q4's "whether" is partly answered by the request: "Ill also likely give the meta agents access to QRO-Crate".

**12. IEEE 754. No wrong statement found (BELIEVED, from memory). Note: N18.**

**13. Anything else: A6, B2, B3, B6, and N6, N10, N13, N15.**

---

## What I did not do

- I did not run check_method.py with full history, so "passes with full history" stays BELIEVED.
- I did not open loganw.dev or any URL.
- I did not read whole files of the following:
  - cft-fp256's docs beyond the cited ranges, the 2026-09-25 to 09-30 entries and EMBEDDED.md;
  - QRO-Crate beyond its code lines that name cft-fp256 and its record's headings;
  - round 2 to 4 members beyond the term counts.
- I did not check the IEEE statements against the text of the standard.
- I did not check the privacy shapes against QRO-Crate's allowed-domain list. "Refused" for <address> is BELIEVED.
- I did not test whether the Read tool's count includes its line-number prefixes.
- I did not read docs/CERTIFICATES.md in cft-fp256 to see how far QRO-Crate's spelling follows it.

Background processes: none started. Final sha256 of the draft: `91a3972cebadd2f066092e887f5f8e4a7074d92fd4bcdd97650ea909658bca87`, which matches.
