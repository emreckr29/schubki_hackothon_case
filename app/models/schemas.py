from pydantic import BaseModel
from typing import List


class PageDocument(BaseModel):
    source: str
    page: int
    text: str


class ParsedPaper(BaseModel):
    paper_id: str
    pages: List[PageDocument]