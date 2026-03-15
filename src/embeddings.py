try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    # Fallback to old import if langchain-huggingface not installed
    from langchain_community.embeddings import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL

def get_embedding_function():
    """
    Initialize HuggingFace embeddings
    """
    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    embedding_function = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'}, # 'cpu' or 'cuda'
        encode_kwargs={'normalize_embeddings': True}
    )
    return embedding_function

