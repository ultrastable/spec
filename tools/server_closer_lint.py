#!/usr/bin/env python3
# DIR-1 (DIRECTIVES.md): every loop closes server-side with zero user action.
# Fails when (a) a DIRECTIVES.md entry has no `Enforced-by:` line naming an existing file,
# or (b) a change adds text that makes a local machine or a person the closer of a loop.
# Usage: server_closer_lint.py [--base origin/main] [--no-diff] [--selftest]
import re, subprocess, sys
from pathlib import Path

LOCAL = re.compile(
    r"run\s+(it\s+)?(locally|manually|by\s+hand)|on\s+(your|the\s+owner'?s|a\s+local)\s+(machine|laptop|pc|desktop)"
    r"|windows\s+(task\s+scheduler|scheduled\s+task)|\bschtasks\b|\bcrontab\s+-e\b|startup\s+folder"
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
    print("server_closer_lint selftest: 10 passed, 0 failed")


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
