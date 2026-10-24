# v1's verifier, the sixth re-check: the brief

Sent to v1's verifier, which keeps its context from its first pass and its five re-checks, at 2026-10-24 02:40 +0000 or a
minute after. Its earlier briefs, [verifier-brief.md](verifier-brief.md) to [recheck5-brief.md](recheck5-brief.md),
still hold, but for what this one changes.

---

A sixth scoped re-check of v1: the sixth fix round's answer to your fifth re-check's one (b) is ready in the same tree.

**The loose cap holds for this pass too,** as your fifth brief stated it: only a defect in what the code does blocks,
and everything else is a note the lead takes in before the commit. Logan's word was for "this pass", the fifth; the
lead holds it for this one, which closes the fifth's one finding, and says why in docs/VALIDATION.md ("The loose
cap"). That reading is the lead's, for Logan to overrule.

**The tree.** Its digest, taken as before, is
`6e456ad6017f88b7de013c35a4542c8bf730a58f0b2b24ac3ab4feb4435f17a1`. It covers every file but those under
docs/reviews/v1/ and those .gitignore leaves out (dist/, .gate-state/ and `__pycache__/`). Check it before you start
and when you finish. The zip at this dispatch is `dist/softfloat-bootstrap-kit-v1.zip`, sha256
`0c36e7df969ed42967004bc7be9765307ea17a7684996225ba6f83aee0ced364`.

**What changed, and where it says so.**
- build/build_kit.py, `manifest_equal_but_bundle`: it compares the manifests' bytes.
- tests/controls.py: builder-refusals' two new trials, CR LF line ends and no last line end; bundle-compare's new
  control, a bundle repacked into other bytes and named so by its manifest, which must pass `--check`.
- docs/KIT-0.md, section 11, "v1's verifier, its fifth re-check", and section 12, item 61.
- docs/VALIDATION.md, restated in place.
- Your fifth re-check's report, as kept: docs/reviews/v1/verifier-v1-recheck5.md.

**What to check.**
1. Your (b)1: closed, not closed, or closed by a fix that is itself wrong. Can `--check` still pass a dist/ that
   differs from what the sources make, by its manifest or its bundle? Does it now refuse one that is the same?
2. Any regression the sixth fix round made.

**Ground rules and report:** as in your first six briefs. A time box of about forty minutes.
