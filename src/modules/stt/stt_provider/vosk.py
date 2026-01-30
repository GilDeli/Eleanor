import websockets
import json
import shutil
from .base import SttProvider

class VoskProvider(SttProvider):
    def __init__(self):
        pass

    async def recognize(self,audio_queue,sample_rate=16000):
        async with websockets.connect('ws://127.0.0.1:2700') as websocket:
            config = {
                "config":{
                    "sample_rate": sample_rate,
                    "max_alternatives": 0,
                }
            }
            await websocket.send(json.dumps(config))

            while True:
                data = await audio_queue.get()
                if data is None:
                    yield None
                    break
                await websocket.send(data)
                response = await websocket.recv()
                try:
                    result_json = json.loads(response)
                    partial_text = result_json.get("partial", "")
                    if partial_text:
                        print (f"> {partial_text}",end="\r",flush=True)
                    final_text = result_json.get("text", "")
                    if final_text:
                        print(" " * shutil.get_terminal_size().columns, end="\r", flush=True)
                        print(": " +final_text)
                        yield final_text
                        yield None
                except json.JSONDecodeError:
                    print(f"Failed to parse JSON: {response}")
                    continue

    async def close(self):
        pass