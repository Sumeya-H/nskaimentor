# NSK.AI Mentor Agent

An AI-powered teaching assistant built to support **bootcamp participants** and **mentors** at scale.  
It helps students navigate study materials, get instant project feedback, and reuse knowledge from past cohorts — all in one place.  

---

## 🚩 The Problem
Bootcamp cohorts face recurring challenges:
- New participants feel lost navigating tons of study materials, recordings, and GitHub repos.
- Mentors are overwhelmed and can’t provide personalized support to every student.
- Project submissions often miss criteria due to unclear requirements.
- Valuable knowledge from past cohorts gets lost.

👉 Result: Students struggle, mentors burn out, and institutional knowledge disappears.

---

## ✅ Our Solution
The **NSK.AI Mentor Agent** supports bootcamp participants 24/7 through:

- **Q&A Agent**  
  Answers technical & non-technical questions from:  
  - Bootcamp study materials  
  - Session recordings (YouTube transcripts)  
  - Public GitHub repos  
  - Project requirements & rubrics  

- **Project Evaluator Agent**  
  Students submit their GitHub repo → Agent checks criteria → Provides feedback:  
  - ✅ Criteria met  
  - ❌ Missing components  
  - 💡 Suggestions for improvement  

- **Knowledge Search**  
  Semantic search across past projects & sessions:  
  - “Show me a Phase One project with RAG + Pinecone.”  
  - “Find all sessions about Agentic AI.”  

---

## 🧩 How It Works
### Demo Flow
1. **Student logs in** → Asks “What’s the difference between Phase One and Hackathon requirements?”  
   - Agent retrieves docs → Returns clear, cited answer.  

2. **Student uploads repo** → Agent evaluates against checklist.  
   - Example: Checks for RAG, embeddings, Streamlit imports.  
   - Returns ✅/❌ + improvement tips.  

3. **Student searches past work** → Finds relevant repos & transcripts.  

---

## 🛠 Tech Stack
- **LLM Frameworks:** LangChain, LlamaIndex  
- **Vector DB:** FAISS (for hackathon), Pinecone/Weaviate (scalable)  
- **Frontend:** Streamlit  
- **Repo Analysis:** GitHub API, Python (AST, regex, tree-sitter)  
- **Agents:** Multi-agent orchestration (Q&A, Repo Evaluator, Coordinator)  

---

## 📂 Project Structure
