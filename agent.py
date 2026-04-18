from dotenv import load_dotenv
load_dotenv()
import litellm
from config import config
from tools.tool_registry import get_tool_schemas
from utils.run_tool_calls import run_tool_calls
from utils.prune_messages import prune_messages
from utils.print_utils import print_banner
from utils.print_utils import print_line

def main():
    print_banner()

    messages = [{"role": "system", 
    "content": config.system_prompt}]

    while True:
        print_line()
        input_prompt=input("You ")
        print_line()
        messages.append({
            "role" : "user",
            "content" : input_prompt
        })

        tools = get_tool_schemas()
        
        for i in range(0,config.max_iters):
            try:
                response = litellm.completion(
                    model=config.LLM,
                    messages=messages,
                    tools=tools,
                    api_key=config.LLM_API_KEY
                )
                message = response.choices[0].message
                msg = {
                    "role": message.role
                }

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
                                "arguments": call.function.arguments
                            }
                        })

                    msg["tool_calls"] = tool_calls

                messages.append(msg)

                if message.tool_calls:
                    tool_results = run_tool_calls(message.tool_calls)
                    messages.extend(tool_results)
                else:
                    print(f"\n[Agent] {message.content}")
                    break

            except litellm.AuthenticationError as e:
                print(f"\n[Error] Bad API key: {e}")
                break

            except litellm.RateLimitError as e:
                print(f"\n[Error] Rate limited: {e}")
                break

            except litellm.APIError as e:
                print(f"\n[Error] API error: {e}")
                break

            except Exception as e:
                print(f"\n[Error] Unexpected error: {e}")
                break
    
        messages = prune_messages(messages)


if __name__ == "__main__":
    main()
