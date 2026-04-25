from tools.bash_access import bash_access
from tools.create_path import create_path
from tools.delete_path import delete_path
from tools.edit_file import edit_file
from tools.list_files import list_files
from tools.read_file import read_file
from tools.semantic_search import semantic_search
from tools.update_file import update_file
from tools.web_search import web_search
from tools.repomap.get_repomap import get_repomap
from tools.read_file import read_file_range
from tools.ask_human import ask_human
from tools.read_observation import read_observation


TOOL_REGISTRY = {
    "read_file": {
        "fn": read_file,
        "schema": {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read the full contents of a file. Use ONLY as a last resort when read_file_range cannot be used.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Absolute or relative path of the file to read."}
                    },
                    "required": ["path"]
                }
            }
        }
    },

    "read_file_range": {
        "fn": read_file_range,
        "schema": {
            "type": "function",
            "function": {
                "name": "read_file_range",
                "description": "Read a range of lines from a file. Always call this before edit_file so you have the exact text to use as old_str.",
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
        "schema": {
            "type": "function",
            "function": {
                "name": "edit_file",
                "description": "Surgically edit a file by replacing an exact string match. Call read_file_range or read_file first. old_str must be an exact copy (including indentation) and must appear exactly once in the file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Absolute or relative path of the file to edit."},
                        "old_str": {"type": "string", "description": "The exact text to find and replace. Include surrounding lines to make it unique."},
                        "new_str": {"type": "string", "description": "The replacement text. Keep correct indentation."}
                    },
                    "required": ["path", "old_str", "new_str"]
                }
            }
        }
    },

    "update_file": {
        "fn": update_file,
        "schema": {
            "type": "function",
            "function": {
                "name": "update_file",
                "description": "Overwrite a file with entirely new content. Use only when creating from scratch. For targeted changes use edit_file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Absolute or relative path of the file to overwrite."},
                        "content": {"type": "string", "description": "The full new content to write."}
                    },
                    "required": ["path", "content"]
                }
            }
        }
    },

    "create_path": {
        "fn": create_path,
        "schema": {
            "type": "function",
            "function": {
                "name": "create_path",
                "description": "Create a new file (with optional content) or a new directory.",
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
        "schema": {
            "type": "function",
            "function": {
                "name": "delete_path",
                "description": "Permanently delete a file or directory. Directories are deleted recursively.",
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
        "schema": {
            "type": "function",
            "function": {
                "name": "list_files",
                "description": "List files and folders inside a directory (one level deep). Common build artefacts, caches, dependency trees, and IDE folders are excluded by default.",
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
                        }
                    },
                    "required": ["path"]
                }
            }
        }
    },

    "bash_access": {
        "fn": bash_access,
        "schema": {
            "type": "function",
            "function": {
                "name": "bash_access",
                "description": "Execute a shell command. Use for running tests, installing packages, or inspecting the environment. Avoid destructive commands.",
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
        "schema": {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Search the web for up-to-date information such as docs, error explanations, or API references.",
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

    "semantic_search": {
        "fn": semantic_search,
        "schema": {
            "type": "function",
            "function": {
                "name": "semantic_search",
                "description": "Search the codebase semantically using vector embeddings. Finds conceptually related files even without exact keyword matches.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Natural language description of what you're looking for, e.g. 'authentication logic'."}
                    },
                    "required": ["query"]
                }
            }
        }
    },

    "get_repomap": {
        "fn": get_repomap,
        "schema": {
            "type": "function",
            "function": {
                "name": "get_repomap",
                "description": "Get the repomap of a file.",
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
