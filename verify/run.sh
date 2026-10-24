#!/bin/bash
# The builder's front door: one command answers "does it still hold?" It is HonestFramework's
# templates/gate-runner.sh at 65447fd, its stage block replaced (KIT-0, section 9). What each stage proves is its
# description below; `--list` prints them.
#
#   bash verify/run.sh                   every stage, about a minute
#   bash verify/run.sh --budget quick    build, kit-gate, tools, gate-refuses, must-fail
#   bash verify/run.sh --only zip        by name (an unknown name is refused)
#   bash verify/run.sh --skip zip
#   bash verify/run.sh --require-all     a skipped stage FAILS the run
#   bash verify/run.sh --list            stages, with * on what would run
#   bash verify/run.sh --resume          continue the most recent run, on the same commit only
#   bash verify/run.sh --fresh           force a new run id
#
# SOURCES is the directory holding HonestFramework, ParcelRound, QRO-Crate and cft-fp256 (default: this
# repository's parent). The build reads them only from git objects, at the commits build/sources.lock pins.
#
# The run builds dist/softfloat-bootstrap-kit/ and, in the zip stage, the zip with its SHA256SUMS: what Logan
# receives is what this run checked. A stage's log is in .gate-state/<run>/<stage>.log, and every verdict is in
# that run's stages.jsonl.
#
# THERE IS NO CACHE ACROSS RUNS: --resume skips only what passed in this run id, and refuses another commit.
set -uo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
SOURCES="${SOURCES:-$(dirname "$ROOT")}"
STATEROOT="${STATEROOT:-$ROOT/.gate-state}"

ONLY=""; SKIP=""; REQUIRE_ALL=0; LIST=0; RESUME=""; FRESH=0; BUDGET=""

# Named cuts. Keep them as comma lists of stage names; the validation below
# checks them against the derived list, so a typo here fails loudly at start
# rather than quietly selecting nothing.
BUDGET_QUICK=build,kit-gate,tools,gate-refuses,must-fail
BUDGET_FULL=""          # empty means every stage

die () { echo "FATAL: $*" >&2; exit 2; }

while [ $# -gt 0 ]; do
  case "$1" in
    --only)        [ $# -ge 2 ] || die "--only needs a list"; ONLY="$ONLY,$2"; shift 2;;
    --skip)        [ $# -ge 2 ] || die "--skip needs a list"; SKIP="$SKIP,$2"; shift 2;;
    --budget)      [ $# -ge 2 ] || die "--budget needs quick or full"
                   case "$2" in
                     quick) BUDGET=quick; ONLY="$ONLY,$BUDGET_QUICK";;
                     full)  BUDGET=full;;
                     *) die "--budget: unknown budget '$2' (quick, full)";;
                   esac; shift 2;;
    --require-all) REQUIRE_ALL=1; shift;;
    --list)        LIST=1; shift;;
    --resume)      if [ $# -gt 1 ] && [[ ${2:-} != --* ]]; then RESUME=$2; shift 2
                   else RESUME=last; shift; fi;;
    --fresh)       FRESH=1; shift;;
    -h|--help)     sed -n '2,30p' "$0"; exit 0;;
    *)             die "unknown option $1";;
  esac
done

# Defined here, above --list, because --list exits before the other helpers
# and must answer "would this stage run?" with the SAME predicate stage()
# uses. Two copies of that rule is how a stage list starts lying.
in_list() {  # name, comma-list
  case ",$2," in *",$1,"*) return 0;; esac
  return 1
}

# §4: the only copy of the stage list is the `stage` calls themselves.
SELF="${BASH_SOURCE[0]}"
STAGELIST=$(grep -E '^stage [a-z0-9-]+ "' "$SELF" | awk '{print $2}' | tr '\n' ' ')
STAGELIST="${STAGELIST% }"

