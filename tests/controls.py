#!/usr/bin/env python3
"""The builder's controls. Each shows that a check this repository relies on can fail, or holds a property of the
build that no other stage states. verify/run.sh runs each as its own stage.

    python3 -I tests/controls.py NAME [--sources DIR]

  gate-refuses     a copy of the built kit with one cft-fp256 URL planted in NOTICE.md, which no generated table
                   measures: the gate refuses it by check 2 alone, naming the file, with exit 1 and its REFUSED
                   verdict
  gate-on-planted  the same planted copy, returning the gate's own exit code, for the runner's stage that must fail
  real-names       a copy of the built kit holding ParcelRound's four archives as ParcelRound holds them: the gate
                   refuses each archive a rule changed, by the checks that rule serves (R4's by check 2, R5's by
                   check 4), and refuses none that no rule changed; the built archives are refused by nothing.
                   Wherever R5 replaced an address at one of Logan's domains, or one of the two fragments, the gate
                   names it so, which holds those hashes to the real data. His user name's hash is held to it by the
                   build itself: R5 replaces a name by its hash, and its declared counts (121 in all) fail the build
                   if one moves.
  rule-count       a build with one declared count moved, first a text rule's and then an archive rule's, is
                   refused, naming the rule and the file
  bundle-compare   the rebuild's comparison of bundles: the built bundle equals itself; it differs from the same
                   bundle cut to its header, and from one with a commit added; and a dist/ whose bundle holds the
                   same objects in other bytes, its manifest naming them, passes --check
  builder-refusals each refusal of the builder, provoked once, in a temporary build, with its own trial: the build
                   is refused, naming it. One trial runs --check on a dist/ with a file changed, one taken away and
                   one added, its manifest naming another source commit and its bundle cut to its header, and
                   requires each named and CHECK FAILED; four more change its manifest alone, a bundle line left
                   out or naming another bundle, CR LF line ends, or no last line end, and require MANIFEST.txt
                   alone named
  builder-mutants  each refusal of the builder, and each difference its --check records, taken out alone:
                   builder-refusals, which passes with nothing taken out, then names a trial that failed
  refusal-mutants  every refusal of every agent tool, and each condition plant.py's check refuses a copy for, taken
                   out alone: the tool's own self-test, which passes with nothing taken out, fails each time
  finding-mutants  every finding of the kit's gate, taken out alone: the gate's --control, which catches every plant
                   with nothing taken out, misses one each time
  zip              the zip unpacks to a kit whose gate passes, every member under one top directory with its mode;
                   SHA256SUMS names its sha256; a second zip is the same bytes
  self-privacy     every file git would commit in this repository, every commit message and every commit identity:
                   none of the gate's privacy shapes and none of Logan's names, his own address in an identity
                   excepted
  docs             every relative link in this repository's own documents resolves. kit/'s resolve in the built
                   kit, where the gate holds them; docs/reviews/ holds agents' reports, whose links are their own
                   repositories', as the gate leaves an archived ledger's

Exit 0 when the control holds; 1 when it does not, each line saying what was found; 2 on bad usage. gate-on-planted
is the exception: it returns the gate's exit code. The two mutant controls run four mutants at a time.
"""
import argparse
import concurrent.futures
import hashlib
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
import build_kit  # noqa: E402
import check_kit  # noqa: E402
import rules  # noqa: E402

KIT = build_kit.DIST / build_kit.KIT_NAME
PLANTED_URL = "https://" + "github.com/" + "loganw234/" + "cft" + "-fp256" + "/blob/main/README.md"
WORKERS = min(4, os.cpu_count() or 1)


def need_built():
    if not (KIT / "MANIFEST.txt").is_file():
        print("no built kit at %s: run the build first" % KIT)
        sys.exit(1)


