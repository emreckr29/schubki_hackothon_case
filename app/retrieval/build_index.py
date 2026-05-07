
import json
import faiss
import numpy as np
from pathlib import Path
from tqdm import tqdm

from app.retrieval.embedder import get_embedding

CHUNK_PATH = Path("data/chunks/chunks.json")
INDEX_DIR = Path("data/index")

INDEX_DIR.mkdir(parents=True, exist_ok=True)

with open(CHUNK_PATH, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")

embeddings = []

for chunk in tqdm(chunks):
    emb = get_embedding(chunk["text"])
    embeddings.append(emb)

embeddings = np.array(embeddings).astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

faiss.write_index(index, str(INDEX_DIR / "papers.index"))

with open(INDEX_DIR / "metadata.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)

print("\nFAISS index saved")