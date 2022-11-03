import discord
from discord import Option
import random
import DL
from DogLib.dogcam import DogCam
from NovelAi import NovelAi

bot = discord.Bot()
nai = NovelAi()

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

@bot.slash_command(guild_ids=[446862283600166927])
async def novelai(ctx, 
                  prompt_positive: Option(str, "positive prompt", required=True),
                  seed: Option(int, "seed", required=False),
                  nsfw: Option(bool, "enable nsfw", required=False, default=False),
                  private: Option(bool, "private", required=False, default=False)
                  ):
        
        # Light Generation Logic
        if not seed:
            seed = random.randint(0, 999999999)            

        # Let User Know We're Working On It
        await ctx.response.defer(ephemeral=True)

        await ctx.send_followup(content = f"Prompt: {prompt_positive}, Seed: {seed}",
            file=discord.File(nai.generate_image(prompt_positive, seed, nsfw)))
        

# Token Don't Share
bot.run(open("token.secret", "r").read())
