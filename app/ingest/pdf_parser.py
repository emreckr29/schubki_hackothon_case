import fitz  # PyMuPDF
from pathlib import Path
from typing import List

from app.models.schemas import PageDocument, ParsedPaper


def clean_text(text: str) -> str:
    """
    Basic cleaning for extracted PDF text.
    """
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = " ".join(text.split())

    return text


def parse_pdf(pdf_path: str) -> ParsedPaper:
    """
    Parse a PDF into structured page documents.
    """

    pdf_path = Path(pdf_path)

    doc = fitz.open(pdf_path)

    pages: List[PageDocument] = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        text = page.get_text()

        cleaned = clean_text(text)

        page_doc = PageDocument(
            source=pdf_path.name,
            page=page_num + 1,
            text=cleaned
        )

        pages.append(page_doc)

    parsed_paper = ParsedPaper(
        paper_id=pdf_path.stem,
        pages=pages
    )

    return parsed_paper