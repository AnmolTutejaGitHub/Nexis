from typing import TypedDict
import litellm
from langgraph.graph import END, START, StateGraph
from config import config
from tools.tool_registry import get_tool_schemas
from utils.ui.print_utils import print_token_usage
from utils.prune_messages import prune_messages
from utils.run_tool_calls import run_tool_calls
from events.event_bus import EventBus
from events.types import AgentMessage, Error

# REFERENCE = https://docs.litellm.ai/docs/completion/drop_params needed for prompt cache uuid param (openai compatible apis)
litellm.drop_params = True

class State(TypedDict):
    messages: list
    bus: EventBus


def last_assistant_msg(messages):
    for msg in reversed(messages):
        if msg.get("role") == "assistant":
            return msg


def agent(state):
    messages = prune_messages(list(state["messages"]))
    tools = get_tool_schemas()

    try:
        response = litellm.completion(
            model=config.LLM,
            messages=messages,
            tools=tools,
            api_key=config.LLM_API_KEY,
            prompt_cache_key=config.PROMPT_CACHING_UUID,
        )
        print_token_usage(response.usage) #per call not per loop
        message = response.choices[0].message
        msg = {"role": message.role}

        if message.content:
            msg["content"] = message.content

        if message.tool_calls:
            tool_calls = []
            for call in message.tool_calls:
                tool_calls.append({
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments,
                    },
                })
            msg["tool_calls"] = tool_calls

        if message.tool_calls and message.content:
            # print_agent(message.content)
            state["bus"].emit(AgentMessage(message.content))

        messages.append(msg)
        return {"messages": messages}

    except Exception as e:
        # print_error(str(e))
        state["bus"].emit(Error(str(e)))
        return {"stop": True}


def tools(state):
    msg = last_assistant_msg(state["messages"])
    if not msg or not msg.get("tool_calls"):
        return {}

    tool_results = run_tool_calls(msg["tool_calls"], state["bus"])

    messages = list(state["messages"])
    messages.extend(tool_results)
    return {"messages": messages}


def route(state):
    if state.get("stop"):
        return END

    msg = last_assistant_msg(state["messages"])
    if not msg or not msg.get("tool_calls"):
        if msg and msg.get("content"):
            # print_agent(msg["content"])
            state["bus"].emit(AgentMessage(msg["content"]))
        return END

    return "tools"


graph = StateGraph(State)
graph.add_node("agent", agent)
graph.add_node("tools", tools)
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", route)
graph.add_edge("tools", "agent")
graph = graph.compile()
