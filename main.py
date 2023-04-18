import random
import discord
from pathlib import Path
from discord import Option
from Modules.stable_diffusion import stable_diffusion
import Modules.downloader as downloader
from Modules.caption import caption_this
from Modules.llama import llama
from Modules.utils import *

# Initialize Classes
bot = discord.Bot()
sd_generator = stable_diffusion()
llama = llama()

# Server Scope [Just Me, Paradox Plaza, Shadow Cabinet]
scope = [446862283600166927, 439636881194483723, 844325005209632858]

# Startup
@bot.event
async def on_ready():
    print(f"{bot.user} Has Started Up Successfully")

# Ifunny Downloading -- Exclusive to My Personal Server
@bot.slash_command(guilds=[446862283600166927])
async def download(ctx, url: Option(str, "url to download")):
    await ctx.respond("Downloading")
    await ctx.send(file=discord.File(downloader.get(url)))
    
# Image and Gif Captioner
@bot.slash_command(guilds=scope)
async def caption(ctx, image_url: Option(str, "url to image"),
                    text: Option(str, "top text"),
                    text_position: Option(str, "text position", choices=["top", "bottom"], default="top"),
                    font_size: Option(int, "font size", default=54)):
    await ctx.respond("Adding Text")
    await ctx.send(file=discord.File(caption_this(image_url, text, text_position, font_size)))    

@bot.slash_command(guilds=scope)
async def generate(ctx,
                   prompt: Option(str, "The postive prompt that describes the image to generate", required=True),
                   negative_prompt: Option(str, "the negative prompt", required=False), 
                   orientation: Option(str, "The orientation of the image", required=False, choices=["square", "portrait", "landscape"], default="square"),
                   steps: Option(int, "The number of steps used to generate the image [10, 50]", required=False,  default=20),
                   prompt_obediance: Option(int, "The strictly the AI obeys the prompt [1, 30]", required=False, default=9),
                   sampler: Option(str, "The sampling method used", required=False, choices=["Euler", "DDIM"], default="DDIM"),
                   seed: Option(int, "The seed for image generation, useful for replicating results", required=False)):
    
    await ctx.respond(random.choice(sarcastic_responses))
    await sd_generator.generate(ctx, prompt, negative_prompt, orientation, steps, prompt_obediance, sampler, seed)
    
@bot.slash_command(guilds=scope)
async def generate_help(ctx, info_category: Option(str, "", required=True, choices=["Textual Inversion", "LoRA"])):
    match info_category:
        case "Textual Inversion":
            await ctx.respond(help_inversion)
        case "LoRA":
            await ctx.respond(help_lora)

@bot.slash_command(guilds=scope)
async def ask_alt(ctx, 
                  message: Option(str, "The postive prompt that describes the image to generate", required=True), 
                  max_tokens: Option(int, "A general measure that can be considered an aggregation of complexity and length [200-2000]", min_value=200, default=400, max_value=2000, required=False)):
    
    await ctx.respond(random.choice(sarcastic_responses))
    try:
        await ctx.respond(await llama.generate(ctx, message, max_tokens))
    except:
        pass # we dont care about the crappy library log spam


if __name__ == '__main__':

    # Initialize Logs
    Path("Logs").mkdir(exist_ok=True)

    # Token Don't Share
    try:
        bot.run(open("token.secret", "r").read())
    except FileNotFoundError:
        print("Token Not Found, Please Generate a Token on https://discord.com/developers/applications, and then place it in a file Named \"token.secret\"")