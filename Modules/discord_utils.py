import decimal
import datetime
from random import getrandbits, choice
from discord import Activity, ActivityType, Game, Bot
from Modules.constants import STATUS_WATCHING, STATUS_PLAYING 


async def clear_bot_status(bot: Bot):
    """Clears the Bot's Status"""
    await bot.change_presence(activity=Activity())

async def set_bot_status(bot: Bot):
    """Set's The Bot's Status"""
    if bool(getrandbits(1)):
        await bot.change_presence(activity=Activity(type=ActivityType.watching,name=choice(STATUS_WATCHING)))
    else:
        await bot.change_presence(activity=Game(name=choice(STATUS_PLAYING)))

# Constants
START_DATE = datetime.datetime(2001, 1, 1)
SECONDS_PER_DAY = decimal.Decimal(86400)
LUNATION_CONSTANT = decimal.Decimal("0.20439731")
LUNATION_MULTIPLIER = decimal.Decimal("0.03386319269")
PHASES = [
    ("New Moon", "🌑"), 
    ("Waxing Crescent", "🌒"), 
    ("First Quarter", "🌓"), 
    ("Waxing Gibbous", "🌔"), 
    ("Full Moon", "🌕"),
    ("Waning Gibbous", "🌖"), 
    ("Last Quarter", "🌗"),
    ("Waning Crescent", "🌘")
]

def calculate_moon_phase() -> tuple:
    """
    Calculate the current phase of the moon.

    Returns:
        str: A tuple containing the name of the moon phase and its corresponding emoji.
    """
    def position(now: datetime.datetime = datetime.datetime.now()) -> (tuple, decimal.Decimal): 
        diff = now - START_DATE
        days = decimal.Decimal(diff.days) + (decimal.Decimal(diff.seconds) / SECONDS_PER_DAY)
        lunations = LUNATION_CONSTANT + (days * LUNATION_MULTIPLIER)
        return lunations % 1

    def phase(pos: decimal.Decimal) -> str:
        index = int((pos * 8) + decimal.Decimal("0.5")) & 7
        return PHASES[index]

    pos = position()
    current_phase = phase(pos)
    roundedpos = round(float(pos), 3)
    return current_phase, roundedpos

async def set_moon_phase_status(bot: Bot):
    """Set's the Bot's status of be the moon phase"""
    phase, position = calculate_moon_phase()
    status_message = f"{phase[1]}{phase[0]}"
    await bot.change_presence(activity=Activity(
        type=ActivityType.watching, name=status_message,
        details=f"The Moon's Current Illumination is {position}")
    )