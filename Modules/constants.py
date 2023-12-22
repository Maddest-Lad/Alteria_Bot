from pathlib import Path
from string import Template

# Bot Constants
SCOPE = [446862283600166927, 439636881194483723, 844325005209632858]

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
