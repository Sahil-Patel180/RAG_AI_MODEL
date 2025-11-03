import streamlit as st
import os
import numpy as np
import mimetypes
from src import loader, splitter, embedder, vector_store, retriever, rag_pipeline
from config import EMBED_MODEL, INDEX_PATH, DOCS_PATH
from sentence_transformers import SentenceTransformer

model_embedder = SentenceTransformer(EMBED_MODEL)

st.set_page_config(page_title="RAG AI Agent", layout="wide")

st.title("🤖 RAG AI Agent with Gemini")
st.write("Upload documents and ask questions with context-aware answers!")

uploaded_files = st.file_uploader(
    "Upload your documents or images",
    type=["pdf", "docx", "txt"], #"jpg", "jpeg", "png"
    accept_multiple_files=True
)


if uploaded_files:
    os.makedirs(DOCS_PATH, exist_ok=True)
    all_text = ""

    image_files = []
    for file in uploaded_files:
        path = os.path.join(DOCS_PATH, file.name)
        with open(path, "wb") as f:
            f.write(file.getbuffer())
        
        mime_type, _ = mimetypes.guess_type(path)
        if mime_type and mime_type.startswith("image/"):
            image_files.append(path)
        else:
            all_text += loader.load_text_from_file(path)
    if image_files:
        st.image(image_files, caption=[os.path.basename(p) for p in image_files], use_container_width=True)

    
    st.success("✅ Documents uploaded successfully!")
    
    chunks = splitter.split_text(all_text)
    embeddings = model_embedder.encode(chunks)
    vector_store.create_faiss_index(np.array(embeddings), chunks, INDEX_PATH)
    st.info("🔍 Documents processed and indexed!")

st.divider()
query = st.text_input("Ask your question:")

if st.button("Generate Answer"):
    index, chunks = vector_store.load_faiss_index(INDEX_PATH)
    if index is None:
        st.warning("Please upload and index documents first!")
    else:
        results = retriever.retrieve(query, model_embedder, index, chunks)
        answer = rag_pipeline.generate_rag_response(query, results, image_paths=image_files)
        st.subheader("💬 Answer")
        st.write(answer)
        st.expander("📄 Context Used").write(results)
