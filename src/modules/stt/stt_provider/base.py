from src.core.interfaces import Provider
from abc import abstractmethod
from typing import List,Dict,Any

class SttProvider(Provider):
    @abstractmethod
    async def recognize(self,audio_queue,*args,**kwargs):
        pass