def gate(kit, *flags):
    r = subprocess.run([sys.executable, "-I", str(kit / "tools" / "check_kit.py"), *flags, str(kit)],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def planted_copy(t):
    kit = Path(t) / build_kit.KIT_NAME
    shutil.copytree(KIT, kit)
    notice = kit / "NOTICE.md"
    notice.write_bytes(notice.read_bytes() + ("\nSee %s.\n" % PLANTED_URL).encode("utf-8"))
    check_kit.refresh_manifest(kit)
    return kit


def gate_refuses(_a):
    need_built()
    with tempfile.TemporaryDirectory() as t:
        rc, out = gate(planted_copy(t))
    lines = out.splitlines()
    want = ["manifest   ok", "links      REFUSED  1 finding(s)", "terms      ok", "privacy    ok", "generated  ok",
            "VERDICT: REFUSED, 1 finding(s)"]
    problems = [w for w in want if w not in lines]
    if rc != 1:
        problems.append("exit %d, not 1" % rc)
    if not any(l.strip().startswith("NOTICE.md: a URL into the repository") for l in lines):
        problems.append("no finding names NOTICE.md")
    for p in problems:
        print("gate-refuses: missing or wrong: %s" % p)
    if problems:
        print(out)
        return 1
    print("gate-refuses: the gate refused the planted URL by check 2 alone, naming NOTICE.md, exit 1")
    return 0


def gate_on_planted(_a):
    need_built()
    with tempfile.TemporaryDirectory() as t:
        rc, out = gate(planted_copy(t))
    print(out)
    return rc


def real_names(a):
    need_built()
    srcs = build_kit.load_sources(a.sources)
    problems, said = [], []
    with tempfile.TemporaryDirectory() as t:
        kit = Path(t) / build_kit.KIT_NAME
        shutil.copytree(KIT, kit)
        for name in rules.ARCHIVE_RULES:
            (kit / "method" / "parcelround" / name).write_bytes(build_kit.show(srcs["ParcelRound"], name))
        check_kit.refresh_manifest(kit)
        for name, counts in rules.ARCHIVE_RULES.items():
            rel = "method/parcelround/" + name
            want = set()
            if counts["R4"]:
                want.add("links")
            if counts["R5-names"] or counts["R5-addresses"] or counts["R5-fragments"]:
                want.add("privacy")
            for which, k in (("as ParcelRound holds it", kit), ("as built", KIT)):
                links = check_kit.check_links(k, {rel})
                privacy = check_kit.check_privacy(k, {rel})
                got = {c for c, f in (("links", links), ("privacy", privacy)) if f}
                expect = want if k is kit else set()
                if got != expect:
                    problems.append("%s %s: refused by %s, where the rules say %s" % (
                        name, which, sorted(got) or "nothing", sorted(expect) or "nothing"))
                if k is not kit:
                    continue
                for count, finding in (("R5-addresses", check_kit.F_PERSONAL), ("R5-fragments", None)):
                    if not counts[count]:
                        continue
                    names = (check_kit.F_LABEL, check_kit.F_PREFIX) if finding is None else (finding,)
                    if not any(n in f for f in privacy for n in names):
                        problems.append("%s as ParcelRound holds it: the gate does not name %s, though %s replaced %d"
                                        % (name, " or ".join(names), count, counts[count]))
                said.append("%s: refused by %s (%d and %d findings)" % (
                    name, " and ".join(sorted(got)) or "nothing", len(links), len(privacy)))
    for p in problems:
        print("real-names: %s" % p)
    for s in said:
        print("real-names: %s" % s)
    if not problems:
        print("real-names: each archive as ParcelRound holds it is refused by the checks its rules serve, and as "
              "built by none")
    return 1 if problems else 0


def rule_count(a):
    import copy
    saved_text, saved_archive = copy.deepcopy(rules.TEXT_RULES), copy.deepcopy(rules.ARCHIVE_RULES)
    trials = [("R1", "ParcelRound/METHOD.md", lambda: rules.TEXT_RULES[("ParcelRound", "METHOD.md")].__setitem__(
                  "R1", rules.TEXT_RULES[("ParcelRound", "METHOD.md")]["R1"] + 1)),
              ("R5-names", "archive/round5-ledger.zip", lambda: rules.ARCHIVE_RULES["archive/round5-ledger.zip"]
                  .__setitem__("R5-names", rules.ARCHIVE_RULES["archive/round5-ledger.zip"]["R5-names"] - 1))]
    problems = []
    try:
        for rule, where, move in trials:
            rules.TEXT_RULES.clear()
            rules.TEXT_RULES.update(copy.deepcopy(saved_text))
            rules.ARCHIVE_RULES.clear()
            rules.ARCHIVE_RULES.update(copy.deepcopy(saved_archive))
            move()
            with tempfile.TemporaryDirectory() as t:
                try:
                    build_kit.build(a.sources, Path(t) / build_kit.KIT_NAME)
                    problems.append("a build with %s's count on %s moved was not refused" % (rule, where))
                except build_kit.BuildError as e:
                    if rule not in str(e) or where not in str(e):
                        problems.append("refused, but not naming %s and %s: %s" % (rule, where, e))
                    else:
                        print("rule-count: refused: %s" % e)
    finally:
        rules.TEXT_RULES.clear()
        rules.TEXT_RULES.update(saved_text)
        rules.ARCHIVE_RULES.clear()
        rules.ARCHIVE_RULES.update(saved_archive)
    for p in problems:
        print("rule-count: %s" % p)
    return 1 if problems else 0


def bundle_compare(a):
    need_built()
    bundle = KIT / "reference" / "QRO-Crate.bundle"
    problems = []
    with tempfile.TemporaryDirectory() as t:
        stub = Path(t) / "stub.bundle"
        data = bundle.read_bytes()
        stub.write_bytes(data[:data.index(b"\n\n") + 2])
        w = Path(t) / "w"
        env = dict(os.environ, GIT_AUTHOR_NAME="control", GIT_AUTHOR_EMAIL="control@example.invalid",
                   GIT_COMMITTER_NAME="control", GIT_COMMITTER_EMAIL="control@example.invalid")
        subprocess.run(["git", "clone", "-q", "-b", "main", str(bundle), str(w)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(w), "-c", "commit.gpgsign=false", "commit", "-q", "--allow-empty", "-m", "x"],
                       check=True, capture_output=True, env=env)
        more = Path(t) / "more.bundle"
        subprocess.run(["git", "-C", str(w), "bundle", "create", "-q", str(more), "refs/heads/main"], check=True,
                       capture_output=True)
        if not build_kit.same_bundle_content(bundle, bundle):
            problems.append("the built bundle does not compare equal to itself")
        if build_kit.same_bundle_content(bundle, stub):
            problems.append("the built bundle compares equal to itself cut to its header")
        if build_kit.same_bundle_content(bundle, more):
            problems.append("the built bundle compares equal to one with a commit added")
        import io, contextlib
        kit = Path(t) / "repacked" / build_kit.KIT_NAME
        build_kit.build(a.sources, kit)
        packed, mirror = kit / "reference" / "QRO-Crate.bundle", Path(t) / "mirror"
        old = hashlib.sha256(packed.read_bytes()).hexdigest()
        subprocess.run(["git", "clone", "-q", "--mirror", str(packed), str(mirror)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(mirror), "-c", "pack.compression=0", "repack", "-adfq"], check=True,
                       capture_output=True)
        subprocess.run(["git", "-C", str(mirror), "bundle", "create", "-q", str(packed), "--all"], check=True,
                       capture_output=True)
        new = hashlib.sha256(packed.read_bytes()).hexdigest()
        manifest = kit / "MANIFEST.txt"
        manifest.write_bytes(manifest.read_bytes().replace(old.encode(), new.encode()))
        with Patch((build_kit, "DIST", kit.parent)):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = build_kit.main(["--check", "--sources", a.sources])
        if new == old or rc != 0:
            problems.append("a dist/ whose bundle holds the same objects in other bytes, its manifest naming them, "
                            "does not pass --check: %s" % (buf.getvalue().strip()[:200] or "the same bytes"))
    for p in problems:
        print("bundle-compare: %s" % p)
    if not problems:
        print("bundle-compare: the bundle equals itself, and differs from its header alone and from one more commit; "
              "repacked into other bytes and named so by its manifest, it passes --check")
    return 1 if problems else 0


class Patch:
    """Set attributes for one trial, and put them back after it."""
    def __init__(self, *changes):
        self.changes = changes                  # (object, name, value)

    def __enter__(self):
        self.saved = [(o, n, getattr(o, n)) for o, n, _ in self.changes]
        for o, n, v in self.changes:
            setattr(o, n, v)

    def __exit__(self, *exc):
        for o, n, v in self.saved:
            setattr(o, n, v)


def builder_trials(sources):
    """(the refusal it provokes, what its message must hold, the trial): one for each refusal of build_kit.py."""
    import json as _json
    t = Path(tempfile.mkdtemp(prefix="builder-trials-"))
    real_show, real_r1, real_r5 = build_kit.show, rules.r1_marker, rules.r5_personal
    lock = _json.loads(build_kit.LOCK_FILE.read_text(encoding="utf-8"))
    cases = _json.loads(build_kit.CASES_FILE.read_text(encoding="utf-8"))
    url = cat_url()

    def write_json(name, data):
        q = t / name
        q.write_text(_json.dumps(data), encoding="utf-8")
        return q

    def build():
        build_kit.build(sources, t / ("kit-%d" % len(list(t.iterdir()))))

    def show_with(path_suffix, extra):
        def show(src, path):
            data = real_show(src, path)
            return data + extra if path.endswith(path_suffix) else data
        return show

    def zip_with_binary(src, path):
        data = real_show(src, path)
        if path != "archive/round6-ledger.zip":
            return data
        import io
        buf = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(data)) as a, zipfile.ZipFile(buf, "w") as b:
            for i in a.infolist():
                b.writestr(i, a.read(i))
            b.writestr("parcelround-r6-ledger/planted.bin", b"\xff\xfe" + url.split("//", 1)[1].encode())
        return buf.getvalue()

    def r5_with_line(data):
        out, counts = real_r5(data)
        return (out + b"\n" if out != data else out), counts

    def no_dist_check():
        with Patch((build_kit, "DIST", t / "no-dist")):
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = build_kit.main(["--check", "--sources", sources])
            if rc != 1 or "nothing to check" not in buf.getvalue():
                raise AssertionError("rc %d: %s" % (rc, buf.getvalue().strip()[:120]))
            raise build_kit.BuildError("nothing to check, as main printed")

    def differing_dist_check():
        """--check on a dist/ built, then with one file changed, one taken away and one added, its manifest naming
        another ParcelRound commit, and its bundle cut to its header, so that neither of the comparison's two
        exemptions can hide a difference."""
        import io, contextlib
        kit = t / "differing-dist" / build_kit.KIT_NAME
        build_kit.build(sources, kit)
        with open(kit / "ROLES.md", "ab") as f:
            f.write(b"x")
        (kit / "NOTICE.md").unlink()
        (kit / "EXTRA.md").write_text("x\n", encoding="utf-8")
        manifest = (kit / "MANIFEST.txt").read_text(encoding="utf-8")
        moved = re.sub(r"(?m)^(source ParcelRound )[0-9a-f]{40}$", lambda m: m.group(1) + "0" * 40, manifest)
        if moved == manifest:
            raise AssertionError("the manifest has no ParcelRound source line to move")
        (kit / "MANIFEST.txt").write_text(moved, encoding="utf-8", newline="\n")
        bundle = (kit / "reference" / "QRO-Crate.bundle").read_bytes()
        (kit / "reference" / "QRO-Crate.bundle").write_bytes(bundle[:bundle.index(b"\n\n") + 2])
        with Patch((build_kit, "DIST", kit.parent)):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = build_kit.main(["--check", "--sources", sources])
        said = buf.getvalue()
        want = ["CHECK: differs: ROLES.md", "CHECK: only in the rebuild: NOTICE.md", "CHECK: only in dist/: EXTRA.md",
                "CHECK: differs: MANIFEST.txt", "CHECK: differs: reference/QRO-Crate.bundle",
                "CHECK FAILED: 5 difference(s)"]
        unsaid = [w for w in want if w not in said]
        if rc != 1 or unsaid:
            raise AssertionError("rc %d, not saying %s: %s" % (rc, unsaid, said.strip()[:200]))
        raise build_kit.BuildError("CHECK FAILED, as main printed, naming each difference")

    def manifest_only_check(change):
        """--check on a dist/ whose MANIFEST.txt alone is changed, its bytes given to change."""
        import io, contextlib
        kit = t / ("manifest-only-%d" % len(list(t.iterdir()))) / build_kit.KIT_NAME
        build_kit.build(sources, kit)
        before = (kit / "MANIFEST.txt").read_bytes()
        after = change(before)
        if after == before:
            raise AssertionError("the change left the manifest as it was")
        (kit / "MANIFEST.txt").write_bytes(after)
        with Patch((build_kit, "DIST", kit.parent)):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = build_kit.main(["--check", "--sources", sources])
        said = buf.getvalue()
        if rc != 1 or "CHECK: differs: MANIFEST.txt" not in said or "CHECK FAILED: 1 difference(s)" not in said:
            raise AssertionError("rc %d: %s" % (rc, said.strip()[:200]))
        raise build_kit.BuildError("CHECK FAILED, as main printed, naming MANIFEST.txt alone")

    empty = t / "no-sources"
    empty.mkdir()
    bad_lock = dict(lock, **{"QRO-Crate": dict(lock["QRO-Crate"], commit="0" * 40)})
    bad_cases = _json.loads(_json.dumps(cases))
    bad_cases["groups"][0]["cases"][0]["ranges"][0][2] = "an entry no record holds"
    moved_text = {k: dict(v) for k, v in rules.TEXT_RULES.items()}
    moved_text[("ParcelRound", "METHOD.md")]["R1"] += 1
    moved_archive = {k: dict(v) for k, v in rules.ARCHIVE_RULES.items()}
    moved_archive["archive/round5-ledger.zip"]["R5-names"] -= 1
    trials = [
        ("a git command that fails", "git show", lambda: (Patch((build_kit, "HONEST", build_kit.HONEST + ["NO-SUCH.md"])),)),
        ("a source with no repository", "no git repository at", lambda: build_kit.build(str(empty), t / "k-empty")),
        ("a source pinned to no commit", "is not a commit in",
         lambda: (Patch((build_kit, "LOCK_FILE", write_json("lock.json", bad_lock))),)),
        ("a text rule's count moved", "R1 on ParcelRound/METHOD.md", lambda: (Patch((rules, "TEXT_RULES", moved_text)),)),
        ("a text rule that joins lines", "ParcelRound/METHOD.md: the rules took it from", lambda: (Patch((rules, "r1_marker", lambda n: ", cft-fp256's "
                                                                       "record, not in this kit")),)),
        ("an archive rule that adds a line", "-ledger.zip:", lambda: (Patch((rules, "r5_personal", r5_with_line)),)),
        ("an archive member, binary, naming cft-fp256", "binary member names cft-fp256",
         lambda: (Patch((build_kit, "show", zip_with_binary)),)),
        ("an archive rule's count moved", "R5-names in archive/round5-ledger.zip",
         lambda: (Patch((rules, "ARCHIVE_RULES", moved_archive)),)),
        ("a sample whose lines left their entry", "are not all in an entry holding",
         lambda: (Patch((build_kit, "CASES_FILE", write_json("cases.json", bad_cases))),)),
        ("a generated table's markers missing", "markers must each appear once",
         lambda: build_kit.replace_block("no markers here", "reading", "x")),
        ("a cft-fp256 URL in a file no rule may change", "a cft-fp256 URL in a file no rule may change",
         lambda: (Patch((build_kit, "show", show_with("templates/gate-runner.sh", ("\n# " + url + "\n").encode()))),)),
        ("a text rule for a file the kit does not carry", "which the kit does not carry",
         lambda: (Patch((rules, "TEXT_RULES", {**rules.TEXT_RULES, ("ParcelRound", "NO-SUCH.md"): {"R1": 1}})),)),
        ("a reading list naming a file the kit lacks", "which the kit does not hold",
         lambda: (Patch((build_kit, "READING", build_kit.READING + [("someone", ["NO-SUCH.md"])])),)),
        ("a check with nothing built", "nothing to check", no_dist_check),
        ("a check of a dist/ that differs", "CHECK FAILED", differing_dist_check),
        ("a check of a dist/ whose manifest leaves the bundle out", "naming MANIFEST.txt alone",
         lambda: manifest_only_check(lambda b: re.sub(rb"(?m)^[0-9a-f]{64}  reference/QRO-Crate\.bundle\n", b"", b))),
        ("a check of a dist/ whose manifest names another bundle", "naming MANIFEST.txt alone",
         lambda: manifest_only_check(lambda b: re.sub(rb"(?m)^[0-9a-f]{64}(?=  reference/QRO-Crate\.bundle$)",
                                                      b"0" * 64, b))),
        ("a check of a dist/ whose manifest has CR LF line ends", "naming MANIFEST.txt alone",
         lambda: manifest_only_check(lambda b: b.replace(b"\n", b"\r\n"))),
        ("a check of a dist/ whose manifest lacks its last line end", "naming MANIFEST.txt alone",
         lambda: manifest_only_check(lambda b: b[:-1] if b.endswith(b"\n") else b)),
    ]
    return t, trials, build


