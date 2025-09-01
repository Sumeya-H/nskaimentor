# agent/tools.py
from rag.index import load_chroma
from rag.retrieval import top_k
from rag.loaders import load_youtube_transcript, load_github_readme

VS = None
def _vs():
    global VS
    if VS is None: VS = load_chroma()
    return VS

def tool_search_docs(query: str, k:int=4):
    docs = top_k(_vs(), query, k)
    ctx = "\n\n".join([f"[{i}] {d.page_content}" for i,d in enumerate(docs)])
    refs = [d.metadata for d in docs]
    return ctx, refs

def tool_fetch_youtube_transcript(url_or_id: str):
    return load_youtube_transcript(url_or_id)[0].page_content

def tool_fetch_repo_readme(repo: str):
    docs = load_github_readme(repo)
    return docs[0].page_content if docs else ""
