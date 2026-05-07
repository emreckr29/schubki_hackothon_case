import re
import json
from pathlib import Path

PARSED_DIR = Path("data/parsed")
CHUNK_DIR = Path("data/chunks")

CHUNK_DIR.mkdir(parents=True, exist_ok=True)

MAX_CHARS = 1800
MIN_CHARS = 400


def split_sections(markdown_text):
    pattern = r"(?=^##\s+)"
    sections = re.split(pattern, markdown_text, flags=re.MULTILINE)

    cleaned = [s.strip() for s in sections if s.strip()]

    return cleaned


def chunk_text(text, max_chars=MAX_CHARS):
    paragraphs = text.split("\n\n")

    chunks = []
    current = ""

    for para in paragraphs:
        para = para.strip()

        if not para:
            continue

        if len(current) + len(para) < max_chars:
            current += "\n\n" + para
        else:
            if len(current.strip()) >= MIN_CHARS:
                chunks.append(current.strip())

            current = para

    if current.strip():
        chunks.append(current.strip())

    return chunks


markdown_files = list(PARSED_DIR.glob("*.md"))

print(f"Found {len(markdown_files)} markdown files")

all_chunks = []

for md_file in markdown_files:
    paper_id = md_file.stem

    with open(md_file, "r", encoding="utf-8") as f:
        markdown = f.read()

    sections = split_sections(markdown)

    for section in sections:
        lines = section.split("\n")

        title = lines[0].replace("#", "").strip()

        content = "\n".join(lines[1:]).strip()

        text_chunks = chunk_text(content)

        for idx, chunk in enumerate(text_chunks):
            chunk_data = {
                "paper_id": paper_id,
                "section": title,
                "chunk_id": f"{paper_id}_{title}_{idx}",
                "text": chunk,
            }

            all_chunks.append(chunk_data)

output_path = CHUNK_DIR / "chunks.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=2, ensure_ascii=False)

print(f"\nSaved {len(all_chunks)} chunks")