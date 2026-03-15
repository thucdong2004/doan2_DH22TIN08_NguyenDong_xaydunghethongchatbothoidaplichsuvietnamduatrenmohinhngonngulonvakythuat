import os
import unicodedata
from src.vector_store import get_vector_store
from src.document_loader import get_processed_documents
from langchain_community.retrievers import BM25Retriever
from config import TOP_K_RESULTS, SIMILARITY_THRESHOLD

# Caching the BM25 retriever so it doesn't rebuild on every query
_bm25_retriever = None

def get_bm25_retriever():
    global _bm25_retriever
    if _bm25_retriever is None:
        chunks = get_processed_documents()
        _bm25_retriever = BM25Retriever.from_documents(chunks)
        _bm25_retriever.k = TOP_K_RESULTS
    return _bm25_retriever

def retrieve_documents(question):
    """
    Retrieve relevant documents using Custom Hybrid Search (BM25 + Chroma Vector)
    with Reciprocal Rank Fusion (RRF).
    """
    question = unicodedata.normalize("NFC", question)
    db = get_vector_store()
    
    print(f"\n🔍 [RETRIEVER] Query: {question}")
    
    # 1. Vector Search
    vector_results = db.similarity_search_with_relevance_scores(question, k=TOP_K_RESULTS)
    
    # 2. Keyword Search
    bm25 = get_bm25_retriever()
    bm25_docs = bm25.invoke(question)
    
    # 3. Reciprocal Rank Fusion (RRF)
    rrf_scores = {}
    all_docs = {}
    
    for rank, (doc, score) in enumerate(vector_results):
        content = doc.page_content
        rrf_scores[content] = rrf_scores.get(content, 0.0) + 1.0 / (60 + rank)
        all_docs[content] = doc
        
    for rank, doc in enumerate(bm25_docs):
        content = doc.page_content
        rrf_scores[content] = rrf_scores.get(content, 0.0) + 1.0 / (60 + rank)
        all_docs[content] = doc
        
    # Sort docs by RRF score
    sorted_docs = sorted(all_docs.values(), key=lambda doc: rrf_scores[doc.page_content], reverse=True)
    top_docs = sorted_docs[:TOP_K_RESULTS]
    
    print(f"📊 [RETRIEVER] Hybrid results: {len(top_docs)} documents")
    
    filtered_results = []
    for doc in top_docs:
        score = rrf_scores[doc.page_content]
        source = os.path.basename(doc.metadata.get('source', 'Unknown'))
        preview = doc.page_content[:100].replace('\n', ' ')
        filtered_results.append((doc, score))
        print(f"   ✅ Hybrid-RRF-Score={score:.4f} | {source} | {preview}...")
        
    return filtered_results
