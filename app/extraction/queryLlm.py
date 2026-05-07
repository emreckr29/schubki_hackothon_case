
import json
import os

from openai import OpenAI

from app.extraction.prompts import SYSTEM_PROMPT


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Cheaper + enough for extraction
# MODEL = "openai/gpt-4o-mini"

# Expensive
MODEL = "openai/gpt-5.5-pro"


def extract_evidence(chunk_text: str):

    response = client.chat.completions.create(
        model=MODEL,

        # deterministic extraction
        temperature=0,

        # VERY IMPORTANT
        max_tokens=4096,

        # force JSON output
        response_format={"type": "json_object"},

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

    except Exception:

        print("JSON parse error")
        print(content)

        return None

