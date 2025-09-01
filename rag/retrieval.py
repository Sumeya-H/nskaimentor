# rag/retrieval.py
from typing import List
from langchain_core.documents import Document

def top_k(vs, query: str, k: int=4) -> List[Document]:
    return vs.similarity_search(query, k=k)
