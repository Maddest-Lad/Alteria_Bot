from youtube_transcript_api import YouTubeTranscriptApi
from Modules.utils import log
from Modules.utils import chunk_by

class Summarizer():

    def __init__(self, text_generator):
        self.text_generator = text_generator
    
    async def summarize(self, url: str) -> str:
        log("Downloading Subtitles", url)
        try:
            # Get Video ID and Download Captions to SRT Object
            video_id = url.split("?v=")[1]
            srt = YouTubeTranscriptApi.get_transcript(video_id)

            # Create Unified Text Block
            joined_srt = ' '.join([i['text'].strip() for i in srt])
           
            response = await self.text_generator.instruct(query=f"### Write Bullet Points Summarizing the following transcript \n ### Transcript \n {joined_srt}", max_tokens=1000, min_length=0, include_query=False)           

            # Discord 2000 Char Message Limit
            if len(response > 1999):
                return chunk_by(response, 1999)

            return [response]
            
        except Exception as e:
            return f"Error : {e}" 

    
   
            
