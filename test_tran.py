import os
import sys

# Ensure the parent directory is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.vector_store import get_vector_store
db = get_vector_store()
query = "Nhà Trần thành lập năm nào?"
print(f"Query: {query}")
docs = db.similarity_search_with_relevance_scores(query, k=25)
for i, (doc, score) in enumerate(docs):
    print(f"[{i}] Score: {score}")
    print(f"Source: {doc.metadata.get('source')}")
    print(f"Content: {doc.page_content[:200]}...")
