from pathlib import Path
from docling.document_converter import DocumentConverter
import re

RAW_PDF_DIR = Path("articles")
OUTPUT_DIR = Path("data2/parsed")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

converter = DocumentConverter()

pdf_files = list(RAW_PDF_DIR.glob("*.pdf"))

print(f"Found {len(pdf_files)} PDFs")


def normalize_markdown(md: str):
    """
    Clinical-paper optimized markdown cleanup.
    """

    # normalize line endings
    md = md.replace("\r\n", "\n")

    # remove excessive newlines
    md = re.sub(r"\n{3,}", "\n\n", md)

    # ensure headings separated
    md = re.sub(r"\n(#{1,6}\s)", r"\n\n\1", md)

    # spacing after tables
    md = re.sub(r"(\|.*\|\n)(?=\S)", r"\1\n", md)

    # remove weird unicode spaces
    md = re.sub(r"[ \t]+", " ", md)

    return md.strip()


for pdf_path in pdf_files:

    try:
        print(f"\nProcessing: {pdf_path.name}")

        result = converter.convert(str(pdf_path))

        markdown = result.document.export_to_markdown()

        markdown = normalize_markdown(markdown)

        output_file = OUTPUT_DIR / f"{pdf_path.stem}.md"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown)

        print(f"Saved: {output_file}")

    except Exception as e:
        print(f"ERROR processing {pdf_path.name}: {e}")