from tools.bash_access import bash_access
from tools.create_path import create_path
from tools.delete_path import delete_path
from tools.edit_file import edit_file
from tools.list_files import list_files
from tools.read_file import read_file
from tools.semantic_search import semantic_search
from tools.update_file import update_file
from tools.web_search import web_search


TOOL_REGISTRY = {
    "read_file": {
        "fn": read_file,
        "schema": {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read the full contents of a file. Always call this before edit_file so you have the exact text to use as old_str.",
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

    "edit_file": {
        "fn": edit_file,
        "schema": {
            "type": "function",
            "function": {
                "name": "edit_file",
                "description": "Surgically edit a file by replacing an exact string match. Call read_file first. old_str must be an exact copy (including indentation) and must appear exactly once in the file.",
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
                "description": "List all files and folders inside a directory (one level deep).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Absolute or relative directory path to list."}
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