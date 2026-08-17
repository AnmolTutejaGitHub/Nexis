from tools.bash_access import bash_access
from tools.create_path import create_path
from tools.delete_path import delete_path
from tools.edit_file import edit_file
from tools.list_files import list_files
from tools.read_file import read_file
from tools.web_search import web_search
from tools.code_navigation.repomap.get_repomap import get_repomap
from tools.read_file import read_file_range
from tools.ask_human import ask_human
from tools.read_observation import read_observation
from tools.glob import glob_files
from tools.todowrite.todos import todo_write, DESCRIPTION as TODO_DESCRIPTION, STATUSES as TODO_STATUSES
from utils.human_feedback.preview_edit import show_preview


TOOL_REGISTRY = {
    "read_file": {
        "fn": read_file,
        "parallel_safe": True,
        "schema": {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read a file from the start. Returns up to 400 lines by default; if the file is longer the result says so, and you can pass a higher limit or use read_file_range for a specific section. Takes a file, not a directory — use list_files for a directory. Prefer read_file_range when you already know which part you need. Call in parallel when you want several files.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Absolute or relative path of the file to read."},
                        "limit": {"type": "integer", "description": "Maximum lines to return. Defaults to 400. Raise it only when you genuinely need more of a large file."}
                    },
                    "required": ["path"]
                }
            }
        }
    },

    "read_file_range": {
        "fn": read_file_range,
        "parallel_safe": True,
        "schema": {
            "type": "function",
            "function": {
                "name": "read_file_range",
                "description": "Read a specific range of lines from a file. Line numbers are 1-indexed and inclusive; a range past the end of the file is clamped rather than an error. get_repomap returns each symbol's start_line and end_line — pass those here to read just one function or class instead of the whole file. Always read the target lines before edit_file so you have the exact text for old_str. Call in parallel when you need ranges from several files.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Absolute or relative path of the file to read."},
                        "start_line": {"type": "integer", "description": "Start line number (inclusive)."},
                        "end_line": {"type": "integer", "description": "End line number (inclusive)."}
                    },
                    "required": ["path", "start_line", "end_line"]
                }
            }
        }
    },

    "edit_file": {
        "fn": edit_file,
        "parallel_safe": False,
        "approval": lambda params: (show_preview(params), "Accept this edit? (y/n)")[1],
        "schema": {
            "type": "function",
            "function": {
                "name": "edit_file",
                "description": "Edit a file by replacing an exact string match, or overwrite the whole file when old_str is empty. old_str must appear EXACTLY ONCE — include surrounding lines to make it unique, or the edit is rejected and you are shown the ambiguous region. Read the target lines first so old_str matches byte for byte, including indentation. The user sees a diff and can reject the edit.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Absolute or relative path of the file to edit."},
                        "old_str": {"type": "string", "description": "The exact text to find and replace. Leave empty to overwrite the whole file."},
                        "new_str": {"type": "string", "description": "The replacement text or full new file content."}
                    },
                    "required": ["path", "new_str"]
                }
            }
        }
    },

    "create_path": {
        "fn": create_path,
        "parallel_safe": False,
        "schema": {
            "type": "function",
            "function": {
                "name": "create_path",
                "description": "Create a new file (with optional content) or a new directory. The parent directory must already exist — create it first with type 'folder' if it does not. Use edit_file to change a file that already exists.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Absolute or relative path to create."},
                        "type": {"type": "string", "enum": ["file", "folder"], "description": "'file' or 'folder'."},
                        "content": {"type": "string", "description": "Initial file content (ignored for folders)."}
                    },
                    "required": ["path"]
                }
            }
        }
    },

    "delete_path": {
        "fn": delete_path,
        "parallel_safe": False,
        "approval": "About to delete\n{path}\nAllow? (y/n)",
        "schema": {
            "type": "function",
            "function": {
                "name": "delete_path",
                "description": "Permanently delete a file or directory; directories go recursively and there is no undo. The user is asked to confirm. Only delete when the user asked for it — do not clean up files you merely think are unused.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Absolute or relative path to delete."}
                    },
                    "required": ["path"]
                }
            }
        }
    },

    "list_files": {
        "fn": list_files,
        "parallel_safe": True,
        "schema": {
            "type": "function",
            "function": {
                "name": "list_files",
                "description": "List the contents of one directory, one level deep. Directories end in '/' and files show their size, e.g. 'config.py (452b)' — use that to judge how expensive a file is to read. Build artefacts, caches, images and IDE folders are excluded by default and reported as a 'hidden' count; pass include_hidden or include_ignored to see them. Use glob_files to search recursively.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Absolute or relative directory path to list."
                        },
                        "include_hidden": {
                            "type": "boolean",
                            "description": "If true, include dot-files and dot-directories (e.g. .gitignore). Defaults to false."
                        },
                        "include_ignored": {
                            "type": "boolean",
                            "description": "If true, include paths that would normally be excluded (caches, build dirs, node_modules, etc.). Defaults to false."
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum entries to return. Defaults to 100. Raise it when you genuinely need the full listing of a large directory."
                        }
                    },
                    "required": ["path"]
                }
            }
        }
    },

    "bash_access": {
        "fn": bash_access,
        "parallel_safe": False,
        "approval": "About to run:\n{command}\nAllow? (y/n)",
        "schema": {
            "type": "function",
            "function": {
                "name": "bash_access",
                "description": "Execute a shell command. Full shell interpretation is available — chain independent probes with && or ; and filter with pipes to answer several questions in one call rather than several. Use for running tests, installing packages, or inspecting the environment. Avoid destructive commands.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "The shell command to execute."}
                    },
                    "required": ["command"]
                }
            }
        }
    },

    "web_search": {
        "fn": web_search,
        "parallel_safe": True,
        "schema": {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Search the web and return results. Use it when you need information that is not in this workspace: a library's current API, an unfamiliar error message, or a term, flag or tool you are not confident about. Do not use it for anything answerable by reading this project's code — read the code instead.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The search query string."}
                    },
                    "required": ["query"]
                }
            }
        }
    },
    
    "get_repomap": {
        "fn": get_repomap,
        "parallel_safe": True,
        "schema": {
            "type": "function",
            "function": {
                "name": "get_repomap",
                "description": "Get the structure of ONE source file that you already know exists — its functions, classes and imports with their line ranges — so you can decide which part of that file to read. Takes a single file path: it does not accept directories and is not a way to find files — use glob_files to locate a file. Don't call it on a small file, on a file you're going to read in full anyway, or on one you've already read.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Absolute or relative path of the file to get the repomap of."}
                    },
                    "required": ["path"]
                }
            }
        }
    },

    "ask_human": {
        "fn": ask_human,
        "parallel_safe": False,
        "schema": {
            "type": "function",
            "function": {
                "name": "ask_human",
                "description": "Ask the human user a clarifying question when you need more information to proceed. Use this when the task is ambiguous, you need a preference, or you need confirmation on a critical decision. Do NOT overuse — try to resolve uncertainties with available tools first.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The question to ask the human user."}
                    },
                    "required": ["query"]
                }
            }
        }
    },

    "read_observation": {
        "fn": read_observation,
        "parallel_safe": True,
        "schema": {
            "type": "function",
            "function": {
                "name": "read_observation",
                "description": "Read a saved full tool result by observation id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "observation_id": {"type": "string", "description": "Observation id from a summarized tool result."}
                    },
                    "required": ["observation_id"]
                }
            }
        }
    },
    "glob_files": {
        "fn": glob_files,
        "parallel_safe": True,
        "schema": {
            "type": "function",
            "function": {
                "name": "glob_files",
                "description": "Find files matching a glob pattern. Returns matching paths sorted, up to 100 by default. Files ignored by the project's .gitignore are skipped unless include_ignored is true. Patterns are gitignore-style, so '*.py' matches at any depth. Call in parallel when you have several independent patterns to try.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string",
                            "description": "The glob pattern to match (e.g. '**/*.py').",
                        },
                        "path": {
                            "type": "string",
                            "description": "The directory to search in. Defaults to current directory.",
                            "default": ".",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum results to return. Defaults to 100. Raise it when you genuinely need every match.",
                        },
                        "include_ignored": {
                            "type": "boolean",
                            "description": "If true, also search hidden files and paths excluded by .gitignore (node_modules, build output, virtualenvs). Defaults to false.",
                        },
                    },
                    "required": ["pattern"],
                },
            },
        }
    },

    "todo_write": {
        "fn": todo_write,
        "parallel_safe": True,
        "schema": {
            "type": "function",
            "function": {
                "name": "todo_write",
                "description": TODO_DESCRIPTION,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "todos": {
                            "type": "array",
                            "description": "The updated todo list",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "content": {
                                        "type": "string",
                                        "description": "Brief description of the task",
                                    },
                                    "status": {
                                        "type": "string",
                                        "enum": list(TODO_STATUSES),
                                        "description": "Current status of the task: " + ", ".join(TODO_STATUSES),
                                    },
                                },
                                "required": ["content", "status"],
                            },
                        }
                    },
                    "required": ["todos"],
                },
            },
        }
    },
}


def get_tool_schemas():
    return [entry["schema"] for entry in TOOL_REGISTRY.values()]

def function_call(tool_name: str, tool_args: dict):
    if tool_name not in TOOL_REGISTRY:
        return {
            "error": f"Unknown tool: '{tool_name}'. Available: {list(TOOL_REGISTRY.keys())}"
        }

    fn = TOOL_REGISTRY[tool_name]["fn"]

    try:
        result = fn(**tool_args)
        return result

    except Exception as e:
        return {
            "error": str(e)
        }

def get_tool_summary_for_prompt():
    lines = []
    for name, entry in TOOL_REGISTRY.items():
        fn_schema = entry["schema"]["function"]
        desc = fn_schema["description"].split(".")[0]
        params = list(fn_schema["parameters"]["properties"].keys())
        lines.append(f"- {name}({', '.join(params)}): {desc}")
    return "\n".join(lines)
