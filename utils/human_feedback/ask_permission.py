from utils.print_utils import print_agent, print_user_prompt

def ask_permission(question: str) -> bool:
    print_agent(question)
    print_user_prompt()
    permission = input()

    if permission.strip().lower() in ["y","yes"]:
        return True
    return False
