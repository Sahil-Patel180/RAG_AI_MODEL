import os
import PyPDF2
from docx import Document

def load_text_from_file(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    text = ""

    if ext == ".pdf":
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = " ".join([page.extract_text() for page in reader.pages])
    elif ext == ".docx":
        doc = Document(file_path)
        text = " ".join([p.text for p in doc.paragraphs])
    elif ext in [".txt", ".md"]:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError("Unsupported file format.")
    return text
