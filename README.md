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
├─ data/ # put your PDFs here (not committed by default)
├─ chroma_db/ # local vector database (not committed)
├─ ingest.py # build/update vector DB from PDFs
├─ chat.py # interactive Q&A chatbot
├─ .gitignore
└─ README.md


## Prerequisites

- Ubuntu Desktop 24.04 LTS (or similar Linux)
- Python 3.10+ recommended
- Ollama installed and running

## 1) Install Ollama + Models

### Install Ollama
Follow the official installer:
- https://ollama.com/download

### Pull required models
```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
ollama pull mxbai-embed-large //used

Quick check:
ollama run llama3.2:3b



