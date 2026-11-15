#!/usr/bin/env python3
# SPDX-License-Identifier: LicenseRef-Ultrastable-USL-1.0
# Copyright (c) 2026 Rowan Brad Quni-Gudzinas. Non-commercial use free; commercial use requires a license. See LICENSE.
# DIR-1 (DIRECTIVES.md): every loop closes server-side with zero user action.
# Fails when (a) a DIRECTIVES.md entry has no `Enforced-by:` line naming an existing file,
# or (b) a change adds text that makes a local machine or a person the closer of a loop.
# Usage: server_closer_lint.py [--base origin/main] [--no-diff] [--selftest]
import re, subprocess, sys
from pathlib import Path

LOCAL = re.compile(
    r"run\s+(it\s+)?(locally|manually|by\s+hand)|on\s+(your|the\s+owner'?s|a\s+local)\s+(machine|laptop|pc|desktop)"
    r"|windows\s+(task\s+scheduler|scheduled\s+task)|\bschtasks\b|\bcrontab\b|startup\s+folder"
    r"|register-scheduledtask|new-scheduledtask|schedule\.service|\blaunchctl\b|launchagents|systemctl\s+--user"
    r"|(user|owner|you)\s+(must|should|needs?\s+to)\s+(run|click|trigger|re-?run|execute|merge|deploy)",
    re.I,
)
ALLOW = re.compile(r"IDENTITY-BOUND|IC-GATE-001|lint-allow:\s*local-closer", re.I)
EXT = (".md", ".yml", ".yaml", ".json", ".txt", ".toml", ".sh", ".py", ".mjs", ".ts", ".js")
LOCAL_SCRIPT = (".bat", ".cmd", ".ps1", ".psm1", ".vbs", ".lnk")
SELF = ("tools/server_closer_lint.py", "tools/self_closed_lint.py")


def local_hits(lines):
    return [l for l in lines if LOCAL.search(l) and not ALLOW.search(l)]


def local_script(path):
    return path.lower().endswith(LOCAL_SCRIPT)


RUNNABLE = (".py", ".sh")
WORKFLOWS = ".github/workflows"
NOISE = re.compile(r"\s*(#|-?\s*run:\s*echo\b|echo\b)")


def _read(p):
    return Path(p).read_text(encoding="utf-8", errors="replace")


def unconsumed(paths, wf_text=None, hop_text=None):
    """New .py/.sh scripts must run server-side: named in a workflow, or named/imported by a script a workflow runs."""
    if wf_text is None:
        wf = sorted(Path(WORKFLOWS).glob("*.y*ml")) if Path(WORKFLOWS).exists() else []
        raw = "\n".join(_read(w) for w in wf)
        wf_text = "\n".join(l for l in raw.splitlines() if not NOISE.match(l))
    if hop_text is None:
        hop = [q for q in Path(".").rglob("*") if q.is_file() and q.suffix in RUNNABLE and q.name in wf_text and q.as_posix() not in SELF]
        hop_text = "\n".join(_read(q) for q in hop)
    out = []
    for p in paths:
        if not p.endswith(RUNNABLE) or p.startswith(("tests/", "test/")) or "/tests/" in p or Path(p).name.startswith("test_"):
            continue
        name, stem = Path(p).name, Path(p).stem
        imported = re.search(rf"\bimport\s+{re.escape(stem)}\b|\bfrom\s+{re.escape(stem)}\s+import", hop_text)
        if name in wf_text or name in hop_text or imported:
            continue
        out.append(p)
    return out


def directive_gaps(text, exists=lambda p: Path(p).exists()):
    gaps = []
    for block in re.split(r"(?m)^## ", text)[1:]:
        name = block.splitlines()[0].strip()
        m = re.search(r"(?m)^Enforced-by:\s*(.+)$", block)
        if not m:
            gaps.append(f"{name}: no `Enforced-by:` line")
            continue
        for p in [x.strip(" `") for x in m.group(1).split(",") if x.strip()]:
            if not exists(p):
                gaps.append(f"{name}: Enforced-by names missing file {p}")
    return gaps


