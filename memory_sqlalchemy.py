from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# =========================
# DB SETUP
# =========================
engine = create_engine("sqlite:///chat_memory.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# =========================
# TABLE
# =========================
class Chat(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Text)
    question = Column(Text)
    answer = Column(Text)
    title = Column(Text)  # ✅ NEW

# =========================
# INIT DB
# =========================
def init_db():
    Base.metadata.create_all(bind=engine)

# =========================
# SAVE CHAT
# =========================
def save_chat(session_id, question, answer):
    session = SessionLocal()

    # Check if session already exists
    existing = session.query(Chat).filter(Chat.session_id == session_id).first()

    if existing:
        title = existing.title
    else:
        title = question[:40]  # first question becomes title

    chat = Chat(
        session_id=session_id,
        question=question,
        answer=answer,
        title=title
    )

    session.add(chat)
    session.commit()
    session.close()

# =========================
# LOAD CHAT HISTORY
# =========================
def load_chat_history(session_id):
    session = SessionLocal()

    chats = (
        session.query(Chat)
        .filter(Chat.session_id == session_id)
        .order_by(Chat.id)
        .all()
    )

    session.close()

    history = []
    for chat in chats:
        history.append({
            "user": chat.question,
            "assistant": chat.answer
        })

    return history

# =========================
# GET ALL SESSIONS + TITLES
# =========================
def get_all_sessions():
    session = SessionLocal()

    chats = session.query(Chat).all()
    session.close()

    session_dict = {}

    for chat in chats:
        if chat.session_id not in session_dict:
            session_dict[chat.session_id] = chat.title

    return session_dict


def update_chat_title(session_id, new_title):
    session = SessionLocal()

    chats = session.query(Chat).filter(Chat.session_id == session_id).all()

    for chat in chats:
        chat.title = new_title

    session.commit()
    session.close()