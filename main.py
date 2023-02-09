import discord
from discord import Option
import random
import DL
from Meme import bot_handler

bot = discord.Bot()

# Server Scope [Just Me, Paradox Plaza, Shadow Cabinet ]
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
    
# Stellaris Gif Creator
@bot.slash_command(guild_ids=[439636881194483723])
async def stellaris(ctx, image_url: Option(str, "url to image"),
                    text: Option(str, "top text"),
                    text_position: Option(str, "text position", choices=["top", "bottom"], default="top"),
                    font_size: Option(int, "font size", default=54)):
    await ctx.respond("Adding Text")
    await ctx.send(file=discord.File(bot_handler(image_url, text, text_position, font_size)))    

@bot.slashcommand(guild_ids=scope)
async def generate(ctx):
    
    
    await ctx.respond("blank")


# Token Don't Share
bot.run(open("token.secret", "r").read())
