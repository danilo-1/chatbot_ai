from pydantic import BaseModel
from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework or inappropriate content.",
    output_type=HomeworkOutput,
    model="gpt-4o-mini",
)

async def content_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    data = HomeworkOutput.model_validate(result.final_output)
    return GuardrailFunctionOutput(output_info=data, tripwire_triggered=data.is_homework)