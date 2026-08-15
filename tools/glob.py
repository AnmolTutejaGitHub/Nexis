"""
Find file names matching a pattern.

Backed by `rg --files`, which lists the files ripgrep would search without reading
any of them. The value is ripgrep's directory walker: it honours .gitignore at every
level and never descends into ignored directories, so node_modules, dist and target
cost nothing and drop out for free.

Python's glob is the fallback when rg is missing. Same results, minus the gitignore
awareness, so the tool degrades instead of breaking.
"""

# REFERENCE:  https://github.com/anomalyco/opencode/blob/4643e65ad6/packages/opencode/src/tool/glob.ts#L49-L61 and 
# https://github.com/anomalyco/opencode/blob/4643e65ad6/packages/core/src/ripgrep.ts#L155-L170

import glob
import os
import shutil
import subprocess

DEFAULT_LIMIT = 100


def find_with_ripgrep(pattern, path, include_ignored):
    rg = shutil.which("rg")

    if not rg:
        return None

    command = [
        rg,
        "--no-config",
        "--files",
        "--glob", pattern,
        "--glob", "!**/.git/**",
    ]

    if include_ignored:
        command.extend(["--hidden", "--no-ignore"])

    command.append(".")

    try:
        result = subprocess.run(
            command,
            cwd=path,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except Exception:
        return None

    if result.returncode not in (0, 1): # 0 - matches found, 1 - no matches, anything else - error/failure
        return None

    return result.stdout.splitlines()


def find_with_python(pattern, path):
    matches = glob.glob(os.path.join(path, pattern), recursive=True)

    return [
        os.path.join(".", os.path.relpath(match, path))
        for match in matches
    ]


def glob_files(pattern: str, path: str = ".", limit: int = DEFAULT_LIMIT, include_ignored: bool = False):
    """Find files matching a glob pattern."""

    if not os.path.isdir(path):
        return f"Error: not a directory: {path}"

    try:
        matches = find_with_ripgrep(pattern, path, include_ignored)

        if matches is None:
            matches = find_with_python(pattern, path)

    except Exception as error:
        return f"Error: {error}"

    if not matches:
        return f"No files found matching pattern: {pattern}"

    matches = sorted(matches)

    if len(matches) > limit:
        return (
            "\n".join(matches[:limit])
            + f"\n(Results are truncated: showing first {limit} "
              f"of {len(matches)} results. Use a more specific path "
              "or pattern, or call again with a higher limit if you "
              "need the rest.)"
        )

    return "\n".join(matches)