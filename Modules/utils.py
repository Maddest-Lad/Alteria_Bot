import json
import os
import re
import string
from random import choice, randrange
from datetime import datetime
from pathlib import Path

import aiopytesseract
import markovify

from Modules.constants import LOG_DIRECTORY, NOUNS, VERBS, ADVERBS, ADJECTIVES, PROMPTS, EMOJI_MAP


def log(*value):
    """Logs Value To Local JSON File"""
    mm_dd_yyyy:str = datetime.now().strftime('%m_%d_%Y')
    log_file_path = LOG_DIRECTORY / f"{mm_dd_yyyy}.json"

    log_entry = {"date": datetime.now().isoformat(), "value": json.dumps(value) } 
    with open(log_file_path, 'a') as log_file:
        log_file.write(os.linesep)
        json.dump(log_entry, log_file)

def chunk_by(text: str, chunk_size: int):
    """Converts a String into a list of strings chunk_size long"""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

async def optical_character_recognition(image_path: Path) -> str:
    """Uses Optical Character Recognition (OCR) to extract text from an Image"""
    return await aiopytesseract.image_to_string(str(image_path))


# Experiments For Stable Diffusion / LLM Prompt Refinement
def generate_random_prompt() -> str:
    """Returns a random sentence in the format of (Adjective, Noun, Verb, Adverb)"""
    response = []
    
    for i in range(0, randrange(6, 15)):
        num = randrange(1,4)
        
        match num:
            case 1:
                response.append(choice(ADJECTIVES))
            case 2:
                response.append(choice(NOUNS))
            case 3:
                response.append(choice(VERBS))
            case 4:
                response.append(choice(ADVERBS))
        
        if randrange(1,3) == 3:
            response.append(",")
    
    return " ".join(response)

def text_cleaner(text):
    text = re.sub(r'--', ' ', text)
    text = re.sub('[\[].*?[\]]', '', text)
    text = re.sub(r'(\b|\s+\-?|^\-?)(\d+|\d*\.\d+)\b', '', text)
    text = re.sub(r"http\S+", "", text)
    text = ' '.join(text.split())
    return text

text_model = markovify.Text(text_cleaner(PROMPTS))

def generate_prompt_markov() -> str:
    return text_model.make_sentence()


def convert_to_emoji(text: str) -> str:
    """Converts any emoji adjacent words in a text to emojis ex (grin, smile, happy, joy) -> 😀"""
    words = text.split(" ")
    return " ".join(EMOJI_MAP.get(word.strip(string.punctuation).lower(), word) for word in words)