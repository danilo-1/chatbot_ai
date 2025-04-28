from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas.chat import ChatRequest, ChatResponse, HistoryResponse
from app.schemas.message import Message
from app.schemas.suggestion import SuggestionRequest, SuggestionResponse
from app.services.conversation_svc import ConversationService
from app.services.openai_service import OpenAIService
from app.deps import get_openai_service, get_conversation_svc

router = APIRouter(prefix="/chat", tags=["Chat"])

# ---------- Chat ----------
@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest,
               openai: OpenAIService = Depends(get_openai_service),
               conv: ConversationService = Depends(get_conversation_svc)):
    session_id = req.session_id or conv.new_id()
    history = conv.get(session_id)
    history.append(Message(role="user", content=req.message))

    content = await openai.completion(history, model=req.model)
    answer = content.choices[0].message.content
    history.append(Message(role="assistant", content=answer))

    return ChatResponse(session_id=session_id, response=answer, history=history)

# ---------- Streaming ----------
@router.post("/stream")
async def chat_stream(req: ChatRequest,
                      openai: OpenAIService = Depends(get_openai_service),
                      conv: ConversationService = Depends(get_conversation_svc)):
    session_id = req.session_id or conv.new_id()
    history = conv.get(session_id)
    history.append(Message(role="user", content=req.message))

    async def gen():
        async for token in openai.stream_content(history, req.model):
            yield token
    return StreamingResponse(gen(), media_type="text/plain")

# ---------- Histórico ----------
@router.get("/history/{session_id}", response_model=HistoryResponse)
async def get_history(session_id: str, conv: ConversationService = Depends(get_conversation_svc)):
    hist = conv.get(session_id)
    print(hist)
    if not hist:
        raise HTTPException(404, "Sessão não encontrada")
    return HistoryResponse(session_id=session_id, history=hist)

@router.delete("/history/{session_id}")
async def delete_history(session_id: str, conv: ConversationService = Depends(get_conversation_svc)):
    conv.delete(session_id)
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