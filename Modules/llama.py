import aiohttp
import os
import json

from datetime import datetime

class llama:
    
    def __init__(self):
        self.queue = []
        self.api_endpoint = "http://127.0.0.1:5001/run/textgen"
        
        
    async def generate(self, query: str, max_tokens: int, min_length):

        formatted_input = f"""
        Below is an instruction that describes a task. Write a response that appropriately completes the request.
        ### Instruction:
        {query}
        ### Response:

        """
        
        # Based on Llama 30b Text
        params = {
            'max_new_tokens': max_tokens,
            'do_sample': True,
            'temperature': 0.55,
            'top_p': 0.5,
            'typical_p': 1,
            'repetition_penalty': 1.2,
            'encoder_repetition_penalty' : 1,
            'top_k': 40,
            'min_length': min_length,
            'no_repeat_ngram_size': 0,
            'num_beams': 1,
            'penalty_alpha': 0,
            'length_penalty': 1,
            'early_stopping': False,
            'seed' : -1,
        }
        
        payload = {
            "data": [
                formatted_input,
                params['max_new_tokens'],
                params['do_sample'],
                params['temperature'],
                params['top_p'],
                params['typical_p'],
                params['repetition_penalty'],
                params['encoder_repetition_penalty'],
                params['top_k'],
                params['min_length'],
                params['no_repeat_ngram_size'],
                params['num_beams'],
                params['penalty_alpha'],
                params['length_penalty'],
                params['early_stopping'],
                params['seed']
            ]
        }
        
        #print(payload, self.api_endpoint)
        
        try:
            # Send Request
            async with aiohttp.ClientSession() as session:
                async with session.post(url=self.api_endpoint, json=payload) as response:
                    res = await response.json()
                    
                    #print(res)
                                 
                    # Respond With Input Parameters Included
                    response_message = str(res['data'][0])
                    
                    log_entry = {"date": datetime.now().isoformat(), "query": query, "response" : response_message.split("### Response:")[-1].strip() }
                    with open("Logs/LLaMa.json", 'a') as log:
                        json.dump(log_entry, log)
                        log.write(os.linesep)
                        
                    # Only Respond     
                    #bot_reply = response_message.split("### Response:")[-1]
                    formatted = ''.join([''.join(["> ", i.strip(), "\n"]) for i in response_message.split("### Response:")[-1].strip().split("\n")])
                    return f"{query}\n{formatted}"
        
        except Exception as e:
            return f"Error : {e}"
        
        
# import aiohttp

# from pprint import pprint

# class kobold:
    
#     def __init__(self):
#         self.queue = []
#         self.api_url = "http://127.0.0.1:5000/api/v1"
        
        
#     async def generate(self, ctx, input: str):
        
#         payload = { 
#             "prompt": input,
#             "temperature": 0.5,
#             "top_p": 0.9    
#         }
        
#         # pprint(payload)
        
#         try:
#             # Send Request
#             async with aiohttp.ClientSession() as session:
#                 async with session.post(url=f'{self.api_url}/generate', json=payload) as response:
#                     json = await response.json()
                    
#                     pprint(json)
                                 
#                     # Respond With Input Parameters Included
#                     await ctx.respond(f"> {input}\n" + json['results'][0]['text'])
    
#         except Exception as e:
#             await ctx.respond(content=f"Error : {e}")
        