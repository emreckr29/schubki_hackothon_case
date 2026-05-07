from app.retrieval.search import search
from app.extraction.extractor import extract_evidence


query = "lactate mortality SOFA AUROC"

results = search(query, top_k=1)

chunk = results[0]["text"]

print("\nRETRIEVED CHUNK:\n")
print(chunk)

print("\n" + "="*80)

evidence = extract_evidence(chunk)

print("\nEXTRACTED:\n")
print(evidence)