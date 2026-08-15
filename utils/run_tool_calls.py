"""
Run the model's tool calls in the order it asked for.

Walking the list, each run of back to back parallel-safe calls goes to the thread
pool as one batch, and each sequential call runs on its own. So for P P P S S P P
the order is: the three Ps together, then the first S, then the second S, then the
two Ps together.
"""

 # NOTE: In ThreadPoolExecutor, map runs the lambda once per call on its own thread and returns
 # results in input order, so the batch lines up with parallel_calls.
 # REFERENCE: https://docs.python.org/3/library/concurrent.futures.html


import json
from concurrent.futures import ThreadPoolExecutor
from tools.tool_registry import TOOL_REGISTRY, function_call
from utils.print_utils import print_tool_call, print_tool_result

MAX_WORKERS = 8

def is_parallel_safe(tool_name):
    tool = TOOL_REGISTRY.get(tool_name)
    return bool(tool and tool.get("parallel_safe"))


def run_tool_calls(tool_calls):
    calls = []

    for call in tool_calls:
        calls.append({
            "id": call["id"],
            "name": call["function"]["name"],
            "args": json.loads(call["function"]["arguments"]),
        })

    for call in calls:
        print_tool_call(call["name"], call["args"])

    results = []
    i = 0

    while i < len(calls):
        call = calls[i]

        if is_parallel_safe(call["name"]):
            parallel_calls = []

            while (i < len(calls) and is_parallel_safe(calls[i]["name"])):
                parallel_calls.append(calls[i])
                i+=1

            if len(parallel_calls) > 1:
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    batch_results = list(executor.map(
                        lambda call: function_call(call["name"], call["args"]),
                        parallel_calls,
                    ))
            else:
                call = parallel_calls[0]
                batch_results = [function_call(call["name"], call["args"])]

            results.extend(batch_results)

        else:
            results.append(
                function_call(call["name"],call["args"])
            )
            i += 1

    messages = []

    for i in range(len(calls)):
        call = calls[i]
        result = results[i]

        print_tool_result(result)

        messages.append({
            "role": "tool",
            "tool_call_id": call["id"],
            "name": call["name"],
            "content": (result if isinstance(result, str) else json.dumps(result)),
        })

    return messages
