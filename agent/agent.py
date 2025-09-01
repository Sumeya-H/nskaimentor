import os
from langchain_groq import ChatGroq
from agent.prompts import SYSTEM_TUTOR, QA_TEMPLATE
from agent.tools import tool_search_docs
from langchain.prompts import ChatPromptTemplate

from dotenv import load_dotenv
load_dotenv()

LLM = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)

def answer_question(question: str) -> str:
    ctx, refs = tool_search_docs(question, k=4)
    prompt = ChatPromptTemplate.from_template(QA_TEMPLATE).format(question=question, context=ctx)
    msgs = [{"role":"system","content":SYSTEM_TUTOR},
            {"role":"user","content":prompt}]
    resp = LLM.invoke(msgs).content
    # Append references
    lines = ["\nReferences:"]
    for r in refs:
        src = r.get("source_file") or r.get("repo") or r.get("video_id") or r.get("source","?")
        ref = r.get("reference_text") or f"{r.get('chapter','?')}, {r.get('lesson','?')}"
        lines.append(f"- {src} | {ref}")
    return resp + "\n" + "\n".join(lines)

print("<<<<<", answer_question("What are Phase One requirements?")[:500], ">>>>>")