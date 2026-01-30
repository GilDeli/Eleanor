from abc import ABC,abstractmethod
from typing import Any, Type, TypeVar, Generic, get_origin, get_args, Optional
import asyncio
import inspect

InputType = TypeVar('InputType')
OutputType = TypeVar('OutputType')

class PipelineHandler(ABC, Generic[InputType, OutputType]):
    _init_type: bool = False
    _input_type: Type = None
    _output_type: Type = None

    _coroutines = asyncio.Queue()

    @abstractmethod
    async def start(self,data: asyncio.Queue)-> Optional[asyncio.Queue]:
        pass
   # @abstractmethod
   # async def stop(self,*args,**kwargs):
   #     pass
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for base in cls.__orig_bases__ if hasattr(cls, '__orig_bases__') else []:
            origin = get_origin(base)
            if origin is PipelineHandler:
                args = get_args(base)
                if len(args) >= 2:
                    cls._input_type = args[0]
                    cls._output_type = args[1]
                    cls._init_type = True
                break

    async def _to_async_queue(self,data) -> asyncio.Queue:
        output_data = asyncio.Queue()
        async def task(generator):
            try:
                async for chain_data in generator:
                    if chain_data is not None:
                        await output_data.put(chain_data)
                    else:
                        break
            finally:
                await output_data.put(None)

        if inspect.isasyncgen(data):
            await self._coroutines.put(asyncio.create_task(task(data)))
        elif isinstance(data,asyncio.Queue):
            return data
        else:
            await output_data.put(data)
            await output_data.put(None)
        return output_data