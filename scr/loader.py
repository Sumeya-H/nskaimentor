""" NSK.AI Mentor Agent – Unified Document Loaders

This module provides simple, battle-tested loaders for: • PDFs (local paths or HTTP URLs) • Markdown / plaintext files (local paths or HTTP URLs) • YouTube transcripts (by URL or video id) • GitHub README files (public repos; optional token for private repos)

It returns LangChain Document objects and includes a helper to chunk them.

Requirements (add these to your requirements.txt): langchain>=0.2.7 langchain-community>=0.2.7 langchain-text-splitters>=0.2.2 pypdf>=4.2.0 youtube-transcript-api>=0.6.2 requests>=2.32.2

Optional (for private GitHub repos): set env GH_TOKEN or pass token explicitly. """ from future import annotations

import base64 import os import tempfile from typing import Iterable, List, Optional from urllib.parse import urlparse

import requests from langchain_core.documents import Document from langchain_text_splitters import RecursiveCharacterTextSplitter from langchain_community.document_loaders import ( PyPDFLoader, TextLoader, YoutubeLoader, )

-----------------------------

Internal helpers

-----------------------------

def _is_http_url(path_or_url: str) -> bool: try: p = urlparse(path_or_url) return p.scheme in {"http", "https"} except Exception: return False

def _download_to_temp(url: str, suffix: str = "") -> str: """Download a URL to a temporary file and return its local path.""" resp = requests.get(url, timeout=60) resp.raise_for_status() fd, tmp_path = tempfile.mkstemp(suffix=suffix) with os.fdopen(fd, "wb") as f: f.write(resp.content) return tmp_path

def _fetch_text_url(url: str, token: Optional[str] = None) -> str: headers = {} if token: headers["Authorization"] = f"Bearer {token}" resp = requests.get(url, headers=headers, timeout=60) resp.raise_for_status() return resp.text

-----------------------------

Public loaders

-----------------------------

def load_pdfs(paths_or_urls: Iterable[str]) -> List[Document]: """Load one or many PDFs (local paths or HTTP URLs) into Documents.

Each PDF will be split by pages by the underlying loader. You can later
call `chunk_documents` to further chunk by characters.
"""
docs: List[Document] = []
tmp_files: List[str] = []
try:
    for item in paths_or_urls:
        if _is_http_url(item):
            # Keep original extension if possible for better parsing
            suffix = os.path.splitext(urlparse(item).path)[1] or ".pdf"
            local_path = _download_to_temp(item, suffix=suffix)
            tmp_files.append(local_path)
        else:
            local_path = item

        loader = PyPDFLoader(local_path)
        docs.extend(loader.load())
    return docs
finally:
    # Clean up any temp files we created
    for path in tmp_files:
        try:
            os.remove(path)
        except Exception:
            pass

def load_markdown_or_text(paths_or_urls: Iterable[str]) -> List[Document]: """Load Markdown or plaintext from local paths OR HTTP URLs.

For URLs, we fetch into a single Document. For local files, we use
TextLoader (which reads the file from disk).
"""
docs: List[Document] = []
for item in paths_or_urls:
    if _is_http_url(item):
        text = _fetch_text_url(item)
        docs.append(
            Document(page_content=text, metadata={"source": item, "type": "markdown/url"})
        )
    else:
        # `TextLoader` works well for .md, .txt, .py, etc.
        loader = TextLoader(item, encoding="utf-8")
        file_docs = loader.load()
        # annotate the type for downstream routing if needed
        for d in file_docs:
            d.metadata.setdefault("type", "markdown/local")
        docs.extend(file_docs)
return docs

def load_youtube(video_url_or_id: str, languages: Optional[list[str]] = None) -> List[Document]: """Load YouTube transcript as Documents.

Args:
    video_url_or_id: full URL (https://www.youtube.com/watch?v=...) or the bare video id.
    languages: Preferred transcript languages. Defaults to ["en"].
"""
if languages is None:
    languages = ["en"]

