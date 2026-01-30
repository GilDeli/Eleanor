from typing import Dict, Callable, Any, Set, Type, TypeVar, Generic, List
import asyncio
import inspect
from enum import Enum

EventType = TypeVar('EventType', bound=Enum)

class AsyncEventManager(Generic[EventType]):
    def __init__(self):
        self._listeners: Dict[EventType, Set[Callable[...,None]]] = {}

    def subscribe(self,event_type: EventType, callback: Callable[...,None]):
        if event_type not in self._listeners:
            self._listeners[event_type] = set()
        self._listeners[event_type].add(callback)

    def unsubscribe(self,event_type: EventType,callback: Callable[...,None]):
        if event_type not in self._listeners:
            return False
        try:
            self._listeners[event_type].remove(callback)
            if not self._listeners[event_type]:
                del self._listeners[event_type]
            return True
        except KeyError:
            return False

    async def notify(self,event_type: EventType, *args, **kwargs):
        if event_type not in self._listeners:
            return

        task_queue: List[asyncio.Task] = []
        for listener in self._listeners[event_type]:
            try:
                try: 
                    task_queue.append(asyncio.create_task(listener(*args,**kwargs)))
                except TypeError as e:
                    print(e)
                    try:
                        task_queue.append(asyncio.create_task(listener()))
                    except TypeError as e:
                        print(e)
                        continue
            except Exception as e:
                print(e)
                continue
        for task in task_queue:
            try:
                await task
            except Exception as e:
                print(e)
                continue