#!/bin/env python3
import requests
import json
import threading
import time
from collections import deque 
import sys

from src import text_generator
from src import player
from src import text_format


state={
    'shared_text': '',
    'iter': 0,
    'ai_gen_status': False,
    'len_lim': 100,
    'len_max': 200
}

def get_tts(text, server_url="http://localhost:5500"):
    data = {
        "text": text,
        "length_scale":0.8
    }
    response = requests.post(server_url, json=data, stream=True)
    response.raise_for_status()
    audio = player.process_audio(response)
    return audio
    #return response


def stream_tts(input:dict):
    queue_text = deque()
    thread = None
    text_format.split_text (input,queue_text)
    while len(queue_text) != 0 or input['ai_gen_status']:
        time.sleep(1)
        text_format.split_text (input,queue_text)
        if len(queue_text) == 0:
            continue
        txt = queue_text.popleft()
        if len(txt) <= 1 : 
            break
        audio = get_tts(txt)
        if thread is not None: 
            thread.join()
        thread = threading.Thread(
            target=player.play_audio,
            args=(audio,),
            daemon=True 
        )
        thread.start()
        print(txt, end="|", flush=True)

    if thread is not None: thread.join()



with open('./text.txt','r',encoding='utf-8') as f:
    text = f.read()

state['shared_text'] = text

#thread = threading.Thread(
#            target=text_generator.get_ai_text,
#            args=(sys.argv[1],state,),
#            daemon=True 
#        )
print ("--------------------------------------")
#thread.start()
stream_tts(state)
#thread.join()
print ("\n--------------------------------------")

