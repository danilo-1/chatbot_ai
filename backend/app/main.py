from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.v1 import routes_chat, routes_agents, routes_health, routes_process


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Chatbot OpenAI", version="2.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.allowed_origin],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.include_router(routes_chat.router)
    app.include_router(routes_agents.router)
    app.include_router(routes_health.router)
    app.include_router(routes_process.router)
    return app

app = create_app()  # para uvicorn