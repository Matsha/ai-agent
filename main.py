from dotenv import load_dotenv
import os
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions

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

system_message = [

]
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt}
]

# response
response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions
)
if args.verbose:
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")
    print(f"User prompt: {args.user_prompt}")
print(response.choices[0].message.content)


def main():
    print("Hello from ai-agent!")


if __name__ == "__main__":
    main()
