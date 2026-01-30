from src.core.interfaces import PipelineHandler
import asyncio

from pedalboard import Pedalboard, Gain, Compressor, Reverb, HighpassFilter, LowpassFilter
import numpy as np
import soundfile as sf
import io

class FixSynthetic(PipelineHandler[bytes,bytes]):
    async def start(self,data):
        input_data = await self._to_async_queue(data)
        try:
            while True:
                audio = await input_data.get()
                if audio is None:
                    break
                yield await self._processing(audio)
        finally:
            await input_data.put(None)

    async def _processing(self,audio_bytes):
        audio, samplerate = sf.read(io.BytesIO(audio_bytes))
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)
        
        board = Pedalboard([
            HighpassFilter(cutoff_frequency_hz=60),
            Compressor(threshold_db=-20, ratio=2, attack_ms=5, release_ms=200),
            Gain(gain_db=2),
            Reverb(room_size=0.15, damping=0.7, wet_level=0.08, dry_level=0.92),
            HighpassFilter(cutoff_frequency_hz=60),
            LowpassFilter(cutoff_frequency_hz=8000)
        ])
        
        processed = board(audio, samplerate)
        
        buffer = io.BytesIO()
        sf.write(buffer, processed, samplerate, format='WAV')
        processed_bytes = buffer.getvalue()
        
        return processed_bytes