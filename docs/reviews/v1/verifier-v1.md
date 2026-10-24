<!-- v1's verifier's report, extracted by script from the hand-back call that ends its transcript, unedited
     but for its dotted capital I, written <U+0130> here (6 times), because its planted examples hold that letter
     in the path and key shapes the builder's own privacy stage refuses. -->

NOT READY: 0 (a), 12 (b), 15 notes.

The serious ones are the first four. **plant.py's copies give the plants away.** **Two of check 4's refusals are never watched to fail.** **The gate passes a kit whose bundle it cannot read.** **Its prefilter skips eight shapes on a dotted capital I.** The rest are sentences that claim more than is true.

The main things hold, all MEASURED:
- All 13 stages pass, and the build is deterministic (a copy rebuilt from an empty dist/ makes zip 59d3a1d9…).
- Every rule count matches its declaration, and every archive member keeps its name, order, attributes and (if unchanged) its compressed bytes.
- All 313 quoted sample lines are verbatim.
- The plan's and record's figures re-measure true, and the shipped kit holds no URL naming cft.

Paths are relative to `<repos>/`. "kit:" means `softfloat-bootstrap/dist/softfloat-bootstrap-kit/`. No name of Logan's is written below: names are described, or given by their hash prefix in check_kit.py.

## Findings, heaviest first

**(b) 1. plant.py's copy holds the unplanted text of every planted file, and `check` passes it.**
- **What:** `make` fills the copy with the real_tip blobs the base lacks, excluding the *planted* blob ids. Those ids are never in the parcel's repository, so the filter removes nothing, and the original blob of each planted file is packed into the copy, unreachable from HEAD. One `git fsck --unreachable` and a diff then show every plant's file, place and original text.
- **`check` does not see it:** it reads only HEAD, refs, remotes, the parcel's commits and the tree. It passes this copy, and a copy with any stray object, as "differs from real_tip only by the plants".
- **Where:** kit:tools/plant.py:258-264 (it should exclude `entries[f][2]`).
  - The false sentences are at plant.py:4-11 and :14-17, kit:WORKFLOW.md:124-127 and :140-142, and KIT-0 §13 item 7.
- **Evidence, MEASURED:** a base, one tip commit and two plants.
  - `make` gives rc 0, and `git cat-file -e` finds both unplanted blobs in the copy.
  - `git fsck --unreachable --no-reflogs` lists them, and `git diff --no-index` prints `-…5 of 38…` / `+…5 of 28…`.
  - `check --sha256` gives rc 0, and still rc 0 with a hand-added object.
  - An alternates file is caught. make writes no FETCH_HEAD, one reflog line and a default config. The self-test never lists the copy's objects.
- **Effect:** the plants-caught figure in METRICS.md would measure this, not detection.
- **Reproduce:** `<scratch>/verifier-v1/work/plantleak/`.

**(b) 2. Two of check 4's refusals are never watched to fail.**
- **What:** `--control` gives 59 of 59 and exit 0 in each of two cases.
  - The refusal of a bundle commit identity that is neither kept nor at one of Logan's domains is removed. No plant touches identities.
  - The personal-domain match is disabled. Its plant is caught anyway, as an unkept address, so it tests nothing of its own: the x-api-key case again.
  - Eight privacy plants carry no shape name, so any finding counts for them.
- **Where:** kit:tools/check_kit.py:407 and :192 (the refusals) and :590-591 (the plant).
  - The false sentences are check_kit.py:5-7 ("plant one fault for each shape"), KIT-0 §8 ("one plant for each shape") and §13 item 4 ("caught only by its own shape's name").
- **Evidence:** MEASURED, on mutant copies with refreshed manifests.
- **Reproduce:** `python3 -I -B tools/check_kit.py --control .` in `<scratch>/verifier-v1/work/gm-identity/` and `gm-domain/`.

**(b) 3. The gate passes a kit whose bundle git cannot clone.**
- **What:** the gate scans the raw bytes plus an "(bundle unreadable …)" string, and nothing records a finding.
- **Where:** check_kit.py:247-250 and :304-308. The false sentence is :10-11, "a gate that cannot read the bundle does not pass it".
- **Evidence, MEASURED:** I replaced the bundle three ways: with text, truncated to half, and cut to its 74-byte header. With the manifest refreshed, each gave exit 0 and "VERDICT: PASS". With git absent the gate exits 2, as documented.
- **Reproduce:** `<scratch>/verifier-v1/scripts/badbundle.py`.

