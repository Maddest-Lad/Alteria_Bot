# System Libraries
from pathlib import Path
import datetime
import random

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
from Modules.utils import log, set_status, convert_to_pacific
from Modules.weather import get_current_report

# Initialize Bot
bot = discord.Bot()

# Initalize Class Objects (Only Neccessary For When Queuing Async Handling)
stable_diffusion = stable_diffusion()
llama = llama()
summarizer = summarizer(llama)
downloader = downloader() 

# Server Scope [Just Me, Paradox Plaza, Shadow Cabinet]
scope = [446862283600166927, 439636881194483723, 844325005209632858]

# Load Known Users
data_dir = Path("Data") 
user_list = [User.from_json(item) for item in data_dir.glob('*.json')]

# Startup
@bot.event
async def on_ready():
    print(f"{bot.user} Has Started Up Successfully")
    await send_weather_report("165971552771244033", "Maple+Valley")

# Video Downloading -- Exclusive to My Personal Server
@bot.slash_command(guilds=[446862283600166927], description="Downloads A Video")
async def download(ctx: ApplicationContext, url: Option(str, "url to download")):
    await ctx.defer()
    await ctx.followup.send(file=discord.File(downloader.download(url)))
    log("Downloading", url)

@bot.slash_command(guilds=scope, description="Uses Stable Diffusion to Generate an Image from Text")
async def generate(ctx: ApplicationContext,
                   prompt: Option(str, "The postive prompt that describes the image to generate", required=True),
                   negative_prompt: Option(str, "the negative prompt", required=False), 
                   orientation: Option(str, "The orientation of the image", required=False, choices=["square", "portrait", "landscape"], default="square"),
                   steps: Option(int, "The number of steps used to generate the image [10, 50]", required=False,  default=20),
                   prompt_obediance: Option(int, "The strictly the AI obeys the prompt [1, 30]", required=False, default=9),
                   sampler: Option(str, "The sampling method used", required=False, choices=["Euler", "DDIM"], default="DDIM"),
                   seed: Option(int, "The seed for image generation, useful for replicating results", required=False)):
    await ctx.defer()
    reply, file = await stable_diffusion.generate(ctx, prompt, negative_prompt, orientation, steps, prompt_obediance, sampler, seed)
    await ctx.followup.send(reply, file=file)

@bot.slash_command(guilds=scope, description="Asks Facebook's LLaMA Model a Question - Works Like ChatGPT")
async def ask_alt(ctx: ApplicationContext, 
                  message: Option(str, "The postive prompt that describes the image to generate", required=True), 
                  max_tokens: Option(int, "A general measure that can be considered an aggregation of complexity and length [200-2000]", min_value=200, default=400, max_value=2000, required=False),
                  min_length: Option(int, "The minimum length for a generation", min_value=0, default=0, max_value=1500)):
    await ctx.defer()
    await ctx.followup.send(await llama.generate(message, max_tokens, min_length))

@bot.slash_command(guilds=scope, description="Uses /Ask_Alt and scraped video captions to summarize the video")
async def summarize_video(ctx: ApplicationContext, url: Option(str, "The url of the video to summarize", required=True)):
    await ctx.defer()
    await ctx.followup.send(await summarizer.summarize(url))

@bot.slash_command(guild=scope, description="Opt in for a daily weather report of your City")
async def daily_weather(ctx: ApplicationContext,
                  city : Option(str, "The Name of the City to Report", required=True),
                  time_zone: Option(str, "Your Time Zone", choices=["Pacific", "Mountain", "Central", "Eastern"], required=True),
                  report_time: Option(int, "what hour would you Like to Recieve The Report 1-24", min_value=1,  max_value=24),
                  stop_reports: Option(bool, "set this to true to cancel weather notifications", required=False),
                  ):
    # Get User Object (Creates New if It Doesn't Exist)
    user = await get_user(ctx, user_list)
    
    if stop_reports:
        user.set_location(None)
    else:
        # Format Correctly
        location = city.strip().replace(" ", "+")
        
        # Schedule Time
        report_time = convert_to_pacific(time_zone, report_time)
        
        # Update User Object
        user.set_location(location)
        user.set_report_time(report_time)
        # Register New Scheduler
        scheduler.add_job(func=send_weather_report, args=[user.id, user.location], trigger='cron', hour=user.report_time)
    
    await ctx.respond(random.choice(sarcastic_responses), ephemeral=True)  
        
# Get User From a Given ApplicationContext
async def get_user(ctx: ApplicationContext, user_list: list) -> User:
    for user in user_list:
        if user.id == str(ctx.user.id):
            return user
    return User(str(ctx.user.id), ctx.user.name)

# Sends Weather Report
async def send_weather_report(user_id: str, location: str):
    user = await bot.fetch_user(user_id)
    report = await get_current_report(location)
    await user.send(report)
    
if __name__ == '__main__':   
    
    # Initialize Logs
    Path("Logs").mkdir(exist_ok=True)
    
    # Initalize the Scheduler
    scheduler = AsyncIOScheduler(daemon=True)

    # Register Jobs
    scheduler.add_job(func=moon_phase, args=[bot], trigger='cron', hour=17) # Turn on @ 5pm PST 
    scheduler.add_job(func=set_status, args=[bot], trigger='cron', hour=5) # Turn off @ 5am PST
    
    # Register Weather Job For Each User
    for user in user_list:
        if user.location and user.report_time:
            scheduler.add_job(func=send_weather_report, args=[user.id, get_current_report(user.location)], trigger='cron', hour=user.report_time)
    
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