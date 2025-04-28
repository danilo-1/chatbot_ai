from fastapi import APIRouter, HTTPException, Body
from app.services.process_service import ProcessService

router = APIRouter(prefix="/process", tags=["Process"])

@router.post("/", response_model=str)
async def process_code(code: str = Body(..., embed=True)):
    """
    Executa o código fornecido em um contêiner Docker e retorna a saída.
    """
    try:
        process_service = ProcessService()
        return process_service.executar_codigo_docker(codigo=code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))