from src.core.interfaces import PipelineHandler
from .input_provider import Microphon

class InputAudio(PipelineHandler[None,bytes]):
    agent = Microphon()
    async def start(self):
        #async for chunk in self.agent.listen():
        #    yield chunk
        return await self._to_async_queue(self.agent.listen())
    
    async def stop():
        pass