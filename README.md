# DocuMind-AI

DocuMind AI is a document intelligence system that allows users to interact with PDF files using natural language. Instead of manually going through long documents, users can upload a file and ask questions to get relevant and concise answers.

The project combines Retrieval-Augmented Generation (RAG) with a simple persistent memory system so that conversations are stored and can be revisited later.

---

## About the Project

Working with large documents is time-consuming and often inefficient when trying to extract specific information. This system is designed to simplify that process.

It reads the uploaded PDF, breaks it into smaller chunks, retrieves relevant parts based on the query, and generates answers using a language model. At the same time, it stores the conversation so users can continue from where they left off.

---

## How It Works

1. A PDF is uploaded by the user  
2. The document is split into smaller chunks  
3. Two retrieval methods are used:
   - Semantic search (FAISS)
   - Keyword-based search (BM25)  
4. Relevant content is selected  
5. The language model generates an answer  
6. The interaction is stored in a database  

---

## Features

- Ask questions from uploaded PDF documents  
- Hybrid retrieval for better accuracy  
- Stores chat history using a database  
- Supports multiple chat sessions  
- Allows renaming of chats  
- Provides concise answers, tables, and structured outputs when required  

---

## Use Cases

- Students reviewing study material  
- Understanding technical documentation  
- Extracting insights from reports  
- Resume or profile analysis  
- Research and academic reading  

---

## Tech Stack

Frontend:
- Streamlit  

Backend:
- Python  

Retrieval:
- FAISS (semantic search)  
- BM25 (keyword search)  

Model:
- Groq (LLaMA 3)

Database:
- SQLite with SQLAlchemy  

---

## Requirements

Make sure Python 3.9 or above is installed.

Install the required libraries manually using:

```bash
pip install streamlit langchain langchain-community langchain-groq faiss-cpu sentence-transformers sqlalchemy python-dotenv
```

Environment Setup
Create a .env file in the project directory and add your API key:

GROQ_API_KEY=your_api_key_here

How to Run
streamlit run app.py
Project Structure
app.py                 - Streamlit UI
rag_pipeline.py        - Retrieval and response logic
memory_sqlalchemy.py   - Database and memory handling
.gitignore             - Ignored files
Notes
API keys are not hardcoded

Temporary files and database files are excluded using .gitignore

Chat history is stored and can be reused across sessions

Conclusion
This project demonstrates how retrieval-based systems and memory can be combined to build a more interactive and practical document analysis tool.
