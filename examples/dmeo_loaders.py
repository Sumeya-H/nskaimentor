from src.loaders import (
    load_pdfs, load_markdown_or_text, load_youtube,
    load_github_readme, chunk_documents
)

docs = []
docs += load_pdfs(["https://arxiv.org/pdf/1706.03762.pdf"])
docs += load_markdown_or_text(["https://raw.githubusercontent.com/langchain-ai/langchain/master/README.md"])
docs += load_youtube("dQw4w9WgXcQ")  # replace with your session video
docs += load_github_readme("https://github.com/langchain-ai/langchain")

chunks = chunk_documents(docs)
print("docs:", len(docs), "chunks:", len(chunks))
