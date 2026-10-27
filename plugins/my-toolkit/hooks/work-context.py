#!/usr/bin/env python3
# Re-injects work state (branches, pending changes, task notes) at session start and after compaction.
import json
import os
import re
import subprocess
import sys

BASE_BRANCHES = {"main", "master", "qa", "develop", "dev", "staging", "prod", "production"}
MAX_TASK_LINES = 40
MAX_OUTPUT_CHARS = 6000


def git(repo, *args):
    try:
        result = subprocess.run(
            ["git", "--no-optional-locks", "-C", repo, *args],
            capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def repo_state(repo):
    branch = git(repo, "branch", "--show-current") or "(detached)"
    status = git(repo, "status", "--porcelain") or ""
    changed = [line for line in status.splitlines() if line.strip()]
    return {"path": repo, "name": os.path.basename(repo), "branch": branch, "changed": changed}


def is_work(state):
    return state["branch"] not in BASE_BRANCHES or bool(state["changed"])


def child_repos(folder):
    try:
        entries = os.listdir(folder)
    except OSError:
        return []
    return sorted(
        os.path.join(folder, entry) for entry in entries
        if os.path.isdir(os.path.join(folder, entry, ".git"))
    )


def find_workspace(cwd):
    # Returns (mode, repos, tasks_dir); a folder holding several repos shares one docs/tasks.
    top = git(cwd, "rev-parse", "--show-toplevel")
    if top:
        parent = os.path.dirname(top)
        if len(child_repos(parent)) >= 2:
            return "repo", [top], os.path.join(parent, "docs", "tasks")
        return "repo", [top], os.path.join(top, ".claude", "tasks")
    return "workspace", child_repos(cwd), os.path.join(cwd, "docs", "tasks")


def load_tasks(tasks_dir):
    tasks = []
    if not os.path.isdir(tasks_dir):
        return tasks
    for entry in sorted(os.listdir(tasks_dir)):
        path = os.path.join(tasks_dir, entry)
        if not entry.endswith(".md") or not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8", errors="replace") as handle:
            text = handle.read()
        match = re.search(r"^\s*(?:Ramas|Branches)\s*:\s*(.+)$", text, re.IGNORECASE | re.MULTILINE)
        refs = re.split(r"[,\s]+", match.group(1).strip()) if match else []
        tasks.append({"path": path, "slug": entry[:-3], "refs": [r for r in refs if r], "text": text})
    return tasks


def task_matches(task, state):
    slug = state["branch"].rsplit("/", 1)[-1]
    if task["slug"] == slug:
        return True
    for ref in task["refs"]:
        repo, _, branch = ref.rpartition("@")
        if branch == state["branch"] and (not repo or repo == state["name"]):
            return True
    return False


def build_report(cwd):
    mode, repos, tasks_dir = find_workspace(cwd)
    states = [repo_state(repo) for repo in repos]
    work = [s for s in states if is_work(s)]
    if not work:
        return ""

    lines = [f"Work context ({mode}: {cwd})"]
    for s in work:
        lines.append(f"- {s['name']}: branch {s['branch']}, {len(s['changed'])} uncommitted file(s)")
        for change in s["changed"][:10]:
            lines.append(f"    {change}")
        if len(s["changed"]) > 10:
            lines.append(f"    ... {len(s['changed']) - 10} more")
    skipped = len(states) - len(work)
    if skipped:
        lines.append(f"- {skipped} other repo(s) on a base branch with no changes (omitted)")

    if mode == "repo":
        log = git(repos[0], "log", "--oneline", "-5")
        if log:
            lines.append("Recent commits:")
            lines.extend(f"    {line}" for line in log.splitlines())

    tasks = load_tasks(tasks_dir)
    shown = set()
    for s in work:
        if s["branch"] in BASE_BRANCHES:
            continue
        matched = [t for t in tasks if task_matches(t, s)]
        if not matched:
            slug = s["branch"].rsplit("/", 1)[-1]
            lines.append(f"No task notes for {s['name']}@{s['branch']} (expected {os.path.join(tasks_dir, slug + '.md')})")
        for task in matched:
            if task["path"] in shown:
                continue
            shown.add(task["path"])
            body = task["text"].strip().splitlines()
            lines.append(f"Task notes ({task['path']}):")
            lines.extend(f"    {line}" for line in body[:MAX_TASK_LINES])
            if len(body) > MAX_TASK_LINES:
                lines.append(f"    ... truncated, {len(body) - MAX_TASK_LINES} more line(s) in the file")

    on_work_branch = any(s["branch"] not in BASE_BRANCHES for s in work)
    if on_work_branch and mode == "repo" and tasks_dir.startswith(repos[0] + os.sep):
        probe = os.path.join(tasks_dir, "probe.md")
        if git(repos[0], "check-ignore", "-q", "--no-index", probe) is None:
            lines.append(f"{os.path.relpath(tasks_dir, repos[0])}/ is not in .gitignore")

    report = "\n".join(lines)
    return report[:MAX_OUTPUT_CHARS]


def main():
    try:
        payload = json.load(sys.stdin)
        cwd = payload.get("cwd") or os.getcwd()
        report = build_report(cwd)
    except Exception:
        return
    if report:
        print(json.dumps({
            "hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": report}
        }))


if __name__ == "__main__":
    main()
