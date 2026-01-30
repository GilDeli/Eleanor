from .base import InputProvider
import sounddevice as sd
import asyncio
import subprocess

class Microphon(InputProvider):

    async def listen(self):
        loop = asyncio.get_running_loop()
        audio_queue =  asyncio.Queue()
        def callback(indata, frames, time, status):
            loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))
        device = sd.RawInputStream(samplerate=16000, blocksize = 4000, device=12, dtype='int16', channels=1, callback=callback)
        try:
            device.start()
            print('> microphon listen')
            while True:
                item = await audio_queue.get()
                yield item
        finally:
            device.stop

    
    async def close(self):
        pass
