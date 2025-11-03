import numpy as np

def retrieve(query, model, index, chunks, top_k=3):
    # Create query embedding
    q_emb = model.encode([query])
    q_emb = np.array(q_emb, dtype="float32")

    # Handle shape (1D → 2D)
    if q_emb.ndim == 1:
        q_emb = q_emb.reshape(1, -1)

    # Debug print (will show in Streamlit logs)
    print(f"[DEBUG] query embedding shape: {q_emb.shape}, index dim: {index.d}")

    # --- Core Fix: dimension alignment ---
    if q_emb.shape[1] != index.d:
        raise ValueError(
            f"❌ Embedding dimension mismatch: query={q_emb.shape[1]} vs index={index.d}. "
            f"Rebuild index using the same model!"
        )

    # Search safely
    _, I = index.search(q_emb, top_k)
    results = [chunks[i] for i in I[0] if i < len(chunks)]
    return results
