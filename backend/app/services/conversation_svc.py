from uuid import uuid4
from app.schemas.message import Message

class ConversationService:
    """In‑memory store; easily replace with Redis/DB if needed"""
    _store: dict[str, list[Message]] = {}

    @classmethod
    def get(cls, session_id: str):
        # Ensure the session exists in the store
        return cls._store.setdefault(session_id, [])

    @classmethod
    def add(cls, session_id: str, message: Message):
        cls._store.setdefault(session_id, []).append(message)

    @classmethod
    def new_id(cls) -> str:
        session_id = str(uuid4())
        cls._store.setdefault(session_id, [])
        return session_id

    @classmethod
    def delete(cls, session_id: str):
        cls._store.pop(session_id, None)