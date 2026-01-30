import asyncio
import aiohttp
from .base import TtsProvider

class PiperProvider(TtsProvider):
    def __init__(self,config:dict = None):
        config = config or {}
        self.url = config.get('url') or "http://localhost:5500"
        self.params = {k: v for k,v in config.items() if k not in ('url')}

    async def synthesize(self,txt_queue:asyncio.Queue,**kwargs):
        while True:
            chunk = await txt_queue.get()
            if chunk is None:
                txt_queue.task_done()
                yield None
                break
            if len(chunk)<=1:
                txt_queue.task_done()
                continue
            try:
                response = await self._synthesize(chunk,**kwargs)
                yield response
                await asyncio.sleep(0.1)
            finally:
                txt_queue.task_done()

    async def _synthesize(self,txt: str,**kwargs):
        data = {
            "text":txt,
            **self.params,
            **kwargs
        }
        #print(txt,end='' ,flush=True)
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url,json=data) as response:
                response.raise_for_status()
                return await response.read()
    
    async def close(self):
        pass