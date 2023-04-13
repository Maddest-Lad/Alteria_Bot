import discord
from discord import Option
from SD import SD
import DL
import random
from Meme import bot_handler
from llama import llama

bot = discord.Bot()
sd_generator = SD()
llama = llama()


# Server Scope [Just Me, Paradox Plaza, Shadow Cabinet, Alt Testing]
scope = [446862283600166927, 439636881194483723, 844325005209632858, 1073887217128308766]

# Voice Chat Tracking
connections = {}

# Startup
@bot.event
async def on_ready():
    print(f"{bot.user} Has Started Up Successfully")

# Ifunny Downloading -- Exclusive to My Personal Server
@bot.slash_command(guilds=[446862283600166927])
async def download(ctx, url: Option(str, "url to download")):
    await ctx.respond("Downloading")
    await ctx.send(file=discord.File(DL.get(url)))
    
# Stellaris Gif Creator
# @bot.slash_command(guilds=[439636881194483723])
# async def stellaris(ctx, image_url: Option(str, "url to image"),
#                     text: Option(str, "top text"),
#                     text_position: Option(str, "text position", choices=["top", "bottom"], default="top"),
#                     font_size: Option(int, "font size", default=54)):
#     await ctx.respond("Adding Text")
#     await ctx.send(file=discord.File(bot_handler(image_url, text, text_position, font_size)))    

@bot.slash_command(guilds=scope)
async def generate(ctx,
                   prompt: Option(str, "The postive prompt that describes the image to generate", required=True),
                   negative_prompt: Option(str, "the negative prompt", required=False), 
                   orientation: Option(str, "The orientation of the image", required=False, choices=["square", "portrait", "landscape"], default="square"),
                   steps: Option(int, "The number of steps used to generate the image [10, 50]", required=False,  default=20),
                   prompt_obediance: Option(int, "The strictly the AI obeys the prompt [1, 30]", required=False, default=9),
                   sampler: Option(str, "The sampling method used", required=False, choices=["Euler", "DDIM"], default="DDIM"),
                   seed: Option(int, "The seed for image generation, useful for replicating results", required=False)):
    
    await ctx.respond(random.choice(["Sure thing", "Absolutely", "Indubitably", "No problemo", "You got it", "Consider it done", "By all means", "Sure thing boss", "I'm on it", "On it like a car bonnet", "Right away", "Righto", "My pleasure", "Glad to help", "Of course", "My apologies, how can I serve you today My Lord", "As you command", "At your service", "Gotcha", "Yep", "Yessir", "You got it boss", "As you wish", "As you will it My Lord", "I'm all over it", "Got it covered", "Don't mention it", "It's my pleasure", "I'm here for you", "I'm all ears", "Say no more", "I got this"]))
    await sd_generator.generate(ctx, prompt, negative_prompt, orientation, steps, prompt_obediance, sampler, seed)
    
@bot.slash_command(guilds=scope)
async def generate_help(ctx, info_category: Option(str, "", required=True, choices=["Textual Inversion", "LoRA"])):
    match info_category:
        case "Textual Inversion":
            await ctx.respond("Textual Inversion Keywords: \n```001glitch-core, 80s-anime-ai, anime-background-style-v2, bad_prompt_version2, minecraft-concept-art, Style-Autumn, Style-Invisible-Inc-2, Style-Lofi, style-of-marc-allante, terraria-style, trigger-studio, valorantstyle, wayne-reynolds-character```")
        case "LoRA":
            await ctx.respond("Low Rank Adpations: \n You Can Adjust the :1 from [0.0-1.0] to Change the Effect's Strength  ```<lora:Lora-1990sAnimeStyle:1> <lora:Lora-Arcane:1> <lora:Lora-BOTW:1>  <lora:Lora-FlatColor:1> <lora:Lora-Ghibli:1> <lora:Lora-NecoArc:1> <lora:Lora-Persona:1>  <lora:Lora-SamYang:1> <lora:Lora-Synthpunk:1> <lora:Lora-Tokiame:1> <lora:Lora-Vaporwave:1> <lora:Lora-VoxMachina:1> <lora:Lora-Wanostyle:1> <lora:Lora-ZeldaCid:1>```")

@bot.slash_command(guilds=scope)
async def ask_alt(ctx, 
                  message: Option(str, "The postive prompt that describes the image to generate", required=True), 
                  max_tokens: Option(int, "A general measure that can be considered an aggregation of complexity and length [200-2000]", min_value=200, default=400, max_value=2000, required=False)):
    
    await ctx.respond(random.choice(["Sure thing", "Absolutely", "Indubitably", "No problemo", "You got it", "Consider it done", "By all means", "Sure thing boss", "I'm on it", "On it like a car bonnet", "Right away", "Righto", "My pleasure", "Glad to help", "Of course", "My apologies, how can I serve you today My Lord", "As you command", "At your service", "Gotcha", "Yep", "Yessir", "You got it boss", "As you wish", "As you will it My Lord", "I'm all over it", "Got it covered", "Don't mention it", "It's my pleasure", "I'm here for you", "I'm all ears", "Say no more", "I got this"]))
    try:
        await ctx.respond(await llama.generate(ctx, message, max_tokens))
    except:
        pass # we dont care about the crappy library log spam

#VC Fun
@bot.slash_command(guilds=scope)
async def join_me(ctx):
    
    if ctx.guild.id in connections:
        vc = connections[ctx.guild.id]
        vc.stop_recording()
        del connections[ctx.guild.id]
        await ctx.delete()
    
    voice = ctx.author.voice
    if not voice:
        return await ctx.respond("You're not in a vc right now")
    
    vc = await voice.channel.connect()
    connections.update({ctx.guild.id: vc})
    


# Token Don't Share

bot.run(open("token.secret", "r").read())
