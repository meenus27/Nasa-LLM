import os, json, pickle
import faiss
import torch
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# Directories
CHUNK_DIR = "data/processed"
EMBED_DIR = "data/embeddings"
os.makedirs(EMBED_DIR, exist_ok=True)

# Auto-detect device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"⚙️ Using device: {device}")

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2", device=device)

# FAISS index for 384-dim MiniLM embeddings
index = faiss.IndexFlatL2(384)
id_map = {}

# Collect all chunks
all_chunks = []
for filename in os.listdir(CHUNK_DIR):
    if filename.endswith("_chunks.json"):
        with open(os.path.join(CHUNK_DIR, filename), "r", encoding="utf-8") as f:
            chunks = json.load(f)
            all_chunks.extend(chunks)

# Batch encode texts
texts = [chunk["text"] for chunk in all_chunks]
embeddings = model.encode(texts, batch_size=32, show_progress_bar=True)

# Add to FAISS index and build ID map
for i, (chunk, embedding) in enumerate(zip(all_chunks, embeddings)):
    index.add(embedding.reshape(1, -1))
    id_map[i] = {
        "pmc_id": chunk["pmc_id"],
        "chunk_id": chunk["chunk_id"],
        "section": chunk["section"]
    }

# Save index and metadata
faiss.write_index(index, os.path.join(EMBED_DIR, "index.faiss"))
with open(os.path.join(EMBED_DIR, "index.pkl"), "wb") as f:
    pickle.dump(id_map, f)

print(f"✅ Embedded {len(all_chunks)} chunks.")

