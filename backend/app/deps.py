from functools import lru_cache
from fastapi import Depends
from app.core.config import get_settings, Settings
from app.services.openai_service import OpenAIService
from app.services.conversation_svc import ConversationService

@lru_cache
def get_openai_service(settings: Settings = Depends(get_settings)):
    return OpenAIService(api_key=settings.openai_api_key)

def get_conversation_svc():
    return ConversationService