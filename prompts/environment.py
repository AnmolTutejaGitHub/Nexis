"""
Environment context for the system prompt.
Without this the model has no idea where it is
"""
# REFERENCE: https://github.com/anomalyco/opencode/blob/4643e65ad6/packages/opencode/src/session/system.ts#L74-L82

import os
import platform
import subprocess
from datetime import date

from config import config
from prompts.scratchpad import scratchpad
from tools.list_files import list_files


def git_info(cwd):
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=cwd, capture_output=True, text=True, timeout=2,
        )
    except Exception:
        return None

    if result.returncode != 0:
        return None
    return result.stdout.strip()


def top_level(cwd):
    """Entry names only — list_files returns text, with the path on the first
    line, a trailing '(...)' note when it truncated or hid entries, and a size
    suffix on files that is noise for an orientation listing."""
    listing = list_files(cwd)
    if listing.startswith("Error:"):
        return []

    entries = []
    for line in listing.splitlines()[1:]:
        if line.startswith("("):
            continue
        entries.append(line.split(" (")[0])

    return entries


def environment_context(cwd=None):
    cwd = cwd or os.getcwd()
    branch = git_info(cwd)
    entries = top_level(cwd)

    lines = [
        f"You are powered by the model named {config.LLM.split('/')[-1]}. "
        f"The exact model ID is {config.LLM}",
        "Here is some useful information about the environment you are running in:",
        "<env>",
        f"  Working directory: {cwd}",
        f"  Is directory a git repo: {'yes' if branch else 'no'}",
        f"  Git branch: {branch}" if branch else None,
        f"  Platform: {platform.system()} {platform.release()}",
        f"  Home directory: {os.path.expanduser('~')}",
        f"  Scratch directory: {scratchpad()}",
        f"  Today's date: {date.today().strftime('%a %b %d %Y')}",
        f"  Top level of working directory: {', '.join(entries)}" if entries else None,
        "</env>",
    ]

    return "\n".join(line for line in lines if line)


