import sounddevice as sd
import asyncio
import subprocess

class Microphon():
    micro_audio_queue = asyncio.Queue()

    def __init__(self):
        loop = asyncio.get_running_loop()
        def callback(indata, frames, time, status):
            loop.call_soon_threadsafe(self.micro_audio_queue.put_nowait, bytes(indata))
        self.device = sd.RawInputStream(samplerate=16000, blocksize = 4000, device=8, dtype='int16', channels=1, callback=callback)

    def _clear_audio_queue(self):
        while not self.micro_audio_queue.empty():
            try:
                self.micro_audio_queue.get_nowait()
                self.micro_audio_queue.task_done()
            except asyncio.QueueEmpty:
                break

    async def get_audio(self):
        self._clear_audio_queue()
        self.device.start()
        print('\n> microphon listen')
        return self.micro_audio_queue

class Mpv():
    async def play_audio_stream(self,audio_queue:asyncio.Queue()):
        while True:
            try:
                audio_chunk =  await audio_queue.get()
                if audio_chunk is None:
                    break
                await self.play_audio(audio_chunk)
            finally:
                audio_queue.task_done()

    async def play_audio(self,audio_chunk):
        try:
            mpv_process = await asyncio.create_subprocess_exec(
                'mpv', '--no-cache', '--force-seekable=yes', '-',
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            mpv_process.stdin.write(audio_chunk)
            await mpv_process.stdin.drain()
        finally:
            mpv_process.stdin.close()
            await mpv_process.wait()