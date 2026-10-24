# v1's verifier, the second re-check: the brief

Sent to v1's verifier, which keeps its context from its first pass and its re-check, at 2026-10-23 23:42 +0000 or
a minute after. Its first brief, [verifier-brief.md](verifier-brief.md), and its re-check's,
[recheck-brief.md](recheck-brief.md), still hold, but for what this one changes.

---

A second scoped re-check of v1: the second fix round's answers to your re-check's 5 (b) and 7 notes are ready in the
same tree.

**The tree.** Its digest, taken as before (every file but those under docs/reviews/v1/), is
`189820e695cdefd034080f8ef669006e92d042b394e69d5c28ed0061c92e75fa`. Check it before you start and when you finish.
The zip at this dispatch is `dist/softfloat-bootstrap-kit-v1.zip`, sha256
`1fb81970a679dcdb506cb43c5748254e56e4595a39a6c8ef62d5842a2eb8563c`.

**What changed, and where it says so.**
- docs/KIT-0.md, section 11, "v1's verifier, its re-check": each of your re-check's findings, and what the second
  fix round did with it.
- Section 12, items 42 to 46; section 13, items 14, 20 and 22, restated.
- docs/VALIDATION.md, restated in place, every earlier figure beside its new one.
- Your re-check's report, as kept: docs/reviews/v1/verifier-v1-recheck.md.

**What to check.**
1. Each of your re-check's findings: closed, not closed, or closed by a fix that is itself wrong. Pick your own
   faults again: in particular, look for another route by which a copy could hold a planted file's unplanted text,
   or another way `check` could pass a copy that is not what its key says.
2. The two new builder stages, builder-refusals and builder-mutants, and the refusal-mutants stage's new reach:
   can any of them pass where it should fail? Is CLAUDE.md item 7's statement of their reach now true?
3. Any regression the second fix round made, anywhere in the kit or the builder.
4. Section 13, item 20, as restated: whether it now says what is true.

**Ground rules and report:** as in your first two briefs. The loose cap still does not apply: this is the second
send-back of v1. If this pass is NOT READY, the next is the third, and the lead will consider the cap then, by
OWNER.md rule 6, if Logan applies it. A time box of about an hour.
