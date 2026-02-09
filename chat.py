from pathlib import Path

from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

DB_DIR = Path("chroma_db")
COLLECTION = "pdf_docs"

PROMPT = ChatPromptTemplate.from_template(
    """You are a document Q&A assistant.
Answer ONLY using the provided context. If the answer is not in the context, say: "I don't know."

Context:
{context}

Question:
{question}

Answer (include brief citations like [filename, page N]):
"""
)

def format_docs_with_citations(docs):
    blocks = []
    for d in docs:
        src = d.metadata.get("source", "unknown_source")
        page = d.metadata.get("page", "unknown_page")
        cite = f"[{Path(src).name}, page {page}]"
        blocks.append(f"{cite}\n{d.page_content}")
    return "\n\n---\n\n".join(blocks)

def main():
    #embeddings = OllamaEmbeddings(model="nomic-embed-text")
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    vector_store = Chroma(
        collection_name=COLLECTION,
        embedding_function=embeddings,
        persist_directory=str(DB_DIR),
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 8})
    llm = ChatOllama(model="llama3.2:3b", temperature=0)

    chain = PROMPT | llm | StrOutputParser()

    print("PDF RAG chat. Type 'exit' to quit.\n")
    while True:
        question = input("You> ").strip()
        if question.lower() in {"exit", "quit"}:
            break

        docs = retriever.invoke(question)
        context = format_docs_with_citations(docs)

        answer = chain.invoke({"context": context, "question": question})
        print("\nAssistant>\n" + answer + "\n")

if __name__ == "__main__":
    main()
