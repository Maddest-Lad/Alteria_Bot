import base64
import uuid
from time import sleep
import aiohttp
from timeit import default_timer as timer
import discord

headers = {
    'Host': '192.168.1.11',
    # 'Content-Length': '332',
    'Authorization': 'Bearer',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.63 Safari/537.36',
    # Already added when you pass json=
    # 'Content-Type': 'application/json',
    'Accept': '*/*',
    'Origin': 'http://192.168.1.11',
    # 'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'close',
}

low_quality = "lowres, text, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry"

async def generate_image(ctx, prompt, negate, orientation, steps, resolution, prompt_obediance, filter_out, seed):
    

    # Resolution & Orientation
    match resolution:
        case "normal":
            if orientation == "portrait":
                height = 768
                width = 512
            elif orientation == "landscape":
                height = 512
                width = 768    
            else:
                height = 512
                width = 512  
                
        case "high":
            if orientation == "portrait":
                height = 1024
                width = 512
            elif orientation == "landscape":
                height = 512
                width = 1024    
            else:
                height = 768
                width = 768
    
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
    
    # Fucking Steps
    if steps < 1:
        steps = 1
    elif steps > 50:
        steps = 50
    
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
    
    try:
        # Send Request
        async with aiohttp.ClientSession() as session:
            async with session.post('http://192.168.1.11:80/generate-stream', headers=headers, json=json_data) as response:
                
                # Get Reason For Failure if It's Returned By Server                
                try:
                    raw = await response.text()
                    data = raw[raw.find("data")+5:]
                    
                    # Generate Random Filename
                    path = "Images/" + str(uuid.uuid4()) + ".png"
                    
                    with open(path, "wb") as f:
                        f.write(base64.b64decode(data))
                                   
                    
                    # Respond With Input Parameters Included
                    await ctx.respond(content=f"**Image Generated In**: {round(timer() - start, 2)} Seconds \n**Prompt**: {prompt} \n**Negate**: {negate} \n**Steps**: {steps} \n**Dims**: {width}x{height} \n**Prompt Obediance**: {scale} \n**Seed**: {seed}", file=discord.File(path))
                
                except base64.binascii.Error:
                    await ctx.respond(content=f"Error : {e}")
                    return 
    
    except Exception as e:
        await ctx.respond(content=f"Error : {e}")

# @bot.slash_command(guild_ids=scope, description="Generate an Image from a Prompt using NovelAI")
# async def novelai(ctx,
#                  prompt: Option(str, "The prompt for the AI to generate an image from", required=True),
#                  negate: Option(str, "A prompt for the AI to negate in the output", required=False, default=""), 
#                  orientation: Option(str, "The orientation of the image", required=False, choices=["square", "portrait", "landscape"], default="square"),
#                  steps: Option(int, "The number of steps used to generate the image [1, 50]", required=False,  default=20),
#                  resolution: Option(str, "The size of the longest dimension", required=False, choices=["normal", "high"], default="normal"),
#                  prompt_obediance: Option(str, "The strictly the AI obeys the prompt [6, 12, 20]", required=False, choices=["low", "medium", "high"], default="medium"),
#                  filter_out: Option(str, "Premade Categories to Negate", required=False, choices=["Bad Anatomy", "NSFW"]),
#                  seed: Option(int, "The seed for image generation, useful for replicating results", required=False)
#                  ):

#        # Preseed
#        if not seed:
#            seed = random.randint(0, 999999999)

#        # Let User Know We're Working On It
#        await ctx.respond("Command Received", ephemeral=False)
#        await generate_image(ctx, prompt, negate, orientation, steps, resolution, prompt_obediance, filter_out, seed)