def cat_url():
    return "".join(("https", "://", "github", ".com/", "loganw", "234/", "cft", "-fp256"))


def builder_refusals(a):
    t, trials, build = builder_trials(a.sources)
    problems = []
    try:
        for name, want, trial in trials:
            try:
                patches = trial()
                if isinstance(patches, tuple):
                    for patch in patches:
                        with patch:
                            build()
                problems.append("%s: the build was not refused" % name)
            except build_kit.BuildError as e:
                if want not in str(e):
                    problems.append("%s: refused, but not naming %r: %s" % (name, want, e))
                else:
                    print("builder-refusals: %s: refused: %s" % (name, str(e)[:120]))
            except Exception as e:
                problems.append("%s: the builder failed instead of refusing: %s: %s" % (name, type(e).__name__, e))
    finally:
        shutil.rmtree(t, ignore_errors=True)
    for p in problems:
        print("builder-refusals: FAIL: %s" % p)
    if not problems:
        print("builder-refusals: %d refusals of the builder, its --check's comparison among them, each provoked once "
              "and refused by name" % len(trials))
    return 1 if problems else 0


# Every refusal of the builder, and each difference its --check records. Taken out, it is computed and dropped.
BUILDER_SITES = re.compile(r"raise BuildError\(|diffs\.append\(")


