import base64
import io
from pathlib import Path
import uuid

from PIL import Image

from Modules.constants import MEDIA_DIRECTORY
from Modules.session_handler import SessionHandler

# Constants
API_URL = "http://localhost:5002"
INTERROGATE_ENDPOINT = f"{API_URL}/sdapi/v1/interrogate"
TEXT_TO_IMG_ENDPOINT = f"{API_URL}/sdapi/v1/txt2img"
SD_IMAGE_PATH =  MEDIA_DIRECTORY / "StableDiffusion"
SD_BASE_NEGATIVE_PROMPT = "bad-anime-horror bad_prompt_version2 verybadimagenegative_v1.3 negative_hand-neg <lora:EasyFix:0.5> "
SD_BASE_POSITIVE_PROMPT = "[[anime, anime style, Japanese animation, flat colors]] "

class StableDiffusion(SessionHandler):
    """Class for generating and analyzing images using stable diffusion"""       

    async def interogate_clip(self, image_path: Path) -> str:
        """
        Returns an image description using CLIP 
        https://openai.com/research/clip

        Args:
            image_path (pathlib.Path): Path to image

        Returns:
            str: Image Description
        """
        # https://stackoverflow.com/questions/3715493/encoding-an-image-file-with-base64
        encoded_image = base64.b64encode(open(image_path, 'rb').read()).decode()

        data = {
            "image": encoded_image,
            "model": "clip"
        }

        response_dict = await self._make_post_request(INTERROGATE_ENDPOINT, data=data)
        return response_dict['caption']

    async def generate_image(self, prompt: str) -> Path:
        """
        Generates an image using Stable Diffusion

        Args:
            prompt str: Image Prompt

        Returns:
            str: image generation settings
            str: generated image path  
        """
        prompt = prompt.lower()
        prompt = prompt.replace("`", "")

        if len(prompt) > 2000:
            prompt = prompt[:1800]
      
        data = {
            "cfg_scale" : 6,
            "denoising_strength" : 0.8,
            "disable_extra_networks" : False,
            "enable_hr" : False,
            "height" : 1296,
            "width" : 1024,
            "hr_negative_prompt" : SD_BASE_NEGATIVE_PROMPT + " young, child, illegal",
            "hr_prompt" : SD_BASE_POSITIVE_PROMPT + prompt,
            "hr_scale" : 1.5,
            "hr_second_pass_steps" : 10,
            "hr_upscaler" : "None",
            "n_iter" : 1,
            "negative_prompt" : SD_BASE_NEGATIVE_PROMPT + " young, child, illegal",
            "prompt" : SD_BASE_POSITIVE_PROMPT + prompt,
            "restore_faces" : False,
            "sampler_name" : "Euler a",
            "steps" : 15,
        }

        response_dict = await self._make_post_request(TEXT_TO_IMG_ENDPOINT, data=data)

        image = Image.open(io.BytesIO(base64.b64decode(response_dict['images'][0].split(",",1)[0])))
        filename = str(uuid.uuid4())

        path = SD_IMAGE_PATH / f"{filename}.png"
        image.save(path)
        
        return path
