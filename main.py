import asyncio
import datetime
import json
from pathlib import Path
import time
import random

import aiofiles

# Main Library https://github.com/Pycord-Development/pycord
import discord
from discord import Option, ApplicationContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Modules
from Modules.constants import *
from Modules.downloader import Downloader
from Modules.moon import moon_phase
from Modules.text_generation import TextGenerator
from Modules.stable_diffusion import StableDiffusion
from Modules.summarizer_youtube_video import summarize
from Modules.user import User
from Modules.utils import set_status, ocr
from Modules.youtube_downloader import download_video

# Initialize Bot
bot = discord.Bot()

# Initalize aiohttp sesison classes
text_generator = TextGenerator()
stable_diffusion = StableDiffusion()
downloader = Downloader() 


@bot.event
async def on_ready():
    """Pycord Startup Callback"""
    print(f"{bot.user} Has Started Up Successfully")

@bot.slash_command(guilds=[446862283600166927], description="Downloads A Video")
async def download(ctx: ApplicationContext, url: Option(str, "url to download")):
    """Slash Command to Download a Video"""
    await ctx.defer()
    await ctx.followup.send(file=discord.File(downloader.download_if(url)))

@bot.slash_command(guilds=SCOPE, description="Generates an image with Stable Diffusion")
async def generate(ctx: ApplicationContext,
                   prompt: Option(str, "The prompt for the image, if left empty it will be automatically generated", required=False, default=None),
                   auto_improve_prompt: Option(bool, "Whether to improve the prompt with a language model", required=False,  default=False),
                   images_to_generate: Option(int, "The number of images to generate", required=False,  default=1),
                   noun: Option(str, "Base Guidance", required=False, default=None)):
    """Generates an Image with Stable Diffusion"""
    await ctx.defer()
    
    flag = not noun

    # Generation Loop
    for _ in range(0, images_to_generate):
        if flag:
            noun = random.choice(NOUNS)

        if prompt:
            image_prompt = prompt
        else:
            async with text_generator: 
                image_prompt = await text_generator.generate_instruct_response(message=NEW_PROMPT_TEMPLATE.substitute({'Noun' : noun }))
           
        if auto_improve_prompt:
            async with text_generator: 
                image_prompt = await text_generator.generate_instruct_response(message=IMPROVE_PROMPT_TEMPLATE.substitute({'Prompt' : image_prompt}))

        image_prompt = image_prompt.replace("!", "").replace("|", ",").replace("_", " ")

        async with stable_diffusion:
            reply, file = await stable_diffusion.generate_image(prompt=image_prompt)

        # Include Source Noun When Relevant
        if not prompt:
            reply = f"**Noun:** {noun}\n" + reply
        
        # Send Image
        await ctx.followup.send(reply, file=file)

    if images_to_generate > 1:
        await ctx.followup.send("All Images Generated")

@bot.slash_command(guilds=SCOPE, description="Generates a response to your message using a local language model (Just Like ChatGPT)")
async def ask_alt(ctx: ApplicationContext, message: Option(str, "The message to send", required=True)):
    """Generates a Response Using Locally Hosted Large Langauge Model"""
    await ctx.defer()
    async with text_generator:
        response = await text_generator.generate_instruct_response(message=message)
    
    await ctx.followup.send(f"{message}```{response}```")
  
@bot.slash_command(guilds=[446862283600166927], description="Chat with an local language model's persona")
async def chat(ctx: ApplicationContext, message: Option(str, "The message to send", required=True)):
    """Generates a Response In a Contextualized Chat """
    await ctx.defer()
    user = await get_user_object(ctx)

    async with text_generator:
        response = await text_generator.generate_chat_response(message=message, user=user)

    await ctx.followup.send(f"{message}```{response}```")

@bot.slash_command(guilds=SCOPE, description="Uses CLIP and OCR to summarize and image")
async def process_image(ctx: ApplicationContext, url: Option(str, "The url of the image to process", required=True)):
    """Generates desciptions of an image using OCR and CLIP"""
    await ctx.defer()
    # Check URL
    if not any(filetype in url for filetype in ["png", "jpg", "webm", "jpeg"]): # Hacky
        await ctx.followup.send("Image must be a PNG, JPG/JPEG or WEBM")
    else:
        try:
            image_path = downloader.download_image(url)
            # Parse OCR Text and CLIP Description from Image
            ocr_text = await ocr(image_path)

            async with stable_diffusion:
                clip_description = await stable_diffusion.interogate_clip(image_path)
            
            await ctx.followup.send(f"""Optical Character Recognition (OCR):\n```{ocr_text}```CLIP:\n```{clip_description}```""", file=discord.File(image_path))
        except Exception as e:
            await ctx.followup.send(str(e))

@bot.slash_command(guilds=[446862283600166927], description="Download a Youtube Video and Import it Into Plex")
async def youtube_to_plex(ctx: ApplicationContext, url: Option(str, "The URL of the Youtube Video", required=True)):
    """Download a Youtube Video and Import it Into Plex"""
    await ctx.defer()
    await ctx.followup.send(await download_video(url, media_library_path=Path("/mnt/md0/Plex/Youtube")))

# Summarizes a Youtube Video - Disabled Due to LLM Limitations 
@bot.slash_command(guilds=SCOPE, description="Uses /Ask_Alt and scraped video captions to summarize the video")
async def summarize_video(ctx: ApplicationContext, url: Option(str, "The url of the video to summarize", required=True)):
    await ctx.defer()

    async with text_generator:
        summary: list = await summarize(text_generator, url)

        for chunk in summary:
            await ctx.followup.send(chunk)
            time.sleep(0.25)
        
async def get_user_object(ctx: ApplicationContext) -> User:
    """Get User From a Given ApplicationContext"""
    user_file_path = DATA_DIRECTORY / f"{ctx.user.id}.json"

    if user_file_path.exists():
        async with aiofiles.open(user_file_path, mode='r', encoding='utf-8') as user_file:
            user_data = json.loads(await user_file.read())
            return User(user_data['id'], user_data['username'], user_data['history'])    
    
    return User(str(ctx.user.id), ctx.user.name)
 
if __name__ == '__main__':

    # Initialize Logs
    Path("Logs").mkdir(exist_ok=True)

    # Initalize the Scheduler
    scheduler = AsyncIOScheduler(daemon=True)

    # Register Jobs
    scheduler.add_job(func=moon_phase, args=[bot], trigger='cron', hour=17) # Turn on @ 5pm PST 
    scheduler.add_job(func=set_status, args=[bot], trigger='cron', hour=5) # Turn off @ 5am PST

    # Using the Scheduler, Queue Setting Bot Status For 15 Seconds After the Bot Starts
    run_time = datetime.datetime.now() + datetime.timedelta(seconds=15)

    # Set Normal Status During The Day and Moon Phase During The Night
    if datetime.datetime.now().hour < 17:
        scheduler.add_job(func=set_status, args=[bot], trigger='date', run_date=run_time)
    else:
        scheduler.add_job(func=moon_phase, args=[bot], trigger='date', run_date=run_time)

    # Start Scheduler
    scheduler.start()

    # Start Bot
    bot.start(open("token.secret", "r").read())

