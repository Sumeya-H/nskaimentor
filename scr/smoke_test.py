"""
smoke_test.py
Quick smoke test for NSK.AI Mentor Agent retrieval pipeline.
"""

from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA


def build_index(file_path: str, persist_dir: str = "chroma_index"):
    """
    Load a text file, chunk it, embed it, and store it in Chroma DB.
    """
    print(f"📂 Loading file: {file_path}")
    loader = TextLoader(file_path)
    docs = loader.load()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    # Build embeddings and store in Chroma
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(chunks, embeddings, persist_directory=persist_dir)
    db.persist()

    print(f"✅ Index built and saved to {persist_dir}")
    return db


def run_smoke_test(db):
    """
    Run two simple test questions to verify retrieval + LLM answering.
    """
    retriever = db.as_retriever()
    llm = ChatOpenAI(temperature=0)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    test_questions = [
        "What are the Phase One project requirements?",
        "What tools do I need for a Hackathon project?"
    ]

    for q in test_questions:
        print(f"\n❓ Question: {q}")
        response = qa({"query": q})
        print("💡 Answer:", response["result"])
        print("📖 Sources:")
        for doc in response["source_documents"]:
            print("-", doc.metadata.get("source", "Unknown"), ":", doc.page_content[:150], "...")


if __name__ == "__main__":
    # 🔧 Replace this with one of your real data files (Markdown, txt, etc.)
    sample_file = "data/phase_one_requirements.md"

    db = build_index(sample_file)
    run_smoke_test(db)