def builder_mutants(a):
    source = (ROOT / "build" / "build_kit.py").read_text(encoding="utf-8")
    sites = list(BUILDER_SITES.finditer(source))

    def run(text):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / "builder"
            for d in ("build", "kit", "tests"):
                shutil.copytree(ROOT / d, root / d, ignore=shutil.ignore_patterns("__pycache__"))
            (root / "build" / "build_kit.py").write_text(text, encoding="utf-8")
            return subprocess.run([sys.executable, "-I", str(root / "tests" / "controls.py"), "builder-refusals",
                                   "--sources", a.sources], capture_output=True, text=True)

    base = run(source)
    if base.returncode != 0 or not sites:
        print("builder-mutants: FAIL: builder-refusals fails with nothing taken out, or there is no site to take out, "
              "so no mutant can show anything: %s" % (base.stdout.strip().splitlines() or ["no output"])[-1])
        return 1

    def one(m):
        inert = "BuildError(" if m.group(0).startswith("raise") else "("
        r = run(source[:m.start()] + inert + source[m.end():])
        if r.returncode != 0 and "builder-refusals: FAIL: " in r.stdout:
            return None
        line = source.count("\n", 0, m.start()) + 1
        return "build_kit.py:%d: builder-refusals names no failed trial with this taken out: %s" % (
            line, source[m.start():source.find("\n", m.start())].strip()[:100])

    with concurrent.futures.ThreadPoolExecutor(WORKERS) as pool:
        problems = [r for r in pool.map(one, sites) if r]
    for p in problems:
        print("builder-mutants: %s" % p)
    if not problems:
        n = sum(1 for m in sites if m.group(0).startswith("raise"))
        print("builder-mutants: %d refusals of the builder and the %d differences its --check records, each taken out "
              "alone, and each time builder-refusals passed unmutated and then named a trial that failed"
              % (n, len(sites) - n))
    return 1 if problems else 0


