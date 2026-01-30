from .tts_provider import Piper
from src.core.interfaces import PipelineHandler
from typing import Union
import asyncio

class TtsManager(PipelineHandler[str,bytes]):
    agent = Piper()
    async def start(self,data: Union[str,asyncio.Queue]):
        audio = await self._to_async_queue(data)
        async for chunk in self.agent.synthesize(audio):
            yield chunk
    
    async def stop():
        pass