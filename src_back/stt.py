#!/usr/bin/env python3

import json
import os
import sys
import asyncio
import websockets
import logging
import sounddevice as sd
import argparse

import shutil

def int_or_str(text):
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))

async def run_test():
    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 4000, device=args.device, dtype='int16',
                           channels=1, callback=callback) as device:

        async with websockets.connect(args.uri) as websocket:
            config = {
                "config": {
                    "sample_rate": device.samplerate,
                    "max_alternatives": 0,
                }
            }
            await websocket.send(json.dumps(config))

            while True:
                data = await audio_queue.get()
                await websocket.send(data)
                response = await websocket.recv()
                try:
                    result_json = json.loads(response)
                    print (result_json)
                    partial_text = result_json.get("partial", "")
                    if partial_text:
                        print (f"> {partial_text}",end="\r",flush=True)
                    final_text = result_json.get("text", "")
                    if final_text:
                        print(" " * shutil.get_terminal_size().columns, end="\r", flush=True)
                        print(final_text)
                        #os.system('python3 ./main.py \"'+final_text+'\"')
                        #break
                except json.JSONDecodeError:
                    print(f"Failed to parse JSON: {response}")
                    continue


async def main():

    global args
    global loop
    global audio_queue

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-l', '--list-devices', action='store_true',
                        help='show list of audio devices and exit')
    args, remaining = parser.parse_known_args()
    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    parser = argparse.ArgumentParser(description="ASR Server",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     parents=[parser])
    parser.add_argument('-u', '--uri', type=str, metavar='URL',
                        help='Server URL', default='ws://127.0.0.1:2700')
    parser.add_argument('-d', '--device', type=int_or_str,
                        help='input device (numeric ID or substring)')
    parser.add_argument('-r', '--samplerate', type=int, help='sampling rate', default=16000)
    args = parser.parse_args(remaining)
    loop = asyncio.get_running_loop()
    audio_queue = asyncio.Queue()

    logging.basicConfig(level=logging.INFO)
    await run_test()

if __name__ == '__main__':
    asyncio.run(main())
