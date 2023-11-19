import aiohttp
import base64
import io
import json
import os
import pathlib
import random
import uuid

import discord

from PIL import Image
from timeit import default_timer as timer

class stable_diffusion:
    
    def __init__(self):
        self.queue = []
        self.api_url = "http://localhost:5002"
        self.filter_list = open("Resources/filter.txt").read().split("\n")
        
    
    async def interogate_clip(self, image_path: pathlib.Path):
        # Convert Image to Base64
        # See for why decode() is neccessary https://stackoverflow.com/questions/3715493/encoding-an-image-file-with-base64
        encoded_image = base64.b64encode(open(image_path, 'rb').read()).decode() 

        payload = {
            "image": encoded_image,
            "model": "clip"
        }
        
        # Log Payload
        with open("Logs/stable-diffusion.json", 'a') as log:
            json.dump(payload, log)
            log.write(os.linesep)
        
        try:
            # Send Request
            async with aiohttp.ClientSession() as session:
                async with session.post(url=f'{self.api_url}/sdapi/v1/interrogate', json=payload) as promise:                
                    response = await promise.json()

                    return response['caption']
        
        except Exception as e:
            return f"CLIP Error : {e}"
    
    async def generate(self, ctx, prompt, negative_prompt, orientation, steps, prompt_obediance, sampler, seed=None):
        
        if not seed:
            seed = random.randint(0, 10000000000)
        
        # Oreintation
        match orientation:
            case "square":
                width = 768
                height = 768
            case "portrait":
                width = 768
                height = 1280
            case "landscape":
                width = 1280
                height = 768

        if not negative_prompt:
            negative_prompt = " "
        
        neg = negative_prompt + "child, young, illegal, bad-anime-horror bad_prompt_version2 verybadimagenegative_v1.3 negative_hand-neg"
        
        if len(prompt) > 2000:
            prompt = prompt[:1800]
        
        payload = {
            'prompt': prompt,
            'negative_prompt': neg,
            'width': width,
            'height': height,
            'cfg_scale': prompt_obediance,
            'sampler_name': sampler,
            'steps': steps,
            'seed': seed,
        }
            
        # Log Payload
        with open("Logs/stable-diffusion.json", 'a') as log:
            json.dump(payload, log)
            log.write(os.linesep)
        
        try:
            # Send Request
            async with aiohttp.ClientSession() as session:
                async with session.post(url=f'{self.api_url}/sdapi/v1/txt2img', json=payload) as promise:
                    # Get Reason For Failure if It's Returned By Server                

                    response = await promise.json()
                    
                    # NSFW Spoilering 
                    spoiler = False
                    
                    for i in response['images']:
                       # Load Image From Request
                        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
                        
                        # Save Image and Parameters
                        filename = str(uuid.uuid4())
                        path = "Media/StableDiffusion/" + filename  + ".png"
                        image.save(path)
                        
                        # Save Generation Parameters
                        with open(f"Media/StableDiffusion/{filename}.txt", 'w') as file:
                            file.write(f"{prompt} \n {negative_prompt}")
                        
                        # NSFW Check
                        items = prompt.split(" ")
                        for item in items:
                            if item.lower() in self.filter_list:
                                spoiler = True
                                break
                                
                        # Respond With Input Parameters Included
                        return f"**Prompt**:```{prompt}```**Steps**: {steps} \n**Prompt Obediance**: {prompt_obediance} \n**Seed**: {seed}", discord.File(path, spoiler=spoiler)
        
        except Exception as e:
            await ctx.followup.send(content=f"Error : {e}")
