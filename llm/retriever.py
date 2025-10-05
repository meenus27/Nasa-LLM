def search(query, index, model):
    query_embedding = model.encode([query])
    D, I = index.search(query_embedding, k=5)
    return I
