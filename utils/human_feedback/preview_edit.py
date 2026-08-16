from utils.print_utils import console, print_agent, print_user_prompt
from rich.panel import Panel
from rich.text import Text


def render_diff(path: str, old_str: str, new_str: str) -> None:
    diff_text = Text()

    for line in old_str.splitlines():
        diff_text.append(f"- {line}\n",style="bold red")
    for line in new_str.splitlines():
        diff_text.append(f"+ {line}\n", style="bold #34d399")

    console.print(Panel(
        diff_text,
        title=f"[bold #f59e0b]Edit Preview — {path}[/]",
        border_style="#f59e0b",
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

    render_diff(path, old_str, new_str)


def preview_edit(path: str,old_str: str,new_str: str) -> bool:
    render_diff(path, old_str, new_str)

    print_agent("Accept this edit? (y/n)")
    print_user_prompt()
    answer = input().strip().lower()
    return answer in ("y", "yes")