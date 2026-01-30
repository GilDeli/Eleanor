from src.core.interfaces import Provider
from abc import abstractmethod

class OutputProvider(Provider):
    @abstractmethod
    async def transfer(self,*args,**kwargs):
        pass