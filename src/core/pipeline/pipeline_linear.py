from typing import List, Any, TypeVar, Generic, Optional
from types import NoneType
from src.core.interfaces import PipelineHandler
from .pipeline import PipelineBase
import asyncio
import inspect

class PipelineLinear(PipelineBase):
    _stop: bool = False
    def __init__(self, pipeline: List[PipelineHandler]):
        self._pipeline = pipeline
        super().__init__(input_type=pipeline[0]._input_type,output_type=pipeline[-1]._output_type)

    async def start(self,data: asyncio.Queue = None) -> Optional[asyncio.Queue]:
        prev_chain = None
        data = await self._to_async_queue(data)
        for chain in self._pipeline:
            if self._stop:
                return
            elif chain._input_type is NoneType:
                if asyncio.iscoroutinefunction(chain.start):
                    result = await chain.start()
                else:
                    result = chain.start()
            elif data is None:
                return
            elif (prev_chain is None) or (prev_chain._output_type == chain._input_type):
                if asyncio.iscoroutinefunction(chain.start):
                    result = await chain.start(data)
                else:
                    result = chain.start(data)
            else:
                return
            data = await self._to_async_queue(result)
            prev_chain = chain
        await self._coroutines.put(None)
        return data

    async def await_end(self):
        while True:
            corutine = await self._coroutines.get()
            if corutine is None:
                break
            if asyncio.iscoroutine(corutine):
                await corutine
    async def stop(self):
        self._stop = True
        await asyncio.sleep(0.1)
        for chain in self._pipeline:
            chain.stop()
        

    async def _catch_stream_data(self,function ,data = None):
        output_data = asyncio.Queue()
        async def task():
            try:
                if data is not None:
                    generator = function(data)
                else:
                    generator = function()
                async for chain_data in generator:
                    if chain_data is not None:
                        await output_data.put(chain_data)
                    else:
                        break
            finally:
                await output_data.put(None)

        asyncio.create_task(task())
        return output_data