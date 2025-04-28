from fastapi import APIRouter, HTTPException
from app.schemas.agent import AgentResponse
from app.services.agent_service import AgentService

router = APIRouter(prefix="/agents", tags=["Agents"])

@router.post("/", response_model=AgentResponse)
async def run_agent(message: str):
    try:
        return await AgentService.run(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))