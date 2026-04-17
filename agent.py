import litellm
from dotenv import load_dotenv
import os
from config import config
import json
from tools.tool_registry import function_call
from tools.tool_registry import get_tool_schemas

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

def main():
    load_dotenv()
    messages = [{"role": "system", 
    "content": config.system_prompt}]

    while True:
        input_prompt=input("You ")
        messages.append({
            "role" : "user",
            "content" : input_prompt
        })

        tools = get_tool_schemas()
        
        for i in range(0,config.max_iters):
            try:
                response = litellm.completion(
                    model="gemini/gemini-flash-latest",
                    messages=messages,
                    tools=tools,
                    api_key=os.getenv("GEMINI_API_KEY")
                )
                print(response)
                message = response.choices[0].message
                messages.append(message)
                if message.tool_calls:
                    tool_results = run_tool_calls(message.tool_calls)
                    messages.extend(tool_results)
                else:
                    print(f"[Agent] {message.content}")
                    break

            except litellm.AuthenticationError as e:
                print(f"[Error] Bad API key: {e}")
                break

            except litellm.RateLimitError as e:
                print(f"[Error] Rate limited: {e}")
                break

            except litellm.APIError as e:
                print(f"[Error] API error: {e}")
                break

            except Exception as e:
                print(f"[Error] Unexpected error: {e}")
                break



if __name__ == "__main__":
    main()
