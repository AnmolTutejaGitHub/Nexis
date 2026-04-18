import json

def run_tool_calls(tool_calls):
    results = []
    for call in tool_calls:
        print(call)
        name = call.function.name
        args = json.loads(call.function.arguments)

        print(f"\n[TOOL] {name}({args})")
        result = function_call(name,args)
        print(f"[RESULT] {result}")

        results.append({
            "role": "tool",
            "tool_call_id": call.id,
            "name": name,
            "content": json.dumps(result)
        })
        
    return results