def mutants(label, source_rel, sites, inert, run_one):
    """Take out each site of the file at source_rel alone, in a copy of the built kit, and run run_one(kit, file) on
    it; return the problems: each site whose removal run_one did not notice."""
    source = (KIT / source_rel).read_text(encoding="utf-8")
    found = list(sites.finditer(source))
    if not found:
        return ["%s: no site found to take out" % source_rel], 0
    with tempfile.TemporaryDirectory() as t:
        kit = Path(t) / build_kit.KIT_NAME
        shutil.copytree(KIT, kit)
        if run_one(kit, kit / source_rel):
            return ["%s: its check fails with nothing taken out, so no mutant can show anything" % source_rel], 0

    def one(m):
        with tempfile.TemporaryDirectory() as t:
            kit = Path(t) / build_kit.KIT_NAME
            shutil.copytree(KIT, kit)
            (kit / source_rel).write_text(source[:m.start()] + inert(m.group(0)) + source[m.end():], encoding="utf-8")
            noticed = run_one(kit, kit / source_rel)
        if noticed:
            return None
        line = source.count("\n", 0, m.start()) + 1
        text = source[m.start():source.find("\n", m.start())].strip()
        return "%s:%d: %s with this taken out: %s" % (source_rel, line, label, text[:110])

    with concurrent.futures.ThreadPoolExecutor(WORKERS) as pool:
        results = list(pool.map(one, found))
    return [r for r in results if r], len(found)


