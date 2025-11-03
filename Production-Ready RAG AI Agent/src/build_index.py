import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader

# 📁 Paths
DATA_DIR = "data"
INDEX_PATH = os.path.join(DATA_DIR, "index.faiss")
CHUNKS_PATH = os.path.join(DATA_DIR, "chunks.pkl")

# 🧠 Model
EMBED_MODEL = "all-MiniLM-L6-v2"

# ✅ Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def read_pdfs(pdf_folder="sample_docs"):
    texts = []
    if not os.path.exists(pdf_folder):
        print(f"⚠️ Folder '{pdf_folder}' not found.")
        return texts

    for file in os.listdir(pdf_folder):
        if file.endswith(".pdf"):
            path = os.path.join(pdf_folder, file)
            print(f"📄 Reading: {file}")
            try:
                reader = PdfReader(path)
                text = "".join([page.extract_text() or "" for page in reader.pages])
                if text.strip():
                    texts.append(text)
            except Exception as e:
                print(f"❌ Error reading {file}: {e}")
    return texts

def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def build_embeddings(chunks, model_name=EMBED_MODEL):
    model = SentenceTransformer(model_name)
    print("⚙️ Creating embeddings...")
    embeddings = model.encode(chunks, show_progress_bar=True)
    return np.array(embeddings, dtype="float32")

def save_index(embeddings, chunks):
    dim = embeddings.shape[1]
    print(f"🧱 Building FAISS index with dimension: {dim}")
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)

    print(f"✅ Saved index to {INDEX_PATH}")
    print(f"✅ Saved chunks to {CHUNKS_PATH}")

if __name__ == "__main__":
    pdf_texts = read_pdfs()

    if not pdf_texts:
        print("⚠️ No PDFs found in 'sample_docs/'. Please add some and rerun.")
        exit()

    all_chunks = []
    for text in pdf_texts:
        all_chunks.extend(chunk_text(text))

    print(f"✂️ Total chunks created: {len(all_chunks)}")

    embeddings = build_embeddings(all_chunks)
    save_index(embeddings, all_chunks)
    print("🎉 Done building FAISS index!")