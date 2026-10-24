#!/usr/bin/env python3
"""Build the softfloat bootstrap kit from pinned sources, or check that a built one is what the sources make.

    python3 -I build/build_kit.py             build dist/softfloat-bootstrap-kit/
    python3 -I build/build_kit.py --check     rebuild in a temporary directory and compare with dist/, byte for byte
    python3 -I build/build_kit.py --zip       build, then write dist/softfloat-bootstrap-kit-<version>.zip and SHA256SUMS
    --sources DIR                              where the four source repositories are (default: this repository's
                                               parent directory)

The plan is docs/KIT-0.md. What this does, by its sections:
- 4.1: the method texts, read from git objects at the commits build/sources.lock pins (never from a working tree, so
  an uncommitted edit cannot reach the kit), changed only by the rules in build/rules.py, each count checked;
- 4.1: the archived ledgers repacked by R4, R5 and R6, every member's timestamp and order kept;
- 4.2 and 4.4: the hackathon's layer and tools, from kit/ in this repository;
- 4.3: the samples, cut from cft-fp256's record by build/cases.json and by the gate's own term list, which this
  imports from kit/tools/check_kit.py so the two cannot drift;
- 4.3: QRO-Crate as a git bundle of main at its pinned commit, made from a temporary mirror, so nothing is written
  into the source repository;
- 4.5: MANIFEST.txt.

It needs git and Python 3.9 or later, and nothing else. It writes nothing outside dist/ but a temporary directory,
which it removes. Exit 0 on success; 1 when a count, a source or a check disagrees, with a line that names it; 2 on
bad usage.
"""
import argparse
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
sys.path.insert(0, str(ROOT / "kit" / "tools"))
import rules  # noqa: E402
import check_kit  # noqa: E402  (the gate: its term list, its table parsers)

KIT_NAME = "softfloat-bootstrap-kit"
KIT_VERSION = "v1"
DIST = ROOT / "dist"

# KIT-0 section 4.1: what is carried from each method repository, at its pinned commit.
HONEST = ["README.md", "METHOD.md", "FAILURE-MODES.md", "ADOPTING.md", "WITH-PARCELROUND.md", "CASE-STUDY.md",
          "LICENSE", "templates/README.md", "templates/agent-notes.md", "templates/controls.md", "templates/ledger.md",
          "templates/manifest.md", "templates/gate-runner.sh", "templates/check_generated.py", "tools/check_claims.py"]
PARCELROUND = ["README.md", "METHOD.md", "ADOPTION.md", "LICENSE", "CASE-STUDY.md"] + \
              [f"CASE-STUDY-{i}.md" for i in range(2, 7)] + \
              ["templates/brief.md", "templates/verifier.md", "templates/ledger.md", "templates/checklists.md",
               "archive/round6-practice-survey.md"]
ARCHIVES = list(rules.ARCHIVE_RULES)            # the four archives R4, R5 and R6 repack
EXCLUDED = ["archive/round2-ledger.zip", "archive/round3-ledger.zip", "tools/check_method.py"]  # KIT-0 4.1

# START-HERE.md's reading table: per role, what to read, in order (KIT-0 section 4.2). Bytes are measured at build.
READING = [
    ("everyone, first", ["CLEAN-ROOM.md", "ROLES.md", "GLOSSARY.md"]),
    ("the lead, before the first dispatch", ["OWNER.md", "WORKFLOW.md", "PROJECT.md", "METRICS.md", "HARNESS.md",
        "BOARD.md", "method/honest/README.md", "method/honest/METHOD.md", "method/honest/FAILURE-MODES.md",
        "method/parcelround/README.md", "method/parcelround/METHOD.md", "method/parcelround/templates/brief.md",
        "method/parcelround/templates/verifier.md", "method/parcelround/templates/ledger.md",
        "method/parcelround/templates/checklists.md", "examples/README.md"]),
    ("a parcel, with its brief", ["method/honest/METHOD.md", "method/parcelround/templates/ledger.md",
        "AGENTS.md"]),
    ("a verifier, with its brief", ["method/parcelround/METHOD.md", "method/honest/METHOD.md"]),
    ("when it is needed", ["method/honest/ADOPTING.md", "method/honest/WITH-PARCELROUND.md",
        "method/honest/CASE-STUDY.md", "method/honest/templates/README.md", "method/parcelround/ADOPTION.md",
        "method/parcelround/CASE-STUDY.md", "method/parcelround/CASE-STUDY-6.md",
        "method/parcelround/archive/round6-practice-survey.md"]),
]