def selftest():
    assert local_hits(["Run it locally every morning"]), "local run"
    assert local_hits(["Registered as a Windows scheduled task"]), "task scheduler"
    assert local_hits(["The owner must click deploy"]), "person closer"
    assert local_hits(["IDENTITY-BOUND: the owner must click sign"]) == [], "gate exempt"
    assert local_hits(["A cron worker closes the loop"]) == [], "clean"
    assert directive_gaps("## DIR-9: x\nno line\n"), "missing enforcer"
    assert directive_gaps("## DIR-9: x\nEnforced-by: a.py\n", lambda p: False), "missing file"
    assert directive_gaps("## DIR-9: x\nEnforced-by: a.py\n", lambda p: True) == [], "ok"
    assert local_hits(["subprocess.run(['schtasks', '/create'])"]), "schtasks call"
    assert local_hits(["Register-ScheduledTask -TaskName x"]), "powershell scheduler"
    assert local_hits(["os.system('crontab mycron')"]) and local_hits(["launchctl load x.plist"]), "unix scheduler"
    wf = "run: python3 tools/a.py"
    assert unconsumed(["tools/orphan.py"], wf, "") == ["tools/orphan.py"], "orphan flagged"
    assert unconsumed(["tools/a.py"], wf, "") == [], "workflow-run ok"
    assert unconsumed(["tools/helper.py"], wf, "import helper") == [], "imported by run script ok"
    assert unconsumed(["tests/test_x.py", "docs/x.md"], wf, "") == [], "tests and non-scripts skipped"
    assert NOISE.match("      - run: echo tools/e.py") and NOISE.match("  # tools/e.py"), "noise lines dropped"
    assert not NOISE.match("      - run: python3 tools/e.py"), "real run kept"
    print("server_closer_lint selftest: 17 passed, 0 failed")


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)


def main():
    if "--selftest" in sys.argv:
        return selftest()
    fail = []
    d = Path("DIRECTIVES.md")
    if d.exists():
        fail += [f"DIRECTIVES.md {g}" for g in directive_gaps(d.read_text(encoding="utf-8"))]
    else:
        fail.append("DIRECTIVES.md missing")
    base = "origin/main"
    if "--base" in sys.argv:
        i = sys.argv.index("--base")
        if i + 1 >= len(sys.argv):
            print("FAIL --base needs a ref"); sys.exit(1)
        base = sys.argv[i + 1]
    if "--no-diff" in sys.argv:
        print("server_closer_lint: --no-diff given; added-line scan not run")
    elif sh("git", "rev-parse", "--verify", base).returncode != 0:
        fail.append(f"base {base} not found; fetch it or pass --no-diff")
    else:
        added = sh("git", "diff", "--name-only", "--diff-filter=AR", f"{base}...HEAD").stdout.split()
        fail += [f"{p}: local-machine script; closers run server-side (cron, worker, workflow)" for p in added if local_script(p)]
        fail += [f"{p}: new script has no server-side runner; run it from {WORKFLOWS}/*.yml or from a script a workflow runs" for p in unconsumed(added)]
        cur = None
        for l in sh("git", "diff", "-U0", f"{base}...HEAD").stdout.splitlines():
            if l.startswith("+++ b/"):
                cur = l[6:]
            elif l.startswith("+") and not l.startswith("+++") and cur and cur.endswith(EXT) and cur not in SELF:
                if local_hits([l[1:]]):
                    fail.append(f"{cur}: local or manual closer: {l[1:].strip()[:100]}")
    for f in fail:
        print("FAIL " + f)
    print(f"server_closer_lint: {'FAILED' if fail else 'ok'}")
    sys.exit(1 if fail else 0)


main()
