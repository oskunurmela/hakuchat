import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

import web_search

load_dotenv()

MODEL = "nvidia/nemotron-3.5-super-vl:free"
BASE_URL = "https://openrouter.ai/api/v1"
MAX_ROUNDS = 5

web_search_tool = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search Finnish Wikipedia for information about a topic.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query, e.g. Helsinki",
                },
            },
            "required": ["query"],
        },
    },
}

client = OpenAI(
    base_url=BASE_URL,
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)


def chat(messages: list[dict]) -> str:
    current_messages = list(messages)

    for round_index in range(MAX_ROUNDS):
        response = client.chat.completions.create(
            model=MODEL,
            messages=current_messages,
            tools=[web_search_tool],
        )

        message = response.choices[0].message
        tool_calls = message.tool_calls or []

        if not tool_calls:
            return message.content or ""

        current_messages.append(message)

        for tool_call in tool_calls:
            name = tool_call.function.name
            arguments = tool_call.function.arguments

            if name == "web_search":
                import json

                args = json.loads(arguments)
                query = args.get("query", "")
                print(f"[kierros {round_index + 1}] Työkalukutsu: web_search(query={query!r})")
                results = web_search.web_search(query)
                print(f"[kierros {round_index + 1}] Tuloksia: {len(results)}")
                current_messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(results, ensure_ascii=False),
                    }
                )
            else:
                print(f"[kierros {round_index + 1}] Tuntematon työkalu: {name}")
                current_messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps({"error": f"Unknown tool: {name}"}),
                    }
                )

    return "(Vastaus ei valmis enimmäiskierrosten jälkeen.)"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Käyttö: python chat_core.py <kysymys>")
        sys.exit(1)

    user_question = sys.argv[1]
    messages = [{"role": "user", "content": user_question}]
    answer = chat(messages)
    print("\n--- Vastaus ---")
    print(answer)
