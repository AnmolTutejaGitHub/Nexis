from dotenv import load_dotenv

load_dotenv()

from config import config
from graph import graph
from prompts.build_system_prompt import build_system_prompt
from utils.print_utils import print_banner, user_input

from events.event_bus import EventBus
from events.listeners.ui import register_ui_listeners
from events.listeners.permission import register_permission_listener

def main():
    print_banner()

    bus = EventBus()
    register_ui_listeners(bus)
    register_permission_listener(bus)
    
    messages = [{"role": "system", "content": build_system_prompt()}]

    while True:
        input_prompt = user_input()
        messages.append({"role": "user", "content": input_prompt})

        result = graph.invoke(
            {"messages": messages, "bus": bus},
            config={"recursion_limit": config.max_iters * 3},
        )
        messages = result["messages"]

if __name__ == "__main__":
    main()
