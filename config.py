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
# Since we use MarkdownHeaderTextSplitter, hard chunk size is less important 
# but still useful for large sections.
CHUNK_SIZE = 500  
CHUNK_OVERLAP = 100

# Embedding model - multilingual support for Vietnamese
EMBEDDING_MODEL = "keepitreal/vietnamese-sbert"

# Ollama LLM settings
OLLAMA_MODEL = "llama3.2"  # Can change to: llama3.2, mistral, llama2, phi3, etc.
OLLAMA_BASE_URL = "http://localhost:11434"

# Retrieval settings
TOP_K_RESULTS = 8  # Number of relevant documents to retrieve
SIMILARITY_THRESHOLD = 0.2  # Minimum similarity score to include a document

# Rate limiting settings (đồ án - giới hạn tài nguyên)
MAX_QUESTIONS_PER_SESSION = 10   # Số câu hỏi tối đa mỗi phiên
RATE_LIMIT_SECONDS = 10          # Thời gian chờ giữa các câu hỏi (giây)
MAX_CONCURRENT_USERS = 1         # Số người dùng đồng thời tối đa

# Create directories if not exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)
