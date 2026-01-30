from .base import OutputProvider

import asyncio
import subprocess

class MpvProvider(OutputProvider):
    async def transfer(self,audio_queue:asyncio.Queue()):
        while True:
            try:
                audio_chunk =  await audio_queue.get()
                if audio_chunk is None:
                    break
                await self._play_audio(audio_chunk)
            finally:
                audio_queue.task_done()

    async def close():
        pass

    async def _play_audio(self,audio_chunk):
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