from src.loaders import (
    load_pdfs,
    load_markdown_or_text,
    load_youtube,
    load_github_readme,
    chunk_documents
)

# Step 1: Collect resources
docs = []

# Example PDF (replace with your bootcamp docs)
docs += load_pdfs(["https://arxiv.org/pdf/1706.03762.pdf"])

# Example Markdown (replace with your study notes or repo files)
docs += load_markdown_or_text([
    "https://raw.githubusercontent.com/langchain-ai/langchain/master/README.md"
])

# Example YouTube transcript (replace with your bootcamp session link)
docs += load_youtube("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Example GitHub repo README (replace with your participant repos)
docs += load_github_readme("https://github.com/langchain-ai/langchain")

# Step 2: Chunk docs
chunks = chunk_documents(docs, chunk_size=1200, chunk_overlap=200)

print(f"Total documents: {len(docs)}")
print(f"Total chunks: {len(chunks)}")
