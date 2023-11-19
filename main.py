# System Libraries
import asyncio
import datetime
import random
import re
import time

from pathlib import Path
from string import Template

# Installed Libraries
import discord
from discord import Option, ApplicationContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Modules
from Modules.constants import *
from Modules.downloader import downloader
from Modules.moon import moon_phase
from Modules.llama import llama
from Modules.stable_diffusion import stable_diffusion
from Modules.summarizer import summarizer
from Modules.user import User
from Modules.utils import log, set_status, ocr
from Modules.youtube_downloader import download_video
# from Modules.weather import get_current_report

# Initialize Bot
bot = discord.Bot()

# Initalize Module Class Objects
stable_diffusion = stable_diffusion()
llama = llama()
summarizer = summarizer(llama)
downloader = downloader() 

# Server Scope [Just Me, Paradox Plaza, Shadow Cabinet]
scope = [446862283600166927, 439636881194483723, 844325005209632858]
 
# Load Known Users
data_dir = Path("Data") 
user_list = [User.from_json(item) for item in data_dir.glob('*.json')]

# Load Prompts
prompts = []
with open("75000 prompts.txt", 'r') as file:
    prompts = file.read().replace("\"", "").split("\n")

# Load AI Templates
improve_prompt_template = Template(open("Modules/prompt_template.txt").read())

# Startup
@bot.event
async def on_ready():
    print(f"{bot.user} Has Started Up Successfully")

# IF Downloading -- Exclusive to My Personal Server / DMs
@bot.slash_command(guilds=[446862283600166927], description="Downloads A Video")
async def download(ctx: ApplicationContext, url: Option(str, "url to download")):
    await ctx.defer()
    await ctx.followup.send(file=discord.File(downloader.download_if(url)))
    log("Downloading", url)

# Generates an Image Using Stable Diffusion
@bot.slash_command(guilds=scope, description="Uses Stable Diffusion to Generate an Image from Text")
async def generate(ctx: ApplicationContext,
                   prompt: Option(str, "The postive prompt that describes the image to generate", required=True),
                   negative_prompt: Option(str, "the negative prompt", required=False), 
                   orientation: Option(str, "The orientation of the image", required=False, choices=["square", "portrait", "landscape"], default="square"),
                   steps: Option(int, "The number of steps used to generate the image [10, 50]", required=False,  default=35),
                   prompt_obediance: Option(int, "The strictly the AI obeys the prompt [1, 30]", required=False, default=9),
                   sampler: Option(str, "The sampling method used", required=False, choices=["DPM++ 2M Karras", "DDIM"], default="DPM++ 2M Karras"),
                   seed: Option(int, "The seed for image generation, useful for replicating results", required=False),
                   improve_prompt: Option(bool, "Whether to improve the prompt using a language model", required=False,  default=False)
                   ):
    await ctx.defer()

    if improve_prompt: 
        prompt = await llama.generate(query=improve_prompt_template.substitute({'Prompt' : prompt}), raw_response=True)

    reply, file = await stable_diffusion.generate(ctx, prompt, negative_prompt, orientation, steps, prompt_obediance, sampler, seed)
    await ctx.followup.send(reply, file=file)

# Generates a Random Image with Stable Diffusion
@bot.slash_command(guilds=scope, description="Generates a random image")
async def random_image(ctx: ApplicationContext,
                       images_to_generate: Option(int, "The number of images to generate", required=False,  default=1),
                       randomize_checkpoints: Option(bool, "Whether to use a random SDXL model or not", required=False,  default=False),
                       improve_prompt: Option(bool, "Whether to improve the prompt with a language model", required=False,  default=False)):
    
    await ctx.defer()
    
    orientations = ["square", "portrait", "landscape"]
    for _ in range(0, images_to_generate):
        
        # Choose Prompt
        image_prompt = random.choice(prompts)

        # Improve Prompt
        if improve_prompt: 
            image_prompt = await llama.generate(query=improve_prompt_template.substitute({'Prompt' : image_prompt}), raw_response=True)

        reply, file = await stable_diffusion.generate(ctx, 
                                                      prompt=image_prompt, 
                                                      negative_prompt="", 
                                                      orientation=random.choice(orientations),
                                                      steps=35,
                                                      prompt_obediance=9, 
                                                      sampler="DPM++ 2M Karras")
        await ctx.followup.send(reply, file=file)
    if images_to_generate > 1:
        await ctx.followup.send("All Images Generated")

# Generates a Response Using Locally Hosted Large Langauge Model  
@bot.slash_command(guilds=scope, description="Asks Facebook's LLaMA Model a Question - Works Like ChatGPT")
async def ask_alt(ctx: ApplicationContext, 
                  message: Option(str, "The postive prompt that describes the image to generate", required=True), 
                  max_tokens: Option(int, "A general measure that can be considered an aggregation of complexity and length [200-2000]", min_value=200, default=400, max_value=2000, required=False),
                  min_length: Option(int, "The minimum length for a generation", min_value=0, default=0, max_value=1500)):
    await ctx.defer()
    await ctx.followup.send(await llama.generate(message, max_tokens, min_length))

# Download a Youtube Video and Import it Into Plex  
@bot.slash_command(guilds=[446862283600166927], description="Download a Youtube Video and Import it Into Plex")
async def youtube_to_plex(ctx: ApplicationContext, 
                  url: Option(str, "The URL of the Youtube Video", required=True)):
    await ctx.defer()
    await ctx.followup.send(await download_video(url, media_library_path=Path("/mnt/md0/Plex/Youtube")))

# Uses OCR to Detect Text and Reverse Stable Diffusion to Generate a Description Based on the Current Image Model Loaded
@bot.slash_command(guilds=scope, description="Uses CLIP and OCR to summarize and image")
async def process_image(ctx: ApplicationContext, url: Option(str, "The url of the image to process", required=True)):
    await ctx.defer()
    # Check URL
    if not any(filetype in url for filetype in ["png", "jpg", "webm", "jpeg"]): # Hacky
        await ctx.followup.send("Image must be a PNG, JPG/JPEG or WEBM")
    else:
        try:
            image_path = downloader.download_image(url)
            # Parse OCR Text and CLIP Description from Image
            ocr_text = ocr(image_path)
            clip_description = await stable_diffusion.interogate_clip(image_path)

            await ctx.followup.send(f"""Optical Character Recognition (OCR):\n```{ocr_text}```CLIP:\n```{clip_description}```""", file=discord.File(image_path))
        except Exception as e:
            await ctx.followup.send(str(e))
        
# Get User From a Given ApplicationContext
async def get_user(ctx: ApplicationContext, user_list: list) -> User:
    for user in user_list:
        if user.id == str(ctx.user.id):
            return user
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
    
    if datetime.datetime.now().hour < 17:
        scheduler.add_job(func=set_status, args=[bot], trigger='date', run_date=run_time)
    else:
        scheduler.add_job(func=moon_phase, args=[bot], trigger='date', run_date=run_time)
    
    # Start Scheduler
    scheduler.start()

    # Start Bot
    bot.run(open("token.secret", "r").read())
