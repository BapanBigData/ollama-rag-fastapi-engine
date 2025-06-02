import os
from docx import Document
import chromadb
import requests
from app.utils.path_utils import get_docs_path, get_rag_chroma_path

OLLAMA_EMBEDDING_MODEL = "mxbai-embed-large"
OLLAMA_BASE_URL = "http://localhost:11434"

DOCS_DIR = str(get_docs_path())
CHROMA_PATH = str(get_rag_chroma_path())
COLLECTION_NAME = "pmt_pro_docs"


def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks

def get_ollama_embedding(text):
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/embeddings",
        json={"model": OLLAMA_EMBEDDING_MODEL, "prompt": text}
    )
    return response.json()["embedding"]

def build_vector_store_if_needed():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(COLLECTION_NAME)

    if collection.count() > 0:
        print("✅ Vector store already exists.")
        return

    print("🔄 Building vector store from docs...")
    all_text = ""
    for filename in os.listdir(DOCS_DIR):
        if filename.endswith(".docx"):
            path = os.path.join(DOCS_DIR, filename)
            all_text += extract_text_from_docx(path) + "\n"

    chunks = chunk_text(all_text)
    for i, chunk in enumerate(chunks):
        embedding = get_ollama_embedding(chunk)
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"chunk_{i}"]
        )
    print("✅ Vector store built successfully.")
