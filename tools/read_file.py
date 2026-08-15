import os

DEFAULT_LIMIT = 400

def read_file(path, limit=DEFAULT_LIMIT):
    if os.path.isdir(path):
        return f"Error: not a file: {path}. Use list_files for a directory."

    try:
        with open(path, "r") as f:
            lines = f.readlines()
    except Exception as e:
        return f"Error: {str(e)[:500]}"

    body = "".join(lines[:limit])

    if len(lines) > limit:
        return (
            f"{path} (showing first {limit} of {len(lines)} lines)\n{body}"
            f"\n(Use read_file_range for a specific section, get_repomap for the "
            f"structure, or call again with a higher limit.)"
        )

    return f"{path}\n{body}"


def read_file_range(path, start_line, end_line):
    try:
        with open(path, "r") as f:
            lines = f.readlines()
    except Exception as e:
        return f"Error: {str(e)[:500]}"

    start = max(0, start_line - 1)
    end = min(len(lines), end_line)

    return f"{path} lines {start_line}-{end_line}\n" + "".join(lines[start:end])