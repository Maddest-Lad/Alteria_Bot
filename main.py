import datetime
import json
from pathlib import Path
from time import sleep
import aiofiles

# Main Library https://github.com/Pycord-Development/pycord
import discord
from discord import Option, ApplicationContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Modules
from Modules.constants import *
from Modules.text_generation import TextGenerator
from Modules.stable_diffusion import StableDiffusion
from Modules.download_manager import DownloadManager
from Modules.user import User
from Modules.utils import optical_character_recognition, generate_random_prompt, generate_prompt_markov, convert_to_emoji
from Modules.discord_utils import set_bot_status, set_moon_phase_status
from Modules.minecraft import MinecraftServerManager

# Initialize Bot
bot = discord.Bot()

# Initalize aiohttp sesison handlers
text_generator = TextGenerator()
stable_diffusion = StableDiffusion()
download_manager = DownloadManager()

@bot.event
async def on_ready():
    """Pycord Startup Callback"""
    print(f"{bot.user} Has Started Up Successfully")

@bot.slash_command(guilds=SCOPE, description="Downloads A Video")
async def download(ctx: ApplicationContext, url: Option(str, "url to download")):
    """Slash Command to Download a Video"""
    await ctx.defer()
    video_path = await download_manager.download_video(url)
    await reply(ctx, file=discord.File(video_path))

@bot.slash_command(guilds=SCOPE, description="Generates an Image with Stable Diffusion")
async def generate(ctx: ApplicationContext,
                   prompt: Option(str, "The prompt for the image, if left empty it will be automatically generated", required=True, default=None),
                   auto_improve_prompt: Option(bool, "Whether to improve the prompt with a language model", required=False,  default=False),
                   images_to_generate: Option(int, "The number of images to generate", required=False,  default=1)):
    """Generates an Semi Random Image with Stable Diffusion"""
    await ctx.defer()

    # Generation Loop
    for _ in range(0, images_to_generate):

        if auto_improve_prompt:
            image_prompt = await text_generator.generate_instruct_response(message=PROMPT_TEMPLATE_V2.substitute({'Prompt' : prompt}))
        else:
            image_prompt = prompt

        file = await stable_diffusion.generate_image(prompt=image_prompt)

        if auto_improve_prompt:
            response = f"**Base Prompt**:```{prompt}```**Final Prompt**:```{image_prompt}```"
        else:
            response = f"**Prompt**:```{image_prompt}```"

        await reply(ctx, response, file=discord.File(file))

    if images_to_generate > 1:
        await reply(ctx, "All Images Generated")

@bot.slash_command(guilds=SCOPE, description="Generates a Random Image with Stable Diffusion")
async def generate_random_images(ctx: ApplicationContext,
                   images_to_generate: Option(int, "The number of images to generate", required=False,  default=1),
                   auto_improve_prompt: Option(bool, "Whether to improve the prompt with a language model", required=False,  default=False),
                   use_markov : Option(bool, "Whether to use a markov model while generating the promt", required=False,  default=False),
                   use_emoji : Option(bool, "Whether to use a emoji converter while generating the promt", required=False,  default=False),
                   show_prompt : Option(bool, "Whether to output the promt", required=False,  default=False)
                   ):
    """Generates an Semi Random Image with Stable Diffusion"""
    await ctx.defer()

    # Generation Loop
    for _ in range(0, images_to_generate):

        random_prompt = None
        while not random_prompt:
            random_prompt = generate_prompt_markov() if use_markov else generate_random_prompt() 

        if auto_improve_prompt:
            image_prompt = await text_generator.generate_instruct_response(message=PROMPT_TEMPLATE_V2.substitute({'Prompt' : random_prompt}))
        else:
            image_prompt = random_prompt

        if use_emoji:
            image_prompt = convert_to_emoji(image_prompt)

        file = await stable_diffusion.generate_image(prompt=image_prompt)

        if show_prompt:
            response = f"**Semi-Random Base Prompt**:```{random_prompt}```**Final Prompt**:```{image_prompt}```"
            await reply(ctx, response, file=discord.File(file))
        else:
            await reply(ctx, response=None, file=discord.File(file))

    if images_to_generate > 1:
        await reply(ctx, "All Images Generated")

