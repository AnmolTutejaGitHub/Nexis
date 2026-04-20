import json
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

console = Console()


def print_banner():
    console.print(Align.center("""
[bold #a78bfa]
███╗   ██╗███████╗██╗  ██╗██╗███████╗
████╗  ██║██╔════╝╚██╗██╔╝██║██╔════╝
██╔██╗ ██║█████╗   ╚███╔╝ ██║███████╗
██║╚██╗██║██╔══╝   ██╔██╗ ██║╚════██║
██║ ╚████║███████╗██╔╝ ██╗██║███████║
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝
[/]
"""))


def print_tool_call(name, args):
    console.print(Panel(
        f"{name}({args})",
        title="[bold #f59e0b]TOOL[/]",
        border_style="#f59e0b",
        padding=(0,1)
    ))


def print_tool_result(result):
    console.print(Panel(
        Text(_format_json(result),style="dim"),
        title="[bold #34d399]TOOL RESULT[/]",
        border_style="#34d399",
        padding=(0,1)
    ))


def print_agent(content):
    console.print(Panel(
        content,
        title="[bold #a78bfa]Nexis[/]",
        border_style="#a78bfa",
        padding=(0,1)
    ))


def print_error(error):
    console.print(Panel(
        _format_json(error),
        title="[bold red]Error[/]",
        border_style="red",
        padding=(0,1)
    ))

def print_user_prompt():
    console.print("[bold #60a5fa]You[/bold #60a5fa]", end=" ")


def user_input():
    console.print()
    print_user_prompt()
    console.print("[dim]Ask Nexis anything…[/dim]", end=" ")

    value = input()

    return value


def _format_json(data):
    if isinstance(data, (dict,list)):
        return json.dumps(data,indent=2,ensure_ascii=False)

    if isinstance(data, str):
        try:
            parsed = json.loads(data)
            if isinstance(parsed, (dict,list)):
                return json.dumps(parsed,indent=2,ensure_ascii=False)
        except Exception:
            pass
        return data

    return str(data)