import json
import os
import re
from random import choice
from datetime import datetime
from pathlib import Path

import aiopytesseract
import markovify

from Modules.constants import LOG_DIRECTORY, NOUNS, VERBS, ADVERBS, ADJECTIVES, PROMPTS


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
    """ Returns a random sentence in the format of (Adjective, Noun, Verb, Adverb)"""
    return f"{choice(ADJECTIVES)} {choice(NOUNS)} {choice(VERBS)} {choice(ADVERBS)}"

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
