from functools import lru_cache
from fastapi import Depends
from app.core.config import get_settings, Settings
from app.services.openai_service import OpenAIService
from app.services.conversation_svc_db import ConversationServiceDB
from app.db.session import async_session
from sqlalchemy.ext.asyncio import AsyncSession

@lru_cache
def get_openai_service(settings: Settings = Depends(get_settings)):
    return OpenAIService(api_key=settings.openai_api_key)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

def get_conversation_service(db: AsyncSession = Depends(get_db)) -> ConversationServiceDB:
    return ConversationServiceDB(db)