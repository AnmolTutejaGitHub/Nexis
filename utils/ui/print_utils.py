from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
from rich.align import Align

from utils.ui import tool_format as fmt

console = Console()

# COLOURS - Everforest Dark 
AGENT_COLOR       = "#a7c080"
TOOL_COLOR        = "#c1be7f"
ERROR_COLOR       = "#e67e80"
CALL_TEXT_COLOR   = "#9da9a0"
RESULT_TEXT_COLOR = "#7a8478"
USER_COLOR        = "#a7c080"
REMOVED_COLOR     = "#e67e80"
ADDED_COLOR       = "#a7c080"

# COLOURS — Gruvbox Dark
# AGENT_COLOR       = "#83a598"
# TOOL_COLOR        = "#fabd2f"
# ERROR_COLOR       = "#fb4934"
# CALL_TEXT_COLOR   = "#a89984"
# RESULT_TEXT_COLOR = "#928374"
# USER_COLOR        = "#83a598"
# REMOVED_COLOR     = "#fb4934"
# ADDED_COLOR       = "#b8bb26"

# Symbols
AGENT_SYMBOL       = "Nexis"
TOOL_CALL_SYMBOL   = "⏺"
TOOL_RESULT_SYMBOL = "_"
ERROR_SYMBOL       = "✗"
PROMPT_SYMBOL      = "❯"
SEPARATOR          = "·"

# BANNER = [
#     ("███╗   ██╗███████╗██╗  ██╗██╗███████╗", "#83c092"),
#     ("████╗  ██║██╔════╝╚██╗██╔╝██║██╔════╝", "#91c08b"),
#     ("██╔██╗ ██║█████╗   ╚███╔╝ ██║███████╗", "#a0c084"),
#     ("██║╚██╗██║██╔══╝   ██╔██╗ ██║╚════██║", "#b1bf80"),
#     ("██║ ╚████║███████╗██╔╝ ██╗██║███████║", "#c6be7f"),
#     ("╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝", "#dbbc7f"),
# ]
# def print_banner():
#     console.print()
#     for line, shade in BANNER:
#         console.print(Text(line, style=shade))

BANNER = [
    "███╗   ██╗███████╗██╗  ██╗██╗███████╗",
    "████╗  ██║██╔════╝╚██╗██╔╝██║██╔════╝",
    "██╔██╗ ██║█████╗   ╚███╔╝ ██║███████╗",
    "██║╚██╗██║██╔══╝   ██╔██╗ ██║╚════██║",
    "██║ ╚████║███████╗██╔╝ ██╗██║███████║",
    "╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝",
]

def print_banner():
    console.print()
    console.print(Align.center(Text("\n".join(BANNER), style=AGENT_COLOR)))
    console.print()

def spinner(label="thinking"):
    return console.status(
        Text(f"{label}…", style=RESULT_TEXT_COLOR),
        spinner="dots",
        spinner_style=AGENT_COLOR,
    )

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


def _render_diff(path: str, changes: list) -> None:
    header = Text("    ")
    header.append(f"{TOOL_RESULT_SYMBOL} ", style=RESULT_TEXT_COLOR)
    header.append(path, style=RESULT_TEXT_COLOR)
    console.print(header)

    for index, (old_str, new_str) in enumerate(changes):
        if index:
            console.print()
        for line in old_str.splitlines():
            console.print(Text(f"      - {line}", style=REMOVED_COLOR))
        for line in new_str.splitlines():
            console.print(Text(f"      + {line}", style=ADDED_COLOR))


def show_preview(params: dict) -> None:
    path = params.get("path", "")
    edits = params.get("edits") or [
        {"old_str": params.get("old_str", ""), "new_str": params.get("new_str", "")}
    ]

    changes = []
    for edit in edits:
        old_str = edit.get("old_str", "")
        new_str = edit.get("new_str", "")

        # An empty old_str overwrites the file, so diff against what is there now.
        if not old_str:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    old_str = f.read()
            except OSError:
                old_str = ""

        changes.append((old_str, new_str))

    _render_diff(path, changes)


def user_input():
    console.print(Text(f"{PROMPT_SYMBOL} ", style=f"bold {AGENT_COLOR}"), end="")
    return input()

def ask_permission(question: str) -> bool:
    print_agent(question)
    permission = console.input(
        f"[bold {USER_COLOR}]{PROMPT_SYMBOL}[/bold {USER_COLOR}] "
        f"[{RESULT_TEXT_COLOR}](y/n)[/{RESULT_TEXT_COLOR}] "
    )
    return permission.strip().lower() in ("y", "yes")