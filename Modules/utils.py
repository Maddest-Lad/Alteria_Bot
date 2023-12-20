import json 
import os
import discord

from random import getrandbits, choice
from datetime import datetime
from pathlib import Path
from PIL import Image
from pytesseract import pytesseract

from Modules.constants import STATUS_PLAYING, STATUS_WATCHING

def log(*value):
    log_entry = {"date": datetime.now().isoformat(), "value": json.dumps(value) } 
    with open(Path("Logs/log.json"), 'a') as log:
        log.write(os.linesep)
        json.dump(log_entry, log)
        
 
async def clear_status(bot):
    await bot.change_presence(activity=discord.Activity())
    
async def set_status(bot):
    if bool(getrandbits(1)):
        # Watching
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=choice(STATUS_WATCHING)))
    else:
        # Playing
        await bot.change_presence(activity=discord.Game(name=choice(STATUS_PLAYING)))

def convert_to_pacific(time_zone: str, hours: int) -> int:
    # Calculate the offset in hours from the Pacific time zone to the input time zone
    offset_hours = None
    match time_zone:
        case "Pacific":
            offset_hours = 0
        case "Mountain":
            offset_hours = 1
        case "Central":
            offset_hours = 2
        case "Eastern":
            offset_hours = 3

    # Convert the input hours to Pacific time
    pacific_hours = (hours - offset_hours) % 24

    return pacific_hours

def chunk_by(string: str, chunk_size: int):
    # Converts a String into a list of strings chunk_size long 
    return [string[i:i+chunk_size] for i in range(0, len(string), chunk_size)]

def ocr(image_path: Path) -> str:
    img = Image.open(image_path)
    return pytesseract.image_to_string(img)