# poc-risk-eaizy

# PDF RAG Bot (Ollama + LangChain + Chroma)

A simple local Q&A assistant that answers questions **from PDF documents** using **RAG (Retrieval-Augmented Generation)**:
1) Ingest PDFs → split into chunks → generate embeddings → store in a local vector database (Chroma)
2) Ask questions → retrieve relevant chunks → LLM answers using only retrieved context

## Architecture (High Level)

- **LLM runtime:** Ollama (local model execution)
- **Embeddings:** `nomic-embed-text` (or optional `mxbai-embed-large`)
- **Vector store:** Chroma (persisted locally on disk)
- **Orchestration:** LangChain (load → split → embed → retrieve → prompt → answer)

## Repository Structure
pdf-rag-bot/
- data/ # put your PDFs here (not committed by default)
- case-study/ #
- chroma_db/ # local vector database (not committed)
- ingest.py # build/update vector DB from PDFs
- chat.py # interactive Q&A chatbot
- .gitignore
- README.md


## Prerequisites

- Ubuntu Desktop 24.04 LTS (or similar Linux)
- Python 3.10+ recommended
- Ollama installed and running

## 1) Install Ollama + Models

### Install Ollama
Follow the official installer:
- https://ollama.com/download

### Pull required models
ollama pull llama3.2:3b
ollama pull nomic-embed-text
ollama pull mxbai-embed-large //used

Quick check:
ollama run llama3.2:3b

Exit with /bye.


## 2) Python Environment Setup (Ubuntu)
### Install Python tooling:
sudo apt update
sudo apt install -y python3 python3-venv python3-pip


### Create virtual environment:
python3 -m venv .venv
source .venv/bin/activate

### Install dependencies:
python3 -m pip install -U pip wheel setuptools
python3 -m pip install -U langchain-core langchain-community langchain-ollama langchain-chroma langchain-text-splitters chromadb pypdf


## 3) Add Your PDFs

Create data/ and place PDFs inside:
  mkdir -p data
  copy PDFs into ./data

Example:
  data/dora.pdf


## 4) Ingest (Build the Vector Database)

### Run ingestion:
  python3 ingest.py

This will:
  - load all *.pdf in ./data
  - split pages into chunks
  - embed chunks
  - store them in ./chroma_db

### Rebuild from scratch
If you change chunking settings or embeddings model:
  rm -rf chroma_db
  python3 ingest.py


## 5) Chat (Ask Questions)

### Start the interactive chatbot:
python3 chat.py

Type questions; type exit to quit.

### Behavior
  - The assistant is prompted to answer only using retrieved context.
  - If the answer is not in the provided context, it should respond with: I don't know.
  - The prompt includes simple source citations: [filename, page N]




## Common Issues / Troubleshooting

### python: command not found
Use python3:
python3 --version

### Missing packages (ModuleNotFoundError)
Ensure venv is active:
source .venv/bin/activate
python3 -m pip install -U <package>

### Ollama not responding
Check Ollama:
ollama list
systemctl status ollama --no-pager

### No PDFs found
Make sure PDFs are in ./data and have .pdf extension:
ls -lah data


## Notes

This project uses RAG, not fine-tuning, to answer from PDF content. RAG is typically the best approach for document-grounded Q&A because it keeps the knowledge source explicit and updateable.
Fine-tuning can be added later for style/format consistency, but should not replace retrieval for factual grounding.
