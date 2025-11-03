import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Set this in your environment
genai.configure(api_key=GEMINI_API_KEY)

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2" # BAAI/bge-small-en-v1.5
INDEX_PATH = "data/faiss_index"
DOCS_PATH = "data/sample_docs"