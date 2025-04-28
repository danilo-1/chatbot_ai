from app.schemas.agent import AgentResponse
from agents import Runner
from app.llm import triage_agent

class AgentService:
    @staticmethod
    async def run(message: str) -> AgentResponse:
        agent = triage_agent()
        result = await Runner.run(agent, message)
        return AgentResponse(
            response=result.final_output,
            thoughts={
                "agent": result.last_agent.name,
                "model": result.last_agent.model,
            },
        )