@bot.slash_command(guilds=SCOPE, description="Generates a response to your message using a local language model (Just Like ChatGPT)")
async def ask_alt(ctx: ApplicationContext, message: Option(str, "The message to send", required=True)):
    """Generates a Response Using Locally Hosted Large Langauge Model"""
    await ctx.defer()
    response = await text_generator.generate_instruct_response(message=message)
 
    await reply(ctx, f"{message}```{response}```")

@bot.slash_command(guilds=[446862283600166927], description="Chat with an local language model's persona")
async def chat(ctx: ApplicationContext, message: Option(str, "The message to send", required=True)):
    """Generates a Response In a Contextualized Chat """
    await ctx.defer()
    user = await get_user_object(ctx)
    response = await text_generator.generate_chat_response(message=message, user=user)

    await reply(ctx, f"{message}```{response}```")

@bot.slash_command(guilds=SCOPE, description="Uses CLIP and OCR to summarize and image")
async def process_image(ctx: ApplicationContext, url: Option(str, "The url of the image to process", required=True)):
    """Generates desciptions of an image using OCR and CLIP"""
    await ctx.defer()
    image_path = await download_manager.download_image(url)

    ocr_text = await optical_character_recognition(image_path)
    clip_description = await stable_diffusion.interogate_clip(image_path)

    await reply(ctx, f"""Optical Character Recognition:\n```{ocr_text}```CLIP:\n```{clip_description}```""",
                             file=discord.File(image_path))


# @bot.slash_command(guilds=SCOPE, description="Starts the Minecraft server")
# async def start_server(ctx: ApplicationContext):
#     await ctx.defer()
#     manager = MinecraftServerManager.get_instance()
#     response = manager.start_server()
#     await ctx.respond(response)

# @bot.slash_command(guilds=SCOPE, description="Stops the Minecraft server")
# async def stop_server(ctx: ApplicationContext):
#     await ctx.defer()
#     manager = MinecraftServerManager.get_instance()
#     response = manager.stop_server()
#     await ctx.respond(response)

# @bot.slash_command(guilds=SCOPE, description="Restarts the Minecraft server")
# async def restart_server(ctx: ApplicationContext):
#     await ctx.defer()
#     manager = MinecraftServerManager.get_instance()
#     response = manager.restart_server()
#     await ctx.respond(response)

@bot.event
async def on_ready():
    """Pycord Startup Callback"""
    print(f"{bot.user} Has Started Up Successfully")
    

### Utils
async def get_user_object(ctx: ApplicationContext) -> User:
    """Get User From a Given ApplicationContext"""
    user_file_path = DATA_DIRECTORY / f"{ctx.user.id}.json"

    if user_file_path.exists():
        async with aiofiles.open(user_file_path, mode='r', encoding='utf-8') as user_file:
            user_data = json.loads(await user_file.read())
            return User(user_data['id'], user_data['username'], user_data['history'])    

    return User(str(ctx.user.id), ctx.user.name)
 
async def reply(ctx: ApplicationContext, response: str, file=None):
    """Reply to a Given Context, Chunking Messages to 2000 Characters"""
    if file:
        await ctx.followup.send(file=file)
    
    if response:
        for chunk in [response[i:i + 2000] for i in range(0, len(response), 2000)]:
            await ctx.followup.send(chunk)
            sleep(0.25) # Avoid Rate Limiting / Spam


if __name__ == '__main__':

    # Initialize Logs
    Path("Logs").mkdir(exist_ok=True)

    # Initialize Scheduler
    scheduler = AsyncIOScheduler(daemon=True)

    # Register Jobs -  swapping between moon phase and status messages every 12 hours (5pm/5am PST) 
    scheduler.add_job(func=set_moon_phase_status, args=[bot], trigger='cron', hour=17)
    scheduler.add_job(func=set_bot_status, args=[bot], trigger='cron', hour=5)

    # Using the Scheduler, Queue Setting Bot Status For 15 Seconds After the Bot Starts
    run_time = datetime.datetime.now() + datetime.timedelta(seconds=15)

    # Set Normal Status During The Day and Moon Phase During The Night
    if datetime.datetime.now().hour < 17:
        scheduler.add_job(func=set_bot_status, args=[bot], trigger='date', run_date=run_time)
    else:
        scheduler.add_job(func=set_moon_phase_status, args=[bot], trigger='date', run_date=run_time)

    # Start Scheduler
    scheduler.start()

    # Start Bot (Blocking)
    bot.run(open("token.secret", "r").read())

