from utils.print_utils import print_agent, console

def ask_permission(question: str) -> bool:
    print_agent(question)
    permission = console.input("[bold #60a5fa]You[/bold #60a5fa] (y/n) ")

    if permission.strip().lower() in ["y", "yes"]:
        return True
    return False
