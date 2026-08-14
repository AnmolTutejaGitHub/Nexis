import glob
import os


def glob_files(pattern: str, path: str = "."):
    """Find files matching a glob pattern. (works for both relative/abs)"""
    try:
        matches = glob.glob(os.path.join(path, pattern), recursive=True)
    except Exception as e:
        return f"Error: {e}"
    if not matches:
        return f"No files found matching pattern: {pattern}"
    return "\n".join(sorted(matches))
