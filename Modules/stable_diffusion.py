import base64
import uuid
import aiohttp
import io
import random
import os
import discord
from PIL import Image
from timeit import default_timer as timer

class stable_diffusion:
    
    def __init__(self):
        self.queue = []
        self.api_url = "http://127.0.0.1:5002"
        self.filter_list = open("Resources/filter.txt").read().split("\n")
        
    
    async def generate(self, ctx, prompt, negative_prompt, orientation, steps, prompt_obediance, sampler, seed):
        
        if not seed:
            seed = random.randint(0, 10000000000)
        
        # Oreintation
        match orientation:
            case "square":
                width = 512
                height = 512
            case "portrait":
                width = 512
                height = 768
            case "landscape":
                width = 768
                height = 512

        if not negative_prompt:
            negative_prompt = " "
        
        neg = negative_prompt + "child, young, illegal, [bad_prompt_version2]"
        
        if len(prompt) > 2000:
            prompt = prompt[:1800]
        
        payload = {
            'prompt': prompt,
            'negative_prompt': neg,
            'width': width,
            'height': height,
            'scale': prompt_obediance,
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
                async with session.post(url=f'{self.api_url}/sdapi/v1/txt2img', json=payload) as response:
                    # Get Reason For Failure if It's Returned By Server                

                    json = await response.json()
                    
                    # NSFW Spoilering 
                    spoiler = False
                    
                    for i in json['images']:
                       # Load Image From Request
                        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
                        
                        # Save Image and Parameters
                        filename = str(uuid.uuid4())
                        path = "Media/StableDiffusion/" + filename  + ".png"
                        image.save(path)
                        
                        # Save Generation Parameters
                        with open(f"Media/StableDiffusion/{filename}.txt") as file:
                            file.write(prompt, "\n", negative_prompt)
                        
                        # NSFW Check
                        items = prompt.split(" ")
                        for item in items:
                            if item.lower() in self.filter_list:
                                spoiler = True
                                break
                                
                        # Respond With Input Parameters Included
                        await ctx.respond(content=f"**Prompt**:```{prompt}```**Steps**: {steps} \n**Prompt Obediance**: {prompt_obediance} \n**Seed**: {seed}", file=discord.File(path, spoiler=spoiler))
        
        except Exception as e:
            await ctx.respond(content=f"Error : {e}")
