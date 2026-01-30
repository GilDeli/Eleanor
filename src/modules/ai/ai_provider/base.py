from src.core.interfaces import Provider
from abc import abstractmethod
from typing import List,Dict,Any

class AIProvider (Provider):
    @abstractmethod
    async def generate(self, promt: str, *args,**kwargs):
        pass