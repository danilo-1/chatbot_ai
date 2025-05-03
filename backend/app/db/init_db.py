# Em um script separado, por exemplo: backend/app/db/init_db.py
import asyncio
from app.db.session import engine
from app.db.base import Base
from app.models import message_model  # Para importar os models

async def init_db():
    async with engine.begin() as conn:
        # Cria todas as tabelas
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())