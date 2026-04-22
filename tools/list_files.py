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
]


def is_excluded(name):
    for pattern in DEFAULT_EXCLUDE_PATTERNS:
        if fnmatch.fnmatch(name,pattern):
            return True
    return False


def list_files(path,include_hidden=False,include_ignored=False):
    try:
        items = os.listdir(path)

        result = []
        skipped = []
        for name in items:
            if not include_ignored and is_excluded(name):
                skipped.append(name)
                continue

            if not include_hidden and name.startswith("."):
                skipped.append(name)
                continue

            full_path = os.path.join(path, name)
            result.append({
                "name": name,
                "full_path": full_path,
                "type": "dir" if os.path.isdir(full_path) else "file"
            })

        return {
            "success": True,
            "path": path,
            "items": result,
            # "skipped": skipped
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }