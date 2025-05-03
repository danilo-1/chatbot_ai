from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas.chat import ChatRequest, ChatResponse, HistoryResponse
from app.schemas.message import Message
from app.schemas.suggestion import SuggestionRequest, SuggestionResponse
from app.services.openai_service import OpenAIService
from app.deps import get_openai_service, get_conversation_service
from app.db.session import AsyncSession
from app.services.conversation_svc_db import ConversationServiceDB

router = APIRouter(prefix="/chat", tags=["Chat"])

# ---------- Chat ----------
@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest,
               openai: OpenAIService = Depends(get_openai_service),
               conv_service: AsyncSession = Depends(get_conversation_service)):
    conversation = None
    if req.session_id:
        conversation = await conv_service.get_conversation(req.session_id)
    if not conversation:
        conversation = await conv_service.create_conversation(req.session_id)
    session_id = conversation.session_id
    # Adiciona a mensagem do usuário
    await conv_service.add_message(conversation, "user", req.message)
    # Obtém o histórico (converte os DBMessage para o schema Message)
    history = [Message(role=m.role, content=m.content) for m in conversation.messages]


    content = await openai.completion(history, model=req.model)
    answer = content.choices[0].message.content
    await conv_service.add_message(conversation, "assistant", answer)

    # Atualiza o histórico e retorna a resposta
    await conv_service.db.refresh(conversation)
    history = [Message(role=m.role, content=m.content) for m in conversation.messages]
    return ChatResponse(session_id=session_id, response=answer, history=history)

# ---------- Histórico ----------
@router.get("/history/{session_id}", response_model=HistoryResponse)
async def get_history(session_id: str, conv_service: AsyncSession = Depends(get_conversation_service)):
    conversation = await conv_service.get_conversation(session_id)
    if not conversation:
        raise HTTPException(404, "Sessão não encontrada")
    history = [Message(role=m.role, content=m.content) for m in conversation.messages]
    return HistoryResponse(session_id=session_id, history=history)

@router.delete("/history/{session_id}")
async def delete_history(session_id: str, conv_service: AsyncSession = Depends(get_conversation_service)):
    deleted = await conv_service.delete_conversation(session_id)
    if not deleted:
        raise HTTPException(404, "Sessão não encontrada")
    return {"detail": f"Sessão {session_id} removida"}


# ---------- Sugestões ----------
@router.post("/suggestion", response_model=SuggestionResponse)
async def suggestion(req: SuggestionRequest, openai: OpenAIService = Depends(get_openai_service)):
    prompt = ("Analise o histórico e sugira 3 perguntas que avancem o diálogo, cada uma em uma linha, "
              "retornando APENAS as perguntas:\n")
    for m in req.history:
        prompt += f"{m.role}: {m.content}\n"

    resp = await openai.completion(req.history + [Message(role="system", content=prompt)], model="gpt-4o-mini")
    suggestions = [s.strip() for s in resp.choices[0].message.content.splitlines() if s.strip()][:3]
    return SuggestionResponse(suggestions=suggestions)

@router.get("/default-suggestions", response_model=SuggestionResponse)
async def default_suggestions(openai: OpenAIService = Depends(get_openai_service)):
    prompt = ("Sem histórico. Sugira 5 perguntas SOBRE ASSUNTOS DISTINTOS para iniciar a conversa, "
              "retornando APENAS as perguntas:")
    resp = await openai.completion([Message(role="system", content=prompt)], model="gpt-4o-mini")
    suggestions = [s.strip() for s in resp.choices[0].message.content.splitlines() if s.strip()][:5]
    return SuggestionResponse(suggestions=suggestions)