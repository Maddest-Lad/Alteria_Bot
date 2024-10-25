from pathlib import Path
from string import Template
import json

# Bot Constants
SCOPE = [446862283600166927, 439636881194483723, 844325005209632858]

# Paths
DATA_DIRECTORY = Path("Data") 
MEDIA_DIRECTORY = Path("Media")
LOG_DIRECTORY = Path("Log")
RESOURCE_DIRECTORY = Path("Resources")
WORDLIST_DIRECTORY = RESOURCE_DIRECTORY / "Words"

# Const Lists 
NOUNS = open(WORDLIST_DIRECTORY / "nouns.txt", 'r').read().split("\n")
VERBS = open(WORDLIST_DIRECTORY / "verbs.txt", 'r').read().split("\n")
ADVERBS = open(WORDLIST_DIRECTORY / "adverbs.txt", 'r').read().split("\n")
ADJECTIVES = open(WORDLIST_DIRECTORY / "adjectives.txt", 'r').read().split("\n")
PROMPTS = open(WORDLIST_DIRECTORY / "75000 prompts.txt", 'r').read()

# Text Generation
IMPROVE_PROMPT_TEMPLATE = Template(open(RESOURCE_DIRECTORY / "improve_prompt_template.txt").read())
NEW_PROMPT_TEMPLATE = Template(open(RESOURCE_DIRECTORY / "new_prompt_template.txt").read())
PROMPT_TEMPLATE_V2 = Template(open(RESOURCE_DIRECTORY / "prompt_template_v2.txt").read())
EMOJI_PROMPT_TEMPLATE = Template(open(RESOURCE_DIRECTORY / "improve_prompt_template.txt").read())


# Stable Diffusion
NSFW_FILTER_LIST = open("Resources/NSFW_filter.txt").read().split("\n")

# Emoji Dict
EMOJI_MAP = {}

# Invert From emoji-en-US to Map Words to Emojis
with open("Resources/emoji-en-US.json") as json_file:
    data = json.load(json_file) # Str (Emoji) -> List (Words)
    
    for emoji in data.keys():
        for word in data[emoji]:
            EMOJI_MAP[word] = emoji
