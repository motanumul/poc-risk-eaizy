from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

DATA_DIR = Path("data")
DB_DIR = Path("chroma_db")
COLLECTION = "pdf_docs"

def load_pdfs(data_dir: Path):
    docs = []
    for pdf_path in sorted(data_dir.glob("*.pdf")):
        loader = PyPDFLoader(str(pdf_path))
        docs.extend(loader.load())  # one Document per page
    return docs

def main():
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Missing folder: {DATA_DIR.resolve()}")

    raw_docs = load_pdfs(DATA_DIR)
    if not raw_docs:
        raise RuntimeError(f"No PDFs found in {DATA_DIR.resolve()}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
    chunks = splitter.split_documents(raw_docs)

    #embeddings = OllamaEmbeddings(model="nomic-embed-text")
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")

    # Build + persist vector DB
    _ = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION,
        persist_directory=str(DB_DIR),
    )

    print(f"Loaded {len(raw_docs)} pages, created {len(chunks)} chunks.")
    print(f"Vector DB saved to: {DB_DIR.resolve()}")

if __name__ == "__main__":
    main()
