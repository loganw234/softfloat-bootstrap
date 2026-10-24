<!-- The verifier's scoped re-check of KIT-0 draft 2 (sha256 2f661b28...), extracted by script from its
     transcript's final message, unedited but for one absolute path, written <repos>/ here, as round 6's
     verifier brief has a report write its paths. -->

# Verifier re-check of KIT-0 draft 2

**NOT READY: 1 (a), 4 (b), 9 notes.** Draft 2 fixes almost all of draft 1's findings. What still sends it back is new: check 4, and check 2's relative-link rule, now read inside the archives and the QRO-Crate snapshot, but the rules that say what passes were never re-derived against those contents. One of the (b)s is my own error from draft 1, carried into draft 2 (B13).

I checked draft 2's sha256 at 20:28 and again at 20:41 UTC: `2f661b283140943f99befe5ae8f5913b330941093cc23c3b8175c5e265e4a403` both times (MEASURED). All four sources were clean before and after: `git status --porcelain` printed 0 lines in each. I wrote only to my scratch directory, `verifier-KIT0/` (`kitsim4`, `repack/`, `qrosnap/`, `qro-snap.tar`, and scripts `priv.py`, `repack.py`, `rules2.py`). I did not read `docs/reviews/KIT-0/draft1-verifier.md`, because I still had my own report, and I wrote nothing under `<repos>/softfloat-bootstrap`. Below I name the lines that hold Logan's address and personal domains, never the values.

## The findings

### (a)

**A7. Checks 2 and 4 now read inside the archives and the snapshot, but what they let pass was not re-derived against those contents.** As specified, the gate fails on the planned kit in three places. All counts are MEASURED, using QRO-Crate's own `ALTERNATIVES` patterns, imported from a scratch copy.
- **Check 4, the addresses kept.** Section 4.1 keeps three reserved domains by name: example.com, example.invalid and evil.example. The QRO-Crate snapshot holds 5 addresses at example.org (tests/tools/test_tools.py:73, :120 and :307; tests/docs/test_stage_registry.py:318; docs/reviews/P0/round6.md:134) and 1 at x.example.com (tools/check_privacy.py:90). None of those is on the list.
- **Check 4, the user@host rule.** The snapshot's IRI test strings have the user@host shape, and only the HonestFramework template placeholder is exempt: `"a@b/c"` at tests/format/test_sweep.py:172, and `"a@b"` and `"#a/b?c:d@e"` at tests/format/test_spelling.py:162. Nothing says what "names a machine" means.
- **Check 2, relative links.** Inside the members there are 13 relative links, written relative to ParcelRound's root: 1 in round 5, and 12 in round 6 (for example P2.md:98 and :207, both to `archive/round6-practice-survey.md`). Read relative to the member, none resolves. The plan does not say which base check 2 uses inside an archive.

The gate would catch this at build step 6. The fix:
- keep reserved names as a class (RFC 2606/6761);
- define the user@host rule, or exempt by path;
- say where links inside an archive are resolved from;
- re-scan the snapshot.

### (b)

**B11. "The zip carries cft-fp256's text only in these places, and check 3 reads each of them" (section 3, item 1) is false.** cft-fp256's text also appears in places check 3 does not read (READ):
- QRO-Crate docs/studies/QRO-0.md:292-295 quotes cft-fp256's CERT-V2.md: "No PROV-O, SLSA or RO-Crate serialization is part of version 2..."
- Round 5's briefs/P1.md:77-78 quotes cft-fp256's README.md:319: "CI's green tick does not cover synthesis, timing or silicon".
- ParcelRound's own texts quote cft-fp256's record throughout.

None of it is arithmetic. N6's disposition ("lists every place") falls with this sentence.

**B12. The 61 home-path lines for round 4 should be 60.** By check 4's own shapes there are 60. The 61st, verifier-P3.md:7, is `/c/Users/.../sab`, which has no user segment for R5 to replace (MEASURED).

