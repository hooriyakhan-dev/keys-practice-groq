import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

SYSTEM_PROMPT = """
You are the assistant for ChassisWear (ChassisWear.pk), a custom clothing brand from Pakistan.
Always reply in English only, in 2-3 short sentences.
Only talk about the ChassisWear brand: what it is, its custom clothing, its quality and style.
Be friendly and positive about the brand.
Do not mention prices, discounts, or any details you are not sure about.
If the user asks about anything unrelated to ChassisWear, politely say:
"I can only help with questions about ChassisWear."
Never answer general questions, coding, news, or anything off-topic.
"""


def ask(question):
    response = client.responses.create(
        instructions=SYSTEM_PROMPT,
        input=question,
        model="openai/gpt-oss-20b",
    )
    return response.output_text


while True:
    q = input("Aap: ").strip()
    if q.lower() in ("exit", "quit"):
        break
    if q:
        print("Agent:", ask(q), "\n")