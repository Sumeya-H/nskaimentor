from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings

embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = FAISS.load_local("faiss_index", embedding=embedding_model)

def retrieve_top_k(query: str, k: int = 5):
    results = vector_store.similarity_search_with_score(query, k=k)
    output = []
    for doc, score in results:
        output.append({
            "content": doc.page_content,
            "metadata": doc.metadata,
            "score": score
        })
    return output
