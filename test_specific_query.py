import sys
import os

# Ensure the parent directory is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.retriever import retrieve_documents
from src.llm_chain import ask_question

import unicodedata

queries = [
    "Nhà nguyễn thành lập năm nào ?", # user's exact string
    "Nhà nguyễn thành lập năm nào ?", # composed, lowercase
    "Nhà Nguyễn thành lập năm nào?" # composed, uppercase
]

for query in queries:
    print(f"\n={'='*50}")
    print(f"Query: {query}")
    print(f"Length: {len(query)}, Repr: {repr(query)}")
    print(f"Normalized NFC: {repr(unicodedata.normalize('NFC', query))}")
    
    print("\n--- Testing Retriever ---")
    docs = retrieve_documents(query)
    for i, (doc, score) in enumerate(docs[:3]): # only top 3
        print(f"[{i}] Score: {score}")
        print(f"Source: {doc.metadata.get('source')}")
    print('='*50)
