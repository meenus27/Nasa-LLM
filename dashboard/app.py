import streamlit as st
import pickle, faiss, numpy as np, json, os, re
from sentence_transformers import SentenceTransformer

# --- Page config ---
st.set_page_config(
    page_title="NASA Bioscience Explorer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Absolute paths ---
INDEX_FAISS = "data/embeddings/index.faiss"
INDEX_PKL = "data/embeddings/index.pkl"
SUMMARIES_DIR = "data/summaries"


# --- Load model ---
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Load index and metadata ---
if not os.path.exists(INDEX_PKL) or not os.path.exists(INDEX_FAISS):
    st.error("❌ Index files not found. Please generate them first.")
    st.stop()

try:
    with open(INDEX_PKL, "rb") as f:
        raw = pickle.load(f)
        metadata = raw["metadata"]
        id_map = {i: m for i, m in enumerate(metadata)}
    index = faiss.read_index(INDEX_FAISS)
except Exception as e:
    st.error(f"❌ Failed to load index files: {e}")
    st.stop()

# --- Highlight query terms ---
def highlight(text, query):
    for word in query.split():
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        text = pattern.sub(f"**{word}**", text)
    return text

# --- Semantic search ---
def search(query, top_k=10):
    query_vec = model.encode([query])
    _, indices = index.search(np.array(query_vec).astype("float32"), top_k)
    results = []
    for idx in indices[0]:
        key = int(idx)
        if key not in id_map:
            continue
        entry = id_map[key]
        pmc_id, chunk_id, section, link = entry["pmc_id"], entry["chunk_id"], entry["section"], entry.get("link")
        summary_path = os.path.join(SUMMARIES_DIR, f"{pmc_id}_summary.json")
        summary_text = None
        if os.path.exists(summary_path):
            with open(summary_path, "r", encoding="utf-8") as f:
                summaries = json.load(f)
                summary_text = next((s["summary"] for s in summaries if s.get("chunk_id") == chunk_id), None)
        if not summary_text:
            summary_text = entry["text"]
        results.append({"section": section, "summary": summary_text, "link": link})
    return results

# --- Sidebar ---
st.sidebar.title("🧭 Navigation")
section = st.sidebar.radio("Go to:", ["Semantic Search", "About"])
st.sidebar.markdown("### 📊 Stats")
st.sidebar.metric("Papers Indexed", len(id_map))
st.sidebar.metric("Last Updated", "Oct 4, 2025")

# --- Main UI ---
if section == "Semantic Search":
    st.title("🔬 NASA Bioscience Explorer")
    st.markdown("Ask a question about bioscience research in space. Try examples like:")
    st.markdown("- 🧠 *Immune system changes in spaceflight*")
    st.markdown("- 💧 *Biofilm formation in ISS water systems*")
    st.markdown("- 🧫 *Burkholderia antifungal genes*")
    st.markdown("- 🧬 *Nanopore sequencing onboard the ISS*")

    query = st.text_input("Enter your research question:", placeholder="e.g. stem cell differentiation in microgravity")
    if query:
        with st.spinner("🔎 Searching NASA summaries..."):
            results = search(query)
        if results:
            st.success(f"Found {len(results)} matching summaries.")
            for i, r in enumerate(results):
                with st.expander(f"🧪 Insight {i+1} — {r['section']} section"):
                    st.markdown(highlight(r["summary"], query))
                    if r.get("link"):
                        st.markdown(f"[🔗 View Full Article]({r['link']})", unsafe_allow_html=True)
        else:
            st.warning("No matching summaries found. Try a different keyword or phrasing.")

elif section == "About":
    st.title("📘 About This App")
    st.markdown("""
    This dashboard uses semantic search powered by Sentence Transformers and FAISS to explore NASA bioscience publications.
    Built by **Vyomx** to support research, education, and outreach in space bioscience.
    """)

# --- Footer ---
st.markdown("---")
st.markdown("Made by Vyomx | Powered by LLMs + NASA Bioscience")









