from loaders import load_pdf, load_markdown, load_youtube_transcript, load_github_readme

# Test PDF loader
pdf_docs = load_pdf("sample.pdf")
print("PDF:", pdf_docs[:1])  # print just first chunk

# Test Markdown loader
md_docs = load_markdown("README.md")
print("Markdown:", md_docs[:1])

# Test YouTube loader
yt_docs = load_youtube_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
print("YouTube:", yt_docs[:1])

# Test GitHub loader
repo_docs = load_github_readme("https://github.com/your-org/your-repo")
print("GitHub README:", repo_docs[:1])
