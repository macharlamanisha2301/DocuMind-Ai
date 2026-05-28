# import streamlit as st
# import uuid
# import time
# from memory_sqlalchemy import update_chat_title
# from rag_pipeline import load_pdf, split_documents, create_retriever, ask_question
# from memory_sqlalchemy import init_db, load_chat_history, get_all_sessions

# # =========================
# # INIT
# # =========================
# st.set_page_config(page_title="DocuMind AI", layout="wide")
# init_db()

# st.title("🤖 DocuMind AI")

# # =========================
# # SESSION
# # =========================
# if "session_id" not in st.session_state:
#     st.session_state.session_id = str(uuid.uuid4())

# if "retriever" not in st.session_state:
#     st.session_state.retriever = None

# # =========================
# # SIDEBAR (FIXED 🔥)
# # =========================
# st.sidebar.title("💬 Chats")

# # ➕ New Chat
# if st.sidebar.button("➕ New Chat"):
#     st.session_state.session_id = str(uuid.uuid4())

#     # 🔥 CLEAR OLD DATA
#     st.session_state.retriever = None
#     st.session_state.last_file = None

#     # Optional (clears uploader UI)
#     st.session_state.uploaded_file = None

# st.sidebar.markdown("---")

# sessions = get_all_sessions()

# for s_id, title in sessions.items():

#     display_name = title if title else "New Chat"

#     if len(display_name) > 30:
#         display_name = display_name[:30] + "..."

#     if s_id == st.session_state.session_id:
#         display_name = "👉 " + display_name

#     if st.sidebar.button(display_name):
#         st.session_state.session_id = s_id

# # =========================
# # RENAME CHAT (ADD HERE 🔥)
# # =========================
# st.sidebar.markdown("---")
# st.sidebar.subheader("✏️ Rename Chat")

# new_title = st.sidebar.text_input("Enter new chat name")

# if st.sidebar.button("Save Name"):
#     if new_title.strip() != "":
#         update_chat_title(st.session_state.session_id, new_title)
#         st.sidebar.success("✅ Renamed!")
#         st.rerun()

# # =========================
# # LOAD CHAT HISTORY
# # =========================
# history = load_chat_history(st.session_state.session_id)

# for chat in history:
#     with st.chat_message("user"):
#         st.markdown(chat["user"])

#     with st.chat_message("assistant"):
#         st.markdown(chat["assistant"])

# # =========================
# # FILE UPLOAD
# # =========================
# uploaded_file = st.file_uploader("📎 Upload PDF", type=["pdf"])

# if uploaded_file:

#     with st.chat_message("assistant"):
#         status = st.empty()

#         status.markdown("📄 Loading PDF...")
#         time.sleep(0.3)

#         with open("temp.pdf", "wb") as f:
#             f.write(uploaded_file.read())

#         docs = load_pdf("temp.pdf")

#         status.markdown("✂️ Splitting document...")
#         time.sleep(0.3)

#         chunks = split_documents(docs)

#         status.markdown("🧠 Creating embeddings...")
#         time.sleep(0.3)

#         retriever = create_retriever(chunks)
#         st.session_state.retriever = retriever

#         status.markdown("✅ Ready!")

# # =========================
# # INPUT
# # =========================
# query = st.chat_input("Ask something about your document...")

# # =========================
# # HANDLE QUERY
# # =========================
# if query:

#     with st.chat_message("user"):
#         st.markdown(query)

#     with st.chat_message("assistant"):
#         placeholder = st.empty()

#         steps = [
#             "🤔 Thinking...",
#             "🔍 Searching document...",
#             "🧠 Generating response..."
#         ]

#         for step in steps:
#             placeholder.markdown(step)
#             time.sleep(0.3)

#         retriever = st.session_state.retriever

#         if retriever:
#             answer = ask_question(
#                 retriever,
#                 query,
#                 st.session_state.session_id
#             )
#         else:
#             answer = "⚠️ Please upload a PDF first."

#         # typing effect
#         typed = ""
#         for ch in answer:
#             typed += ch
#             placeholder.markdown(typed)
#             time.sleep(0.002)


import streamlit as st
import uuid
import time

from rag_pipeline import load_pdf, split_documents, create_retriever, ask_question
from memory_sqlalchemy import (
    init_db,
    load_chat_history,
    get_all_sessions,
    update_chat_title
)

# =========================
# INIT
# =========================
st.set_page_config(page_title="DocuMind AI", layout="wide")
init_db()

st.title("🤖 DocuMind AI")

# =========================
# SESSION
# =========================
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "retriever" not in st.session_state:
    st.session_state.retriever = None

# =========================
# SIDEBAR
# =========================
st.sidebar.title("💬 Chats")

# ➕ New Chat
if st.sidebar.button("➕ New Chat"):
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.retriever = None
    st.session_state.last_file = None

st.sidebar.markdown("---")

sessions = get_all_sessions()

# =========================
# CHAT LIST WITH INLINE ACTIONS
# =========================
for s_id, title in sessions.items():

    col1, col2 = st.sidebar.columns([8,1])

    display_name = title if title else "New Chat"

    if len(display_name) > 25:
        display_name = display_name[:25] + "..."

    if s_id == st.session_state.session_id:
        display_name = "👉 " + display_name

    # Chat select
    if col1.button(display_name, key=f"chat_{s_id}"):
        st.session_state.session_id = s_id

    # Rename button
    if col2.button("✏️", key=f"rename_{s_id}"):
        st.session_state.rename_id = s_id

# =========================
# INLINE RENAME INPUT
# =========================
if "rename_id" in st.session_state:

    st.sidebar.markdown("### ✏️ Rename Chat")

    new_name = st.sidebar.text_input("New name")

    if st.sidebar.button("Save", key="save_rename"):
        if new_name.strip():
            update_chat_title(st.session_state.rename_id, new_name)
            del st.session_state.rename_id
            st.rerun()

# =========================
# LOAD CHAT HISTORY
# =========================
history = load_chat_history(st.session_state.session_id)

for chat in history:
    with st.chat_message("user"):
        st.markdown(chat["user"])

    with st.chat_message("assistant"):
        st.markdown(chat["assistant"])

# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader(
    "📎 Upload PDF",
    type=["pdf"],
    key=st.session_state.session_id  # reset on new chat
)

if uploaded_file:

    with st.chat_message("assistant"):
        status = st.empty()

        status.markdown("📄 Loading PDF...")
        time.sleep(0.3)

        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        docs = load_pdf("temp.pdf")

        status.markdown("✂️ Splitting document...")
        time.sleep(0.3)

        chunks = split_documents(docs)

        status.markdown("🧠 Creating embeddings...")
        time.sleep(0.3)

        retriever = create_retriever(chunks)
        st.session_state.retriever = retriever

        status.markdown("✅ Ready!")

# =========================
# INPUT
# =========================
query = st.chat_input("Ask something about your document...")

# =========================
# HANDLE QUERY
# =========================
if query:

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        placeholder = st.empty()

        steps = [
            "🤔 Thinking...",
            "🔍 Searching document...",
            "🧠 Generating response..."
        ]

        for step in steps:
            placeholder.markdown(step)
            time.sleep(0.3)

        retriever = st.session_state.retriever

        if retriever:
            answer = ask_question(
                retriever,
                query,
                st.session_state.session_id
            )
        else:
            answer = "⚠️ Please upload a PDF first."

        # typing effect
        typed = ""
        for ch in answer:
            typed += ch
            placeholder.markdown(typed)
            time.sleep(0.002)