from abc import ABC,abstractmethod

class Provider(ABC):
    @abstractmethod
    async def close():
        pass