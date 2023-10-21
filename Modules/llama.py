import aiohttp
import os
import json

from datetime import datetime

class llama:
    
    def __init__(self):
        self.queue = []
        self.api_endpoint = "http://localhost:5000/api/v1/generate"
        
        
    async def generate(self, query: str, max_tokens: int, min_length, include_query=True):
                
        params = {
            'prompt': query,
            'max_new_tokens': max_tokens,
            'do_sample': True,
            'temperature': 0.72,
            'top_p': 0.1,
            'typical_p': 1,
            'repetition_penalty': 1.18,
            'encoder_repetition_penalty': 1.0,
            'top_k': 40,
            'min_length': min_length,
            'no_repeat_ngram_size': 0,
            'num_beams': 1,
            'penalty_alpha': 0,
            'length_penalty': 1,
            'early_stopping': False,
            'seed': -1,
            'add_bos_token': True,
            'truncation_length': 2048,
            'ban_eos_token': False,
            'skip_special_tokens': True,
            'stopping_strings': [],
        }
        
        try:
            # Send Request
            async with aiohttp.ClientSession() as session:
                async with session.post(url=self.api_endpoint, json=params) as response:
                    res = await response.json()

                    # Respond With Input Parameters Included
                    response_message = str(res['results'][0]['text'])

                    log_entry = {"date": datetime.now().isoformat(), "query": query, "response" : response_message }
                    with open("Logs/LLaMa.json", 'a') as log:
                        json.dump(log_entry, log)
                        log.write(os.linesep)
                        
                    # # Only Respond     
                    formatted = ''.join([''.join(["> ", i.strip(), "\n"]) for i in response_message.strip().split("\n")])
                    if include_query:
                        return f"{query}\n{formatted}"
                    else:
                        return f"{formatted}"
                    
        except Exception as e:
            return f"Error : {e}"
