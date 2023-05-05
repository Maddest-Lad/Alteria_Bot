from youtube_transcript_api import YouTubeTranscriptApi
from Modules.utils import log

class summarizer():

    def __init__(self, llama):
        self.llama = llama
    
    async def summarize(self, url: str) -> str:
        log("Downloading Subtitles", url)
        try:
            # Get Video ID and Download Captions to SRT Object
            video_id = url.split("?v=")[1]
            srt = YouTubeTranscriptApi.get_transcript(video_id)

            # Create Unified Text Block
            joined_srt = ' '.join([i['text'].strip() for i in srt])
           
            response = await self.llama.generate(query=f"### Write Bullet Points Summarizing the following transcript \n ### Transcript \n {joined_srt}", max_tokens=1000, min_length=0, include_query=False)           
            
            if len(response) > 2000:
                response = response[:1999]
            
            return f"{url}\n**Summary:**\n{response}"
            
        except Exception as e:
            return f"Error : {e}" 

    
   
            
