import faiss
import numpy as np
import os
import pickle

def create_faiss_index(embeddings, chunks, index_path):
    # Ensure embeddings is a 2D numpy array
    embeddings = np.array(embeddings, dtype="float32")
    if embeddings.ndim == 1:
        embeddings = embeddings.reshape(1, -1)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save chunks
    with open(index_path + ".pkl", "wb") as f:
        pickle.dump(chunks, f)
    faiss.write_index(index, index_path)
    return index


def load_faiss_index(index_path):
    if not os.path.exists(index_path):
        return None, []
    index = faiss.read_index(index_path)
    with open(index_path + ".pkl", "rb") as f:
        chunks = pickle.load(f)
    return index, chunks
