import pickle
import faiss
import numpy as np

with open("data/index.pkl", "rb") as f:
    index = pickle.load(f)

embeddings = np.array(index["embeddings"]).astype("float32")
faiss_index = faiss.IndexFlatL2(embeddings.shape[1])
faiss_index.add(embeddings)

faiss.write_index(faiss_index, "data/embeddings/index.faiss")
