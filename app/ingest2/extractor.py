from pathlib import Path
from docling.document_converter import DocumentConverter

RAW_PDF_DIR = Path("articles")
OUTPUT_DIR = Path("data/parsed")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

converter = DocumentConverter()

pdf_files = list(RAW_PDF_DIR.glob("*.pdf"))

print(f"Found {len(pdf_files)} PDFs")

for pdf_path in pdf_files:
    try:
        print(f"\nProcessing: {pdf_path.name}")

        result = converter.convert(str(pdf_path))

        markdown = result.document.export_to_markdown()

        output_file = OUTPUT_DIR / f"{pdf_path.stem}.md"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown)

        print(f"Saved: {output_file}")

    except Exception as e:
        print(f"ERROR processing {pdf_path.name}: {e}")



