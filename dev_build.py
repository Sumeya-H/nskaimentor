# dev_build.py (ad-hoc)
from pathlib import Path
from rag.loaders import load_pdf, load_markdown, load_youtube_transcript, load_github_readme
from rag.chunking import split_and_tag
from rag.index import build_chroma

docs = []
docs += load_markdown(Path("data/phase_one_requirements.md"))
docs += load_github_readme("Sumeya-H/textbook-tutor")  # adjust if needed
docs += load_youtube_transcript("https://www.youtube.com/watch?v=GR42jIvQjHs")  # sample
# add a sample PDF locally: data/guide.pdf
docs += load_pdf(Path("data/Level 1.pdf"))

chunks = split_and_tag(docs)
build_chroma(chunks)
print("Index built with", len(chunks), "chunks")


from rag.index import load_chroma
from rag.retrieval import top_k
vs = load_chroma()
for d in top_k(vs, "What are Phase One requirements?", 3):
    print(d.metadata, d.page_content[:200], "\n---")
