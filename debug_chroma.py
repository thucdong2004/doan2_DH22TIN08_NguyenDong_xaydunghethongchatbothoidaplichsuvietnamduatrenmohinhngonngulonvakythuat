import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.vector_store import get_vector_store

db = get_vector_store()
results = db.get(where={"source": "d:\\test1\\data\\vietnam_history\\chronology\\03_nha_tran.md"})
if not results['documents']:
    # Fallback to just basename since loaders sometimes do that
    results_all = db.get()
    print(f"Total docs in DB: {len(results_all['documents'])}")
    for i, meta in enumerate(results_all['metadatas']):
        if "03_nha_tran.md" in meta.get("source", ""):
            print(f"--- Chunk {i} ---")
            print(results_all['documents'][i][:200])

else:
    for i, doc in enumerate(results['documents']):
        print(f"--- Chunk {i} ---")
        print(doc)