if [ "$LIST" = 1 ]; then
  while IFS=$'\t' read -r _nm _ds; do
    if [ -z "$ONLY" ] || in_list "$_nm" "$ONLY"; then _mk="*"; else _mk=" "; fi
    printf '%s %-16s %s\n' "$_mk" "$_nm" "$_ds"
  done < <(grep -E '^stage [a-z0-9-]+ "' "$SELF" \
      | sed -E 's/^stage ([a-z0-9-]+) +"([^"]*)".*/\1\t\2/')
  echo
  if [ -n "$ONLY" ]; then
    printf '* = would run%s. Unmarked stages are NOT in this selection.\n' \
        "${BUDGET:+ under --budget $BUDGET}"
  else
    echo "* = would run: every stage (no --only, no --budget)."
  fi
  exit 0
fi

# §5: refuse a name we do not know. A typo'd filter that selects nothing and
# reports "passed, nothing skipped" is the worst outcome available.
check_names() {  # <flagname> <comma-list>
  local n
  for n in $(echo "$2" | tr ',' ' '); do
    [ -z "$n" ] && continue
    case " $STAGELIST " in
      *" $n "*) ;;
      *) echo "ERROR: $1 names unknown stage '$n'" >&2
         echo "       stages: $STAGELIST" >&2
         exit 2;;
    esac
  done
}
check_names --only "$ONLY"
check_names --skip "$SKIP"

# §6: run identity. Timestamp plus commit, and a resume may not cross commits.
COMMIT=$(git -C "$ROOT" rev-parse --short HEAD 2>/dev/null || echo nogit)
if [ -n "$RESUME" ] && [ "$FRESH" = 1 ]; then
  die "--resume and --fresh are contradictory"
fi
if [ -n "$RESUME" ]; then
  if [ "$RESUME" = last ]; then
    RUNID=$(ls -1 "$STATEROOT" 2>/dev/null | sort | tail -n 1)
    [ -n "$RUNID" ] || die "--resume: no previous run under $STATEROOT"
  else
    RUNID=$RESUME
  fi
  case "$RUNID" in
    *-"$COMMIT") ;;
    *) die "run $RUNID was a different commit than $COMMIT; half a run of one
  tree glued to half a run of another is a report about neither. Use --fresh.";;
  esac
else
  RUNID="$(date +%Y%m%d-%H%M%S)-$COMMIT"
fi
RUNDIR="$STATEROOT/$RUNID"
mkdir -p "$RUNDIR"
JSONL="$RUNDIR/stages.jsonl"

PASSED=0; FAILED=0; SKIPPED=0; CACHED=0
note () { echo "   $*"; }

echo "== run $RUNID"
echo "   commit $COMMIT, state in $RUNDIR"
[ -n "$BUDGET" ] && echo "   budget $BUDGET"

