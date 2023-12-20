import os
import requests
import pathlib
import re
import subprocess
import urllib3
import uuid
import wget

urllib3.disable_warnings()

HEADERS = {
    'Host': 'ifunny.co',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'close',
}

PARAMS = {
    's': 'cl',
}

class Downloader():

    def download_if(self, url: str):
        response = requests.get(url, params=PARAMS, headers=HEADERS, verify=False).text

        # Search for the video tags
        result = re.search('{start}(.*){end}'.format(start='<video', end='</video>'), response).group(1)

        # Now filter down to the data-src link
        video_url = result[result.index("data-src=\"") + 10:result.index(".mp4\"") + 4]

        # Download the video    
        return pathlib.Path(wget.download(video_url, out="Media/Videos"))
    
    def download_image(self, url: str):
        try:
            match = re.search(r"\.(png|jpg|jpeg)(?:\?|$)", url)
            
            if match is None:
                raise ValueError("Invalid URL or unsupported file type")
            
            # Group 1 contains the matched file extension
            filetype = match.group(1)
            
            outpath = f"Media/Images/{str(uuid.uuid4())}.{filetype}" # Unique* Filename
            
            subprocess.run(['wget', '-O', outpath, url])

            return pathlib.Path(outpath)        
                        
        except Exception as e:
            return f"Image Download Error : {e}"