class BuildError(Exception):
    pass


def git(repo, *args, binary=False):
    r = subprocess.run(["git", "-C", str(repo)] + list(args), capture_output=True,
                       env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"))
    if r.returncode != 0:
        raise BuildError(f"git {' '.join(args)} in {repo}: {r.stderr.decode(errors='replace').strip()}")
    return r.stdout if binary else r.stdout.decode("utf-8")


LOCK_FILE = ROOT / "build" / "sources.lock"
CASES_FILE = ROOT / "build" / "cases.json"


def load_sources(sources_dir):
    lock = json.loads(LOCK_FILE.read_text(encoding="utf-8"))
    out = {}
    for name, spec in lock.items():
        repo = Path(sources_dir) / name
        if not (repo / ".git").exists():
            raise BuildError(f"source {name}: no git repository at {repo}")
        commit = spec["commit"]
        r = subprocess.run(["git", "-C", str(repo), "cat-file", "-t", commit], capture_output=True, text=True)
        if r.returncode or r.stdout.strip() != "commit":
            raise BuildError(f"source {name}: {commit} is not a commit in {repo}")
        out[name] = (repo, commit, spec)
    return out


def show(src, path):
    repo, commit, _ = src
    return git(repo, "show", f"{commit}:{path}", binary=True)


def apply_text_rules(source, path, data, tally):
    """Every text rule, on every carried text file: a match in a file the table does not name fails, as does a count
    that differs from the one declared (rules.TEXT_RULES)."""
    declared = rules.TEXT_RULES.get((source, path), {})
    lines = data.count(b"\n")
    for rule, func in rules.RULE_FUNCS.items():
        data, n = func(data)
        want = declared.get(rule, 0)
        if n != want:
            raise BuildError(f"{rule} on {source}/{path}: {n} matches, {want} declared")
        if n:
            tally[rule] = tally.get(rule, 0) + n
    after = data.count(b"\n")
    if after != lines:
        raise BuildError(f"{source}/{path}: the rules took it from {lines} line ends to {after}, so a citation by "
                         "line number would land elsewhere")
    return data


def repack(name, data, tally):
    """R4, R5 and R6 inside one archive. Each member keeps its name, order, timestamp, attributes and extra fields;
    a member no rule changes keeps its bytes; the archive's own bytes change (KIT-0 4.1, the verifier's N20)."""
    src = zipfile.ZipFile(io.BytesIO(data))
    buf = io.BytesIO()
    counts = {"R4": 0, "R5-names": 0, "R5-addresses": 0, "R5-fragments": 0, "R6": 0}
    with zipfile.ZipFile(buf, "w") as dst:
        dst.comment = src.comment
        for info in src.infolist():
            body = src.read(info)
            if not info.is_dir():
                try:
                    body.decode("utf-8")
                    text = True
                except UnicodeDecodeError:
                    text = False
                if text:
                    lines = body.count(b"\n")
                    body, n4 = rules.r4_cft_urls(body)
                    body, (n5a, n5b, n5c) = rules.r5_personal(body)
                    body, n6 = rules.r6_site_urls(body)
                    counts["R4"] += n4; counts["R5-names"] += n5a; counts["R5-addresses"] += n5b
                    counts["R5-fragments"] += n5c; counts["R6"] += n6
                    after = body.count(b"\n")
                    if after != lines:
                        raise BuildError(f"{name}:{info.filename}: the rules took it from {lines} line ends to "
                                         f"{after}, so a citation by line number would land elsewhere")
                elif re.search(rb"loganw234.{0,3}cft-fp256", body):
                    raise BuildError(f"{name}:{info.filename}: binary member names cft-fp256, which no rule can mend")
            new = zipfile.ZipInfo(info.filename, info.date_time)
            new.compress_type = info.compress_type
            new.external_attr = info.external_attr
            new.create_system = info.create_system
            new.comment = info.comment
            new.extra = info.extra
            dst.writestr(new, body, compress_type=info.compress_type,
                         compresslevel=6 if info.compress_type == zipfile.ZIP_DEFLATED else None)
    declared = rules.ARCHIVE_RULES[name]
    for k, v in counts.items():
        if v != declared[k]:
            raise BuildError(f"{k} in {name}: {v}, {declared[k]} declared")
        tally[k] = tally.get(k, 0) + v
    return buf.getvalue()


def bundle_qro(src, out_path):
    repo, commit, spec = src
    ref = spec.get("bundle_ref", "main")
    with tempfile.TemporaryDirectory() as t:
        mirror = Path(t) / "mirror"
        subprocess.run(["git", "clone", "-q", "--mirror", str(repo), str(mirror)], check=True,
                       env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"))
        git(mirror, "update-ref", f"refs/heads/{ref}", commit)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        git(mirror, "-c", "pack.threads=1", "bundle", "create", "-q", str(out_path), f"refs/heads/{ref}")


def entry_heading(lines, n):
    """The '## ' heading of the record entry that holds line n (1-based)."""
    for i in range(n - 1, -1, -1):
        if lines[i].startswith("## "):
            return lines[i][3:].strip()
    return ""


def build_cases(src, out_root):
    """KIT-0 4.3: the samples. Each is verbatim lines of cft-fp256's docs/VALIDATION.md at the pinned commit. A line
    the spec cuts by hand, or one holding a term of the gate's list, is replaced by a marker that says so; nothing
    else is changed. Each sample's entry heading is asserted, so a spec whose lines drifted fails."""
    spec = json.loads(CASES_FILE.read_text(encoding="utf-8"))
    record = show(src, "docs/VALIDATION.md").decode("utf-8").split("\n")
    files = {}
    for group in spec["groups"]:
        files[group["file"]] = group
    written = []
    for fname, group in files.items():
        parts = [f"# {group['title']}\n", "\n", f"{group['intro']}\n", "\n"]
        for case in group["cases"]:
            parts.append(f"## {case['id']}. {case['title']}\n\n")
            froms = []
            for a, b, entry in case["ranges"]:
                head = entry_heading(record, a)
                if entry not in head or entry_heading(record, b) != head:
                    raise BuildError(f"case {case['id']}: lines {a}-{b} are not all in an entry holding '{entry}'")
                froms.append(f"the entry \"{entry}\", line{'s' if a != b else ''} {a}{'-' + str(b) if a != b else ''}")
            parts.append(f"- **From:** cft-fp256's docs/VALIDATION.md at `{src[1][:7]}`: " + "; ".join(froms) +
                         ". Not in this kit.\n")
            parts.append(f"- **What it shows** (the kit's reading): {case['shows']}\n")
            cut_lines = []
            body = []
            manual = {int(k): v for k, v in case.get("cut", {}).items()}
            for a, b, _ in case["ranges"]:
                if body:
                    body.append("[...]")
                for n in range(a, b + 1):
                    line = record[n - 1]
                    if n in manual:
                        cut_lines.append((n, manual[n])); body.append(f"[line {n} cut: {manual[n]}]")
                    elif check_kit.term_hit(line):
                        cut_lines.append((n, "a term from the gate's list")); body.append(
                            f"[line {n} cut: it holds a term from the gate's arithmetic list]")
                    else:
                        body.append(line)
            if cut_lines:
                parts.append(f"- **Cut:** {len(cut_lines)} line(s): " +
                             "; ".join(f"{n} ({why})" for n, why in cut_lines) + ".\n")
            else:
                parts.append("- **Cut:** nothing.\n")
            parts.append("\n" + "\n".join(f"> {l}" if l else ">" for l in body) + "\n\n")
        parts.append("---\n\n" + spec["licence"] + "\n")
        p = out_root / "examples" / "cases" / fname
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("".join(parts), encoding="utf-8", newline="\n")
        written.append((fname, group))
    return written


def replace_block(text, name, block):
    a, b = f"<!-- {name}:begin -->", f"<!-- {name}:end -->"
    if text.count(a) != 1 or text.count(b) != 1:
        raise BuildError(f"the {name} markers must each appear once")
    i, j = text.index(a) + len(a), text.index(b)
    return text[:i] + "\n" + block + text[j:]


def build(sources_dir, out):
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    srcs = load_sources(sources_dir)
    tally = {}
    # 4.1: the method texts.
    for source, base, files in (("HonestFramework", "method/honest", HONEST),
                                ("ParcelRound", "method/parcelround", PARCELROUND)):
        for path in files:
            data = show(srcs[source], path)
            if path.endswith(".md"):
                data = apply_text_rules(source, path, data, tally)
            elif re.search(rb"https?://(github\.com/loganw234/cft-fp256|loganw234\.github\.io/cft-fp256)", data):
                raise BuildError(f"{source}/{path}: a cft-fp256 URL in a file no rule may change")
            p = out / base / path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
    for (source, path) in rules.TEXT_RULES:
        files = HONEST if source == "HonestFramework" else PARCELROUND
        if path not in files:
            raise BuildError(f"rules.TEXT_RULES names {source}/{path}, which the kit does not carry")
    for name in ARCHIVES:
        p = out / "method" / "parcelround" / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(repack(name, show(srcs["ParcelRound"], name), tally))
    # 4.2 and 4.4: the layer and the tools, as this repository holds them.
    for p in sorted((ROOT / "kit").rglob("*")):
        if p.is_dir() or "__pycache__" in p.parts:
            continue
        rel = p.relative_to(ROOT / "kit")
        q = out / rel
        q.parent.mkdir(parents=True, exist_ok=True)
        q.write_bytes(p.read_bytes())
        if q.suffix in (".py", ".sh"):
            q.chmod(0o755)
    # 4.3: the samples, and QRO-Crate.
    cases = build_cases(srcs["cft-fp256"], out)
    bundle_qro(srcs["QRO-Crate"], out / "reference" / "QRO-Crate.bundle")
    # The generated tables (check 5 holds them): the sample table first, since the reading table measures
    # examples/README.md, which the sample table changes.
    ex = out / "examples" / "README.md"
    rows = []
    for fname, group in cases:
        ids = ", ".join(c["id"] for c in group["cases"])
        rows.append(f"| [cases/{fname}](cases/{fname}) | {group['title']} | {ids} |")
    table = "| file | situation | samples |\n|---|---|---|\n" + "\n".join(rows) + "\n"
    ex.write_text(replace_block(ex.read_text(encoding="utf-8"), "cases", table), encoding="utf-8", newline="\n")
    sh = out / "START-HERE.md"
    rows = []
    for role, paths in READING:
        for i, rel in enumerate(paths, 1):
            if not (out / rel).is_file():
                raise BuildError(f"START-HERE's reading list names {rel}, which the kit does not hold")
            rows.append(f"| {role if i == 1 else ''} | {i} | [{rel}]({rel}) | {(out / rel).stat().st_size:,} |")
    table = "| who | order | file | bytes |\n|---|---:|---|---:|\n" + "\n".join(rows) + "\n"
    sh.write_text(replace_block(sh.read_text(encoding="utf-8"), "reading", table), encoding="utf-8", newline="\n")
    # 4.5: the manifest.
    write_manifest(out, srcs, tally)
    return tally


def builder_identity():
    """The last commit that changed build/ or kit/, which is all a build reads of this repository, so that a commit
    to docs/ alone leaves the manifest as it was; and whether either has changed since."""
    try:
        last = git(ROOT, "log", "-1", "--format=%H", "--", "build", "kit").strip()
    except BuildError:
        return "no commit yet"
    if not last:
        return "no commit yet"
    dirty = git(ROOT, "status", "--porcelain", "--", "build", "kit").strip()
    return last + (" (build/ or kit/ modified since)" if dirty else "")


def write_manifest(out, srcs, tally):
    lines = [f"kit {KIT_NAME} {KIT_VERSION}", f"builder softfloat-bootstrap {builder_identity()}"]
    for name, (_, commit, _) in sorted(srcs.items()):
        lines.append(f"source {name} {commit}")
    for k in sorted(tally):
        lines.append(f"rule {k} {tally[k]}")
    lines.append("")
    for p in sorted(out.rglob("*")):
        if p.is_file() and p.name != "MANIFEST.txt":
            rel = p.relative_to(out).as_posix()
            lines.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {rel}")
    (out / "MANIFEST.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def compare_trees(a, b):
    """Every file in each, byte for byte; the bundle, if its bytes differ, by its heads and every object it holds
    (another git can pack the same objects otherwise). Returns a list of differences."""
    diffs = []
    fa = {p.relative_to(a).as_posix() for p in a.rglob("*") if p.is_file()}
    fb = {p.relative_to(b).as_posix() for p in b.rglob("*") if p.is_file()}
    for x in sorted(fa - fb):
        diffs.append(f"only in the rebuild: {x}")
    for x in sorted(fb - fa):
        diffs.append(f"only in dist/: {x}")
    for x in sorted(fa & fb):
        if (a / x).read_bytes() != (b / x).read_bytes():
            if x == "reference/QRO-Crate.bundle" and same_bundle_content(a / x, b / x):
                continue
            if x == "MANIFEST.txt" and manifest_equal_but_bundle(a / x, b / x):
                continue
            diffs.append(f"differs: {x}")
    return diffs


def bundle_content(p):
    """A bundle's heads and the ids of every object it holds, read through a temporary bare repository; None when
    git cannot read it, or it holds nothing."""
    with tempfile.TemporaryDirectory() as t:
        g = ["git", "--git-dir", t]
        subprocess.run(["git", "init", "-q", "--bare", t], capture_output=True, check=True)
        if subprocess.run(g + ["fetch", "-q", str(p), "refs/*:refs/*"], capture_output=True).returncode:
            return None
        heads = subprocess.run(g + ["for-each-ref", "--format=%(objectname) %(refname)"], capture_output=True,
                               text=True, check=True).stdout
        objects = subprocess.run(g + ["cat-file", "--batch-all-objects", "--batch-check=%(objectname)"],
                                 capture_output=True, text=True, check=True).stdout
    return (heads, objects) if heads and objects else None


def same_bundle_content(x, y):
    """Two bundles hold the same heads and the same objects. Another git can pack the same objects in other bytes."""
    a = bundle_content(x)
    return a is not None and a == bundle_content(y)


def manifest_equal_but_bundle(x, y):
    """Two manifests whose bytes differ in the bundle's line alone, the one line at the same place in each, each naming
    its own tree's bundle by that bundle's sha256: another git can pack the same objects in other bytes, and
    compare_trees holds the bundles to their content."""
    name = b"  reference/QRO-Crate.bundle"

    def masked(m):
        lines = m.read_bytes().split(b"\n")
        bundle = m.parent / "reference" / "QRO-Crate.bundle"
        at = [i for i, line in enumerate(lines) if line.endswith(name)]
        if len(at) != 1 or not bundle.is_file() or \
                lines[at[0]] != hashlib.sha256(bundle.read_bytes()).hexdigest().encode() + name:
            return None
        return lines[:at[0]] + [b""] + lines[at[0] + 1:]
    a = masked(x)
    return a is not None and a == masked(y)


def write_zip(out):
    """A deterministic zip: sorted names, one fixed timestamp, fixed modes, one top directory."""
    z = DIST / f"{KIT_NAME}-{KIT_VERSION}.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as f:
        for p in sorted(out.rglob("*")):
            if not p.is_file():
                continue
            rel = f"{KIT_NAME}/{p.relative_to(out).as_posix()}"
            info = zipfile.ZipInfo(rel, (1980, 1, 1, 0, 0, 0))
            info.external_attr = (0o100755 if p.suffix in (".py", ".sh") else 0o100644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            f.writestr(info, p.read_bytes(), compresslevel=9)
    digest = hashlib.sha256(z.read_bytes()).hexdigest()
    (DIST / "SHA256SUMS").write_text(f"{digest}  {z.name}\n", encoding="utf-8", newline="\n")
    return z, digest


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--zip", action="store_true")
    ap.add_argument("--sources", default=str(ROOT.parent))
    a = ap.parse_args(argv)
    if a.check and a.zip:
        ap.error("--check and --zip are separate steps")
    try:
        if a.check:
            built = DIST / KIT_NAME
            if not built.is_dir():
                raise BuildError(f"nothing to check: {built} does not exist (run the build first)")
            with tempfile.TemporaryDirectory() as t:
                tally = build(a.sources, Path(t) / KIT_NAME)
                diffs = compare_trees(Path(t) / KIT_NAME, built)
            if diffs:
                for d in diffs:
                    print(f"CHECK: {d}")
                print(f"CHECK FAILED: {len(diffs)} difference(s) between dist/ and what the sources make")
                return 1
            print(f"check: dist/{KIT_NAME} is what the pinned sources and kit/ make; rules " +
                  ", ".join(f"{k} {v}" for k, v in sorted(tally.items())))
            return 0
        out = DIST / KIT_NAME
        tally = build(a.sources, out)
        n = sum(1 for p in out.rglob("*") if p.is_file())
        print(f"built dist/{KIT_NAME}: {n} files; rules " + ", ".join(f"{k} {v}" for k, v in sorted(tally.items())))
        if a.zip:
            z, digest = write_zip(out)
            print(f"zip {z.relative_to(ROOT)}: {z.stat().st_size:,} bytes, sha256 {digest}")
        return 0
    except BuildError as e:
        print(f"BUILD FAILED: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
