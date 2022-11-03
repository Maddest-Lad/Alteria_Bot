import discord
from discord import Option
import random
import DL
from NovelAi import generate_image

bot = discord.Bot()

# Server Scope
scope = [446862283600166927, 439636881194483723, 844325005209632858]

# Startup
@bot.event
async def on_ready():
    print(f"{bot.user} Has Started Up Successfully")


# Ifunny Downloading -- Exclusive to My Personal Server
@bot.slash_command(guild_ids=[446862283600166927])
async def download(ctx, url: Option(str, "url to download")):
    await ctx.respond("Downloading")
    await ctx.send(file=discord.File(DL.get(url)))

@bot.slash_command(guild_ids=scope, description="Generate an Image from a Prompt using NovelAI")
async def novelai(ctx,
                  prompt: Option(str, "The prompt for the AI to generate an image from", required=True),
                  negate: Option(str, "A prompt for the AI to negate in the output", required=False, default=""), 
                  orientation: Option(str, "The orientation of the image", required=False, choices=["square", "portrait", "landscape"], default="square"),
                  steps: Option(int, "The number of steps used to generate the image [1, 50]", required=False,  default=20),
                  resolution: Option(str, "The size of the longest dimension", required=False, choices=["normal", "high"], default="normal"),
                  prompt_obediance: Option(str, "The strictly the AI obeys the prompt [6, 12, 20]", required=False, choices=["low", "medium", "high"], default="medium"),
                  filter_out: Option(str, "Premade Categories to Negate", required=False, choices=["Bad Anatomy", "NSFW"]),
                  seed: Option(int, "The seed for image generation, useful for replicating results", required=False)
                  ):
    
        # Preseed
        if not seed:
            seed = random.randint(0, 999999999)            

        # Let User Know We're Working On It
        await ctx.respond("Command Received", ephemeral=False)
        await generate_image(ctx, prompt, negate, orientation, steps, resolution, prompt_obediance, filter_out, seed)       

# Token Don't Share
bot.run(open("token.secret", "r").read())
