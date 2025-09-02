# evaluator/repo_eval.py
import re
import requests
from langchain_groq import ChatGroq

LLM = ChatGroq(model="llama3-8b-8192", temperature=0)

PHASE_ONE_CRITERIA = {
    "Document ingestion with chunking": [
        r"PDFLoader", r"docx", r"TextSplitter", r"chunk"
    ],
    "Embeddings generated (model noted)": [
        r"OpenAIEmbeddings", r"HuggingFaceEmbeddings"
    ],
    "Vector store used": [
        r"FAISS", r"Chroma", r"Pinecone"
    ],
    "Retrieval implemented": [
        r"similarity_search", r"as_retriever", r"BM25"
    ],
    "Prompt template + chain": [
        r"PromptTemplate", r"Chain", r"Runnable"
    ],
    "User interaction (CLI/Web/API)": [
        r"streamlit", r"gradio", r"fastapi", r"flask", r"notebook"
    ]
}

def fetch_repo_tree(owner_repo: str):
    url = f"https://api.github.com/repos/{owner_repo}/git/trees/HEAD?recursive=1"
    return requests.get(url).json()

def fetch_file(owner_repo: str, path: str) -> str:
    url = f"https://raw.githubusercontent.com/{owner_repo}/HEAD/{path}"
    r = requests.get(url)
    return r.text if r.status_code == 200 else ""

def heuristic_scan(owner_repo: str):
    tree = fetch_repo_tree(owner_repo)
    paths = [it["path"] for it in tree.get("tree", []) if it.get("type") == "blob"]
    big = ""
    for p in paths:
        if p.endswith((".py", ".md", ".txt", ".ipynb")):
            txt = fetch_file(owner_repo, p)
            big += f"\n\n## {p}\n{txt[:20000]}"
    results = {crit: any(re.search(p, big, re.I) for p in pats) 
               for crit, pats in PHASE_ONE_CRITERIA.items()}
    return results, big[:80000]

def evaluate_repo(owner_repo: str) -> str:
    checks, excerpt = heuristic_scan(owner_repo)
    score, total = sum(checks.values()), len(checks)
    report = "\n".join([f"- {c}: {'✅' if v else '❌'}" for c, v in checks.items()])
    prompt = f"""
You are a senior reviewer.
Repo: {owner_repo}

Phase One results ({score}/{total}):
{report}

Based on this excerpt, give fixes for unmet items only:
{excerpt[:6000]}
"""
    resp = LLM.invoke(prompt)
    return f"Checklist:\n{report}\n\nFeedback:\n{getattr(resp,'content',resp)}"
