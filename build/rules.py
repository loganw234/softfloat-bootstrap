"""The rules that change the carried texts, each with its declared counts (KIT-0, section 4.1).

A rule is a function from bytes to (bytes, count). The build applies each rule to the files the table names and
fails if a count differs from the one declared, so a source that moves cannot slip through: the counts are
declared once, here, beside the rules they count (ParcelRound METHOD.md section 1, the second grade).

No rule may change a byte it does not name, and no rule changes a file's line count: a citation by line number
lands where it did in the source (the build checks it). Every replacement marks itself in the text, so a reader of
the kit can see that a source was changed and how.

Logan's user name, his desktop's name and the two fragments R5 removes are held by sha256 only, and this file never
spells them. It spells two names the rules must match: his GitHub account's, in cft-fp256's URLs, and his site's
domain, which R6 keeps as text.
"""
import hashlib
import re

def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

# Logan's user name and his personal domains, by sha256. They are held once, in the kit's gate, and imported here,
# so the rule that removes a name and the check that refuses it cannot drift apart (KIT-0, sections 4.1 and 8).
from check_kit import USER_NAMES, PERSONAL_DOMAINS, FRAGMENTS, F_LABEL, F_PREFIX  # noqa: E402

CFT_URL = (r"https?://(?:www\.)?(?:github\.com/loganw234/cft-fp256|raw\.githubusercontent\.com/loganw234/cft-fp256"
           r"|api\.github\.com/repos/loganw234/cft-fp256|codeload\.github\.com/loganw234/cft-fp256"
           r"|loganw234\\?\.github\\?\.io/cft-fp256)")
# R1 and R4's link form: a Markdown link whose target is a cft-fp256 URL, the target allowed to start on the next
# line, as twelve of ParcelRound's do. The link's text is kept; the target goes.
CFT_LINK = re.compile(r"\[([^\]]*)\]\(\s*" + CFT_URL + r"[^)\s]*\s*\)")
# R4's bare form: a cft-fp256 URL that is no link's target. Its scheme and host go; the path after them stays, as
# text, so the record still says what it cited.
CFT_BARE = re.compile(CFT_URL)


MARK = ("cft-fp256's", "record,", "not", "in", "this", "kit")


def r1_marker(line_ends):
    """R1's marker, ", cft-fp256's record, not in this kit", with its last spaces written as line ends, one for each
    line end the removed target held, so that the file keeps its line count."""
    gaps = [" "] * (len(MARK) - 1)
    for i in range(1, min(line_ends, len(gaps)) + 1):
        gaps[-i] = "\n"
    out = MARK[0] + "".join(g + w for g, w in zip(gaps, MARK[1:]))
    return ", " + out + "\n" * max(0, line_ends - len(gaps))


def r1_cft_links(data):
    """R1 (and R4's link form): a Markdown link into cft-fp256 keeps its text and loses its target."""
    text = data.decode("utf-8")
    def mark(m):
        removed = m.group(0)[len(m.group(1)) + 2:]   # what follows "[text]": the target, with its line ends
        return m.group(1) + r1_marker(removed.count("\n"))
    new, n = CFT_LINK.subn(mark, text)
    return new.encode("utf-8"), n


def r4_cft_urls(data):
    """R4: inside an archived ledger's member, every URL into cft-fp256 stops being one. A link keeps its text, as
    R1 has it; a bare URL loses its scheme and host, and the rest of it stays."""
    data, links = r1_cft_links(data)
    text = data.decode("utf-8")
    new, bare = CFT_BARE.subn("[cft-fp256 URL removed]", text)
    return new.encode("utf-8"), links + bare


def r2_parcelround_links(data):
    """R2: a link to ParcelRound's repository becomes the kit-relative path to its README (from method/honest/)."""
    text = data.decode("utf-8")
    new, n = re.subn(r"\[([^\]]*)\]\(https://github\.com/loganw234/ParcelRound/?\)", r"[\1](../parcelround/README.md)",
                     text)
    return new.encode("utf-8"), n


R3_TARGETS = ("archive/round2-ledger.zip", "archive/round3-ledger.zip", "tools/check_method.py")


