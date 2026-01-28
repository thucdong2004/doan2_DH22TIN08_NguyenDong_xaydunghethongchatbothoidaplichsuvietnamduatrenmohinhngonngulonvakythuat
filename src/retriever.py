from src.vector_store import get_vector_store
from config import TOP_K_RESULTS

def get_retriever():
    """
    Get the retriever with configuration
    """
    db = get_vector_store()
    
    # Configure retriever
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K_RESULTS}
    )
    
    return retriever
