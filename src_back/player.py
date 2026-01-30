from pedalboard import Pedalboard, Gain, Compressor, Reverb, HighpassFilter, LowpassFilter
import requests
from requests.models import Response
import subprocess
import numpy as np
import soundfile as sf
import io

def play_audio (audio):
    mpv_process = subprocess.Popen(
        ['mpv', '--no-cache', '--force-seekable=yes', '-'],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    for chunk in audio.iter_content(chunk_size=8192):
        if chunk:  
            mpv_process.stdin.write(chunk)
    
    mpv_process.stdin.close()
    mpv_process.wait()  

def process_audio(original_response: requests.Response) -> requests.Response:
    """Обработка аудио без пересоздания Response"""
    audio_bytes = original_response.content

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
    
    original_response._content = processed_bytes
    original_response.headers['Content-Type'] = 'audio/wav'
    original_response.headers['Content-Length'] = str(len(processed_bytes))
    original_response.headers['X-Processed'] = 'true'
    
    original_response.raw._body = processed_bytes
    if hasattr(original_response.raw, '_fp'):
        original_response.raw._fp = io.BytesIO(processed_bytes)
    return original_response