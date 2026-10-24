# v1's verifier, the fourth re-check: the brief

Sent to v1's verifier, which keeps its context from its first pass and its three re-checks, at 2026-10-24 01:41
+0000 or a minute after. Its earlier briefs, [verifier-brief.md](verifier-brief.md), [recheck-brief.md](recheck-brief.md),
[recheck2-brief.md](recheck2-brief.md) and [recheck3-brief.md](recheck3-brief.md), still hold, but for what this one
changes.

---

A fourth scoped re-check of v1: the fourth fix round's answers to your third re-check's 1 (b) and 5 notes are ready in
the same tree.

**The tree.** Its digest, taken as before, is
`d26330ee2cc6b6c10ea89b921ba54c0bc1127914ab5711a70d9f7ed4cdabe0a3`. It covers every file but those under
docs/reviews/v1/ and those .gitignore leaves out (dist/, .gate-state/ and `__pycache__/`). Check it before you start
and when you finish.
The zip at this dispatch is `dist/softfloat-bootstrap-kit-v1.zip`, sha256
`8f578e8b15fde1720aa77e0296032dcc073413d22b1c4816a5a40d7fe5c58c55`.

**What changed, and where it says so.**
- docs/KIT-0.md, section 11, "v1's verifier, its third re-check": each of your findings, and what the fourth fix round
  did with it. Section 12, items 52 to 56; item 56 is a defect the lead found in `ledger.sh` while it worked. Section
  13: items 14, 15, 23 and 24 restated, and 25 new.
- docs/VALIDATION.md, restated in place, every earlier figure beside its new one.
- Your third re-check's report, as kept: docs/reviews/v1/verifier-v1-recheck3.md.

**What to check.**
1. Each of your findings: closed, not closed, or closed by a fix that is itself wrong. For (b)1, the test is again
   whether what `--dispatch` says it reads is what it reads, and no more.
2. The new code: `make`'s refusal of a history `git fsck` flags, the named refusal when `git status` fails, the
   shared index on the list, `ledger.sh`'s fenced blocks and here-strings, and the `--check` trial's two new
   differences. Can any of them refuse what it should accept, or pass what it should refuse?
3. Any regression the fourth fix round made, anywhere in the kit or the builder.

**Ground rules and report:** as in your first four briefs. The loose cap does not apply. This is v1's fifth pass,
and the cap's condition is met, but which standing rules apply is Logan's to decide, and he has not applied it
(docs/VALIDATION.md, "The loose cap, not applied"). A time box of about an hour.
