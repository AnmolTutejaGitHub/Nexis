from events.types import PreToolUse, PostToolUse, AgentMessage, Error
from utils.ui.print_utils import print_tool_call, print_tool_result, print_agent, print_error

def show_tool_call(event):
    print_tool_call(event.tool_name, event.tool_params)

def show_tool_result(event):
    print_tool_result(event.result, event.tool_name, event.tool_params)

def show_agent_message(event):
    print_agent(event.text)

def show_error(event):
    print_error(event.message)


def register_ui_listeners(bus):
    bus.on(PreToolUse, show_tool_call)
    bus.on(PostToolUse, show_tool_result)
    bus.on(AgentMessage, show_agent_message)
    bus.on(Error, show_error)