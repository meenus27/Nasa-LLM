import os, json, pickle
from sentence_transformers import SentenceTransformer
import faiss

# Define paths relative to current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUMMARIES_DIR = os.path.join(BASE_DIR, "..", "data", "summaries")
EMBEDDINGS_DIR = os.path.join(BASE_DIR, "..", "data", "embeddings")

# Load summaries
texts = []
for filename in os.listdir(SUMMARIES_DIR):
    if filename.endswith(".json"):
        with open(os.path.join(SUMMARIES_DIR, filename), "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                texts.append(item["summary"])  # adjust key if needed

# Generate embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts)

# Build FAISS index
index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(embeddings)

# Save index
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)
faiss.write_index(index, os.path.join(EMBEDDINGS_DIR, "index.faiss"))
with open(os.path.join(EMBEDDINGS_DIR, "index.pkl"), "wb") as f:
    pickle.dump(texts, f)

print("✅ FAISS index and pickle file saved successfully.")