def r3_left_out(data):
    """R3: a link to a file the kit leaves out keeps its text, loses its target, and says so."""
    text = data.decode("utf-8")
    pat = r"\[([^\]]*)\]\((" + "|".join(re.escape(t) for t in R3_TARGETS) + r")\)"
    new, n = re.subn(pat, r"\1 (not in this kit)", text)
    return new.encode("utf-8"), n


def r6_site_urls(data):
    """R6: a URL to loganw.dev becomes text: the site is built partly from cft-fp256 (KIT-0, section 3, item 3)."""
    text = data.decode("utf-8")
    new, n = re.subn(r"https?://loganw\.dev\b", "loganw.dev", text)
    return new.encode("utf-8"), n


# R5's shapes. A home path's last named segment, in the forms the archives hold; and an address.
HOME_SEGMENT = re.compile(r"(?i)((?:[a-z]:[\\/]+users[\\/]+|/[a-z]/users/|/mnt/[a-z]/users/|/home/))([^\W_][\w.-]*)")
ADDRESS = re.compile(r"(?<![A-Za-z0-9._%+-])([A-Za-z0-9._%+-]+)@((?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,})")


FRAGMENT_TOKEN = re.compile(r"(?<![A-Za-z0-9])[A-Za-z0-9]+(?![A-Za-z0-9])")
FRAGMENT_MARKS = {F_LABEL: "<domain>", F_PREFIX: "<id-prefix>"}


def r5_personal(data):
    """R5: in an archived ledger's member, Logan's user name in a home path becomes <user>, an address at one of his
    personal domains becomes <address>, and each of the two fragments the gate holds (FRAGMENTS) becomes <domain> or
    <id-prefix> where it stands alone. Returns (bytes, (names, addresses, fragments))."""
    text = data.decode("utf-8")
    names = 0
    def seg(m):
        nonlocal names
        if sha(m.group(2)) in USER_NAMES or sha(m.group(2).lower()) in USER_NAMES:
            names += 1
            return m.group(1) + "<user>"
        return m.group(0)
    text = HOME_SEGMENT.sub(seg, text)
    addresses = 0
    def addr(m):
        nonlocal addresses
        if sha(m.group(2).lower()) in PERSONAL_DOMAINS:
            addresses += 1
            return "<address>"
        return m.group(0)
    text = ADDRESS.sub(addr, text)
    fragments = 0
    def frag(m):
        nonlocal fragments
        name = FRAGMENTS.get(sha(m.group(0).lower()))
        if name:
            fragments += 1
            return FRAGMENT_MARKS[name]
        return m.group(0)
    text = FRAGMENT_TOKEN.sub(frag, text)
    return text.encode("utf-8"), (names, addresses, fragments)


# The declared counts. Text rules: (source, path) -> {rule: count}. Every file a text rule touches is named here,
# and a rule that matches in a file not named here fails the build as surely as a wrong count does.
TEXT_RULES = {
    ("ParcelRound", "METHOD.md"): {"R1": 12},
    ("HonestFramework", "METHOD.md"): {"R2": 1},
    ("HonestFramework", "FAILURE-MODES.md"): {"R2": 1},
    ("HonestFramework", "WITH-PARCELROUND.md"): {"R2": 1},
    ("ParcelRound", "CASE-STUDY-2.md"): {"R3": 1},
    ("ParcelRound", "CASE-STUDY-3.md"): {"R3": 1},
    ("ParcelRound", "README.md"): {"R3": 1},
    ("ParcelRound", "CASE-STUDY-5.md"): {"R6": 2},
}
RULE_FUNCS = {"R1": r1_cft_links, "R2": r2_parcelround_links, "R3": r3_left_out, "R6": r6_site_urls}

# Archive rules: archive -> {rule: n}, totals over the archive's members.
ARCHIVE_RULES = {
    "archive/round4-ledger.zip": {"R4": 0, "R5-names": 65, "R5-addresses": 4, "R5-fragments": 6, "R6": 0},
    "archive/round4-second-ledger.zip": {"R4": 0, "R5-names": 14, "R5-addresses": 0, "R5-fragments": 0, "R6": 0},
    "archive/round5-ledger.zip": {"R4": 3, "R5-names": 42, "R5-addresses": 9, "R5-fragments": 1, "R6": 3},
    "archive/round6-ledger.zip": {"R4": 12, "R5-names": 0, "R5-addresses": 0, "R5-fragments": 0, "R6": 0},
}
