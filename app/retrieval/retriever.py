import json
import faiss
import numpy as np

from retrieval.embedder import get_embedding

index = faiss.read_index(
    "data2/index/papers.index"
)

with open(
    "data2/index/metadata.json",
    "r",
    encoding="utf-8"
) as f:

    metadata = json.load(f)

def search(query, top_k=8):

    query_embedding = np.array(
        [get_embedding(query)],
        dtype="float32"
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for rank, idx in enumerate(indices[0]):

        chunk = metadata[idx]

        chunk["score"] = float(
            distances[0][rank]
        )

        results.append(chunk)

    return results