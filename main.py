import asyncio

from src.modules.ai import AssistantCore
from src.modules.output import OutAudio
from src.modules.input import InputAudio
from src.modules.stt import SttManager
from src.modules.tts import TtsManager

from src.modules.transform.txt import BufferSentences
from src.modules.transform.audio import FixSynthetic

from src.core.pipeline import PipelineLinear


async def main():
    ls = list() 
    ls.append( InputAudio() )
    ls.append( SttManager() )
    ls.append( AssistantCore() )
    ls.append( BufferSentences() )
    ls.append( TtsManager() )
    ls.append( FixSynthetic() )
    ls.append( OutAudio() )

    pipeline = PipelineLinear(ls)

    while True:
        await pipeline.start()
        await pipeline.await_end()
    

asyncio.run(main())