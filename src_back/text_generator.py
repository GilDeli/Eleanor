import requests
import json
import time
def get_ai_text(promt:str,output:dict,server_url="http://localhost:11434/api/generate"):
    output['ai_gen_status'] = True
    data = {
        "model": "bambucha/saiga-llama3:latest",
        "prompt": promt,
        "stream": True,
    }
    with requests.post(server_url, json=data, stream=True) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            line = line.decode('utf-8')
            try:
                json_data  = json.loads(line)
                if json_data.get("done",False):
                    break
                chunk = json_data.get("response","")
                if chunk:
                    output['shared_text'] += chunk
                    #print(chunk, end="", flush=True)
            except json.JSONDecodeError:
                continue
    time.sleep(2)
    output['ai_gen_status'] = False