**(b) 4. The prefilter is not a necessary condition of eight shapes.**
- **What:** `str.lower()` turns <U+0130> (U+0130) into "i" plus U+0307. `re`'s (?i) matches <U+0130> as i, so a needle with an i followed by another letter goes unfound and the shape is skipped. FOLD covers ı and ſ only.
- **Where:** check_kit.py:150-167. The false sentences are :150-152 and :166, KIT-0 §13 item 4, and softfloat-bootstrap/CLAUDE.md item 6.
- **Evidence, MEASURED:** each of these shapes matches its own pattern while the prefilter skips it:
  - cygwin-home and ibm-service-id;
  - named:IBMQ_TOKEN, named:IBM_QUANTUM_TOKEN, named:QF_IBM_KEY and named:QISKIT_IBM_TOKEN;
  - named:authorization;
  - windows-home's "Documents and Settings" form.
- **The gate passes them:** NOTICE.md in a copy holding `Author<U+0130>zation: A…`, `/cygdr<U+0130>ve/c/users/x`, `<U+0130>am-ServiceId-…` or `C:\Documents and Sett<U+0130>ngs\x` gives exit 0 and PASS. The QISKIT form was refused only through named:token.
- **Reproduce:** `scripts/prefilter.py` and `scripts/plantgate.py`.

**(b) 5. "None of his machines' names" is false: the kit holds two of them, 21 times.**
- **What:** MACHINE_NAMES holds only the desktop's name (the comment at :55 says so). The hashes match a token only in cft-fp256.
  - The hostname of his separate Linux machine is in the kit 7 times.
  - The WSL distro's name is in it 14 times.
- **The builder's own claims fail too:**
  - The domain hashed bffdbab0… is spelled in build/rules.py (2), docs/KIT-0.md (5), KIT-0-draft1.md (1), KIT-0-draft2.md (5) and draft1-verifier.md (3).
  - docs/reviews/KIT-0/survey-cases.md:186 spells the Linux hostname.
  - privacy_findings returns [] for both, so self-privacy cannot refuse either.
- **Claims:** check_kit.py:23-25, README.md:47-48 ("nothing here spells them"), CLAUDE.md:27-29 ("the self-privacy stage refuses it"), KIT-0 §8.
- **Occurrences, MEASURED:**
  - The Linux hostname: kit:examples/cases/17-remote-runs-asserted.md:11; method/parcelround/CASE-STUDY-3.md:45; and in round4-ledger.zip, verifier-P0.md:49, verifier-P1.md:207, verifier-P2.md:224 and :380, and verifier-P3.md:237.
  - The WSL distro's name: examples/cases/03-send-backs.md:18 and :25; 07-conduct.md:12; in round 4, P2.md:29 and :37, verifier-P0.md:352, :355 and :456, and verifier-P2.md:9, :243, :397, :526 and :621; and the bundle's docs/reviews/P0/round5.md:33.
- **Mitigation, READ:** both names are already in texts Logan published.
- **Reproduce:** `scripts/scan_names.py` and `scripts/ctx.py` (names built in pieces, printed redacted).

**(b) 6. OWNER.md's five METHOD.md citations land on other text in the kit's copy.**
- **What:** R1's pattern (build/rules.py:27) eats the newline of each link whose target starts on the next line. The kit's METHOD.md has 1,436 lines to the source's 1,448.
- **Where, with the source line and where the text now sits:**
  - OWNER.md:37, lines 1125-1127 (the send-back rule), now at 1121-1123;
  - :42, lines 1236-1239, now 1227-1230;
  - :119, lines 1364-1370, now 1353-1359;
  - :101, lines 1372-1377, now 1361-1366;
  - :122, lines 1379-1386, now 1368-1375.
- **Also:** START-HERE's R1 line does not say lines join. R4 likewise shortens round 6's P2, P3 and P4 members by 1, 4 and 5 lines.
- **Evidence:** MEASURED.

**(b) 7. The self-tests do not run "each refusal".**
- **Claims:** ledger.sh:13-14, plant.py:21-22, round_metrics.py:10-11, KIT-0 §4.4.
- **Evidence, MEASURED:** twelve mutants, each in a copy of the tools; every self-test still reports 0 failed.
  - ledger.sh: no "Believed:" line; a fixed, typed stamp; urgent with an empty headline; the compose-race refusal removed.
  - plant.py: a shallow source accepted (the real tool does refuse it); check passing a copy on a branch, holding refs, or with a remote; a key inside the copy; a plant on a non-regular file.
  - round_metrics.py: pass 0; a malformed key_sha256.
