import json
import faiss
import numpy as np
from pathlib import Path

from app.retrieval.embedder import get_embedding

INDEX_PATH = Path("data/index/papers.index")
METADATA_PATH = Path("data/index/metadata.json")

index = faiss.read_index(str(INDEX_PATH))

with open(METADATA_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)

query = input("Query: ")

query_embedding = np.array(
    [get_embedding(query)],
    dtype="float32"
)

k = 5

distances, indices = index.search(query_embedding, k)

print("\n")

for i, idx in enumerate(indices[0]):
    chunk = metadata[idx]

    print("=" * 80)
    print(f"RESULT {i+1}")
    print(f"Paper: {chunk['paper_id']}")
    print(f"Section: {chunk['section']}")
    print()

    print(chunk["text"][:2500])
    print()