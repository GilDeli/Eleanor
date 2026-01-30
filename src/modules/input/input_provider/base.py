from src.core.interfaces import Provider
from abc import abstractmethod

class InputProvider(Provider):
    @abstractmethod
    async def listen(self,*args,**kwargs):
        pass