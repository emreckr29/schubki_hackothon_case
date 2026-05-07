from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

EMBED_MODEL = "openai/text-embedding-3-small"


def get_embedding(text: str, retries: int = 5):

    text = text.replace("\n", " ")

    for attempt in range(retries):

        try:

            response = client.embeddings.create(
                model=EMBED_MODEL,
                input=text
            )

            if not response.data:
                raise ValueError("Empty embedding response")

            return response.data[0].embedding

        except Exception as e:

            wait_time = 2 ** attempt

            print(f"[Embedding Error] Attempt {attempt+1}: {e}")
            print(f"Retrying in {wait_time}s...")

            time.sleep(wait_time)

    return None