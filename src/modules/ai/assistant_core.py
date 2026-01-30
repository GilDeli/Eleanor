from typing import Union
import asyncio

from src.core.interfaces import PipelineHandler
from .ai_provider import Ollama


class AssistantCore(PipelineHandler[str,str]):
    agent = Ollama()

    async def start(self,data:Union[str,asyncio.Queue]):
        if (isinstance(data,asyncio.Queue)):
            promt = await data.get()
        else:
            promt = data
        async for chunk in self.agent.generate(prompt=promt):
            yield chunk

    async def stop():
        pass