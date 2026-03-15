import os
import shutil
import time
from langchain_chroma import Chroma
from src.embeddings import get_embedding_function
from src.document_loader import get_processed_documents
from config import CHROMA_DIR


def create_vector_store(clear_existing=True):
    """
    Create and persist ChromaDB vector store.
    
    Args:
        clear_existing: If True (default), delete existing DB before creating
                        new one to avoid duplicate embeddings.
    """
    # Always clear existing DB by default to prevent duplicates
    if clear_existing and os.path.exists(CHROMA_DIR):
        print("⚠️  Clearing existing vector store...")
        max_retries = 3
        for i in range(max_retries):
            try:
                shutil.rmtree(CHROMA_DIR)
                print("✅ Existing database cleared successfully")
                break
            except PermissionError as e:
                if i < max_retries - 1:
                    print(f"⏳ Database is locked. Waiting 2 seconds... (attempt {i+1}/{max_retries})")
                    time.sleep(2)
                else:
                    print("❌ Cannot clear database — it's being used by another process.")
                    print("💡 Please close any running app.py or Python processes and try again.")
                    raise
            except Exception as e:
                print(f"❌ Error clearing database: {e}")
                raise

    # Get documents and embeddings
    chunks = get_processed_documents()
    embedding_function = get_embedding_function()

    print(f"🔨 Creating vector store with {len(chunks)} chunks...")
    # Create Chroma DB
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        persist_directory=str(CHROMA_DIR)
    )

    # Verify
    count = db._collection.count()
    print(f"✅ Vector store created at {CHROMA_DIR} ({count} embeddings)")
    return db


def get_vector_store():
    """
    Load existing ChromaDB vector store
    """
    embedding_function = get_embedding_function()

    db = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embedding_function
    )
    return db
