import json
from tools.tool_registry import function_call
from utils.print_utils import print_tool_call, print_tool_result

def run_tool_calls(tool_calls):
    results = []
    for call in tool_calls:
        name = call.function.name
        args = json.loads(call.function.arguments)

        print_tool_call(name,args)
        result = function_call(name,args)
        print_tool_result(result)

        results.append({
            "role": "tool",
            "tool_call_id": call.id,
            "name": name,
            "content": json.dumps(result)
        })

    return results