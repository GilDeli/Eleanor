from .stt_provider import Vosk
from src.core.interfaces import PipelineHandler
from typing import Union
import asyncio

class SttManager(PipelineHandler[bytes,str]):
    agent = Vosk()
    async def start(self,data: Union[bytes,asyncio.Queue]):
        audio = await self._to_async_queue(data)
        async for chunk in self.agent.recognize(audio):
            yield chunk
            if chunk is None:
                break

    
    async def stop():
        pass