import os
import json
import pickle
from sentence_transformers import SentenceTransformer

# --- Configuration ---
SUMMARY_DIR = "data/summaries"
INDEX_PATH = "data/embeddings/index.pkl"  # ✅ Save inside embeddings folder
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Storage ---
embeddings = []
metadata = []

# --- Process each summary file ---
for filename in os.listdir(SUMMARY_DIR):
    if not filename.endswith("_summary.json"):
        continue

    pmc_id = filename.replace("_summary.json", "")
    file_path = os.path.join(SUMMARY_DIR, filename)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to load {filename}: {e}")
        continue

    for chunk in chunks:
        text = chunk.get("summary", "").strip()
        if len(text) < 30:
            continue  # skip short or noisy summaries

        emb = model.encode(text)
        embeddings.append(emb)
        metadata.append({
            "pmc_id": pmc_id,
            "chunk_id": chunk.get("chunk_id", ""),
            "section": chunk.get("section", "Unknown"),
            "text": text,
            "link": f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/"
        })

# --- Save index ---
os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
with open(INDEX_PATH, "wb") as f:
    pickle.dump({"embeddings": embeddings, "metadata": metadata}, f)

print(f"✅ Saved {len(embeddings)} embeddings to {INDEX_PATH}")

