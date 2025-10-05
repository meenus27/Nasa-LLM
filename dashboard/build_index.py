import os, json, pickle
from sentence_transformers import SentenceTransformer
import faiss

# Define paths relative to current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUMMARIES_DIR = os.path.join(BASE_DIR, "..", "data", "summaries")
EMBEDDINGS_DIR = os.path.join(BASE_DIR, "..", "data", "embeddings")

# Load summaries and metadata
texts = []
metadata = []

for filename in os.listdir(SUMMARIES_DIR):
    if filename.endswith(".json"):
        with open(os.path.join(SUMMARIES_DIR, filename), "r", encoding="utf-8") as f:
            data = json.load(f)
            pmc_id = filename.replace("_summary.json", "")
            for item in data:
                summary = item.get("summary", "").strip()
                if len(summary) < 30:
                    continue
                texts.append(summary)
                metadata.append({
                    "pmc_id": pmc_id,
                    "chunk_id": item.get("chunk_id", ""),
                    "section": item.get("section", "Unknown"),
                    "text": summary,
                    "link": f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/"
                })

# Generate embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts)

# Build FAISS index
index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(embeddings)

# Save index and metadata
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)
faiss.write_index(index, os.path.join(EMBEDDINGS_DIR, "index.faiss"))
with open(os.path.join(EMBEDDINGS_DIR, "index.pkl"), "wb") as f:
    pickle.dump({"embeddings": embeddings, "metadata": metadata}, f)

print(f"✅ Saved {len(embeddings)} entries to FAISS and index.pkl")

