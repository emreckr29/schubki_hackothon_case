from docling.document_converter import DocumentConverter

converter = DocumentConverter()

result = converter.convert("articles/Baloch_2022.pdf")

print(result.document.export_to_markdown())