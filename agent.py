import litellm
from dotenv import load_dotenv
import os
from config import config

def main():
    load_dotenv()
    messages = [{"role": "system", 
    "content": config.system_prompt}]

    while True:
        input_prompt=input()
        messages.append({
            "role" : "user",
            "content" : input_prompt
        })

        tools=[]
        
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
                    print("Tool call requested")
                else:
                    print(message.content)
                    break

            except litellm.AuthenticationError as e:
                print(f"Bad API key: {e}")
            except litellm.RateLimitError as e:
                print(f"Rate limited: {e}")
            except litellm.APIError as e:
                print(f"API error: {e}")



if __name__ == "__main__":
    main()
