"""
The user's own instructions for a project: AGENTS.md, or CLAUDE.md.
If both AGENTS.md and CLAUDE.md present in a directory then AGENTS.md wins.

Final output is Anestors's agent.md then cwd's agent.md
"""

# REFERENCE: https://github.com/anomalyco/opencode/blob/4643e65ad6/packages/opencode/src/session/instruction.ts#L110-L135

import os
import subprocess

HOME = os.path.expanduser("~")

GLOBAL_PATHS = [
    os.path.join(HOME, ".nexis", "AGENTS.md"),
    os.path.join(HOME, ".claude", "CLAUDE.md"),
]

PROJECT_NAMES = ["AGENTS.md", "CLAUDE.md"]


def _git_root(cwd):
    """The repo containing cwd, or None when cwd is not in one."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd, capture_output=True, text=True, timeout=2,
        )
    except Exception:
        return None

    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _collect_upwards(name, start, stop):
    """Every `name` from stop down to start, outermost first.

    The search runs upward from start; the result is reversed so the nearest
    file ends up last and its instructions override the broader ones.

    Pass stop=None to search start alone: outside a repo there is no boundary,
    and climbing to / would pull in unrelated files.
    """
    found = []
    directory = os.path.realpath(start)
    stop = os.path.realpath(stop) if stop else directory

    while True:
        candidate = os.path.join(directory, name)
        if os.path.isfile(candidate):
            found.append(candidate)

        parent = os.path.dirname(directory)
        if directory == stop or parent == directory:
            break
        directory = parent

    found.reverse()
    return found


def _global_paths():
    """The first global instruction file that exists, if any."""
    for path in GLOBAL_PATHS:
        if os.path.isfile(path):
            return [path]

    return []


def _project_paths(cwd):
    """Paths where AGENTS.md/CLAUDE.md are found"""
    root = _git_root(cwd)

    for name in PROJECT_NAMES:
        found = _collect_upwards(name, cwd, root)
        if found:
            return found

    return []


def _all_paths(cwd=None):
    """Every file that applies here, global ones first."""
    cwd = cwd or os.getcwd()
    return _global_paths() + _project_paths(cwd)


def _read(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""


def render(cwd=None):
    """The files as one prompt section, or "" when there are none."""
    sections = []

    for path in _all_paths(cwd):
        content = _read(path)
        if content:
            sections.append(f"Instructions from {path}:\n{content}")

    if not sections:
        return ""

    return "# Project instructions\n" + "\n\n".join(sections)
