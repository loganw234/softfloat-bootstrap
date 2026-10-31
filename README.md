# softfloat-bootstrap

The builder of the bootstrap kit for Logan's Meta AI hackathon, 2026-10-26 to 2026-11-04: an IEEE 754 softfloat for
the RP2040, in binary16, binary32 and binary64, built by Meta's models with HonestFramework and ParcelRound, and
measured.

The agents work in a clean room: they may not read cft-fp256, which already implements this arithmetic. So they
cannot be pointed at Logan's GitHub. Instead they get one zip that holds the methods, how the round goes, what the
lead owns and asks, Logan's own words, and samples of how situations were handled. **Only the zip moves to the Meta
directories.** This repository, which reads cft-fp256 to build the zip, stays private.

The kit's front door is [kit/START-HERE.md](kit/START-HERE.md). The plan of record is
[docs/KIT-0.md](docs/KIT-0.md), and the record is [docs/VALIDATION.md](docs/VALIDATION.md).

## Does it still hold?

```
bash verify/run.sh                   # every stage, a few minutes, most of them refusal-mutants' and finding-mutants'
bash verify/run.sh --budget quick    # build, kit-gate, tools, gate-refuses, must-fail
bash verify/run.sh --list            # every stage, and what it proves
```

The run builds `dist/softfloat-bootstrap-kit/` and, in its zip stage, `dist/softfloat-bootstrap-kit-v1.zip` with
its `SHA256SUMS`. So the zip Logan receives is the one the run checked. `make` has the same steps under shorter names
(`make build`, `make check`, `make dist`, `make verify`).

It needs git and Python 3.9 or later, and nothing else. The four sources, HonestFramework, ParcelRound, QRO-Crate
and cft-fp256, are read from git objects at the commits [build/sources.lock](build/sources.lock) pins, from
`SOURCES` (default: this repository's parent directory). A working tree's edits never reach the kit.

## What is where

| path | what it is |
|---|---|
| [kit/](kit/START-HERE.md) | the hackathon's layer and the agents' tools, copied into the kit as they are |
| [build/build_kit.py](build/build_kit.py) | the builder: the method texts by rule with counts, the archives repacked, the samples cut, the QRO-Crate bundle, the manifest, the zip |
| [build/rules.py](build/rules.py) | rules R1 to R6, and each one's declared count, per file |
| [build/cases.json](build/cases.json) | the samples: which lines of cft-fp256's record each one quotes, and why |
| [tests/controls.py](tests/controls.py) | the builder's controls: each check it relies on, watched to fail |
| [verify/run.sh](verify/run.sh) | the front door, after HonestFramework's `templates/gate-runner.sh` |
| [docs/KIT-0.md](docs/KIT-0.md) | the plan, its verifiers' findings, and the lead's slips |
| [docs/reviews/](docs/reviews/KIT-0/README.md) | every verifier's and surveyor's report, and the drafts they read |
| [audit/](audit/README.md) | the audit of the project repository against cft-fp256, and the two libraries' cross-test: its tools, and each run's results |
| [docs/AUDIT-1.md](docs/AUDIT-1.md) | the first audit, 2026-10-31: what it found, and its limits |
| `dist/` | ignored: the built kit, the zip and its SHA256SUMS |

## Privacy

- Logan's user name is held by sha256 only, in [kit/tools/check_kit.py](kit/tools/check_kit.py). It is his first
  name in lower case, and the kit names him throughout, so what the hash keeps out is the name's use as a login: a
  home path's segment, which R5 replaces in the archives, and a user@host, which the gate refuses.
- His desktop's name, his email's domain and two fragments of his identifiers are held the same way, and nothing here
  spells them. In the archives the builder replaces them by hash (R5), and its declared counts fail the build if one
  moves.
- Two of his names are spelled here, because the rules must match them: his GitHub account's, in cft-fp256's URLs,
  and his site's domain, which R6 keeps as text. The kit carries the site's domain 81 times (MEASURED by v1's
  verifier).
- His Linux machine's name and his WSL distro's are in the kit, 21 times, as his published texts spell them
  (ParcelRound's CASE-STUDY-3.md, QRO-Crate's history, cft-fp256's record). The gate does not refuse them (MEASURED
  by v1's verifier; the plan's section 13 says why).
- The QRO-Crate bundle's commit identities carry Logan's address, by his word: "Real address is fine" (2026-10-23).
- The IEEE 754 standard is Logan's, under his licence. It is in no file here and in no zip, and the gate refuses a
  PDF anywhere in the kit.

## Licence

The kit's [NOTICE.md](kit/NOTICE.md) gives the licence of each thing the kit carries. This repository has no licence
file: it is private, and its licence is Logan's to choose.
