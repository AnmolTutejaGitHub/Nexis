from utils.print_utils import print_agent, print_user_prompt

def ask_human(query):
    print_agent(query)
    print_user_prompt()
    human_response = input()
    return human_response