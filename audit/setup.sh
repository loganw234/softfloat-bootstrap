#!/usr/bin/env bash
# audit/setup.sh - make everything the audit's runs read, under AUDIT_WORK, from pinned inputs.
#
#     bash audit/setup.sh
#
# Needs git, python3 with venv, node 22, gcc, make, curl and unzip, and the network once (PyPI and
# jhauser.us). The two repositories are read from git objects at MUSE_REV and CFT_REV, never from a
# working tree, as the builder reads its sources. Re-running replaces what it made.
#
#   SOURCES     where the repositories are (default: this repository's parent directory)
#   MUSE_REPO   default $SOURCES/muse-softfloat        MUSE_REV  default HEAD
#   CFT_REPO    default $SOURCES/cft-fp256             CFT_REV   default HEAD
#   AUDIT_WORK  default dist/audit (git ignores dist/)
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/.." && pwd)
SOURCES=${SOURCES:-$(dirname "$ROOT")}
MUSE_REPO=${MUSE_REPO:-$SOURCES/muse-softfloat}
CFT_REPO=${CFT_REPO:-$SOURCES/cft-fp256}
MUSE_REV=${MUSE_REV:-HEAD}
CFT_REV=${CFT_REV:-HEAD}
AUDIT_WORK=${AUDIT_WORK:-$ROOT/dist/audit}
die() { echo "setup: $*" >&2; exit 1; }

for t in git python3 node gcc make curl unzip sha256sum; do command -v "$t" >/dev/null || die "$t is not on PATH"; done
git -C "$MUSE_REPO" rev-parse -q --verify "$MUSE_REV^{commit}" >/dev/null || die "no commit $MUSE_REV in $MUSE_REPO"
git -C "$CFT_REPO" rev-parse -q --verify "$CFT_REV^{commit}" >/dev/null || die "no commit $CFT_REV in $CFT_REPO"
[ "$(git -C "$MUSE_REPO" rev-parse --is-shallow-repository)" = false ] || die "$MUSE_REPO is shallow: the fingerprints read every commit (git fetch --unshallow)"
[ "$(git -C "$CFT_REPO" rev-parse --is-shallow-repository)" = false ] || die "$CFT_REPO is shallow: the fingerprints read every commit (git fetch --unshallow)"
mkdir -p "$AUDIT_WORK"

echo "== 1. Python: numpy (fingerprints), mpmath (cft's vector generator), gmpy2 = MPFR (the arbiter)"
[ -x "$AUDIT_WORK/venv/bin/python" ] || python3 -m venv "$AUDIT_WORK/venv"
"$AUDIT_WORK/venv/bin/pip" install -q numpy==2.5.3 mpmath==1.4.1 gmpy2==2.3.2
PY="$AUDIT_WORK/venv/bin/python"
"$PY" -c "import numpy, mpmath, gmpy2; print('  numpy', numpy.__version__, 'mpmath', mpmath.__version__, 'gmpy2', gmpy2.version(), gmpy2.mpfr_version())"

echo "== 2. Berkeley SoftFloat 3e and TestFloat 3e: the baseline of permitted common sources, and an oracle"
B="$AUDIT_WORK/baseline"
mkdir -p "$B/dl"
fetch() {   # name sha256
    [ -f "$B/dl/$1" ] || curl -fsS --max-time 300 -o "$B/dl/$1" "http://www.jhauser.us/arithmetic/$1"
    echo "$2  $B/dl/$1" | sha256sum -c --quiet - || die "$1 does not have the pinned sha256"
}
fetch SoftFloat-3e.zip 21130ce885d35c1fe73fc1e1bf2244178167e05c6747cad5f450cc991714c746
fetch TestFloat-3e.zip 6d4bdf0096b48a653aa59fc203a9e5fe18b5a58d7a1b715107c7146776a0aad6
rm -rf "$B/src" && mkdir -p "$B/src"
unzip -q "$B/dl/SoftFloat-3e.zip" -d "$B/src" && unzip -q "$B/dl/TestFloat-3e.zip" -d "$B/src"

