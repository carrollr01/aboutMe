#!/usr/bin/env python3
"""
deals_guard.py — Claude Code hook guarding the weekly-deals enforcement layer.

Registered in .claude/settings.json:
  PreToolUse  (Write|Edit|MultiEdit|NotebookEdit|Bash) -> `deals_guard.py pre`
  PostToolUse (Write|Edit|MultiEdit)                   -> `deals_guard.py post`

pre  — refuses (exit 2, which blocks the tool call) edits to LOCKED enforcement
       files, and Bash commands that combine a locked path with a write/mutation
       pattern. Running or reading the builder/validator is always allowed;
       rewriting, deleting, or git-reverting them is not.
post — when a weekly-deals/inputs/deals_*.json is written, runs validate_deals.py
       and feeds any locked-rule violations back into the session (exit 2), so
       bad rows are caught the moment they land, not at build time.

LOCKED (rule enforcement + audit trail):
  .claude/settings.json                                    — hook wiring
  .claude/hooks/**                                         — this guard
  .claude/skills/weekly-fintech-deals/build_workbook.py    — schema enforcement
  .claude/skills/weekly-fintech-deals/validate_deals.py    — locked rules
  weekly-deals/citations/**                                — citation manifests
                                                             (builder-written only)

Changing any of these is a HUMAN decision: disable the guard via /hooks or edit
.claude/settings.json outside a Claude session, make the change, re-enable.
The guard fails OPEN on unexpected payloads so it cannot brick unrelated work;
git history + PR review remain the final backstop.
"""
import json
import os
import re
import subprocess
import sys

LOCKED_FILES = {
    ".claude/settings.json",
    ".claude/skills/weekly-fintech-deals/build_workbook.py",
    ".claude/skills/weekly-fintech-deals/validate_deals.py",
}
LOCKED_DIRS = (".claude/hooks", "weekly-deals/citations")

# A Bash command is suspicious only if it BOTH names an enforcement path and
# contains a mutation pattern — plain execution (python3 build_workbook.py ...)
# and reads (cat, git diff/log) pass through.
BASH_TOKENS = (
    ".claude/settings.json",
    ".claude/hooks",
    "weekly-deals/citations",
    "build_workbook.py",
    "validate_deals.py",
    "deals_guard.py",
    ".claude/skills/weekly-fintech-deals",
)
MUTATION = re.compile(
    r"(?:(?<![\d&])>(?!&)"                      # redirection (not 2>&1 / >&2)
    r"|\btee\b|\brm\b|\bunlink\b|\bmv\b|\bcp\b|\btruncate\b"
    r"|\bsed\b[^|;&\n]*\s-i|\bchmod\b|\bchattr\b|\bln\b|\bdd\b|\bpatch\b"
    r"|\bgit\s+(?:checkout|restore|rm|clean|reset|update-index)\b"
    r"|\bpython3?\b[^|;&\n]*\s-c\s|\bperl\b[^|;&\n]*\s-[ip]"
    r")"
)

VALIDATOR_REL = ".claude/skills/weekly-fintech-deals/validate_deals.py"
INPUTS_RE = re.compile(r"(?:^|/)weekly-deals/inputs/deals_[^/]*\.json$")


def deny(message):
    sys.stderr.write(message + "\n")
    sys.exit(2)


def project_root(payload):
    return os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()


def is_locked(path, root):
    ap = path if os.path.isabs(path) else os.path.join(root, path)
    ap = os.path.normpath(ap).replace(os.sep, "/")
    rel = os.path.relpath(ap, root).replace(os.sep, "/")
    cand = ap if rel.startswith("..") else rel
    if cand in LOCKED_FILES or any(cand == d or cand.startswith(d + "/") for d in LOCKED_DIRS):
        return True
    if rel.startswith(".."):  # path spelled from outside the project root
        return any(ap.endswith("/" + f) for f in LOCKED_FILES) or any(
            "/" + d + "/" in ap or ap.endswith("/" + d) for d in LOCKED_DIRS)
    return False


def pre(payload):
    tool = payload.get("tool_name", "")
    ti = payload.get("tool_input") or {}
    root = project_root(payload)
    if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        path = ti.get("file_path") or ti.get("notebook_path") or ""
        if path and is_locked(path, root):
            deny(
                f"BLOCKED by deals_guard: '{path}' is locked weekly-deals enforcement "
                f"infrastructure (validator / builder / hooks / citation manifests). "
                f"It exists precisely so the locked rules ($25M raise floor, week window, "
                f"deal-type enum, citation trail) cannot be relaxed in-session. If this "
                f"change is genuinely intended, the human owner must disable the guard "
                f"first (/hooks, or edit .claude/settings.json outside a session)."
            )
    elif tool == "Bash":
        cmd = ti.get("command", "") or ""
        # git trailers like "Co-Authored-By: X <a@b.c>" are text, not redirects
        scrubbed = re.sub(r"<[^<>\s]+@[^<>\s]+>", "", cmd)
        if any(t in cmd for t in BASH_TOKENS) and MUTATION.search(scrubbed):
            deny(
                "BLOCKED by deals_guard: this command combines a locked weekly-deals "
                "enforcement path with a write/mutation pattern. Executing the builder/"
                "validator and reading these files is fine; modifying, deleting, or "
                "git-reverting them is a human-only change (disable the guard via /hooks "
                "first). If this is a false positive (e.g. an output redirect in the same "
                "command), rerun without the mutating part."
            )
    sys.exit(0)


def post(payload):
    tool = payload.get("tool_name", "")
    ti = payload.get("tool_input") or {}
    if tool not in ("Write", "Edit", "MultiEdit"):
        sys.exit(0)
    path = ti.get("file_path") or ""
    if not INPUTS_RE.search(path.replace(os.sep, "/")):
        sys.exit(0)
    root = project_root(payload)
    abs_path = path if os.path.isabs(path) else os.path.join(root, path)
    validator = os.path.join(root, VALIDATOR_REL)
    result = subprocess.run(
        [sys.executable, validator, abs_path],
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0:
        sys.stderr.write(
            f"deals_guard: {path} violates the locked weekly-deals rules — fix the "
            f"data (do NOT touch the validator):\n{result.stdout}{result.stderr}"
        )
        sys.exit(2)
    sys.exit(0)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)  # fail open: never brick unrelated work on a malformed payload
    try:
        if mode == "pre":
            pre(payload)
        elif mode == "post":
            post(payload)
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)  # fail open (git history is the backstop)
    sys.exit(0)


if __name__ == "__main__":
    main()
