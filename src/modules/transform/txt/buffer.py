from src.core.interfaces import PipelineHandler
import asyncio

class BufferSentences(PipelineHandler[str,str]):
    async def start(self,data):
        input_txt = await self._to_async_queue(data)
        buffer = ""
        punctuation = {'.', '!', '?', ';', ':'}
        try:
            while True:
                token = await input_txt.get()
                if token is None:
                    break
                buffer += token
                if any(char in token for char in punctuation):
                    yield buffer
                    buffer = ""
        finally:
            if buffer != "":
                await input_txt.put(buffer)
            await input_txt.put(None)