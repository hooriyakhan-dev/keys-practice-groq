import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise SystemExit("GROQ_API_KEY not found. Please add it to your .env file.")

client = Groq(api_key=api_key)

query = input("What do you want to search on the internet? ")

try:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are a research assistant. Use the web browser to find the most recent information available."
            },
            {
                "role": "user",
                "content": f"Search the internet for: {query}. Give the latest value with its date and time, and the source URL. Prefer the most recently updated source."
            }
        ],
        tools=[{"type": "browser_search"}],
        tool_choice="required",
        temperature=0,
        max_completion_tokens=2048,
        reasoning_effort="low"
    )

    print("\nSearch Results:\n")
    print(response.choices[0].message.content or "No content returned.")

except Exception as e:
    print(f"\nSomething went wrong: {e}")