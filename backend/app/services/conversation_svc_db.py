from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.message_model import Conversation, Message as DBMessage

class ConversationServiceDB:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_conversation(self, session_id: str):
        result = await self.db.execute(
            select(Conversation).where(Conversation.session_id == session_id)
        )
        return result.scalars().first()

    async def create_conversation(self, session_id: str = None):
        if not session_id:
            session_id = str(uuid4())
        conversation = Conversation(session_id=session_id)
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        return conversation

    async def add_message(self, conversation: Conversation, role: str, content: str):
        message = DBMessage(role=role, content=content)
        conversation.messages.append(message)
        await self.db.commit()
        await self.db.refresh(conversation)
        return message

    async def delete_conversation(self, session_id: str):
        conversation = await self.get_conversation(session_id)
        if conversation:
            await self.db.delete(conversation)
            await self.db.commit()
            return True
        return False