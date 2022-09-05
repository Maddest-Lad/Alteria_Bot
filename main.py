import discord
from discord import Option
import DL

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} Has Started Up Successfully")

@bot.slash_command(guild_ids=[446862283600166927])
async def download(ctx, url: Option(str, "url to download")):
    await ctx.respond("Downloading")
    await ctx.send(file=discord.File(DL.get(url)))


bot.run("<your_token_here>")
