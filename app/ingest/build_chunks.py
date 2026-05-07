from pathlib import Path
import json
from tqdm import tqdm

from app.ingest.chunker import create_chunks


PROCESSED_DIR = Path("data/processed")
OUTPUT_DIR = Path("data/chunks")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():

    json_files = list(PROCESSED_DIR.glob("*.json"))

    print(f"Found {len(json_files)} processed papers")

    for json_file in tqdm(json_files):

        with open(json_file, "r", encoding="utf-8") as f:
            parsed_paper = json.load(f)

        chunks = create_chunks(parsed_paper)

        output_path = OUTPUT_DIR / f"{parsed_paper['paper_id']}_chunks.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()