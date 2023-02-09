import base64
import uuid
import aiohttp
import io
import discord
import random
from PIL import Image
from timeit import default_timer as timer

class SD:
    
    def __init__(self):
        self.queue = []
        self.api_url = "http://192.168.1.11:80"
    
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
    
        payload = {
            'prompt': prompt,
            'width': width,
            'height': height,
            'scale': prompt_obediance,
            'sampler': sampler,
            'steps': steps,
            'seed': seed,
            'n_samples': 1,
            'uc': negative_prompt
        }
        
        try:
            # Send Request
            async with aiohttp.ClientSession() as session:
                async with session.post(url=f'{self.api_url}/sdapi/v1/txt2img', json=payload) as response:
                    # Get Reason For Failure if It's Returned By Server                

                    json = await response.json()
                    for i in json['images']:
                        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
                        path = "Images/" + str(uuid.uuid4()) + ".png"
                        image.save(path)
                                
                        # Respond With Input Parameters Included
                        await ctx.respond(content=f"**Prompt**:```{prompt}```**Negative Prompt**:```{negative_prompt}``` \n**Steps**: {steps} \n**Prompt Obediance**: {prompt_obediance} \n**Seed**: {seed}", file=discord.File(path))
        
        except Exception as e:
            await ctx.respond(content=f"Error : {e}")
        