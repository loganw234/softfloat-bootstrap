# The reports on AUDIT-1

The three agents the audit's lead dispatched on 2026-10-31. Each was briefed to read and report, and none was told
what the lead suspected. Each report is the agent's final message, extracted by script from the hand-back call that
ends its transcript, and each one's first lines say so. None of them changed a repository.

| file | what it is |
|---|---|
| [record-review.md](record-review.md) | muse-softfloat's own record, read for cft-fp256: every mention on every branch and in every commit message, the fetch log, the harness, day 1. No near-miss and no use is recorded; it also names the gaps that keep the record from excluding access |
| [structural-review.md](structural-review.md) | an expert read of both libraries' code: weak similarities that common sources explain, and the strongest differences |
| [wasm-map.md](wasm-map.md) | both WebAssembly modules' interfaces, verified; the operation table; the first differential runs, which met the exp2m1 flag first, through muse's vectors |