# Every refusal of every agent tool. Taken out, the refusal becomes a statement that does nothing.
REFUSALS = [
    ("tools/ledger.sh", re.compile(r'(?<![\w-])die "'), lambda s: ': "', ["bash", "{tool}", "selftest"]),
    ("tools/plant.py", re.compile(r"raise Refused\(|problems\.append\("),
     lambda s: "Refused(" if s.startswith("raise") else "(", [sys.executable, "-I", "{tool}", "selftest"]),
    ("tools/round_metrics.py", re.compile(r"raise Refused\("), lambda s: "Refused(",
     [sys.executable, "-I", "{tool}", "--selftest"]),
]


def refusal_mutants(_a):
    need_built()
    problems, n = [], 0
    for rel, sites, inert, cmd in REFUSALS:
        def run_one(kit, tool, cmd=cmd):
            r = subprocess.run([c.replace("{tool}", str(tool)) for c in cmd], capture_output=True, text=True)
            return r.returncode != 0 and "FAIL" in r.stdout
        p, k = mutants("its self-test still passes", rel, sites, inert, run_one)
        problems += p
        n += k
    for p in problems:
        print("refusal-mutants: %s" % p)
    if not problems:
        print("refusal-mutants: %d refusals in %d tools, plant.py's copy conditions among them, each taken out alone, "
              "and each time the tool's self-test, which passed with nothing taken out, failed" % (n, len(REFUSALS)))
    return 1 if problems else 0


