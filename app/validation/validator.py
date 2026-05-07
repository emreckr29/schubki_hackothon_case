import json
import os

from openai import OpenAI


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = "openai/gpt-4o-mini"


VALIDATION_PROMPT = """
You are a clinical evidence validation system.

Your task:
Determine whether the extracted evidence is explicitly supported by the source text.

Rules:
- ONLY return supported=true if the information is clearly present
- Do NOT infer
- Do NOT assume
- Be strict
- If uncertain, return false

Return JSON only:

{
  "supported": true,
  "reason": ""
}
"""


def validate_extraction(chunk_text, extraction):

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": VALIDATION_PROMPT
            },
            {
                "role": "user",
                "content": f"""
SOURCE TEXT:
{chunk_text}

EXTRACTED EVIDENCE:
{json.dumps(extraction, indent=2)}
"""
            }
        ]
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)

    except:
        print("Validation parse error")
        print(content)

        return {
            "supported": False,
            "reason": "parse_error"
        }