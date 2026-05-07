import json
import faiss
import numpy as np

from app.retrieval.embedder import get_embedding


INDEX_PATH = r"data/index/papers.index"
METADATA_PATH = r"data/index/metadata.json"


# index yükle
index = faiss.read_index(INDEX_PATH)

# metadata yükle
with open(METADATA_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)


def search(query: str, top_k: int = 5):

    query_embedding = get_embedding(query)

    vector = np.array([query_embedding], dtype="float32")

    distances, indices = index.search(vector, top_k)

    results = []

    for i, idx in enumerate(indices[0]):

        item = metadata[idx]

        results.append({
            "score": float(distances[0][i]),
            "paper_id": item["paper_id"],
            "section": item["section"],
            "text": item["text"]
        })

    return results


if __name__ == "__main__":

    query = "lactate mortality sepsis SOFA AUC"

    results = search(query)

    for r in results:
        print("\n" + "="*80)
        print("PAPER:", r["paper_id"])
        print("PAGE:", r["page"])
        print("SCORE:", r["score"])
        print(r["text"][:1000])