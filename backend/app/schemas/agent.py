from typing import Any, Dict
from pydantic import BaseModel

class AgentResponse(BaseModel):
    response: Any
    thoughts: Dict[str, Any]