# Every place the gate records a finding: an append to a list of findings, and the one early return. Taken out, the
# finding is computed and dropped.
FINDING_SITES = re.compile(r"\b(?:f|out)\.append\((?!\()|\bfound\.append\(|\breturn \[(?=\")")


def finding_mutants(_a):
    need_built()

    def run_one(kit, _tool):
        check_kit.refresh_manifest(kit)
        rc, out = gate(kit, "--control")
        return rc != 0 and "MISSED" in out

    problems, n = mutants("the gate's --control still catches every plant", "tools/check_kit.py", FINDING_SITES,
                          lambda s: "return [] and [" if s.startswith("return") else "(", run_one)
    for p in problems:
        print("finding-mutants: %s" % p)
    if not problems:
        print("finding-mutants: %d places the gate records a finding, each taken out alone, and each time its "
              "--control, which caught every plant with nothing taken out, missed one" % n)
    return 1 if problems else 0


def zip_control(_a):
    need_built()
    problems = []
    z, first = build_kit.write_zip(KIT)
    sums = (build_kit.DIST / "SHA256SUMS").read_text(encoding="utf-8")
    if sums != "%s  %s\n" % (first, z.name):
        problems.append("SHA256SUMS says %r, not the zip's sha256 %s" % (sums.strip(), first))
    _, second = build_kit.write_zip(KIT)
    if second != first:
        problems.append("a second zip is %s, the first %s" % (second, first))
    built = sorted(p.relative_to(KIT).as_posix() for p in KIT.rglob("*") if p.is_file())
    with tempfile.TemporaryDirectory() as t:
        with zipfile.ZipFile(z) as f:
            infos = f.infolist()
            top = build_kit.KIT_NAME + "/"
            for i in infos:
                parts = i.filename.split("/")
                if not i.filename.startswith(top) or ".." in parts or i.filename.startswith("/"):
                    problems.append("a member outside %s: %s" % (top, i.filename))
            f.extractall(t)
            for i in infos:
                os.chmod(os.path.join(t, i.filename), (i.external_attr >> 16) & 0o777)
        names = sorted(i.filename[len(top):] for i in infos)
        if names != built:
            problems.append("the zip holds %d files, the built kit %d" % (len(names), len(built)))
        execs = sorted(n for n in names if (n.endswith(".py") or n.endswith(".sh")))
        for n in execs:
            if not os.access(os.path.join(t, top, n), os.X_OK):
                problems.append("%s lost its executable mode" % n)
        rc, out = gate(Path(t) / build_kit.KIT_NAME)
        if rc != 0 or "VERDICT: PASS, all five checks hold" not in out:
            problems.append("the gate in the unpacked kit: exit %d\n%s" % (rc, out))
    for p in problems:
        print("zip: %s" % p)
    if not problems:
        print("zip: %s, %s bytes, sha256 %s, made twice alike; it unpacks to %d files whose gate passes"
              % (z.name, format(z.stat().st_size, ","), first, len(names)))
    return 1 if problems else 0


