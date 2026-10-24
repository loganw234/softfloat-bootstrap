# The reports on KIT-0, and the drafts they read

Each report is an agent's final message, extracted by script from its transcript. Each one's first lines say what
was changed, if anything. The harness refused two of the agents' own writes of their reports, so the transcript holds
the only copy.

| file | what it is |
|---|---|
| [KIT-0-draft1.md](KIT-0-draft1.md) | the plan's draft 1, frozen when its verifier was dispatched |
| [draft1-verifier.md](draft1-verifier.md) | the verifier's report on draft 1: NOT READY, 6 (a), 10 (b), 18 notes |
| [KIT-0-draft2.md](KIT-0-draft2.md) | the plan's draft 2, frozen when its re-check was dispatched |
| [draft2-recheck.md](draft2-recheck.md) | the same verifier's scoped re-check of draft 2: NOT READY, 1 (a), 4 (b), 9 notes |
| [survey-cases.md](survey-cases.md) | the read-only surveyor's report on samples of how things were handled, in cft-fp256's record |

## The drafts' hashes

Each report quotes the sha256 of the draft it read. Each draft here differs from that file in one line: its one
absolute path, the container's `/home/` directory followed by `user/`, is written `<repos>/`, as round 6's verifier
brief has a report write its paths. No line is added or removed, so every line number a report cites still holds.

| draft | sha256 as the verifier read it | sha256 as kept here |
|---|---|---|
| 1 | `91a3972cebadd2f066092e887f5f8e4a7074d92fd4bcdd97650ea909658bca87` | `6030a356981fec0438922b8e42fce541cfe5c1d785bcd943a7bb06dd3eb99515` |
| 2 | `2f661b283140943f99befe5ae8f5913b330941093cc23c3b8175c5e265e4a403` | `8def3ebec3de87741090dc3d19ae6759ad2b1a497d794d0806be2c0ce4684da6` |

To check one: write `<repos>/` back as that path in the draft (on line 12 of draft 1, and line 19 of draft 2),
then hash it.
