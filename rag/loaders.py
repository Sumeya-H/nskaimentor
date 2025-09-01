# rag/loaders.py
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.schema import Document
import requests, re, base64

def load_pdf(path: Path) -> list[Document]:
    return PyPDFLoader(str(path)).load()

def load_markdown(path: Path) -> list[Document]:
    return TextLoader(str(path), encoding="utf-8").load()

def load_youtube_transcript(url_or_id: str) -> list[Document]:
    video_id = url_or_id.split("v=")[-1].split("&")[0] if "youtube" in url_or_id else url_or_id
    print("<<<<<<<<<<<<<<<<<<<<<<<",video_id)
    transcript = YouTubeTranscriptApi.fetch(video_id)
    text = " ".join([t["text"] for t in transcript])
    return [Document(page_content=text, metadata={"source":"youtube", "video_id":vid})]

def load_github_readme(repo: str) -> list[Document]:
    # repo example: "owner/name"
    api = f"https://api.github.com/repos/{repo}/readme"
    r = requests.get(api, headers={"Accept":"application/vnd.github+json"})
    if r.status_code != 200: return []
    content = base64.b64decode(r.json()["content"]).decode("utf-8", errors="ignore")
    return [Document(page_content=content, metadata={"source":"github", "repo":repo, "path":"README.md"})]