# Normalize to URL for the LangChain loader
if "http" not in video_url_or_id:
    video_url = f"https://www.youtube.com/watch?v={video_url_or_id}"
else:
    video_url = video_url_or_id

loader = YoutubeLoader.from_youtube_url(
    video_url,
    add_video_info=True,
    language=languages,
    translation="en",
)
docs = loader.load()
for d in docs:
    d.metadata.setdefault("type", "youtube_transcript")
return docs

def load_github_readme(repo_url: str, branch: str = "main", token: Optional[str] = None) -> List[Document]: """Load README from a GitHub repository (public or private with token).

Accepts a GitHub repo web URL like:
  https://github.com/org/repo

Tries common README filenames via raw.githubusercontent.com. If not found,
falls back to the GitHub REST API (base64 content).
"""
# Extract owner/repo from URL
parsed = urlparse(repo_url)
parts = [p for p in parsed.path.split("/") if p]
if len(parts) < 2:
    raise ValueError("repo_url must look like https://github.com/<owner>/<repo>")
owner, repo = parts[0], parts[1].replace(".git", "")

token = token or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")

# Try raw content endpoints first
candidates = [
    "README.md",
    "README.MD",
    "Readme.md",
    "README.rst",
    "readme.md",
]

headers = {"Accept": "application/vnd.github.v3+json"}
if token:
    headers["Authorization"] = f"Bearer {token}"

for name in candidates:
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{name}"
    resp = requests.get(raw_url, headers=headers, timeout=60)
    if resp.status_code == 200 and resp.text.strip():
        return [
            Document(
                page_content=resp.text,
                metadata={
                    "source": raw_url,
                    "repo": f"{owner}/{repo}",
                    "branch": branch,
                    "filename": name,
                    "type": "github_readme",
                },
            )
        ]

# Fall back to GitHub API: /repos/{owner}/{repo}/readme (returns base64 content)
api_url = f"https://api.github.com/repos/{owner}/{repo}/readme?ref={branch}"
resp = requests.get(api_url, headers=headers, timeout=60)
if resp.status_code == 200:
    data = resp.json()
    content_b64 = data.get("content")
    encoding = data.get("encoding")
    path = data.get("path", "README.md")
    if content_b64 and encoding == "base64":
        text = base64.b64decode(content_b64).decode("utf-8", errors="ignore")
        return [
            Document(
                page_content=text,
                metadata={
                    "source": api_url,
                    "repo": f"{owner}/{repo}",
                    "branch": branch,
                    "filename": path,
                    "type": "github_readme",
                },
            )
        ]

raise FileNotFoundError(
    f"README not found for {owner}/{repo} on branch '{branch}'."
)

-----------------------------

Utilities

-----------------------------

def chunk_documents( docs: List[Document], chunk_size: int = 1200, chunk_overlap: int = 200, ) -> List[Document]: """Chunk Documents for better retrieval (RAG).

Uses RecursiveCharacterTextSplitter so Markdown, code blocks, and paragraphs
chunk intelligently. Tune sizes for your model context window.
"""
splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size, chunk_overlap=chunk_overlap
)
return splitter.split_documents(docs)

all = [ "load_pdfs", "load_markdown_or_text", "load_youtube", "load_github_readme", "chunk_documents", ]

if name == "main": # Minimal smoke test (won't run on GitHub web UI; for local dev): # python src/loaders.py pdfs = load_pdfs(["https://arxiv.org/pdf/1706.03762.pdf"])  # Attention is All You Need md = load_markdown_or_text(["https://raw.githubusercontent.com/langchain-ai/langchain/master/README.md"]) yt = load_youtube("dQw4w9WgXcQ")  # example video id gh = load_github_readme("https://github.com/langchain-ai/langchain") all_docs = pdfs + md + yt + gh chunks = chunk_documents(all_docs) print( f"Loaded: PDFs={len(pdfs)} MD/TXT={len(md)} YT={len(yt)} GH={len(gh)} | chunks={len(chunks)}" )

