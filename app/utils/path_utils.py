from pathlib import Path

def get_project_root() -> Path:
    """Returns the root directory of the project."""
    return Path(__file__).resolve().parent.parent.parent  # → points to project root

def get_rag_chroma_path() -> Path:
    """Returns the path to the rag_chroma directory."""
    return get_project_root() / "rag_chroma"

def get_docs_path() -> Path:
    """Returns the path to the rag_chroma directory."""
    return get_project_root() / "docs"