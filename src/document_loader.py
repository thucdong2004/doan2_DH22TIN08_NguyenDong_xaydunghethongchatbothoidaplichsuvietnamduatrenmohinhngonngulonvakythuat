import os
import re
import unicodedata
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP


MIN_CHUNK_LENGTH = 80  


def normalize_vietnamese(text):
    """
    Preprocess Vietnamese text:
    - Normalize Unicode (NFC)
    - Remove excessive whitespace
    - Merge standalone headers with the paragraph below them
    """
    text = unicodedata.normalize("NFC", text)

    text = re.sub(r'(^#{1,3} .+)\n\n(?=\S)', r'\1\n', text, flags=re.MULTILINE)

    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()


def load_documents():
    """
    Load all markdown documents from the data directory
    """
    text_loader = DirectoryLoader(
        str(DATA_DIR),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )

    docs = text_loader.load()
    print(f"📄 Loaded {len(docs)} documents")
    for doc in docs:
        source = os.path.basename(doc.metadata.get('source', 'Unknown'))
        print(f"   - {source} ({len(doc.page_content)} chars)")
    return docs


def split_documents(docs):
    """
    Split documents using RecursiveCharacterTextSplitter.
    chunk_size=400, chunk_overlap=80 for fine-grained retrieval.
    Filters out header-only chunks (< MIN_CHUNK_LENGTH chars).
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    all_chunks = []
    dropped = 0
    for doc in docs:
        # Normalize text — merges headers with body text
        doc.page_content = normalize_vietnamese(doc.page_content)
        chunks = text_splitter.split_documents([doc])

        for chunk in chunks:
            # Filter out header-only or too-short chunks
            content = chunk.page_content.strip()
            # Remove markdown header markers for length check
            clean = re.sub(r'^#{1,3}\s+', '', content, flags=re.MULTILINE).strip()
            if len(clean) >= MIN_CHUNK_LENGTH:
                all_chunks.append(chunk)
            else:
                dropped += 1

    print(f"✂️  Split {len(docs)} documents into {len(all_chunks)} chunks "
          f"(chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    if dropped:
        print(f"   ⚠️  Dropped {dropped} header-only/too-short chunks")
    return all_chunks


def get_processed_documents():
    """
    Load and split documents in one step
    """
    docs = load_documents()
    chunks = split_documents(docs)
    return chunks
