from app.retrieval.embedder import get_embedding

embedding = get_embedding("sepsis mortality")

print(len(embedding))
print(embedding[:10])