# stage <name> <description> -- command...
#
# MUST_FAIL=1 before a stage inverts its verdict: the command is expected to
# fail, and its SUCCESS is the failure. That is how the negative control at
# the bottom proves this runner can say no. MUST_FAIL_LINE, set beside it,
# is a line the failing command's output must hold: a control that fails for
# another reason, a crash or a missing build, proves nothing, and fails the
# run (HonestFramework METHOD.md, section 5: exit codes are not reports).
stage() {
  local name=$1 desc=$2; shift 3
  local t0 t1 rc verdict reason="" expect_fail="${MUST_FAIL:-0}" must_line="${MUST_FAIL_LINE:-}"
  MUST_FAIL=0; MUST_FAIL_LINE=""

  if [ -n "$ONLY" ] && ! in_list "$name" "$ONLY"; then
    return 0                         # not selected: not reported either
  fi
  if [ -f "$RUNDIR/$name.ok" ]; then
    CACHED=$((CACHED+1))
    note "$(printf '%-16s %-7s %s' "$name" "ok" "(passed earlier in this run)")"
    echo "{\"stage\":\"$name\",\"verdict\":\"ok-cached\"}" >> "$JSONL"
    return 0
  fi
  # §5: a skip is announced by name, with a reason, always.
  if in_list "$name" "$SKIP"; then
    verdict=SKIP; reason="requested"
  elif [ -n "${STAGE_SKIP_REASON:-}" ]; then
    verdict=SKIP; reason=$STAGE_SKIP_REASON
  fi
  if [ "${verdict:-}" = SKIP ]; then
    SKIPPED=$((SKIPPED+1))
    note "$(printf '%-16s %-7s %s' "$name" "SKIP" "$reason")"
    echo "{\"stage\":\"$name\",\"verdict\":\"skip\",\"reason\":\"$reason\"}" >> "$JSONL"
    [ "$REQUIRE_ALL" = 1 ] && FAILED=$((FAILED+1))
    STAGE_SKIP_REASON=""
    return 0
  fi

  t0=$(date +%s)
  "$@" > "$RUNDIR/$name.log" 2>&1
  rc=$?
  t1=$(date +%s)

  if [ "$expect_fail" = 1 ]; then
    if [ "$rc" -eq 0 ]; then
      FAILED=$((FAILED+1))
      note "$(printf '%-16s %-7s %s' "$name" "FAIL" \
          "NEGATIVE CONTROL DID NOT FAIL - this runner cannot detect a defect")"
      echo "{\"stage\":\"$name\",\"verdict\":\"control-passed\"}" >> "$JSONL"
      return 1
    fi
    if [ -n "$must_line" ] && ! grep -qF -- "$must_line" "$RUNDIR/$name.log"; then
      FAILED=$((FAILED+1))
      note "$(printf '%-16s %-7s %s' "$name" "FAIL" \
          "the control failed without printing '$must_line': it failed for another reason; see $RUNDIR/$name.log")"
      echo "{\"stage\":\"$name\",\"verdict\":\"control-failed-otherwise\",\"rc\":$rc}" >> "$JSONL"
      return 1
    fi
    rc=0
    note "$(printf '%-16s %-7s %s' "$name" "ok" "(negative control failed, as it must)")"
  fi

  if [ "$rc" -eq 0 ]; then
    : > "$RUNDIR/$name.ok"
    PASSED=$((PASSED+1))
    [ "$expect_fail" = 1 ] || \
      note "$(printf '%-16s %-7s %ss  %s' "$name" "ok" "$((t1-t0))" "$desc")"
    echo "{\"stage\":\"$name\",\"verdict\":\"ok\",\"seconds\":$((t1-t0))}" >> "$JSONL"
  else
    : > "$RUNDIR/$name.fail"
    FAILED=$((FAILED+1))
    note "$(printf '%-16s %-7s rc=%s  see %s' "$name" "FAIL" "$rc" "$RUNDIR/$name.log")"
    echo "{\"stage\":\"$name\",\"verdict\":\"fail\",\"rc\":$rc}" >> "$JSONL"
  fi
}

# Set STAGE_SKIP_REASON before a stage when its tools are absent, so the skip
# says WHY. Never let a missing tool look like a pass.
need () {  # <command> <reason if missing>
  command -v "$1" >/dev/null 2>&1 || STAGE_SKIP_REASON="$2"
}

# ======================================================================
# THE STAGES. One `stage` line each, its description in double quotes on the same line, so the derivation and
# --list find it.
# ======================================================================

need git "git is not on PATH: the build reads its sources from git objects"
stage build "dist/ built from the pinned sources and kit/, every rule's count as declared" -- \
  python3 -I "$ROOT/build/build_kit.py" --sources "$SOURCES"

need git "git is not on PATH"
stage rebuild "a second build is dist/, byte for byte, and the bundle object for object" -- \
  python3 -I "$ROOT/build/build_kit.py" --check --sources "$SOURCES"

stage kit-gate "the kit's own gate passes on dist/: VERDICT: PASS, all five checks hold" -- \
  python3 -I "$ROOT/dist/softfloat-bootstrap-kit/tools/check_kit.py" "$ROOT/dist/softfloat-bootstrap-kit"

