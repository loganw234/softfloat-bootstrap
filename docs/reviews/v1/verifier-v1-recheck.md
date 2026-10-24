<!-- v1's verifier's scoped re-check, extracted by script from the last hand-back call in its transcript,
     unedited but for its absolute paths, written <scratch>/ (0) and <repos>/ (0) here, and its dotted
     capital I, written <U+0130> (0 times). -->

NOT READY: 0 (a), 5 (b), 7 notes.

Most of the fix round holds against faults I picked myself, and every figure the record gives re-measures. But five sentences still claim more than is true. The heaviest is that the fix for (b)1 claims more than it does: a planted copy can still hold the unplanted text, through the base's history.

Paths are relative to `<repos>/`; "kit:" means `softfloat-bootstrap/dist/softfloat-bootstrap-kit/`. No name of Logan's is written below; hashed names are given by their prefix only.

## My first pass's findings, closed or not

- **(b)1, unplanted blobs in the copy: closed for its case, but the fix claims more (new (b)1 below).** My first-pass case now copies clean: 0 unreachable objects, no unplanted text, and `check` refuses a stray object (MEASURED). All 12 `copy_problems` conditions, taken out one at a time, fail the self-test (MEASURED).
- **(b)2, refusals never watched to fail: closed.** My own fault made `address_kept` keep every address; `--control` then gives 77 of 80, the identity plant among the three missed (MEASURED).
- **(b)3, an unreadable bundle passes: closed.** A thin bundle lacking its first commit is refused by checks 2 and 4 (MEASURED).
- **(b)4, the prefilter's fold: closed.** I scanned every Unicode code point. `re`'s case-insensitive matching takes exactly four for ASCII letters, and the new FOLD maps each one. With the old fold, 15 of the 96 spellings are missed, as the record says (MEASURED).
- **(b)5, machine names: closed as restated.** README's "nothing here spells them" holds: no file git would commit here holds the desktop's name, the email domain or a fragment, by a hash scan of every token (MEASURED). Section 13 item 20 is assessed below.
- **(b)6, line counts: closed.** All 133 carried texts and archive members keep their source's line count, and OWNER.md's five citations land on the same text (MEASURED). The build's new refusal has no control, though: see new (b)2.
- **(b)7, self-tests: closed in substance.** My twelve first-pass mutants, re-aimed at the new code, each fail their tool's self-test (MEASURED). The stage's reach is new (b)2.
- **(b)8, bundle comparison: closed.** A bundle with the same heads plus one unreachable object compares unequal (MEASURED).
- **(b)9, URL spellings: closed.** git+ssh, upper case, www, a .wiki remote, a percent-encoded hyphen and a double-encoded redirect are all refused (MEASURED). The restated claim names only the forms its list holds.
- **(b)10, ROLES.md's attribution: not closed.** See new (b)3.
- **(b)11 and (b)12: closed.**
- **N1, fragments: closed in part.** R5's 7 replacements are where they belong: round 4 verifier-P0.md:376, :382 and :385, verifier-P3.md:178, and round 5 P2.md:127. What remains is note 1 below.
- **N2, "None of its code": restated wrongly.** See new (b)4.
- **N3, operation names: closed.** The only new cut is line 23392. Samples re-checked: 312 lines verbatim and 39 cuts. But 4b's restated sentence is new (b)5.
- **N4, must-fail: closed.** It now fails with no built kit and with a gate that crashes on the planted copy (MEASURED).
- **N5 to N10, N13 and N15: closed.** The quick budget runs in 18 s; the full run takes 3 min 8 s. No live link to the site remains anywhere in the kit (MEASURED).
- **N11, a stray `__pycache__`: closed in part.** See note 2.
- **N12, read-only files on Windows:** implemented; whether it works there is BELIEVED, not run.
- **N14, typed headings: closed in part.** See note 3.

## New findings

**(b)1. A planted copy still holds the unplanted text whenever the base's history already holds it.**
- **What:** the copy holds the base's history by design. So a planted file whose real_tip text the base already holds puts that text in the copy, reachable from HEAD. Two cases:
  - B: the tip reverts a file to an older version.
  - C: the tip renames a file unchanged.
- In both, `make` prints no note (it notes only a file left untouched at the same path, which I confirmed) and `check` passes. The twin refusal rejects the same situation, "so the copy would hold the unplanted text", but only for another file at real_tip.
- **False sentences:** kit:tools/plant.py:7-10 ("not the unplanted text of a planted file"), plant.py:15-19 ("so … none of a planted file's unplanted text"), and KIT-0 §11's (b)1 row ("leaves each planted file's original blob out").
- **Evidence, MEASURED:** in cases B and C a blob holding "5 of 38" is in the copy, against the copy's "5 of 28", and `check` gives rc 0.
- **Reproduce:** `<scratch>/verifier-v1/re/plant/` (repositories B and C, lead/dB.json and dC.json).

