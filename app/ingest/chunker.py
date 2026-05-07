import uuid
from typing import List, Dict


CHUNK_SIZE = 1200
OVERLAP = 200


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = OVERLAP
) -> List[str]:

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_chunks(parsed_paper: Dict):

    all_chunks = []

    paper_id = parsed_paper["paper_id"]

    for page_data in parsed_paper["pages"]:

        page_num = page_data["page"]

        text = page_data["text"]

        chunks = chunk_text(text)

        for chunk in chunks:

            chunk_obj = {
                "chunk_id": str(uuid.uuid4()),
                "paper_id": paper_id,
                "source": page_data["source"],
                "page": page_num,
                "text": chunk,
                "char_count": len(chunk)
            }

            all_chunks.append(chunk_obj)

    return all_chunks