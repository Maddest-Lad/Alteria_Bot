from pathlib import Path
from string import Template

# Bot Constants
SARCASTIC_RESPONSES = ["Sure thing", "Absolutely", "Indubitably", "No problemo", "You got it", "Consider it done", "By all means", "Sure thing boss", "I'm on it", "On it like a car bonnet", "Right away", "Righto", "My pleasure", "Glad to help", "Of course", "My apologies, how can I serve you today My Lord", "As you command", "At your service", "Gotcha", "Yep", "Yessir", "You got it boss", "As you wish", "As you will it My Lord", "I'm all over it", "Got it covered", "Don't mention it", "It's my pleasure", "I'm here for you", "I'm all ears", "Say no more", "I got this"]
STATUS_PLAYING = ["with my emotions", "hide-and-seek", "with fire", "hard to get", "", "it cool", "dumb", "games", "catch up", "hooky", "favorites", "fast and loose", "dirty", "minecraft", "the victim", "mind games", "second fiddle", "the long game", "the fool", "for time", "the blame game", "the odds", "it by ear", "with fate"]
STATUS_WATCHING = ["cat videos", "ants march", "eggs hatch", "stars twinkle", "noodles dance", "cheese age", "plants drink", "ice melt", "spiders web", "turtles sprint", "rain fall", "otters float", "sand shift", "clouds race", "rocks erode", "snails speed", "paint dry", "toast"]
SCOPE = [446862283600166927, 439636881194483723, 844325005209632858] # Server Scope [Just Me, Paradox Plaza, Shadow Cabinet]

# Paths
DATA_DIRECTORY = Path("Data") 
MEDIA_DIRECTORY = Path("Media")
LOG_DIRECTORY = Path("Log")

# Text Generation
NOUNS = open("Resources/nounlist.txt", 'r').read().split("\n")
IMPROVE_PROMPT_TEMPLATE = Template(open("Resources/improve_prompt_template.txt").read())
NEW_PROMPT_TEMPLATE = Template(open("Resources/new_prompt_template.txt").read())

# Stable Diffusion
NSFW_FILTER_LIST = open("Resources/NSFW_wordlist_filter.txt").read().split("\n")
SD_BASE_NEGATIVE_PROMPT = "bad-anime-horror bad_prompt_version2 verybadimagenegative_v1.3 negative_hand-neg <lora:EasyFix:0.5>"
SD_IMAGE_PATH =  MEDIA_DIRECTORY / "StableDiffusion"