**(b)2. "A new refusal … without its own case fails the run" is false.**
- **What:** refusal-mutants finds only `raise Refused(` and `die "` sites. plant.py's 12 `copy_problems` refusals all feed one raise, so the stage never takes them out alone.
- **Evidence, MEASURED:** I added an untested refusal (ORIG_HEAD naming another commit) to a copy's plant.py. The stage still reported "55 refusals in 3 tools, each … failed", exit 0.
- **Also:** the build's new line-count refusal has no control. With it removed and R1's old line-joining marker restored, all 15 stages pass, and METHOD.md is back to 1,436 lines (MEASURED).
- **Where:** softfloat-bootstrap/CLAUDE.md item 7; the refusal-mutants stage description; docs/VALIDATION.md:73-75 ("Every refusal of the three tools, 55 in all").
- **Reproduce:** `<scratch>/verifier-v1/re/builder/` (it still holds the guard-removed build).

**(b)3. ROLES.md:9 says "Each line cites its source".** About eighteen items cite nothing: owner lines 14-17; parcel lines 59, 62, 66, 70-72 and 75; verifier lines 83-87, 92 and 93 (READ).

**(b)4. CLEAN-ROOM.md:52-53 says "None of its code, but for two statements … (sample 3a)".** At least two more fragments of cft-fp256's code are quoted (READ):
- kit:examples/cases/09-flakes.md:21, an expression of its test harness: `ts == sorted(ts)`;
- 18-notes-not-taken.md:17, a command its verify/run.sh runs.

In my first pass I classed the bare sentence a note, by the clean room's purpose. The fix makes it an inventory a reader would rely on, and the inventory is incomplete.

**(b)5. 4b's restated "What it shows" (04-known-limits.md:22) calls line 23392 "the entry's last line".** It is the last line of the entry's known-limits section; the entry runs on through 23397, with "Sent back once." and "Records." (READ).

## Notes
1. Round 4's verifier-P0.md:391 still gives his address's local part, which is his user name, as a pattern. §11's N1 row does not say it is kept.
2. A `tools/__pycache__` also trips check 4, with 5 findings: NEEDLES literals and the self-test's address, each followed by marshal type bytes. START-HERE's advice to delete the directory is right (MEASURED).
3. ledger.sh lets through a heading written with up to three leading spaces, with a tab after `##`, or after a lone CR, and a headline holding a lone CR (MEASURED).
4. `check` passes a copy whose ORIG_HEAD, or a deleted branch's reflog, names the tip. `make` writes neither (MEASURED).
5. ROLES.md:6, "He settles them live, at kickoff, once he has seen what the harness offers", is the kit's reading, unmarked. His "determine that live" refers to the TUI.
6. CLEAN-ROOM's list of GLOSSARY's quotations ("the evidence tags' sentence") leaves out GLOSSARY's other record examples (:18913, :20929, :17961, :15854 and others).
7. Check 2 passes a renamed fork and the submodule's view on GitHub. Its stated exceptions name only a mirror on another host. The kit holds neither (MEASURED).

## Section 13, items 18 and 20
- **Item 18, K5's wording:** not major. It relaxes an approved must-hold to match Logan's records, and every figure I scanned now carries its tag. Since it rewords one of the plan's K's, it belongs before Logan, as §13 puts it.
- **Item 20, the two machine names:** not major by the lead's test. But it departs from approved text: §8's "his machines' names, held by sha256" and K1.
  - Its reason, "cannot be rewritten", holds only for the bundle's one occurrence.
  - The other 20 occurrences are in samples the builder writes, in CASE-STUDY-3.md and in round 4's members, where a rule like R5 could reach them. So keeping them is a choice, which is right to put to Logan.

## What I ran
- **The front door:** a full run in the builder, state in my scratch (15 of 15, 3 min 8 s), and the quick budget. After each, dist/ came out byte for byte: zip 20958f28…, MANIFEST.txt 892c306c….
- **Diffs:** of the 23 changed files against my first-pass copy.
- **plant.py:** cases A to D; three stray-route tests of `check`; 12 copy_problems mutants; 12 re-aimed mutants; refusal-mutants with an untested refusal.
- **The gate:** an exhaustive fold scan; the old fold; the address_kept fault; a thin bundle; 9 URL spellings; the .pyc test.
- **The builder:** bundle-compare with an extra object; must-fail with no kit and with a crash; all 15 stages without the line-count guard.
- **Python versions:** under 3.11, the build's check, the gate, its controls and the three self-tests pass. All six files parse as Python 3.7.
- **Text checks:** line counts of the carried texts and members; the sample checker and its cuts; each new quotation at its source; R5's replacements; the two fragment hashes; the scans for names, live links and code fragments.

## What I did not check
- tiktoken's 3.98 and 3.82 (tiktoken is not installed here).
- Windows, and Python 3.9 and 3.10.
- docs/reviews/v1/verifier-v1.md's fidelity to my first report.
- A re-grade of the cold read.
- KIT-0 sections other than 11 to 13.

## The tree's digest
- Before: db3f365b5d9dc823c9f2c06b310dcdcf1c300e1646f7c547ff53e0e683e46cbc
- After: db3f365b5d9dc823c9f2c06b310dcdcf1c300e1646f7c547ff53e0e683e46cbc

## What this brief got wrong
Nothing I found.
