import discord
from pathlib import Path
import datetime
from discord import Option
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from Modules.stable_diffusion import stable_diffusion
from Modules.llama import llama
from Modules.downloader import downloader
from Modules.utils import log, clear_status, set_status
from Modules.moon import moon_phase
from Modules.summarizer import summarizer
from Modules.constants import *

# Initialize Bot
bot = discord.Bot()

# Initalize Class Objects
sd_generator = stable_diffusion()
llama = llama()
summarizer = summarizer(llama)
downloader = downloader() 

# Server Scope [Just Me, Paradox Plaza, Shadow Cabinet]
scope = [446862283600166927, 439636881194483723, 844325005209632858]
authorized_users = [165971552771244033, 256847158349660160]

# Startup
@bot.event
async def on_ready():
    print(f"{bot.user} Has Started Up Successfully")

# Ifunny Downloading -- Exclusive to My Personal Server
@bot.slash_command(guilds=[446862283600166927], description="Downloads A Video")
async def download(ctx, url: Option(str, "url to download")):
    await ctx.defer()
    await ctx.followup.send(file=discord.File(downloader.download(url)))
    log("Downloading", url)

@bot.slash_command(guilds=scope, description="Uses Stable Diffusion to Generate an Image from Text")
async def generate(ctx,
                   prompt: Option(str, "The postive prompt that describes the image to generate", required=True),
                   negative_prompt: Option(str, "the negative prompt", required=False), 
                   orientation: Option(str, "The orientation of the image", required=False, choices=["square", "portrait", "landscape"], default="square"),
                   steps: Option(int, "The number of steps used to generate the image [10, 50]", required=False,  default=20),
                   prompt_obediance: Option(int, "The strictly the AI obeys the prompt [1, 30]", required=False, default=9),
                   sampler: Option(str, "The sampling method used", required=False, choices=["Euler", "DDIM"], default="DDIM"),
                   seed: Option(int, "The seed for image generation, useful for replicating results", required=False)):
    await ctx.defer()
    reply, file = await sd_generator.generate(ctx, prompt, negative_prompt, orientation, steps, prompt_obediance, sampler, seed)
    await ctx.followup.send(reply, file=file)
    
@bot.slash_command(guilds=scope, description="Provides a List of Present Textual Inversion and LoRAs Usable for Stable Diffusion")
async def generate_help(ctx, info_category: Option(str, "", required=True, choices=["Textual Inversion", "LoRA"])):
    match info_category:
        case "Textual Inversion":
            await ctx.respond(help_inversion)
        case "LoRA":
            await ctx.respond(help_lora)

@bot.slash_command(guilds=scope, description="Asks Facebook's LLaMA Model a Question - Works Like ChatGPT")
async def ask_alt(ctx, 
                  message: Option(str, "The postive prompt that describes the image to generate", required=True), 
                  max_tokens: Option(int, "A general measure that can be considered an aggregation of complexity and length [200-2000]", min_value=200, default=400, max_value=2000, required=False),
                  min_length: Option(int, "The minimum length for a generation", min_value=0, default=0, max_value=1500)):
    await ctx.defer()
    await ctx.followup.send(await llama.generate(message, max_tokens, min_length))

@bot.slash_command(guilds=scope, description="Uses /Ask_Alt and scraped video captions to summarize the video")
async def summarize_video(ctx, url: Option(str, "The url of the video to summarize", required=True)):
    await ctx.defer()
    await ctx.followup.send(await summarizer.summarize(url))

if __name__ == '__main__':

    # Initialize Logs
    Path("Logs").mkdir(exist_ok=True)
    
    # Initalize the Scheduler
    scheduler = AsyncIOScheduler(daemon=True)

    # Register Jobs
    scheduler.add_job(func=moon_phase, args=[bot], trigger='cron', hour=17) # Turn on @ 5pm PST 
    scheduler.add_job(func=set_status, args=[bot], trigger='cron', hour=5) # Turn off @ 5am PST
    
    # Using the Scheduler, Queue Up Status Setting Jobs 15 Seconds After the Bot Starts
    run_time = datetime.datetime.now() + datetime.timedelta(seconds=15)
    if datetime.datetime.now().hour < 17:
        scheduler.add_job(func=set_status, args=[bot], trigger='date', run_date=run_time)
    else:
        scheduler.add_job(func=moon_phase, args=[bot], trigger='date', run_date=run_time)
    
    # Start Scheduler
    scheduler.start()

    # Start Bot
    bot.run(open("token.secret", "r").read())