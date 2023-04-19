import json 
import discord
from random import getrandbits, choice
from datetime import datetime
from pathlib import Path
from Modules.constants import status_playing, status_watching


def log(*value):
    log_entry = {"date": datetime.now().isoformat(), "value": json.dumps(value) } 
    with open(Path("Logs/log.json"), 'a') as log:
        json.dump(log_entry, log)
 
async def clear_status(bot):
    await bot.change_presence(activity=discord.Activity())
    
async def set_status(bot):
    
    if bool(getrandbits(1)):
        # Watching
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=choice(status_watching)))
    else:
        # Playing
        await bot.change_presence(activity=discord.Game(name=choice(status_playing)))
