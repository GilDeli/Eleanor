from collections import deque 
from razdel import sentenize
import re

def split_text(input:dict,queue_text:deque()):
    if len(queue_text) >= 2:
        return
    text = input['shared_text'][(input['iter']):(input['iter']+((input['len_max']+100)*4))]
    if not text.strip():
        return
    pattern = r'(?:(?<=[,.!?:;—])|(?<=\n)|(?<=и))'
    sentences = re.split(pattern, text)
    split = ""
    for txt in sentences:
        split += txt
        last = ''
        if split:
            last = split[-1]
        if  len(split) >=  input['len_lim'] or last=='.' or last == '!' or last=='?':
            queue_text.append(split)
            input['len_lim'] += (input['len_max'] - input['len_lim']) / 2
            split = ""

    if not input['ai_gen_status']:
        queue_text.append(split)
        split = ""
    input['iter'] += (len(text)-len(split))