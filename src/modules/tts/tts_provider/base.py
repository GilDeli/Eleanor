from src.core.interfaces import Provider
from abc import abstractmethod

from typing import List,Dict,Any
import asyncio

class TtsProvider(Provider):
    @abstractmethod
    async def synthesize(self,txt_queue:asyncio.Queue,*args,**kwargs):
        pass