from dotenv import load_dotenv
load_dotenv()
import litellm
from config import config
from tools.tool_registry import get_tool_schemas
from utils.run_tool_calls import run_tool_calls
from utils.prune_messages import prune_messages
from utils.print_utils import print_banner, print_agent, print_error, user_input, print_token_usage

def main():
    print_banner()

    messages = [{"role": "system", 
    "content": config.system_prompt}]

    while True:
        input_prompt = user_input()
        messages.append({
            "role" : "user",
            "content" : input_prompt
        })

        tools = get_tool_schemas()
        
        for i in range(0, config.max_iters):
            try:
                response = litellm.completion(
                    model=config.LLM,
                    messages=messages,
                    tools=tools,
                    api_key=config.LLM_API_KEY
                )
                print_token_usage(response.usage)
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
                    if message.content:
                        print_agent(message.content)
                    tool_results = run_tool_calls(message.tool_calls)
                    messages.extend(tool_results)
                else:
                    print_agent(message.content)
                    break

            except litellm.AuthenticationError as e:
                print_error(f"Bad API key: {e}")
                break

            except litellm.RateLimitError as e:
                print_error(f"Rate limited: {e}")
                break

            except litellm.APIError as e:
                print_error(f"API error: {e}")
                break

            except Exception as e:
                print_error(f"Unexpected error: {e}")
                break
    
        messages = prune_messages(messages)


if __name__ == "__main__":
    main()
