import pytest
from httpx import AsyncClient
from app.main import create_app
from app.schemas.message import Message

@pytest.mark.asyncio
async def test_suggestion():
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "history": [Message(role="user", content="Oi").model_dump()]
        }
        resp = await ac.post("/chat/suggestion", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["suggestions"]) == 3