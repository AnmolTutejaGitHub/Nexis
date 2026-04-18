import json
from tools.tool_registry import function_call

def run_tool_calls(tool_calls):
    results = []
    for call in tool_calls:
        name = call.function.name
        args = json.loads(call.function.arguments)

        print(f"\n[TOOL] {name}({args})")
        result = function_call(name,args)
        print(f"\n[TOOL RESULT] {result}")

        results.append({
            "role": "tool",
            "tool_call_id": call.id,
            "name": name,
            "content": json.dumps(result)
        })

    return results