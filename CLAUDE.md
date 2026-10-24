# Working on softfloat-bootstrap

Short, and only what is non-obvious and has already cost time. The README says what this is.

## Start here: one command answers "does it still hold?"

```
bash verify/run.sh                   # every stage, a few minutes; --list says what each proves
bash verify/run.sh --budget quick    # 5 of them, under a minute
```

Reach for it before running the builder's pieces by hand. A stage that cannot run is skipped by name; `--require-all`
makes a skip a failure.

## What bites

1. **The build reads git objects, never a working tree.** Each source is read at the commit
   [build/sources.lock](build/sources.lock) pins. An edit in a source repository reaches the kit only through a new
   pin, and a new pin re-measures every rule's count.
2. **A count that moves fails the build, by design.** [build/rules.py](build/rules.py) declares each rule's count per
   file. A new pin, or an edit to a rule, changes a count. Read what changed before you change the declared number,
   and say why in docs/VALIDATION.md.
3. **"softfloat" is on the gate's term list**, with the other arithmetic words, because check 3 reads every file the
   builder writes from cft-fp256's record (OWNER, GLOSSARY, METRICS, AGENTS and examples/cases). So the kit calls
   the work's repository "the project repository". A term in those files fails the gate; word the sentence another
   way, or cut the line from the sample.
4. **Logan's names are hashes.** His user name, his desktop's name, his personal domains and the two fragments
   in `FRAGMENTS` are in [kit/tools/check_kit.py](kit/tools/check_kit.py) by sha256 only. His user name is his first
   name in lower case: never write it as a login, in a home path or a user@host. Never write the others in any file
   or commit message. The self-privacy stage refuses each, but his site's domain, which the rules spell. His Linux
   machine's and his WSL distro's names are in the kit as his published texts spell them, and nothing refuses them:
   write them nowhere new. A control that needs a name uses the gate's control names, built at run time. A report
   that quotes one is redacted to `<address>` or `<repos>/`, and its header says so.
5. **The generated tables have an order, and the rules keep line counts.** The build writes examples/README.md's
   sample table before START-HERE.md's reading table, because the reading table gives examples/README.md's size. A file the reading table names changes
   that table when its size changes, and check 5 holds it. No rule may change a file's line count, so that a
   citation by line lands where it did in the source: the build refuses one that does.
6. **The gate's prefilter must stay necessary.** check_kit.py runs a privacy shape only on a text holding one of its
   `NEEDLES`. A needle that the shape could match without lets a leak through. `re` folds four letters beyond ASCII
   (a dotted capital I, a dotless i, a long s, the Kelvin sign), so the text is folded the same way before it is
   lowered, and `--control` writes every sample with each of them and requires it found. v1's verifier found the
   dotted I's gap, after the first fold covered two letters.
7. **Each refusal and finding has a test, and the runner shows it, where the mutant stages can find it.** They
   take out alone: each `die "` of ledger.sh, each `raise Refused(` of plant.py and round_metrics.py, each copy
   condition plant.py's check appends, each place check_kit.py records a finding, and each `raise BuildError(` of
   the builder and each difference its `--check` records (`diffs.append(`). Each time, a self-test, the gate's
   `--control` or builder-refusals must fail, and each stage first runs that check with nothing taken out and
   requires it to pass. A new refusal written in one of those forms, without its own case, fails the run. One written
   another way is not found: write it in one of them. The stages take minutes; the quick budget leaves them out.
8. **An agent's report the harness will not let it write is extracted from its transcript.** Its header says so,
   and docs/reviews/ keeps it.
9. **The IEEE 754 PDF never enters this repository or the zip.**
10. **Nothing is committed or pushed without Logan's word.** Logan's word for v1, 2026-10-23: "Go ahead once it
   passes", meaning once v1's verifier finds it READY.
