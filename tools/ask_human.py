from utils.print_utils import print_agent, console


def ask_human(query):
    print_agent(query)
    console.print("[bold #60a5fa]You[/bold #60a5fa]", end=" ")
    human_response = input()
    return human_response