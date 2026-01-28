import os
import shutil
import time
from langchain_community.vectorstores import Chroma
from src.embeddings import get_embedding_function
from src.document_loader import get_processed_documents
from config import CHROMA_DIR

def create_vector_store(clear_existing=False):
    """
    Create and persist ChromaDB vector store
    
    Args:
        clear_existing: If True, delete existing DB before creating new one
    """
    # Clear existing DB if requested
    if clear_existing and os.path.exists(CHROMA_DIR):
        print("⚠️  Clearing existing vector store...")
        try:
            # Try to remove with retry mechanism
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
                        print("❌ Cannot clear database - it's being used by another process.")
                        print("💡 Please close any running app.py or Python processes and try again.")
                        print("💡 Or use update mode: python init_db.py --update")
                        raise
        except Exception as e:
            print(f"❌ Error clearing database: {e}")
            raise

    # Get documents and embeddings
    chunks = get_processed_documents()
    embedding_function = get_embedding_function()

    print("🔨 Creating vector store...")
    # Create Chroma DB
    db = Chroma.from_documents(
        documents=chunks, 
        embedding=embedding_function, 
        persist_directory=str(CHROMA_DIR)
    )
    
    print(f"✅ Vector store created at {CHROMA_DIR}")
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
