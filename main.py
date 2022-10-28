import discord
from discord import Option
import subprocess
import DL
from dogcam import DogCam

bot = discord.Bot()

# Server Scope
scope = [446862283600166927]

# Startup
@bot.event
async def on_ready():
    print(f"{bot.user} Has Started Up Successfully")


# Ifunny Downloading -- Exclusive to My Personal Server
@bot.slash_command(guild_ids=scope)
async def download(ctx, url: Option(str, "url to download")):
    await ctx.respond("Downloading")
    await ctx.send(file=discord.File(DL.get(url)))

# DogCam
@bot.slash_command(guild_ids=scope)
async def dogcam(ctx, action:Option(str, "Start or Stop DogCam", required=True, choices=["start", "stop"])):
        if action == "start":
            await ctx.respond(dc.start())
        if action == "stop":
            await ctx.respond(dc.stop())
        await ctx.respond("Something Went Wrong")

# Create DogCam Class
dc = DogCam()

# Token Don't Share
bot.run(open("token.secret", "r").read())
