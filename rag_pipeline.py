import os
from dotenv import load_dotenv
load_dotenv()

# PDF Loader
from langchain_community.document_loaders import PyPDFLoader

# Text splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Embeddings + Vector DB
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Retriever
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers.ensemble import EnsembleRetriever

# LLM
from langchain_groq import ChatGroq

# 🔥 MEMORY
from memory_sqlalchemy import save_chat, load_chat_history

# =========================
# LOAD PDF
# =========================
def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load()

# =========================
# SPLIT DOCUMENTS
# =========================
def split_documents(documents):
    num_pages = len(documents)

    if num_pages <= 5:
        chunk_size = 600
        overlap = 100
    elif num_pages <= 20:
        chunk_size = 900
        overlap = 150
    else:
        chunk_size = 1200
        overlap = 200

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )

    return splitter.split_documents(documents)

# =========================
# RETRIEVER
# =========================
def create_retriever(chunks):
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = FAISS.from_documents(chunks, embedding)
    vector_retriever = vector_db.as_retriever(search_kwargs={"k": 6})

    bm25 = BM25Retriever.from_documents(chunks)
    bm25.k = 6

    retriever = EnsembleRetriever(
        retrievers=[vector_retriever, bm25],
        weights=[0.7, 0.3]
    )

    return retriever

# =========================
# ASK QUESTION
# =========================
def ask_question(retriever, query, session_id):

    docs = retriever.get_relevant_documents(query)
    context = "\n".join([doc.page_content for doc in docs])

    # 🔥 LOAD MEMORY
    history = load_chat_history(session_id)

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant"
    )

    prompt = f"""
CHAT HISTORY:
{history}

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{query}

INSTRUCTIONS:

0. GREETING HANDLING:
   - If user greets (hi, hello, hey, sup, etc.)
   - 1. If the user greets (hi, hello, hey, sup):
   - Reply ONLY with a greeting like:
     "Hey! 👋 Sup? How can I help you with the document?"
   - DO NOT add anything else to the greeting response. Keep it short and friendly.

1. FIRST check if the question is related to ANY concept, term, or keyword present in the document.

2. IF RELATED:
   - By default → give a SHORT, CLEAN SUMMARY (main points only)
   - Use bullet points where possible
   - Keep it concise and easy to understand

3. IF USER ASKS:
   - "Explain", "Elaborate", "In detail"
   → THEN give a detailed explanation

4. IF USER ASKS:
   - "Differentiate", "Compare"
   → Provide answer in TABLE FORMAT

5. IF USER ASKS:
   - "Give table"
   → Always return structured table

6. IF USER ASKS:
   - "Flowchart", "Workflow", "Steps", "Process"
   → Represent using structured format like:
     Step 1 → Step 2 → Step 3
   → Keep it clean and readable

7. IF TERM EXISTS BUT NOT FULLY EXPLAINED:
   - You ARE ALLOWED to explain it properly using your knowledge

8. IF COMPLETELY UNRELATED:
   - Respond ONLY:
     "This question is not related to the uploaded document."

9. DO NOT hallucinate unrelated info

10. DO NOT give long answers unless explicitly asked


11. RESPONSE STYLE STRICT RULES:
   - DO NOT repeat or restate the user's question
   - DO NOT say phrases like:
     "To answer your question..."
     "The user asked..."
     "Based on your question..."
   - DO NOT explain what you are doing
   - DO NOT add unnecessary introduction
   - ONLY give the final answer directly

12. KEEP ANSWER DIRECT:
   - Start immediately with the answer
   - Use bullet points or structured format if needed

STRICT OUTPUT RULES:

- If the user asks a QUESTION → DO NOT greet
- Greeting should happen ONLY when the message is PURE greeting (no question)

- DO NOT include:
  "USER QUESTION:"
  "FINAL ANSWER:"
  "MAIN MOTTO:"
  or any labels

- DO NOT repeat or restate the question
- DO NOT mix greeting + answer

- ONLY return the answer directly

- If answer is list → return only bullet points

FINAL ANSWER:
"""

    response = llm.invoke(prompt)

    # 🔥 SAVE MEMORY
    save_chat(session_id, query, response.content)

    return response.content