stage kit-controls "each of the gate's plants is caught by its own check, and the unplanted kit is clean" -- \
  python3 -I "$ROOT/dist/softfloat-bootstrap-kit/tools/check_kit.py" --control "$ROOT/dist/softfloat-bootstrap-kit"

stage tools "each agent tool's self-test passes, as dist/ holds it" -- \
  bash -c 'set -e; T="$1/dist/softfloat-bootstrap-kit/tools"; bash "$T/ledger.sh" selftest;
           python3 -I "$T/plant.py" selftest; python3 -I "$T/round_metrics.py" --selftest' _ "$ROOT"

stage bundle-compare "the rebuild's bundle comparison holds equal bundles equal, and a stub or one more commit not; a repacked bundle its manifest names passes --check" -- \
  python3 -I "$ROOT/tests/controls.py" bundle-compare --sources "$SOURCES"

stage refusal-mutants "each refusal of each agent tool, and each of plant.py's copy conditions, taken out alone, fails a self-test that passed unmutated" -- \
  python3 -I "$ROOT/tests/controls.py" refusal-mutants --sources "$SOURCES"

stage finding-mutants "each finding of the kit's gate, taken out alone, fails its --control, which passed unmutated" -- \
  python3 -I "$ROOT/tests/controls.py" finding-mutants --sources "$SOURCES"

stage gate-refuses "a planted cft-fp256 URL is refused by check 2 alone, naming its file" -- \
  python3 -I "$ROOT/tests/controls.py" gate-refuses --sources "$SOURCES"

stage real-names "ParcelRound's archives as it holds them are refused by the checks their rules serve" -- \
  python3 -I "$ROOT/tests/controls.py" real-names --sources "$SOURCES"

stage rule-count "a build with a rule's count moved is refused, naming the rule and the file" -- \
  python3 -I "$ROOT/tests/controls.py" rule-count --sources "$SOURCES"

stage builder-refusals "each refusal of the builder, --check's comparison among them, provoked once in a temporary build, is refused by name" -- \
  python3 -I "$ROOT/tests/controls.py" builder-refusals --sources "$SOURCES"

stage builder-mutants "each refusal of the builder, and each difference --check records, taken out alone, fails builder-refusals, which passed unmutated" -- \
  python3 -I "$ROOT/tests/controls.py" builder-mutants --sources "$SOURCES"

stage zip "the zip unpacks to a kit whose gate passes; SHA256SUMS names it; a second zip is the same bytes" -- \
  python3 -I "$ROOT/tests/controls.py" zip --sources "$SOURCES"

stage self-privacy "no file git would commit here, no commit message and no identity holds a privacy shape" -- \
  python3 -I "$ROOT/tests/controls.py" self-privacy --sources "$SOURCES"

stage docs "every relative link in this repository's own documents resolves" -- \
  python3 -I "$ROOT/tests/controls.py" docs --sources "$SOURCES"

# The control (HonestFramework METHOD.md, section 3): the gate, on a kit with a fault planted, must FAIL. If it
# passes, nothing above means anything, and the run says so.
MUST_FAIL=1
MUST_FAIL_LINE="VERDICT: REFUSED, 1 finding(s)"
stage must-fail "the gate on a kit with a planted fault MUST fail" -- \
  python3 -I "$ROOT/tests/controls.py" gate-on-planted --sources "$SOURCES"

# ======================================================================

echo "== summary"
echo "   passed $PASSED, failed $FAILED, skipped $SKIPPED, cached $CACHED"
echo "   record $JSONL"
if [ "$FAILED" -ne 0 ]; then
  echo "== FAILED"
  exit 1
fi
if [ "$SKIPPED" -ne 0 ] && [ "$REQUIRE_ALL" != 1 ]; then
  echo "== PASSED, with $SKIPPED skipped by name above"
  echo "   (--require-all makes a skip a failure)"
  exit 0
fi
echo "== PASSED"
exit 0
