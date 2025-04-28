from typing import List, Optional
from pydantic import BaseModel, Field
from .message import Message

class ChatRequest(BaseModel):
    message: str
    model: str = Field(..., pattern="^(gpt|o4).+")
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    session_id: str
    response: str
    history: List[Message]

class HistoryResponse(BaseModel):
    session_id: str
    history: List[Message]