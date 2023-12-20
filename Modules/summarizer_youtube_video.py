from youtube_transcript_api import YouTubeTranscriptApi
from Modules.utils import chunk_by
from Modules.text_generation import TextGenerator

async def summarize(textgen: TextGenerator, url: str) -> str:
    """Summarizes a youtube video by it's captions 

    Args:
        url (str): The video url
    Returns:
        str: The LLM summary
    """
    try:
        captions = download_captions(url)
        response = await textgen.instruct(query=f"### Write Bullet Points Summarizing the following transcript \n ### Transcript \n {captions}", max_tokens=1000, min_length=0, include_query=False)           

        # Discord 2000 Char Message Limit
        if len(response > 1999):
            return chunk_by(response, 1999)

        return [response]
        
    except Exception as e:
        return f"Error : {e}"

def download_captions(url: str) -> str:
    """Downloads captions using YouTubeTranscriptApi"""
    video_id = url.split("?v=")[1]  # Get Video ID
    srt = YouTubeTranscriptApi.get_transcript(video_id)
    return ' '.join([i['text'].strip() for i in srt])