- The record's one-mutant-per-tool sentence stays true.
- **Reproduce:** `scripts/mutants.py`.

**(b) 8. The rebuild stage is not "byte for byte" for the bundle.**
- **What:** `same_bundle_content` compares only `git bundle list-heads`, against "byte for byte" in the stage description and "by content" in the docstring.
- **Where:** build/build_kit.py:330-353 and :5, verify/run.sh:217.
- **Evidence, MEASURED:** in a builder copy, I cut dist/'s bundle to its 74-byte header and refreshed the manifest. `--only rebuild,kit-gate,zip,real-names,gate-refuses` then passes, and zip ships the stub.
- A full run is protected: build rewrites dist/ first, and kit-controls crashes on such a bundle. The record's "by its heads" (VALIDATION.md:44-45) is accurate.

**(b) 9. Check 2's "in any spelling" claims more than the code does.**
- **Claims:** check_kit.py:16-18, CLEAN-ROOM.md:46-48.
- **Evidence, MEASURED:** two forms in NOTICE.md each pass with exit 0. One is git's scp-like remote `github.com:<owner>/cft-fp256.git`; the other is a percent-encoded URL inside a redirect.
  - With `git@` prefixed, the scp form is refused only as an unkept address.
  - READ: CLEAN-ROOM.md:13-16 counts forks and mirrors as cft-fp256, but check 2 matches the owner's path only.
- The kit holds none of these (0, MEASURED).
- **Reproduce:** `scripts/plant2.py`.

**(b) 10. ROLES.md:9 attributes every line to ParcelRound's METHOD.md.**
- ROLES.md:71-72 ("never change any git configuration", "never delete what it did not create") are cft-fp256's leads' rules (OWNER.md:90 and :92). "git config" occurs 0 times in METHOD.md at f42242e (MEASURED).

**(b) 11. AGENTS.md:31-32 alters its quotation.**
- It quotes cft-fp256's CLAUDE.md:154-156 without "(2026-09-15, twice in one round)" and with no mark of the cut. Item 4 at :33 marks its cut with "...".
- Searching every quoted passage in the eleven layer files against its source found no other alteration (MEASURED).

**(b) 12. Two samples' "What it shows" claim more than their passages show.**
- examples/cases/01-owners-words.md:8 says the readings are "each with its evidence tagged". Only reading 6 has a tag; record lines 22546, 22550, 22552 and 22553 have none.
- examples/cases/03-send-backs.md:8 says "each (b) measured". (b3) is COMPUTED, and (b5) is a restated sentence with no measurement. The source text is build/cases.json.

## Notes
- **N1. Privacy fragments the gate does not see.** In round4-ledger.zip, quantum-film-round1-ledger/verifier-P0.md has:
  - Logan's email domain (hash 0c6e258f…), bare, at :376 and :382;
  - his address's local part, as a pattern, at :391;
  - an 8-hex string at :376, :382 and :385, which the member calls an account UUID's prefix.
  - Round 5's P2.md member spells the domain bare at :127.
  - R5 strips whole addresses only, as it says, and no stated limit covers these. Logan's word on R5: "not vital".
- **N2. "None of its code" (CLEAN-ROOM.md:41).** Sample 3a (03-send-backs.md:24) quotes two Python statements of cft-fp256's test harness through the record. There is no arithmetic. Read strictly, the sentence is false.
- **N3.** The list has rint and nextup but not roundeven. 04-known-limits.md:35 keeps "the roundeven compile".
- **N4.** `--only must-fail` with no built kit prints "ok (negative control failed, as it must)" and PASSES (MEASURED). It inverts any non-zero exit, a crash's 3 included, where HonestFramework §5 says to assert a success line. gate-refuses holds the exact verdict.
- **N5.** README.md:18 and CLAUDE.md:6 say "about 80 seconds". MEASURED: 24 s.
- **N6.** OWNER.md:68-69 cites "line 15443", but the quotation ends on 15444.
- **N7.** 20-record-skeleton.md:16 says two sections "follow whole". 20a has lines 22593 and 22600 cut, and the section runs on to 22608.
- **N8.** CLEAN-ROOM.md:17-18 says the kit carries Logan's site's address as text, but never gives it.
- **N9. Pending lessons.** WORKFLOW's protocol steps 4, 5 and 8 are CS5#8, CS6#4 and CS6#3, all pending in ADOPTION.md (:143, :151, :152). Separately, "the fix goes back to the verifier that found the problem" (WORKFLOW.md:90-91, GLOSSARY.md:49-50) is not in METHOD.md; it comes from CASE-STUDY-4's observation 7.
- **N10. Check 2's controls.** The codeload alternative is redundant, since every codeload URL holds the github.com form. §8 promises each host form planted inside a zip member, but only the github form is.
- **N11.** A `tools/__pycache__` fails the gate. The .pyc's folded constants hold the controls' samples whole: 1 manifest and 33 privacy findings (MEASURED). The documented commands write no .pyc.
- **N12.** BELIEVED: plant.py:539 and round_metrics.py:545 clean up with `rmtree(ignore_errors=True)`. Sample 7a records that this leaves read-only git objects in Windows Temp.
- **N13.** K5 is unmet. START-HERE.md:80-82, GLOSSARY.md:18-19, WORKFLOW.md:156-157 and sample 20's counts are neither held by a script nor BELIEVED. §2's "Section 8 says which check holds each" names no check for K3 or K5. The figures I could re-measure are true.
- **N14.** ledger.sh:46 writes the body and the headline as given, so either can carry a typed `## <stamp>` heading.
- **N15. §13 and "major".** §13 claims to list each change, but R1's and R4's markers differ from §4.1's wording and are not listed. On "major": I read none of §13's items as major. Finding 1 is in the code, not the design.