def self_privacy(_a):
    git = ["git", "-C", str(ROOT)]
    files = subprocess.run(git + ["ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                           capture_output=True, check=True).stdout.decode("utf-8").split("\0")
    problems = []
    for rel in sorted(f for f in files if f):
        p = ROOT / rel
        if not p.is_file():
            continue
        for finding in check_kit.privacy_findings(check_kit.decode(p.read_bytes()), check_kit.USER_NAMES,
                                                  check_kit.MACHINE_NAMES, check_kit.PERSONAL_DOMAINS):
            problems.append("%s: %s" % (rel, finding))
    has_commits = subprocess.run(git + ["rev-parse", "-q", "--verify", "HEAD"], capture_output=True).returncode == 0
    commits = []
    if has_commits:
        commits = subprocess.run(git + ["rev-list", "--all"], capture_output=True, text=True,
                                 check=True).stdout.split()
    for c in commits:
        msg = subprocess.run(git + ["log", "-1", "--format=%B", c], capture_output=True, text=True, check=True).stdout
        for finding in check_kit.privacy_findings(msg, check_kit.USER_NAMES, check_kit.MACHINE_NAMES,
                                                  check_kit.PERSONAL_DOMAINS):
            problems.append("commit %s's message: %s" % (c[:12], finding))
        for email in subprocess.run(git + ["log", "-1", "--format=%ae%n%ce", c], capture_output=True, text=True,
                                    check=True).stdout.split():
            local, _, domain = email.partition("@")
            if not (check_kit.address_kept(local, domain) or check_kit.sha(domain.lower()) in check_kit.PERSONAL_DOMAINS):
                problems.append("commit %s's identity: an address that is neither kept nor Logan's" % c[:12])
    for p in problems:
        print("self-privacy: %s" % p)
    if not problems:
        print("self-privacy: %d files and %d commits, none holding a privacy shape or one of Logan's names"
              % (sum(1 for f in files if f), len(commits)))
    return 1 if problems else 0


def docs(_a):
    git = ["git", "-C", str(ROOT)]
    files = subprocess.run(git + ["ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "*.md"],
                           capture_output=True, check=True).stdout.decode("utf-8").split("\0")
    files = [f for f in files if f and not f.startswith(("kit/", "docs/reviews/"))]
    problems, n = [], 0
    for rel in sorted(files):
        p = ROOT / rel
        text = re.sub(r"(?s)```.*?```", "", p.read_text(encoding="utf-8"))
        for m in list(check_kit.LINK.finditer(text)) + list(check_kit.REFDEF.finditer(text)):
            target = m.group(1)
            if re.match(r"(?i)[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
                continue
            path = target.split("#", 1)[0].split("?", 1)[0]
            if not path:
                continue
            n += 1
            dest = (p.parent / path).resolve()
            try:
                dest.relative_to(ROOT)
            except ValueError:
                problems.append("%s: link '%s' leaves the repository" % (rel, target))
                continue
            if not dest.exists():
                problems.append("%s: link '%s' does not resolve" % (rel, target))
    for p in problems:
        print("docs: %s" % p)
    if not problems:
        print("docs: %d relative links in %d documents, each resolving" % (n, len(files)))
    return 1 if problems else 0


CONTROLS = {"gate-refuses": gate_refuses, "gate-on-planted": gate_on_planted, "real-names": real_names,
            "rule-count": rule_count, "bundle-compare": bundle_compare, "builder-refusals": builder_refusals,
            "builder-mutants": builder_mutants, "refusal-mutants": refusal_mutants, "finding-mutants": finding_mutants,
            "zip": zip_control, "self-privacy": self_privacy, "docs": docs}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("name", choices=sorted(CONTROLS))
    ap.add_argument("--sources", default=str(ROOT.parent))
    a = ap.parse_args(argv)
    try:
        return CONTROLS[a.name](a)
    except build_kit.BuildError as e:
        print("%s: the build failed: %s" % (a.name, e))
        return 1


if __name__ == "__main__":
    sys.exit(main())
