from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from pydantic import BaseModel

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

# Guardrail agent to check content
guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework or inappropriate content.",
    output_type=HomeworkOutput,
    model="gpt-4o-mini"  # Fast, lightweight model for simple checks
)

# Specialized agents for different purposes
math_tutor_agent = Agent(
    name="Math Tutor",
    instructions="""You are a helpful math tutor. Help explain mathematical concepts clearly and provide step-by-step solutions.
    Always:
    - Break down complex problems
    - Use clear examples
    - Explain your reasoning
    - Be encouraging and patient""",
    model="gpt-4o-mini"  # More powerful model for complex mathematical reasoning
)

history_tutor_agent = Agent(
    name="History Tutor", 
    instructions="""You are a knowledgeable history expert. Help explain historical events, contexts, and connections.
    Always:
    - Provide relevant dates and context
    - Explain cause and effect relationships
    - Reference reliable sources
    - Make history engaging and relatable""",
    model="gpt-4o-mini"  # Strong model for detailed historical analysis
)

coding_tutor_agent = Agent(
    name="Coding Tutor",
    instructions="""You are an experienced programming teacher. Help explain coding concepts and solve programming problems.
    Always:
    - Provide code examples
    - Explain best practices
    - Break down complex concepts
    - Encourage good coding habits""",
    model="gpt-4o-mini"  # Powerful model for code understanding and generation
)

# Guardrail function remains the same
async def content_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.is_homework,
    )

def triage_agent():
    """Creates and returns a configured triage agent"""
    return Agent(
        name="Triage Agent",
        instructions="""You determine which specialized agent would be best suited to help with the user's question.
        Consider the topic and nature of the question carefully.""",
        model="gpt-4o-mini",  # Fast model for initial triage
        handoffs=[math_tutor_agent, history_tutor_agent, coding_tutor_agent],
        input_guardrails=[
            InputGuardrail(guardrail_function=content_guardrail)
        ]
    )