## My conduct slip
At 22:02:19 UTC a one-liner of mine imported the built kit's check_kit.py without -B, from inside dist/. That wrote dist/softfloat-bootstrap-kit/tools/__pycache__/check_kit.cpython-313.pyc. I found it at about 22:19 and removed the file and its directory by exact path.
- dist/'s 75 files then matched my dispatch snapshot by sha256. The zip was never touched, and the digest, which excludes dist/, is unchanged.
- All my later Python ran with -B. `verify/run.sh` in the builder (STATEROOT set to my scratch) also rewrote dist/, byte-identical (MEASURED).

## What I ran
- The front door: `verify/run.sh --list`, `--list --budget quick`, and the full run in the builder (24 s). A full run in a copy started with no dist/. Runs in that copy with a header-only bundle, and with no dist/.
- The gate and its controls on the built kit, timed. Exit codes 0, 1, 2 and 3.
- About forty planted copies: URL spellings, U+0130 forms, broken bundles, and two gate mutants, plus `--control` with FOLD emptied (2 MISSED, as the record says).
- A token scan of every file, member and bundle blob for Logan's names.
- Rule re-application against the four sources' `git show`. A member-by-member comparison of the archives (bytes, compressed bytes, headers, attributes).
- A sample checker over all 45 samples. All 20 sample files read whole, and the eleven layer files.
- A quotation search over the layer files. The cited lines in cft-fp256's, QRO-Crate's and ParcelRound's sources at their pins.
- check 4 diffed against QRO-Crate's ALTERNATIVES: identical, but for x-api-key and private-ipv4.
- A line-identity check of QRO-Crate's .py lines against cft-fp256's code: 48 generic idioms only.
- The plan's figures re-measured: the §2 table; rounds 2 and 3; rounds 5 and 6; QRO-Crate's 52, 43/9, P0 rounds and drafts; 589/228/105/0; 78,786 bytes; check_claims.py's "39 links".
- plant.py `make`, `check` and `list` (on round 6's keys). Fourteen tool mutants. The gate and the self-tests under Python 3.11.

## What I did not check
- The cold read: its papers arrived in docs/reviews/v1/ during my pass, unread.
- o200k_base token counts (no tiktoken here).
- Python 3.9, and Windows or Git Bash.
- Every member read whole: I scanned them all, but read only round 4's scripts and its privacy section.
- Every section citation in ROLES, WORKFLOW and GLOSSARY: spot-checked.
- §12's historical slips.
- The builder after its first commit.

## The tree's digest
- Before: affcf77e741c7aad3841414e9bbc90ca28577eb4666d2826cac99e9ba4b93a58
- After: affcf77e741c7aad3841414e9bbc90ca28577eb4666d2826cac99e9ba4b93a58

## What this brief got wrong
1. **Property 2 and "never write his personal domains".** By the approved plan (§3 item 3, R6), the kit carries his site's domain as text: it is PERSONAL_DOMAINS' bffdbab0…, and appears 81 times (MEASURED).
2. **"The gate holds them … MACHINE_NAMES".** It holds one machine's name, the desktop's, not "his machines' names".
3. **"Run verify/run.sh in the builder" and "edit nothing in dist/" meet:** the run rewrites dist/. Its bytes were identical here.
