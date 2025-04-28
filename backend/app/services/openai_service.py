from openai import OpenAI
from app.schemas.message import Message
from typing import List
from starlette.concurrency import iterate_in_threadpool

class OpenAIService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    async def completion(self, messages: List[Message], model: str, stream: bool = False):
        try:
            resp = self.client.chat.completions.create(
                model=model,
                messages=[m.model_dump() for m in messages],
                stream=stream,
            )
            return resp
        except Exception as e:
            print(f"OpenAI API Error: {str(e)}")
            raise

    async def stream_content(self, messages: List[Message], model: str):
        # Obtém o generator síncrono
        generator = self.client.chat.completions.create(
            model=model,
            messages=[m.model_dump() for m in messages],
            stream=True,
        )
        # Itera o generator dentro do threadpool, possibilitando usar async for
        async for chunk in iterate_in_threadpool(generator):
            # Acessa o atributo 'content' diretamente no objeto delta
            token = chunk.choices[0].delta.content
            yield token if token is not None else ""