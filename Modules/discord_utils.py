import decimal
import datetime
from random import getrandbits, choice
from discord import Activity, ActivityType, Game, Bot

# Constants
SARCASTIC_RESPONSES = ["Sure thing", "Absolutely", "Indubitably", "No problemo", "You got it", "Consider it done", "By all means", "Sure thing boss", "I'm on it", "On it like a car bonnet", "Right away", "Righto", "My pleasure", "Glad to help", "Of course", "My apologies, how can I serve you today My Lord", "As you command", "At your service", "Gotcha", "Yep", "Yessir", "You got it boss", "As you wish", "As you will it My Lord", "I'm all over it", "Got it covered", "Don't mention it", "It's my pleasure", "I'm here for you", "I'm all ears", "Say no more", "I got this"]
STATUS_PLAYING = ["with my emotions", "hide-and-seek", "with fire", "hard to get", "", "it cool", "dumb", "games", "catch up", "hooky", "favorites", "fast and loose", "dirty", "minecraft", "the victim", "mind games", "second fiddle", "the long game", "the fool", "for time", "the blame game", "the odds", "it by ear", "with fate"]
STATUS_WATCHING = ["cat videos", "ants march", "eggs hatch", "stars twinkle", "noodles dance", "cheese age", "plants drink", "ice melt", "spiders web", "turtles sprint", "rain fall", "otters float", "sand shift", "clouds race", "rocks erode", "snails speed", "paint dry", "toast"]

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