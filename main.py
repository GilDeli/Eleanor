import asyncio
import subprocess
import sys

import modules.tts.tts_provider as tts_provider
import modules.ai.ai_provider as ai_provider
import modules.stt.stt_provider as stt_provider
import modules.io as io 

async def main():
    agent_ai = ai_provider.Ollama()
    agent_tts = tts_provider.Piper()
    agent_stt = stt_provider.Vosk()
    micro = io.Microphon()
    mpv = io.Mpv()
    txt_queue = asyncio.Queue()
    audio_queue = asyncio.Queue()
   
    async def get_txt_stt():
        audio_queue_micro = await micro.get_audio()
        txt = await agent_stt.recognize_stream(audio_queue=audio_queue_micro)
        return txt
   
    async def collect_ai_tokens():
        txt = await get_txt_stt()
        buffer = ""
        punctuation = {'.', '!', '?', ';', ':'}
        try:
            async for token in agent_ai.generate_stream(txt):
                buffer += token
                if any(char in token for char in punctuation):
                    await txt_queue.put(buffer)
                    buffer = ""
        finally:
            if buffer != "":
                await txt_queue.put(buffer)
            await txt_queue.put(None)

    async def tts_synthesize():
        try:
            async for audio_chunk in agent_tts.synthesize_stream(txt_queue):
                if isinstance(audio_chunk,Exception):
                    print(f"Ошибка синтезации речи:{audio_chunk}")
                    continue
                if audio_chunk is not None:
                    await audio_queue.put(audio_chunk)
                while audio_queue.qsize() > 5: await asyncio.sleep(0.4)
        finally:
            await audio_queue.put(None)

    while True: await asyncio.gather(collect_ai_tokens(),tts_synthesize(),mpv.play_audio_stream(audio_queue))
    

asyncio.run(main())