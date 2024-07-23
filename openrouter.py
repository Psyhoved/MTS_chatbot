from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.environ.get("OPEN_ROUTER_KEY"),
)
model = "mistralai/mistral-7b-instruct:free"

stream = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "Что ты знаешь об уральских продуктовых сетях ритейла?",
        },
    ],
    stream=True,
    max_tokens=500,
    temperature=1
)
for chunk in stream:
    if not chunk.choices:
        continue

    print(chunk.choices[0].delta.content, end="")
print()