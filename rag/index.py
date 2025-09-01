# rag/index.py
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
from pathlib import Path

EMB = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def build_chroma(docs: list[Document], persist_dir: str="vectorstore"):
    vs = Chroma.from_documents(docs, embedding=EMB, persist_directory=persist_dir)
    return vs

def load_chroma(persist_dir: str="vectorstore"):
    return Chroma(embedding_function=EMB, persist_directory=persist_dir)
