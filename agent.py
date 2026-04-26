from dotenv import load_dotenv

load_dotenv()

from config import config
from graph import graph
from utils.print_utils import print_banner, user_input
from utils.prune_messages import prune_messages


def main():
    print_banner()

    messages = [{"role": "system", "content": config.system_prompt}]

    while True:
        input_prompt = user_input()
        messages.append({"role": "user", "content": input_prompt})

        result = graph.invoke(
            {"messages": messages},
            config={"recursion_limit": config.max_iters * 3},
        )
        messages = prune_messages(result["messages"])


if __name__ == "__main__":
    main()
