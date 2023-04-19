import discord
from pathlib import Path
from discord import Option

from Modules.stable_diffusion import stable_diffusion
from Modules.llama import llama
from Modules.downloader import downloader
from Modules.utils import log
from Modules.constants import *

# Initialize Bot
bot = discord.Bot()

# Initalize Class Objects
sd_generator = stable_diffusion()
llama = llama()
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
                  max_tokens: Option(int, "A general measure that can be considered an aggregation of complexity and length [200-2000]", min_value=200, default=400, max_value=2000, required=False)):
    await ctx.defer()
    await ctx.followup.send(await llama.generate(message, max_tokens))

@bot.slash_command(guilds=scope, description="Set's the Bot's Status")
async def set_status(ctx, status: Option(str, "the status to be set", required=True),
                     status_type: Option(str, "The Type of Custom Status", choices=["Game", "Streaming", "Watching", "Listening"], required=True),
                     url: Option(str, "The Streaming Url (If Streaming Status Type)", default="")):
    match status_type:
        case "Game":  
            await bot.change_presence(activity=discord.Game(name=status)) # Playing <status>
        case "Streaming":  
            await bot.change_presence(activity=discord.Streaming(name="status", url=url)) # Streaming <status>
        case "Listening":
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status)) # Listening to <status>
        case "Watching":
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status)) # Watching <status>

    # Only the Sender Can See This Response
    await ctx.respond("Status Set", ephemeral=True) 
    log(status)

@bot.slash_command(guilds=scope, administrator=True, description="Logs Data")
async def log_data(ctx, all_fields: Option(bool, "All Fields", required=False, default=False)):
    if ctx.author.id in authorized_users:
        data = {
            'guild'        : ctx.guild,
            'channel'      : ctx.channel,
            'user'         : ctx.user,
            'perms'        : ctx.app_permissions    
        }
        
        if all_fields:
            data.update(vars(ctx))  
            
        # User Friendly
        formatted = '\n'.join([key + " : " + str(value) for key, value in data.items()])
        await ctx.respond(f"Data Dump:```{formatted}```")
    else:
        await ctx.respond("You Don't Have Permission for This Command")

if __name__ == '__main__':

    # Initialize Logs
    Path("Logs").mkdir(exist_ok=True)

    # Token Don't Share
    try:
        bot.run(open("token.secret", "r").read())
    except FileNotFoundError:
        print("Token Not Found, Please Generate a Token on https://discord.com/developers/applications, and then place it in a file Named \"token.secret\"")
