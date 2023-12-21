import aiohttp
from Modules.user import User
from Modules.session_handler import SessionHandler

# Constants
API_URL = "http://localhost:5000"
CHAT_ENDPOINT = f"{API_URL}/v1/chat/completions"
INSTRUCT_ENDPOINT = f"{API_URL}/v1/completions"
HEADERS = {"Content-Type": "application/json"}
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

class TextGenerator(SessionHandler):
    """Class for generating text using a local Large Language Model (LLM)"""

    async def generate_chat_response(self, message: str, user: User) -> str:
        """
        Sends a message to the LLM and returns it's response 

        Args:
            message (str): The user query
            user (User): The user object to retrieve history from

        Returns:
            str: The LLM response
        """
        user.add_to_history({"role": "user", "content": message})
        data = {
            **SHARED_PARAMS,
            "mode": "chat",
            "character": "Assistant_Bot",
            "messages" : user.get_history()
        }

        response_dict = await self._make_post_request(CHAT_ENDPOINT, data=data).json()
        response = response_dict['choices'][0]['message']['content']
        user.add_to_history({"role": "Assistant_Bot", "content": response})

        return response

    async def generate_instruct_response(self, message: str) -> str:
        """
        Sends a message to the LLM and returns it's response 

        Args:
            message (str): The user query

        Returns:
            str: The LLM response
        """
        data = {**SHARED_PARAMS, "prompt" : message}
        response_dict = await self._make_post_request(INSTRUCT_ENDPOINT, data=data).json()
        return response_dict['choices'][0]['text']

