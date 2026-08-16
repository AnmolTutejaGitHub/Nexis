from events.types import PreToolUse
from tools.tool_registry import TOOL_REGISTRY
from utils.human_feedback.ask_permission import ask_permission

def _question(event):
    tool = TOOL_REGISTRY.get(event.tool_name)
    template = tool.get("approval") if tool else None

    if template is None:
        return None
    
    if callable(template): # for edit tool
        return template(event.tool_params)

    try:
        return template.format(**event.tool_params)
    except KeyError:
        return f"About to run {event.tool_name}. Allow? (y/n)"
        

def ask_approval(event):
    question = _question(event)
    if question is None:
        return True
    return ask_permission(question)

def register_permission_listener(bus):
    bus.on_approval(ask_approval)