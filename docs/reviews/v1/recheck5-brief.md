# v1's verifier, the fifth re-check: the brief

Sent to v1's verifier, which keeps its context from its first pass and its four re-checks, at 2026-10-24 02:21 +0000 or a
minute after. Its earlier briefs, [verifier-brief.md](verifier-brief.md) to [recheck4-brief.md](recheck4-brief.md),
still hold, but for what this one changes: the loose cap above all.

---

A fifth scoped re-check of v1: the fifth fix round's answers to your fourth re-check's 1 (a), 2 (b) and 3 notes are
ready in the same tree.

**The loose cap applies to this pass.** Logan, 2026-10-24: "Go ahead and apply rule 6 for this pass". Rule 6, as
QRO-Crate's CLAUDE.md, item 6, states it and the kit's OWNER.md quotes it: "After three NOT READY verdicts whose
reasons grow more menial, the next verifier is told that only a defect in what the code does blocks. Prose, test gaps
where the shipped code is right, and other non-code findings become notes the lead takes afterwards." So, for this
pass:
- **A finding blocks,** as (a) or (b), only when it is a defect in what the code does, in the builder, the kit's
  tools and gate, or the stages. A line one of them prints that says what is not so is such a defect.
- **Everything else is a note:** a sentence of a document or a docstring that claims more than is true, and a test
  gap where the shipped code is right. Report each as before, classed as a note. The lead takes every note in
  before the commit, and VALIDATION.md records what it did with each.

**The tree.** Its digest, taken as before, is
`b8ae910f218a9717cc6c797050cad7042caa523197385e48918f8407c8d8811f`. It covers every file but those under
docs/reviews/v1/ and those .gitignore leaves out (dist/, .gate-state/ and `__pycache__/`). Check it before you start
and when you finish. The zip at this dispatch is `dist/softfloat-bootstrap-kit-v1.zip`, sha256
`0c36e7df969ed42967004bc7be9765307ea17a7684996225ba6f83aee0ced364`.

**What changed, and where it says so.**
- docs/KIT-0.md, section 11, "v1's verifier, its fourth re-check": each of your findings, and what the fifth fix round
  did with it. Section 12, items 57 to 60. Section 13: items 14, 15 and 23 restated.
- docs/VALIDATION.md, restated in place, every earlier figure beside its new one, and Logan's word on the cap.
- Your fourth re-check's report, as kept: docs/reviews/v1/verifier-v1-recheck4.md.

**What to check.**
1. Each of your findings: closed, not closed, or closed by a fix that is itself wrong.
2. The fifth round's code: `ledger.sh`'s rule, reverted to the one that reads each line wherever it is;
   `check`'s walks, and its refusal of a directory it cannot read; git's own reason where git will not read a
   repository, in plant.py and round_metrics.py; the refusals of a `--repo` or `--copy` that is no directory;
   `make`'s fsck refusal; and `--check`'s manifest exemption, with its two new trials. Can any of them refuse what it
   should accept, or pass what it should refuse?
3. Any regression the fifth fix round made, anywhere in the kit or the builder.

**Ground rules and report:** as in your first five briefs. A time box of about an hour.
