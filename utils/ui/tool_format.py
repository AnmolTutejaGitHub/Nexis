READS = {"read_file", "read_file_range"}

def call_line(name, args):
    pairs = ", ".join(f"{key}={value}" for key, value in (args or {}).items())
    return f"{name}({pairs})"


def summarize(name, result):
    count = len(str(result).splitlines())
    return f"{count} line" if count == 1 else f"{count} lines"


def preview(name, result):
    if name in READS:
        return []
    return str(result).splitlines()
