#!/usr/bin/env bash
# audit/run.sh - every run of the audit and of the cross-test, in order. Run audit/setup.sh first.
#
#     bash audit/run.sh            # the whole run: 10 min 48 s on 4 cores (2026-10-31)
#     bash audit/run.sh --quick    # every step at a small fraction of the volume: a few minutes
#
# Each step's whole output goes to $AUDIT_WORK/results/<step>.txt and its last lines to the screen; a step
# that fails stops the run and names its file. The steps report; docs/AUDIT-1.md judges what they found.
# The controls are steps too: planted copies (fingerprint-scan), planted wrong answers (mutant-control), the
# arbiter's own references (oracle-check), and each policy class checked case by case (native-classes). A
# control that does not hold fails its step.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/.." && pwd)
export SOURCES=${SOURCES:-$(dirname "$ROOT")}
export MUSE_REPO=${MUSE_REPO:-$SOURCES/muse-softfloat} CFT_REPO=${CFT_REPO:-$SOURCES/cft-fp256}
export MUSE_REV=${MUSE_REV:-HEAD} CFT_REV=${CFT_REV:-HEAD}
export AUDIT_WORK=${AUDIT_WORK:-$ROOT/dist/audit}
die() { echo "run: $*" >&2; exit 1; }
[ -x "$AUDIT_WORK/venv/bin/python" ] && [ -f "$AUDIT_WORK/REVS.txt" ] || die "run audit/setup.sh first"
PY=("$AUDIT_WORK/venv/bin/python" -I -B)
BIN="$AUDIT_WORK/native/bin"

SCALE=1 DENSE_RNE=1048576 DENSE_OTHER=262144 HOST=1500 SF=2000
if [ "${1:-}" = --quick ]; then SCALE=0.05 DENSE_RNE=32768 DENSE_OTHER=8192 HOST=200 SF=200; fi

OUT="$AUDIT_WORK/results"
rm -rf "$OUT" && mkdir -p "$OUT"
cp "$AUDIT_WORK/REVS.txt" "$OUT/REVS.txt"
step() {
    local name=$1 t0=$SECONDS; shift
    printf '== %s\n' "$name"
    if "$@" > "$OUT/$name.txt" 2>&1; then
        tail -n 3 "$OUT/$name.txt" | cut -c1-180 | sed 's/^/   /'; printf '   (%ss)\n' $((SECONDS - t0))
    else
        echo "   FAILED: $OUT/$name.txt"; tail -n 15 "$OUT/$name.txt"; exit 1
    fi
}
expect() {   # step name or file, extended regex that must match a line: a control's own check
    local f="$OUT/$1"
    [ -f "$f" ] || f="$f.txt"
    grep -qE "$2" "$f" || die "control did not hold: '$2' not in $f"
}

# ---------------- part 1: the audit
step fingerprint-scan   "${PY[@]}" "$HERE/fingerprint/run_fp.py" "$AUDIT_WORK/fp"
step fingerprint-report "${PY[@]}" "$HERE/fingerprint/analyze.py" "$AUDIT_WORK/fp" 50 80 12
expect fingerprint-report "controls caught: 17 of 17"
step features           "${PY[@]}" "$HERE/fingerprint/features.py" "$AUDIT_WORK/features"
cp "$AUDIT_WORK/features/features.json" "$OUT/features.json"
step test-data          "${PY[@]}" "$HERE/fingerprint/vecfp.py"

# ---------------- part 2: the cross-test
step oracle-check       "${PY[@]}" "$HERE/crosstest/validate_oracle.py" "$HOST" "$SF"
step smoke              node "$HERE/crosstest/smoke.mjs"
step cft-corpus-wasm    node "$HERE/crosstest/replay_cft_full.mjs"
expect cft-corpus-wasm  "control \(cft module vs cft record\): ok [0-9]+, not ok 0"
step muse-corpus-wasm   node "$HERE/crosstest/replay_muse_vec.mjs"
expect muse-corpus-wasm '"museBad":0'
step native-replay      "${PY[@]}" "$HERE/native/native_replay.py"
step native-classes     "${PY[@]}" "$HERE/native/classes.py"
step mutant-control     env MUTANT=1 node "$HERE/crosstest/bigdiff.mjs" 0.05 "$AUDIT_WORK/bigdiff-mutant"
cp "$AUDIT_WORK/bigdiff-mutant.txt" "$OUT/mutant-control-detail.txt"
expect mutant-control-detail.txt "^ +20  add@32 \| RNE \| VALUE$"
expect mutant-control-detail.txt "div@64 \| RTZ \| flags muse - cft inexact"
step differential       node "$HERE/crosstest/bigdiff.mjs" "$SCALE" "$AUDIT_WORK/bigdiff"
cp "$AUDIT_WORK/bigdiff.txt" "$OUT/differential-detail.txt"
step sample-oracle      "${PY[@]}" "$HERE/crosstest/check_sample.py" "$AUDIT_WORK/bigdiff.sample.jsonl"
step int-delivery       node "$HERE/crosstest/intcheck.mjs"
step exp2m1-probe       "$BIN/exp2m1_probe"

dense() {   # the eight shared functions over contiguous binary32 ranges, four processes at a time
    for spec in "exp2 3f000000" "exp2m1 3c000000" "log2 3f800000" "log2p1 3c000000" \
                "sinpi 3e800000" "cospi 3e800000" "rsqrt 3f800000" "hypot 3f800000"; do
        set -- $spec
        echo "$1 $2 $DENSE_RNE RNE"
        for rm in RTZ RUP RDN RMM; do echo "$1 $2 $DENSE_OTHER $rm"; done
    done | xargs -P 4 -L 1 "$BIN/dense" | sort
}
step dense dense

{ echo "audit/run.sh $(date -u +%Y-%m-%dT%H:%M:%SZ), scale $SCALE"; cat "$OUT/REVS.txt"; echo
  grep -h "controls caught\|paths;" "$OUT/fingerprint-report.txt"
  grep -h "high-entropy words" "$OUT/test-data.txt"
  grep -h "cases," "$OUT/oracle-check.txt"
  grep -h "^control\|^cross" "$OUT/cft-corpus-wasm.txt"
  grep -h "^files" "$OUT/muse-corpus-wasm.txt"
  tail -n 1 "$OUT/native-classes.txt"
  grep -h "^cases\|^ \+[0-9]" "$OUT/differential.txt"
  grep -h "checked answers\|cft ok\|muse ok\|VALUE\|FLAGS" "$OUT/sample-oracle.txt" || true
  grep -h "out-of-range" "$OUT/int-delivery.txt"
  grep -h "exp2m1 at emax+1" "$OUT/exp2m1-probe.txt"
  awk '/^SUMMARY/ {n++; for (i = 1; i <= NF; i++) { if ($i == "same") s += $(i+1); if ($i == "nan-payload") p += $(i+1); if ($i == "differ") d += $(i+1) } }
       END {printf "dense: %d sweeps, same %d, nan-payload %d, differ %d\n", n, s, p, d}' "$OUT/dense.txt"
} > "$OUT/SUMMARY.txt"
echo; cat "$OUT/SUMMARY.txt"
