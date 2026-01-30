from src.core.interfaces import PipelineHandler
from .out_provider import MpvProvider
from typing import Union
import asyncio

class OutAudio(PipelineHandler[bytes,None]):
    agent = MpvProvider() 
    async def start(self,data: Union[bytes,asyncio.Queue]):
        if isinstance(data,bytes):
            audio: asyncio.Queue
            await audio.put(data)
            await audio.put(None)
        else:
            audio = data
        await self.agent.transfer(audio)
    
    async def stop():
        pass