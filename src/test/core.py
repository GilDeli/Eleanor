import asyncio
from typing import Optional
from enum import Enum

from src.core.event_manager import AsyncEventManager
from src.core.pipeline import PipelineLinear
from src.core.interfaces import PipelineHandler


class ModuleTest(PipelineHandler[str,str]):
    def __init__(self,out):
        self.out: str = out
    async def start(self,data: str) -> str:
        print(data + " -> Processing -> " + self.out)
        return self.out
    async def stop(self):
        print("Module stop")

class EventType(Enum):
    TEST_EVENT = 'test_event'

mod1 = ModuleTest("1")
mod2 = ModuleTest("2")
mod3 = ModuleTest("3")

mini_pipeline = PipelineLinear([mod1,mod2,mod3])
test_pipeline = PipelineLinear([mod1,mini_pipeline,mod3])

eve_man = AsyncEventManager[EventType]()

eve_man.subscribe(EventType.TEST_EVENT,test_pipeline.start)

asyncio.run(eve_man.notify(EventType.TEST_EVENT,"0"))