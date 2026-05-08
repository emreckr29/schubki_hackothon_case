import os
import json

from openai import OpenAI
from dotenv import load_dotenv
from pydantic import ValidationError

from extraction.prompts2 import SYSTEM_PROMPT
from extraction.data_schema import ClinicalEvidenceExtraction

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Use 4.1 for extraction unless you really need 5.5-pro reasoning.
# LLM_MODEL = "openai/gpt-5.5-pro"
LLM_MODEL = "openai/gpt-4.1"


def build_context(chunks):
    context_parts = []

    for chunk in chunks:
        section = " > ".join(chunk.get("section_tree", []))

        chunk_type = "TABLE" if chunk.get("is_table") else "TEXT"

        context_parts.append(
            f"""
        [{chunk_type}]
        Paper: {chunk.get("paper_id")}
        Section: {section}

        {chunk.get("text", "")}
            """
        )

    return "\n\n".join(context_parts)

def extract_clinical_evidence(query, chunks):
    context = build_context(chunks)

    schema = ClinicalEvidenceExtraction.model_json_schema()

    user_prompt = f"""
User Query:
{query}

JSON Schema:
{json.dumps(schema, indent=2)}

Context:
{context}
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=0,
        max_tokens=4096,
        response_format={"type": "json_object"},
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
        parsed = ClinicalEvidenceExtraction.model_validate_json(text)
        return [row.model_dump() for row in parsed.rows]

    except ValidationError as e:
        print("Pydantic validation failed:")
        print(e)
        print("Raw LLM response:")
        print(text)
        return []

    except Exception as e:
        print("Unexpected extraction error:")
        print(e)
        print("Raw LLM response:")
        print(text)
        return []