import fnmatch
import os

DEFAULT_EXCLUDE_PATTERNS = [
    ".git",
    ".svn",
    ".hg",

    ".venv",
    "venv",
    ".env",
    "env",
    ".tox",

    "*cache*",
    ".cache",

    "build",
    "dist",
    "out",
    "target",
    "bin",
    "obj", 

    "node_modules", 
    "vendor",  
    "Pods",  
    ".gradle", 

    "*.egg-info", 
    "*.dist-info",
    "*.egg",
    "*.whl",

    "*.o",
    "*.a",
    "*.so",
    "*.dylib",
    "*.dll",
    "*.lib",
    "*.pdb",
    "*.class",


    ".idea",
    ".vscode",
    ".vs",
    "*.iml",

    ".DS_Store",
    "Thumbs.db",

    ".terraform",
    ".next",
    ".nuxt",
    ".serverless",
    "coverage",
    "htmlcov",
    "*.log",

    ".turbo",
    ".vercel",
    ".svelte-kit",
    ".astro",
    ".ipynb_checkpoints",

    "*.pyc",
    "*.pyo",
    "*.min.js",
    "*.map",
    "*.snap",

    "*.png",
    "*.jpg",
    "*.jpeg",
    "*.gif",
    "*.ico",
    "*.webp",
    "*.svg",
    "*.pdf",
    "*.mp4",
    "*.mov",
    "*.mp3",
    "*.wav",

    "*.woff",
    "*.woff2",
    "*.ttf",
    "*.eot",

    "*.zip",
    "*.tar",
    "*.gz",
    "*.tgz",
    "*.7z",
    "*.rar",
    "*.jar",
]


LIMIT = 100


def is_excluded(name):
    for pattern in DEFAULT_EXCLUDE_PATTERNS:
        if fnmatch.fnmatch(name,pattern):
            return True
    return False


def list_files(path,include_hidden=False,include_ignored=False,limit=LIMIT):
    try:
        items = os.listdir(path)

        result = []
        skipped = []
        for name in sorted(items):
            if not include_ignored and is_excluded(name):
                skipped.append(name)
                continue

            if not include_hidden and name.startswith("."):
                skipped.append(name)
                continue

            full_path = os.path.join(path, name)

            if os.path.isdir(full_path):
                result.append(f"{name}/")
                continue

            try:
                result.append(f"{name} ({os.path.getsize(full_path)}b)")
            except OSError:
                result.append(name)

        lines = [path, *result[:limit]]

        if len(result) > limit:
            lines.append(
                f"(Showing first {limit} of {len(result)} entries. "
                "List a more specific path, or call again with a higher limit "
                "if you need the rest.)"
            )

        if skipped:
            lines.append(f"({len(skipped)} entries excluded as hidden or ignored)")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {str(e)[:500]}"
