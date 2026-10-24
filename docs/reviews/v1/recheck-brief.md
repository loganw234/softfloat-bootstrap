# v1's verifier, the re-check: the brief

Sent to v1's verifier, which keeps its context from its first pass, at 2026-10-23 23:04 +0000 or a minute after.
The first pass's brief, [verifier-brief.md](verifier-brief.md), still holds, but for what this one changes.

---

A scoped re-check of v1: the fix round's answers to your 12 (b) and 15 notes, and to the cold reader's findings,
are ready in the same tree.

**The tree.** Its digest, taken as your brief says (every file but those under docs/reviews/v1/), is
`db3f365b5d9dc823c9f2c06b310dcdcf1c300e1646f7c547ff53e0e683e46cbc`. Check it before you start and when you finish.
Nothing in it changes until you report. The zip at this dispatch is `dist/softfloat-bootstrap-kit-v1.zip`, sha256
`20958f28bff0c32af7e0ef82dd4661ecf4889ee05970549ae01ff5f45db719b2`.

**What changed, and where it says so.**
- docs/KIT-0.md, section 11, "v1's verifier": each of your findings, and what the fix round did with it.
- Section 12, items 29 to 41: the lead's slips this round found, your brief's three errors among them.
- Section 13, items 14 to 22: what the fix round changed in the kit against the plan.
- docs/reviews/v1/cold-read-grading.md: the cold read, graded, and the lead's rulings on its findings A to M, each of
  which the fix round took in. The cold read's key is revealed, so its papers in docs/reviews/v1/ are open to you
  now.
- docs/VALIDATION.md: the record, restated in place, with your first pass's figures beside the new ones.

**What to check.**
1. Each of your findings: closed, not closed, or closed by a fix that is itself wrong. Pick your own faults to test
   each fix, rather than the lead's (ParcelRound's CASE-STUDY-4.md, observation 7, which the kit now cites).
2. The cold reader's findings that changed the kit's text: does each change say what is true?
3. Any regression the fix round made, anywhere in the kit or the builder.
4. The new stages: refusal-mutants, finding-mutants and bundle-compare, and the must-fail stage's required line. Can
   any of them pass where it should fail?
5. The new privacy pieces: `FRAGMENTS` in check_kit.py, R5's fragments in build/rules.py, and their counts.
6. Section 13's items 18 (K5's wording) and 20 (two of Logan's machines' names kept): whether either is "major",
   against "Approved if nothing major changes from the check". Item 20 is the lead's reading, for Logan to overrule.

**What your first brief got wrong, and what holds now.**
1. **Logan's personal domains.** By the plan, the kit carries his site's domain as text (R6). Name it in your report
   by its hash prefix, `bffdbab0...`, as you did. Never write his email's domain, or the two fragments, which are held
   by hash: `f194464d...`, the domain's name, and `293e24c7...`, the account id's prefix.
2. **MACHINE_NAMES** holds his desktop's name only. The kit now says so.
3. **`verify/run.sh` rewrites dist/.** That is allowed. Set STATEROOT to your scratch directory, as you did, and check
   that dist/ comes out byte for byte as it was, by its MANIFEST.txt and the zip's sha256.

**Ground rules,** as before: report only; build faults in copies under your own scratch directory; run Python that
imports a kit module with -B; never change any git configuration; read no other agent's scratch directory. The loose
cap does not apply: this is the first send-back. A time box of about 75 minutes, and the scope above.

**Your report,** as before: the first line READY or NOT READY, with counts; then each of your findings, closed or
not; then anything new, with its class, its place and its evidence; what you ran; what you did not check; the tree's
digest before and after; and last, anything this brief got wrong.
