import glob
import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP

def load_documents():
    """
    Load documents from the data directory
    """
    # Load .txt files
    text_loader = DirectoryLoader(
        str(DATA_DIR), 
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    
    docs = text_loader.load()
    print(f"Loaded {len(docs)} documents")
    return docs

def split_documents(docs):
    """
    Split documents into smaller chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(docs)
    print(f"Split {len(docs)} documents into {len(chunks)} chunks")
    return chunks

def get_processed_documents():
    """
    Load and split documents in one step
    """
    docs = load_documents()
    chunks = split_documents(docs)
    return chunks
