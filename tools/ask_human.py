from utils.print_utils import print_agent, console

def ask_human(query):
    print_agent(query)
    human_response = console.input("[bold #60a5fa]You[/bold #60a5fa] ")
    return human_response