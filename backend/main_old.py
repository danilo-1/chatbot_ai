"""backend/main.py – FastAPI chatbot com OpenAI + STREAM e seletor de modelo
================================================================================
Suporta:
- Modelos configuráveis por chamada (gpt-4o, gpt-3.5-turbo etc.)
- Streaming em /chat/stream (envia pedaços da resposta enquanto gera)
- Compatível com SDK v1 e v0.28
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agents import Agent, Runner
from functions.agents import triage_agent

# ---------------------------------------------------------------------------
# Load .env
# ---------------------------------------------------------------------------
try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    raise RuntimeError("Instale python-dotenv: pip install python-dotenv")

load_dotenv(dotenv_path=Path(__file__).with_name(".env"))

# ---------------------------------------------------------------------------
# OpenAI SDK (v1 ou legado)
# ---------------------------------------------------------------------------
try:
    import openai
except ModuleNotFoundError:
    raise RuntimeError("Instale openai: pip install openai")

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY não definida")

client = openai.OpenAI(api_key=API_KEY)
def ask_openai(history: List[Message], model: str) -> str:
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[m.model_dump() for m in history],
        )
        return resp.choices[0].message.content
    except Exception as e:
        raise HTTPException(500, f"Erro OpenAI: {e}")

# ---------------------------------------------------------------------------
app = FastAPI(title="Chatbot OpenAI", version="1.2.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ALLOWED_ORIGIN", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    model: str  # agora obrigatório

class ChatResponse(BaseModel):
    session_id: str
    response: str
    history: List[Message]

class HistoryResponse(BaseModel):
    session_id: str
    history: List[Message]

class SuggestionRequest(BaseModel):
    history: List[Message]

class SuggestionResponse(BaseModel):
    suggestions: list[str]

class TestAgentRequest(BaseModel):
    message: str

# Update the AgentResponse model to match actual response structure
class AgentResponse(BaseModel):
    response: Any
    thoughts: Dict[str, Any] = {
        "agent": None,
        "model": None,
    }

conversations: Dict[str, List[Message]] = {}

@app.post("/chat", response_model=ChatResponse)
def chat(chat: ChatRequest):
    session_id = chat.session_id or str(uuid4())
    conversations.setdefault(session_id, [])

    conversations[session_id].append(Message(role="user", content=chat.message))
    resposta = ask_openai(conversations[session_id], model=chat.model)
    conversations[session_id].append(Message(role="assistant", content=resposta))

    return ChatResponse(session_id=session_id, response=resposta, history=conversations[session_id])

@app.get("/history/{session_id}", response_model=HistoryResponse)
def get_history(session_id: str):
    if session_id not in conversations:
        raise HTTPException(404, "Sessão não encontrada")
    return HistoryResponse(session_id=session_id, history=conversations[session_id])

@app.delete("/history/{session_id}")
def delete_history(session_id: str):
    if session_id not in conversations:
        raise HTTPException(404, "Sessão não encontrada")
    conversations.pop(session_id, None)
    return {"detail": f"Sessão {session_id} removida"}

@app.post("/suggestion", response_model=SuggestionResponse)
def suggestion_endpoint(sugg: SuggestionRequest):
    # Cria um prompt baseado no histórico para gerar 3 sugestões relevantes
    prompt = ("Analise o seguinte histórico de conversa e sugira 3 perguntas que avancem o "
              "diálogo de forma útil, cada uma em uma linha, lembre-se de dar a sugestão como se você estivesse perguntando para a IA e não retorne nada a mais do que só as sugestões:\n")
    for m in sugg.history:
        prompt += f"{m.role}: {m.content}\n"
    # Utilize a IA da OpenAI para gerar as sugestões
    response_text = ask_openai(sugg.history + [Message(role="system", content=prompt)], model="gpt-4o-mini")
    # Divide a resposta em linhas, removendo linhas vazias e limites para 3 sugestões
    suggestions_list = [s.strip() for s in response_text.splitlines() if s.strip()][:3]
    print(f"Suggestions: {suggestions_list}")
    return SuggestionResponse(suggestions=suggestions_list)

@app.get("/default-suggestions", response_model=SuggestionResponse)
def default_suggestions():
    # Cria um prompt para gerar 5 perguntas sobre assuntos bem distintos
    prompt = ("Sem histórico de conversa. Por favor, sugira 5 perguntas "
              "sobre assuntos completamente diferentes e variados "
              "para iniciar uma conversa, lembre-se de dar a sugestão como se você estivesse perguntando para a IA e não retorne nada a mais do que só as sugestões:")
    response_text = ask_openai([Message(role="system", content=prompt)], model="gpt-4o-mini")
    # Divide a resposta em linhas, removendo linhas vazias e limitando a 5 sugestões
    suggestions_list = [s.strip() for s in response_text.splitlines() if s.strip()][:5]
    return SuggestionResponse(suggestions=suggestions_list)

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/agentes", response_model=AgentResponse)
async def test_agent(request: TestAgentRequest):
    try:
        # Create a new triage agent instance
        agent = triage_agent()  # Call the function to get the agent instance
        
        # Run the agent with the provided message and await the result
        result = await Runner.run(agent, request.message)
        print(f"Agent result: {result}")
        # Return the response with thoughts
        return AgentResponse(
            response=result.final_output,  # Changed from final_output to output
            thoughts={
                "agent": result.last_agent.name,
                "model": result.last_agent.model,
                  # Using the agent name directly
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error running agent: {str(e)}"
        )