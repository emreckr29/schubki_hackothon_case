import json
from openai import OpenAI
import os


from app.extraction.prompts import SYSTEM_PROMPT


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


MODEL = "openai/gpt-4o-mini"
#openai/gpt-5.5-pro


def extract_evidence(chunk_text: str):

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": chunk_text
            }
        ]
    )

    content = response.choices[0].message.content

    try:
        data = json.loads(content)
        return data

    except Exception as e:

        print("JSON parse error")
        print(content)

        return None