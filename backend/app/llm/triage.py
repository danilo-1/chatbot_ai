from agents import Agent, InputGuardrail
from .guardrails import content_guardrail
from .specialised.specialists import math_agent, history_agent, coding_agent

__all__ = ["triage_agent"]

def triage_agent():
    return Agent(
        name="Triage Agent",
        instructions="""Determine the best specialised agent for the question…""",
        model="gpt-4o-mini",
        handoffs=[math_agent(), history_agent(), coding_agent()],
        input_guardrails=[
            InputGuardrail(guardrail_function=content_guardrail)
        ],
    )