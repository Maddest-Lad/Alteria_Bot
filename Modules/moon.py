import discord
import math, decimal, datetime

async def moon_phase(bot):
    """
    Adapted from moonphase.py by Sean B. Palmer, inamidst.com
    """

    dec = decimal.Decimal

    def position(now=None): 
        if now is None: 
            now = datetime.datetime.now()

        diff = now - datetime.datetime(2001, 1, 1)
        days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
        lunations = dec("0.20439731") + (days * dec("0.03386319269"))

        return lunations % dec(1)
    
    def phase(pos): 
        index = (pos * dec(8)) + dec("0.5")
        index = math.floor(index)
        return {
            0: ("New Moon", "🌑"), 
            1: ("Waxing Crescent", "🌒"), 
            2: ("First Quarter", "🌓"), 
            3: ("Waxing Gibbous", "🌔"), 
            4: ("Full Moon", "🌕"),
            5: ("Waning Gibbous", "🌖"), 
            6: ("Last Quarter", "🌗"),
            7: ("Waning Crescent", "🌘" )
        }[int(index) & 7]
    
    pos = position()
    phasename = phase(pos)
    roundedpos = round(float(pos), 3)   
    
    # Set Phase With Alt
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{phasename[1]}{phasename[0]}", details=f"The Moon's Current Illumination is {roundedpos}"))
