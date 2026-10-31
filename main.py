from math import e

from dotenv import load_dotenv
import os
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function
import json

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key == None:
    raise RuntimeError("API key not found")

client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1",)

# manage input
parser = argparse.ArgumentParser(description="terminal chatbot")
parser.add_argument("user_prompt",type=str, help="user prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt}
]

# response
def chat_completion():
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions
    )
    if args.verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
        print(f"User prompt: {args.user_prompt}")
    message = response.choices[0].message
    if message.tool_calls != None:
        for tool_call in message.tool_calls:
            tool_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({tool_args})")
            result_message = call_function(tool_call, args.verbose)
            messages.append(result_message)
            if result_message["content"] == None:
                raise Exception
            if args.verbose:
                print(f"-> {result_message['content']}")
    else:
        print(message.content)
    return response

for _ in range(20):
    response1 = chat_completion()
    message = response1.choices[0].message
    messages.append(message)
    if response1.choices[0].message.tool_calls == None:
        break

def main():
    print("Hello from ai-agent!")


if __name__ == "__main__":
    main()
