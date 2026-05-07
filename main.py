from pathlib import Path
import json
from tqdm import tqdm

from app.ingest.pdf_parser import parse_pdf


ARTICLES_DIR = Path("articles")
OUTPUT_DIR = Path("data/processed")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():

    pdf_files = list(ARTICLES_DIR.glob("*.pdf"))

    print(f"Found {len(pdf_files)} PDF files")

    for pdf_file in tqdm(pdf_files):

        try:
            parsed_paper = parse_pdf(pdf_file)

            output_path = OUTPUT_DIR / f"{parsed_paper.paper_id}.json"

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(
                    parsed_paper.model_dump(),
                    f,
                    indent=2,
                    ensure_ascii=False
                )

        except Exception as e:
            print(f"ERROR processing {pdf_file.name}: {e}")


if __name__ == "__main__":
    main()