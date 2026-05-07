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

LLM_MODEL = "openai/gpt-4.1-mini"

def extract_clinical_evidence(query, chunks):

    context = ""

    for chunk in chunks:

        section = " > ".join(
            chunk.get("section_tree", [])
        )

        if chunk["is_table"]:

            context += f"""

[TABLE]
Paper: {chunk['paper_id']}
Section: {section}

{chunk['text']}

"""

        else:

            context += f"""

[TEXT]
Paper: {chunk['paper_id']}
Section: {section}

{chunk['text']}

"""

    user_prompt = f"""
User Query:
{query}

Extract structured evidence relevant to the query.

Return JSON array format.

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

    response = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=0,
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

    text = response.choices[0].message.content

    try:
        return json.loads(text)

    except Exception:
        return []