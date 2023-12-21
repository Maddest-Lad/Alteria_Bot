import base64
import io
import pathlib
import uuid

from PIL import Image

from Modules.constants import SD_BASE_NEGATIVE_PROMPT, SD_IMAGE_PATH
from Modules.session_handler import SessionHandler

# Constants
API_URL = "http://localhost:5002"
INTERROGATE_ENDPOINT = f"{API_URL}/sdapi/v1/interrogate"
TEXT_TO_IMG_ENDPOINT = f"{API_URL}/sdapi/v1/txt2img"

class StableDiffusion(SessionHandler):
    """Class for generating and analyzing images using stable diffusion"""       
    
    async def interogate_clip(self, image_path: pathlib.Path) -> str:
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

        response_dict = await self._make_post_request(INTERROGATE_ENDPOINT, data=data).json()
        return response_dict['caption']

    async def generate_image(self, prompt: str) -> tuple[str, str]:
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
            "hr_negative_prompt" : SD_BASE_NEGATIVE_PROMPT,
            "hr_prompt" : prompt,
            "hr_scale" : 1.5,
            "hr_second_pass_steps" : 10,
            "hr_upscaler" : "None",
            "n_iter" : 1,
            "negative_prompt" : SD_BASE_NEGATIVE_PROMPT,
            "prompt" : prompt,
            "restore_faces" : False,
            "sampler_name" : "Euler a",
            "steps" : 15,
        }

        response_dict = self._make_post_request(TEXT_TO_IMG_ENDPOINT, data=data).json()
      
        # Load Image From Request
        image = Image.open(io.BytesIO(base64.b64decode(response_dict['images'][0].split(",",1)[0])))
          
        # Save Image and Parameters
        filename = str(uuid.uuid4())
        path = SD_IMAGE_PATH.joinpath(f"{filename}.png")
        image.save(path)
      
        # Respond With Input Parameters Included
        return f"**Prompt**:```{prompt}```", path
