import base64
import uuid
from time import sleep
import aiohttp
from timeit import default_timer as timer
import discord

headers = {
    'Host': 'novel.local',
    'Authorization': 'Bearer',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.63 Safari/537.36',
    'Accept': '*/*',
    'Origin': 'http://novel.local',
    # 'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'close',
}

low_quality = "lowres, text, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry"

async def generate_image(ctx, prompt, negate, orientation, steps, resolution, prompt_obediance, filter_out, seed):
    
    # Process Orientation
    match orientation:
        case "square":
            height_mult = 0
            width_mult = 0
        case "portrait":
            height_mult = 1
            width_mult = 0
        case "landscape":
            height_mult = 0
            width_mult = 1
    
    # Resolution
    match resolution:
        case "normal":
            height = 512 + (256 * height_mult)
            width = 512  + (256 * width_mult) 
        case "high":
            height = 512 + (256 * (height_mult + 1))
            width = 512  + (256 * (width_mult + 1))  
    
    # Scale Level
    match prompt_obediance:
        case "low":
            scale = 6
        case "medium":
            scale = 12
        case "high":
            scale = 20
            
    # Negative Prompt Presets
    match filter_out:    
        case "Bad Anatomy":
            ucPreset = 0
            uc = "bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, " + low_quality 
        case "NSFW":
            ucPreset = 4
            uc = "nsfw, " + low_quality    
        case _:
            ucPreset = 1
            uc = low_quality
    
    if negate:
        uc += ", " + negate
    
    json_data = {
        'prompt': 'masterpiece, best quality,' + prompt,
        'width': width,
        'height': height,
        'scale': scale,
        'sampler': 'k_euler',
        'steps': steps,
        'seed': seed,
        'n_samples': 1,
        'ucPreset': ucPreset,
        'uc': uc
    }
    
    # Start Counting Time
    start = timer()
    
    # Send Request
    async with aiohttp.ClientSession() as session:
        async with session.post('http://192.168.50.11/generate-stream', headers=headers, json=json_data) as response:
            
            raw = await response.text()
            data = raw[raw.find("data")+5:]
                
            # Generate Random Filename
            path = "Images/" + str(uuid.uuid4()) + ".png"
            
            with open(path, "wb") as f:
                f.write(base64.b64decode(data))
            
                
            # Respond With Input Parameters Included
            await ctx.respond(content=f"**Image Generated In**: {round(timer() - start, 2)} Seconds \n**Prompt**: {prompt} \n**Negate**: {negate} \n**Steps**: {steps} \n**Dims**: {width}x{height} \n**Prompt Obediance**: {scale} \n**Seed**: {seed}", file=discord.File(path))
    