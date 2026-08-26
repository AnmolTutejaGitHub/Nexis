from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from utils.ui import tool_format as fmt

console = Console()

# COLOURS
AGENT_COLOR       = "#a78bfa"
TOOL_COLOR        = "#f59e0b"
ERROR_COLOR       = "#f87171"
CALL_TEXT_COLOR   = "#9ca3af"
RESULT_TEXT_COLOR = "#6b7280"
USER_COLOR        = "#60a5fa"
REMOVED_COLOR     = "red"
ADDED_COLOR       = "#34d399"

# Symbols
AGENT_SYMBOL       = "· Nexis"
TOOL_CALL_SYMBOL   = "."
TOOL_RESULT_SYMBOL = "_"
ERROR_SYMBOL       = "✗"
PROMPT_SYMBOL      = "›"
SEPARATOR          = "·"

BANNER = [
    ("███╗   ██╗███████╗██╗  ██╗██╗███████╗", "#c4b5fd"),
    ("████╗  ██║██╔════╝╚██╗██╔╝██║██╔════╝", "#b5a0fb"),
    ("██╔██╗ ██║█████╗   ╚███╔╝ ██║███████╗", "#a78bfa"),
    ("██║╚██╗██║██╔══╝   ██╔██╗ ██║╚════██║", "#9061f5"),
    ("██║ ╚████║███████╗██╔╝ ██╗██║███████║", "#7c3aed"),
    ("╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝", "#6d28d9"),
]

def print_banner():
    console.print()
    for line, shade in BANNER:
        console.print(Text(line, style=shade))

def print_agent(content):
    if not content:
        return
    console.print()
    console.print(Text(f"{AGENT_SYMBOL}", style=f"bold {AGENT_COLOR}"))
    console.print(Markdown(str(content).strip()))
    console.print()

def print_tool_call(name, args):
    line = Text("  ")
    line.append(f"{TOOL_CALL_SYMBOL} ", style=TOOL_COLOR)
    line.append(fmt.call_line(name, args), style=f"bold {CALL_TEXT_COLOR}")
    console.print(line)

def print_tool_result(result, name="", params=None):
    summary = fmt.summarize(name, result)

    line = Text("    ")
    line.append(f"{TOOL_RESULT_SYMBOL} ", style=RESULT_TEXT_COLOR)
    if name:
        line.append(f"{fmt.call_line(name, params)} {SEPARATOR} ", style=RESULT_TEXT_COLOR)
    line.append(summary, style=RESULT_TEXT_COLOR)
    console.print(line)

    for preview_line in fmt.preview(name, result):
        console.print(Text(f"      {preview_line}", style=RESULT_TEXT_COLOR))

def print_error(error):
    console.print()
    console.print(Text(f"{ERROR_SYMBOL} {str(error).strip()}", style=ERROR_COLOR))
    console.print()

def print_token_usage(usage):
    details = usage.prompt_tokens_details
    cached = details.cached_tokens if details else 0

    parts = [f"{usage.prompt_tokens} in", f"{usage.completion_tokens} out"]
    if cached:
        parts.append(f"{cached} cached")

    console.print(Text("    " + f" {SEPARATOR} ".join(parts), style=RESULT_TEXT_COLOR))


def _render_diff(path: str, old_str: str, new_str: str) -> None:
    diff_text = Text()

    for line in old_str.splitlines():
        diff_text.append(f"- {line}\n", style=f"bold {REMOVED_COLOR}")
    for line in new_str.splitlines():
        diff_text.append(f"+ {line}\n", style=f"bold {ADDED_COLOR}")

    console.print(Panel(
        diff_text,
        title=f"[bold {TOOL_COLOR}]Edit Preview — {path}[/]",
        border_style=TOOL_COLOR,
        padding=(0,1)
    ))


def show_preview(params: dict) -> None:
    path = params.get("path", "")
    old_str = params.get("old_str", "")
    new_str = params.get("new_str", "")

    if not old_str:
        try:
            with open(path, "r", encoding="utf-8") as f:
                old_str = f.read()
        except OSError:
            old_str = ""

    _render_diff(path, old_str, new_str)


def user_input():
    console.print(Text(f"{PROMPT_SYMBOL} ", style=f"bold {AGENT_COLOR}"), end="")
    return input()

def ask_permission(question: str) -> bool:
    print_agent(question)
    permission = console.input(f"[bold {USER_COLOR}]You[/bold {USER_COLOR}] (y/n) ")

    return permission.strip().lower() in ("y", "yes")