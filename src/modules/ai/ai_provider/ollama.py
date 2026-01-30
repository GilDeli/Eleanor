import aiohttp
import asyncio
import json
from typing import Dict, Any, AsyncGenerator, Optional

from .base import AIProvider

class OllamaProvider(AIProvider):
    def __init__ (
        self,
        config:dict = None
    ):
        config = config or {}
        self.url = config.get('url') or "http://localhost:11434/api/generate"
        self.model = config.get('model') or "bambucha/saiga-llama3:latest"
        self.params = {k: v for k,v in config.items() if k not in ('url','model')}

    async def generate(
        self,
        prompt: str,
        **extra_params
    ):
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            **self.params,
            **extra_params
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=data) as response:
                response.raise_for_status()
                async for line in response.content:
                    if line:
                        line=line.decode('utf-8')
                        try:
                            json_data = json.loads(line)
                            if json_data.get("done",False):
                                break
                            chunk = json_data.get("response","")
                            if chunk:
                                yield chunk
                        except json.JSONDecodeError:
                            continue
    
    async def close(self):
        pass