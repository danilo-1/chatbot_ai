from typing import List
from pydantic import BaseModel
from .message import Message

class SuggestionRequest(BaseModel):
    history: List[Message]

class SuggestionResponse(BaseModel):
    suggestions: List[str]