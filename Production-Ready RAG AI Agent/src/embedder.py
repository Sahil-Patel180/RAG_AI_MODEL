from sentence_transformers import SentenceTransformer

def get_embeddings(chunks, model_name):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(chunks)
    return embeddings
