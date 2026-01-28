"""
Configuration settings for Vietnamese History RAG Chatbot
"""
import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "vietnam_history"
CHROMA_DIR = BASE_DIR / "chroma_db"

# Document processing settings
CHUNK_SIZE = 1000  # Characters per chunk
CHUNK_OVERLAP = 200  # Overlap between chunks

# Embedding model - multilingual support for Vietnamese
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Ollama LLM settings
OLLAMA_MODEL = "llama3.2"  # Can change to: llama3.2, mistral, llama2, phi3, etc.
OLLAMA_BASE_URL = "http://localhost:11434"

# Retrieval settings
TOP_K_RESULTS = 6  # Number of relevant documents to retrieve (increased for better accuracy)

# Create directories if not exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)
