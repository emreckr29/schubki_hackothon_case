import os
import json

from openai import OpenAI
from dotenv import load_dotenv

from extraction.prompts import SYSTEM_PROMPT

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

LLM_MODEL = "openai/gpt-4.1"

MAX_CONTEXT_CHARS = 50000


def extract_clinical_evidence(query, chunks):

    context = ""

    for chunk in chunks:

        section = " > ".join(
            chunk.get("section_tree", [])
        )

        chunk_text = chunk["text"][:2000]

        if chunk["is_table"]:

            context += f"""

[TABLE]
Paper: {chunk['paper_id']}
Section: {section}

{chunk_text}

"""

        else:

            context += f"""

[TEXT]
Paper: {chunk['paper_id']}
Section: {section}

{chunk_text}

"""

    # hard limit
    context = context[:MAX_CONTEXT_CHARS]

    user_prompt = f"""
User Query:
{query}

Extract structured clinical evidence.

Return ONLY valid JSON.

Schema:

[
  {{
    "study": "",
    "population": "",
    "sample_size": "",
    "predictor": "",
    "outcome": "",
    "timing": "",
    "method": "",
    "effect_size": "",
    "performance": "",
    "notes": "",
    "source_text": "",
    "paper_id": "",
    "section": ""
  }}
]

Context:
{context}
"""

    print("Sending request to LLM...")

    response = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=0,
        max_tokens=2500,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    print("LLM response received")

    text = response.choices[0].message.content

    try:

        parsed = json.loads(text)

        return parsed

    except Exception as e:

        print("JSON parse error:", e)
        print(text)

        return []