from pathlib import Path
import json
import numpy as np
import faiss
from tqdm import tqdm
import time
from app.retrieval.embedder import get_embedding


CHUNKS_DIR = Path("data/chunks")
INDEX_DIR = Path("data/index")

INDEX_DIR.mkdir(parents=True, exist_ok=True)


def load_all_chunks():

    all_chunks = []

    chunk_files = list(CHUNKS_DIR.glob("*.json"))

    for chunk_file in chunk_files:

        with open(chunk_file, "r", encoding="utf-8") as f:
            chunks = json.load(f)

            all_chunks.extend(chunks)

    return all_chunks


def main():

    all_chunks = load_all_chunks()

    print(f"Loaded {len(all_chunks)} chunks")

    embeddings = []

    metadata = []

    for chunk in tqdm(all_chunks):

        embedding = get_embedding(chunk["text"])

        if embedding is None:
            print(f"Skipping chunk {chunk['chunk_id']}")
            continue

        embeddings.append(embedding)
        metadata.append(chunk)
        
        time.sleep(0.2)


    embeddings_np = np.array(embeddings).astype("float32")

    dimension = embeddings_np.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings_np)

    faiss.write_index(index, str(INDEX_DIR / "sepsis.index"))

    with open(INDEX_DIR / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print("FAISS index saved")


if __name__ == "__main__":
    main()