# v1's verifier, the third re-check: the brief

Sent to v1's verifier, which keeps its context from its first pass and its two re-checks, at 2026-10-24 00:54 +0000
or a minute after. Its earlier briefs, [verifier-brief.md](verifier-brief.md), [recheck-brief.md](recheck-brief.md)
and [recheck2-brief.md](recheck2-brief.md), still hold, but for what this one changes.

---

A third scoped re-check of v1: the third fix round's answers to your second re-check's 2 (b) and 8 notes are ready in
the same tree.

**The tree.** Its digest, taken as before, is
`938eecf38ff85a696cbc6dcc1a996dfc2c71a270e8e08512890af3a0bca5cccb`. It covers every file but those under
docs/reviews/v1/ and those .gitignore leaves out (dist/, .gate-state/ and `__pycache__/`), which your second
re-check's brief did not say (your report's last section). Check it before you start and when you finish. The zip at
this dispatch is `dist/softfloat-bootstrap-kit-v1.zip`, sha256
`b4e5471884bb54ccefe27cadee03bd7ae016c788af9ae7633cc16eceee0fa113`.

**What changed, and where it says so.**
- docs/KIT-0.md, section 11, "v1's verifier, its second re-check": each of your findings, and what the third fix
  round did with it. Section 12, items 47 to 51. Section 13: items 7, 14, 15 and 22 restated, and 23 and 24 new.
- docs/VALIDATION.md, restated in place, every earlier figure beside its new one.
- Your second re-check's report, as kept: docs/reviews/v1/verifier-v1-recheck2.md, with its header restated.

**What to check.**
1. Each of your findings: closed, not closed, or closed by a fix that is itself wrong. For (b)1, the test is whether
   `plant.py check`'s docstring and the line it prints now say what it reads, and no more. Pick your own routes
   again, with `--dispatch` and without it.
2. The new conditions of `check` and `--dispatch`, `ledger.sh`'s heading rule, and the builder's new trial and
   baselines. Can any of them refuse what it should accept, under a git, an awk or a platform you can reason about?
   Can any pass what it should refuse?
3. Any regression the third fix round made, anywhere in the kit or the builder.

**Ground rules and report:** as in your first three briefs. The loose cap does not apply. This is v1's fourth pass,
and the cap's condition is met (docs/VALIDATION.md, "The loose cap, not applied"). But which standing rules apply is
Logan's to decide, and he has not applied it. A time box of about an hour.
