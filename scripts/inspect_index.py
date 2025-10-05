import pickle

# --- Path to your index file ---
INDEX_PATH = "data/index.pkl"

# --- Load and inspect ---
try:
    with open(INDEX_PATH, "rb") as f:
        data = pickle.load(f)

    print(f"✅ Total embeddings: {len(data['embeddings'])}")
    print(f"✅ Total metadata entries: {len(data['metadata'])}")
    print("🔍 Sample metadata entry:")
    print(data['metadata'][0])

except Exception as e:
    print(f"❌ Failed to load index file: {e}")
