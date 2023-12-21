# Project Overview
Alteria is a Discord bot developed using the Pycord library, integrating various features such as media downloading, image generation using Stable Diffusion, response generation with a local language model, and image processing with OCR and CLIP.

## Key Features
### Video Downloading
* Command: /download
* Description: Downloads a video from a provided URL.

### Image Generation with Stable Diffusion
* Command: /generate
* Description: Generates images based on provided prompts. It includes options for automatic prompt improvement and generating multiple images.

### Text Generation
* Command 1: /ask_alt
* Command 2: /chat
* Description: Generates responses to user messages using a locally hosted large language model, similar to ChatGPT.

### Image Processing
* Command: /process_image
* Description: Processes an image from a provided URL, utilizing OCR and CLIP for summarization and description.

### Modules
* Text Generation: Handles text generation tasks.
* Stable Diffusion: Manages image generation and processing.
* Download Manager: Facilitates downloading videos and images.
* User Management: Manages user data and interactions.
* Utilities: Includes functions like OCR.

## System Initialization
* The bot is initialized using the Pycord library.
* Separate aiohttp session handlers are used for different modules.

### Scheduling and Status Updates
* An AsyncIOScheduler is used for scheduling tasks, such as updating the bot's status.
* The bot's status is updated periodically (every 12 hours) to reflect different themes (day/night).

### Starting the Bot
Windows: 
```batch
./start.bat
```
Linux: 
```
./start.sh
```
Manual Environment Setup (Venv Recommended) 
```
pip install -r requirements.txt
python main.py
```