**B13. Atlas-film is the wrong example of the submodule view of cft-fp256 (section 3, item 3).** The kit's round 4 ledger shows:
- atlas-film is "pure numpy" (briefs/P2.md:3), and its "Pinned mode itself must not require libcft" (:101);
- the submodule is Quantum-Film's `vendor/cft-fp256`: "submodule 7d7285d" (round 4 lead.md:9-11; briefs/P1.md:66; CASE-STUDY-4.md:55).

This came from me. My draft-1 B3 inferred from "onto cft-fp256's pinned arithmetic" that atlas-film carries cft-fp256's code, and that does not follow. Draft 1's original pairing, cft-rebound and "the libcft submodule in round 4's project", was right.

**B14. "There is one plant for each shape the checks refuse" (section 8) is false as listed.**
- No plant covers check 4's key and token shapes. QRO-Crate names about twenty of them (tools/check_privacy.py:94-115).
- A single "IP address" plant covers three private ranges.

### Notes

- **N19. One leak path remains in the planted-fault protocol (A5's residual).** Keys and grading are now held to the round's end, but METRICS has every finding "confirmed or rejected by the lead in the ledger". A mid-round ruling on a finding that touches only the copy describes a plant. That is obs 6's other path: "The lead's entries that graded wave 1 described each plant in prose" (CASE-STUDY-6.md:180-182). Two fixes are needed:
  - hold those rulings to the round's end;
  - put each copy out of reach once its verifier reports. Otherwise the copy and the merged real tip, diffed, give back the key early.
- **N20. "every other byte stays as it was" holds for the members, not for the zip.** I repacked all four archives with Python's zipfile (MEASURED):
  - order and timestamps were kept, and the deflated bytes of every unchanged member were identical;
  - the original zips are deflate level 6, and that level re-compresses all 102 deflated members to their original bytes;
  - the zip files themselves differ, because CRCs, sizes and offsets change.

  It should say "every unchanged member's bytes". R4 re-derives at 15 (3 in round 5, 12 in round 6). After R4 and R5, no cft URL and no home-path line is left.
- **N21. Two carried texts become false about the kit's own copies.** CASE-STUDY-6.md:383-388 says "each checked byte for byte ... The gate pins the archive's SHA-256", and CASE-STUDY-4.md:126 says "checked byte for byte". Add both to START-HERE's limits.
- **N22. Round 4's ledgers carry cft-fp256 tree paths and API facts, though not code.** Among them:
  - `bindings/python/cftmpfr` and `host/cft.dll`;
  - ABI 0.14;
  - "libcft's correctly rounded functions";
  - "cos 0.211 ms and exp 0.110 ms per element" (briefs/P2.md:22-25, :46, :71 and :99).

  The draft's scan terms did not look for these. Name them in the index.
- **N23. Under CLEAN-ROOM's own reading, Logan's site links may count as cft-fp256.** CLEAN-ROOM says pages of Logan's site "that show cft-fp256 count as cft-fp256", yet the kit keeps live links to that site. Round 5's briefs/P1.md:70-74 say the Home page's Verify checks read cft-fp256 at a pin (READ; I did not open the site). If they do, K1 conflicts with the kept links. Ask Logan, or treat those links like R4's.
- **N24. Some counts in section 4.1 are deferred or stale.**
  - R5's occurrence counts are left to the build. The plan of record declares only line counts.
  - Section 4.1's archive token counts are from before the rewrite.
- **N25. Apache-2.0 asks for the licence text and the NOTICE's attributions (§4(a), §4(d)).** The samples' header names cft-fp256's licence, but the kit omits both. As copyright holder, Logan is not bound by his own licence (BELIEVED), so say it is his choice, as the plan does for MIT.
- **N26. A list in section 4.3 groups a file wrongly.** tools/check_docs.py:21 and :34 appear under "The code follows cft-fp256's documented rules". Those lines name cft-fp256 as a foreign repository; they do not follow its rules.
- **N27. A general privacy check is still needed for the snapshot-plus-history form.** It is free of Logan's address as specified (scope 1, A1); one consequence of choosing it is that check 4 must still pass the snapshot's own contents, which A7 shows it does not.

## Scope item 1: does each fix hold?

All MEASURED or READ, using `scripts/{rules2,repack,priv,links}.py`, tar and `git log` in copies, and `sed -n` at each cited line.

- **A1: holds**, apart from A7.
  - **R4.** Its 15 lines re-derive exactly. Round 4 has no cft-fp256 URL and one `cft_convert (` call (P1.md:19).
  - **R5, home paths.** Line counts are 60 (B12), 14, 42 and 0.
  - **R5, addresses.** Round 4 has 4 at Logan's own domain: the same hash as ParcelRound's `KNOWN_PRIVACY` (tools/check_method.py:365). Round 5 has 9 at the site's domain. All the others are kept ones: noreply@anthropic.com, amazon.com, and the reserved names.
  - **The IP rule.** It passes what it says:
    - 5.15.153.1 is "kernel 5.15.153.1" (round 4 verifier-P0.md:361);
    - 127.0.0.1;
    - 15.197.148.33 and 3.33.130.190 (round 5 verifier-P0.md:31), and 185.199.108.153 (round 5 briefs/verifier-seam.md:233).

    The kit holds no private-range address.
  - **QRO-Crate's commits.** All six have the same author and committer address, at that domain (compared by hash).
  - **Messages.** They hold only noreply@anthropic.com, with no home path and no cft-fp256 URL.
  - **The snapshot.** `.gitattributes` has no `export-subst`. The `git archive` tar (265 files) holds 0 addresses at Logan's domain, and its pax comment is only the commit id.
- **A2: holds.** In draft 2's layout:
  - with both LICENSE files and round 4's archives present, the rules count R1 12, R2 3 and R3 3;
  - 98 relative links, 0 unresolved;
  - `check_claims.py` gives rc 0, "39 links resolve".
- **A3: holds.** It is disclosed, and put to Logan as Q5.
- **A4: holds.** The limit is stated by what the list concedes, and four of the lines it cites are the ones I found.
- **A5: holds, apart from N19.** It now matches CS6#3, CS6#4 and CS5#8. The quotations at lead.md:460, :488, :489 and :560, CASE-STUDY-6.md:171 and :346-348, and ADOPTION.md:143, :151 and :152 are verbatim.
- **A6: holds.**
- **B1, B2, B4 to B10: hold.** B3 is superseded by B13.

## Scope item 2: new text

All verbatim at their lines (READ):
- EMBEDDED.md:9-10, 251-253, 450-453, 602-603, 673-677 and 685;
- rule 1 at METHOD.md:1125-1127;
- rule 4 at VALIDATION.md:19293;
- rule 8 at :16510, dated 2026-09-30 by its entry's heading at :16505;
- rule 9 at :15443, with :15797, :16664, :16840 and :17030;
- the glossary at :18913, :20929, :21941, :18110, :18253, :15854, :17961, :15903 and :22587;
- NOTICE ("Copyright 2026 Logan W.", with one URL into cft-fp256);
- CASE-STUDY-4.md:118.

The archive members' extensions are .md, .py, .out and .json, plus one directory entry. The calendar's weekdays are right. Round 4 holds the three briefs.

## Scope item 3: the dispositions of my notes

They are true to draft 2, with three exceptions:
- **N6** fails with B11.
- **N15** is overstated: B14.
- **N17's** pool of shown plant shapes grows now that round 4's `verifier-P0-work/plant_develop.py` and QRO-Crate's `controls/` are in the kit.

## What I did not do

- I did not open the live site or any URL.
- I did not test check 4's real implementation, which does not exist yet; I used QRO-Crate's patterns.
- I did not check atlas-film's repository beyond the ledger.
- I did not read the new survey-cases.md, nor cft-fp256's docs beyond the lines cited.
- I started no background process.
