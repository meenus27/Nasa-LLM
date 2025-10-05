from llm.retriever import search
from llm.summarizer import summarize_chunks
from sentence_transformers import SentenceTransformer
import faiss, json

# Load model and index
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("data/embeddings/index.faiss")

# Load metadata (optional)
with open("data/embeddings/metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Run semantic search
query = "effects of microgravity on muscle tissue"
chunks = search(query, index, model)

# Summarize results
summaries = summarize_chunks(chunks)

# Print summaries
for i, summary in enumerate(summaries, 1):
    print(f"\n🔹 Summary {i}:\n{summary}")