echo "== 3. both trees, from git objects"
rm -rf "$AUDIT_WORK/muse" "$AUDIT_WORK/cft" && mkdir -p "$AUDIT_WORK/muse" "$AUDIT_WORK/cft"
git -C "$MUSE_REPO" archive "$MUSE_REV" src include site compat tests | tar -x -C "$AUDIT_WORK/muse"
git -C "$CFT_REPO" archive "$CFT_REV" | tar -x -C "$AUDIT_WORK/cft"
{ echo "muse-softfloat $(git -C "$MUSE_REPO" rev-parse "$MUSE_REV^{commit}")"
  echo "cft-fp256 $(git -C "$CFT_REPO" rev-parse "$CFT_REV^{commit}")"
  echo "softfloat-bootstrap $(git -C "$ROOT" rev-parse HEAD)"; } > "$AUDIT_WORK/REVS.txt"
sed 's/^/  /' "$AUDIT_WORK/REVS.txt"

echo "== 4. native builds: muse's library, cft's library (software backend), and the programs that link both"
N="$AUDIT_WORK/native" && rm -rf "$N" && mkdir -p "$N/obj" "$N/bin"
for f in msf16 msf32 msf64 msf_alg msf_aug msf_flags msf_math msf_roundpack msf_string msf_wide; do   # site/build.py's list
    gcc -O2 -I "$AUDIT_WORK/muse/include" -c "$AUDIT_WORK/muse/src/$f.c" -o "$N/obj/$f.o"
done
ar rcs "$N/libmsf.a" "$N"/obj/*.o
make -C "$AUDIT_WORK/cft/host" -j4 libcft.a > "$N/libcft-build.log" 2>&1 || die "cft's libcft.a did not build: $N/libcft-build.log"
INC=(-I "$AUDIT_WORK/muse/include" -I "$AUDIT_WORK/cft/host/include")
LIBS=("$N/libmsf.a" "$AUDIT_WORK/cft/host/libcft.a" -lm -lpthread)
for p in xnative dense exp2m1_probe; do gcc -O2 "${INC[@]}" -o "$N/bin/$p" "$HERE/native/$p.c" "${LIBS[@]}"; done
if grep -qw fma /proc/cpuinfo 2>/dev/null && [ "$(uname -m)" = x86_64 ]; then
    gcc -O1 -mfma -frounding-math -fsignaling-nans -o "$N/bin/hostref" "$HERE/crosstest/hostref.c" -lm
else
    echo "  hostref skipped: it needs an x86-64 with FMA (its cases come from the SSE unit)"
fi
cp -r "$B/src/SoftFloat-3e" "$N/SoftFloat-3e"
make -C "$N/SoftFloat-3e/build/Linux-x86_64-GCC" -j4 > "$N/softfloat-build.log" 2>&1 || die "SoftFloat 3e did not build"
gcc -O1 -I "$N/SoftFloat-3e/source/include" -o "$N/bin/sfref" "$HERE/crosstest/sfref.c" "$N/SoftFloat-3e/build/Linux-x86_64-GCC/softfloat.a"
ls "$N/bin" | sed 's/^/  /'

echo "== 5. cft's published fp32/fp64 vector sets, regenerated, each equal to cft's vectors/SHA256SUMS"
V="$AUDIT_WORK/cft/vectors"
rm -rf "$V/out"
"$PY" -B "$V/gen_vectors.py" --out "$V/out" --formats fp32 fp64 --rounding rne rtz rdn rup rmm \
    --directed 3000 --random 4000 --simple 200 --jobs 4 > "$AUDIT_WORK/cft-vectors.log" 2>&1 \
    || die "cft's generator failed: $AUDIT_WORK/cft-vectors.log"
grep -E '  out/fp(32|64)[-.]' "$V/SHA256SUMS" | grep -vE 'to-fp(128|256)' > "$AUDIT_WORK/cft-vectors.sums"
want=$(wc -l < "$AUDIT_WORK/cft-vectors.sums")
ok=$(cd "$V" && sha256sum -c "$AUDIT_WORK/cft-vectors.sums" 2>/dev/null | grep -c ': OK$' || true)
[ "$ok" = "$want" ] || die "$ok of $want regenerated sets equal SHA256SUMS"
echo "  $ok of $want sets equal cft's SHA256SUMS"
echo "setup: done; run: bash audit/run.sh"
