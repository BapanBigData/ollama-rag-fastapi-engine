import requests
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

# Load Chroma DB (persisted)
chroma_client = chromadb.PersistentClient(path="./rag_chroma")
collection = chroma_client.get_or_create_collection("pmt_pro_docs")

# Embedding via Ollama
OLLAMA_EMBEDDING_MODEL = "mxbai-embed-large"
OLLAMA_GENERATE_MODEL = "tinyllama:1.1b"
OLLAMA_BASE_URL = "http://localhost:11434"

def get_ollama_embedding(text: str):
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/embeddings",
        json={"model": OLLAMA_EMBEDDING_MODEL, "prompt": text}
    )
    return response.json()["embedding"]

def retrieve_context(query: str, top_k: int = 3):
    embedding = get_ollama_embedding(query)
    results = collection.query(query_embeddings=[embedding], n_results=top_k)
    return "\n---\n".join(results["documents"][0])

def generate_answer(query: str, context: str):
    prompt = f"""You are a helpful assistant for PMT Pro. Use the context below to answer the user's question.\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"""
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={"model": OLLAMA_GENERATE_MODEL, "prompt": prompt, "stream": False}
    )
    return response.json().get("response", "[No response generated]")


def process_query(query: str):
    context = retrieve_context(query)
    answer = generate_answer(query, context)
    return answer, context