import os, json, requests
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

MODEL = "openai/gpt-oss-20b"   # purana model ab nahi chal raha


# ---------- Tool 1: mausam (free, key nahi) ----------
def get_weather(city):
    return requests.get(f"https://wttr.in/{city}?format=3", timeout=10).text


# ---------- Tool 2: internet search ----------
def web_search(query):
    res = tavily.search(query, max_results=3)
    return "\n".join(r["content"] for r in res["results"])


# ---------- AI ko tools batao ----------
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Kisi shehar ka mausam batata hai",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Internet par taaza info search karta hai",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
]

messages = []

while True:
    user = input("\nTum: ")
    if user == "exit":
        break
    messages.append({"role": "user", "content": user})

    while True:
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=tools
        )
        msg = response.choices[0].message

        # AI ne tool nahi manga, seedha jawab diya
        if not msg.tool_calls:
            print("AI:", msg.content)
            messages.append({"role": "assistant", "content": msg.content})
            break

        # AI ne tool manga
        messages.append(msg)
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            print(f"  [tool chala: {call.function.name} {args}]")

            if call.function.name == "get_weather":
                result = get_weather(args["city"])
            else:
                result = web_search(args["query"])

            messages.append(
                {"role": "tool", "tool_call_id": call.id, "content": result}
            )


    