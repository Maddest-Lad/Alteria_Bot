import aiohttp
from Modules.user import User

HOSTNAME = "http://localhost:5000"
CHAT = f"{HOSTNAME}/v1/chat/completions"
INSTRUCT = f"{HOSTNAME}/v1/completions"

HEADERS = {
    "Content-Type": "application/json"
}

# See The Local Swagger Docs @ HOSTNAME/docs#/default/openai_completions_v1_completions_post
SHARED_PARAMS = {
  "max_tokens": 512,
  "presence_penalty": 0,
  "temperature": 0.7,
  "top_p": 0.1,
  "min_p": 0,
  "top_k": 40,
  "repetition_penalty": 1.18,
  "typical_p": 1,
  "tfs": 1,
  "top_a": 0,
  "epsilon_cutoff": 0,
  "eta_cutoff": 0,
  "guidance_scale": 1,
  "penalty_alpha": 0,
  "mirostat_mode": 0,
  "mirostat_tau": 5,
  "mirostat_eta": 0.1,
  "temperature_last": False,
  "do_sample": True,
  "seed": -1,
  "encoder_repetition_penalty": 1,
  "no_repeat_ngram_size": 0,
  "min_length": 0,
  "num_beams": 1,
  "length_penalty": 1,
  "early_stopping": False,
  "auto_max_new_tokens": False,
  "ban_eos_token": False,
  "add_bos_token": True,
  "skip_special_tokens": True,
}

class TextGeneration:

    # Character Chat Mode (Retains History)
    async def character_chat(self, message: str, user: User) -> str:
        user.add_to_history({"role": "user", "content": message}) 

        data = SHARED_PARAMS | { # Join Params With Chat Specific Values
            "mode": "chat",
            "character": "Assistant_Bot",
            "history" : user.get_history() # History[0] Is Our Request
        }

        response = await self._generate(data, endpoint=CHAT)
        print(response)

        # Add Bot Response to History
        #user.add_to_history({"role": "Assistant_Bot", "content": response})

        return "" # response


    async def instruct(self, message: str) -> str:        
        data =  SHARED_PARAMS | { # Join Params With Instruct Request
            "prompt" : message
        }
        response_dict = await self._generate(data, endpoint=INSTRUCT)
        return response_dict['choices'][0]['text']


    async def _generate(self, data: dict, endpoint: str) -> dict:
        try:
            async with aiohttp.ClientSession() as session:
                    async with session.post(url=endpoint, headers=HEADERS, json=data) as response:
                        response_dict = await response.json()
                        return response_dict
        except Exception as e:
            return f"Error : {e}"
