from pathlib import Path
import re
import uuid

from Modules.session_handler import SessionHandler
from Modules.constants import MEDIA_DIRECTORY

class DownloadManager(SessionHandler):
    """Handles Downloading Media"""

    async def download_image(self, url: str):
        """Downloads an Image from a URL"""
        match = re.search(r"\.(png|jpg|jpeg)(?:\?|$)", url)

        if match is None:
            raise ValueError("Invalid URL or unsupported file type")
        filetype = match.group(1)
        outpath = MEDIA_DIRECTORY / f"{str(uuid.uuid4())}.{filetype}"

        binary_response = await self._make_get_request(url)
         
        with open(outpath, 'wb') as file:
            file.write(binary_response)

        return outpath

    async def download_video(self, url :str) -> Path:
        """Calls Download Functions for Youtube Shorts, Tiktok, Instagram Reels, Reddit Videos, iFunny Videos"""
        base_url = self.remove_protocol_prefixes(url)

        if url.startswith("youtube.com/shorts"):
            return self._download_short(url)
         
        elif url.startswith("tiktok.com"):
            return self._download_tiktok(url)

        elif url.startswith("instagram.com/reels"):
            return self._download_reel(url)

        elif url.startswith("ifunny.co"):
            return self._download_if(url)
        
        else:        
            raise ValueError(f"Could not detect video provider from the {url}")

    # Youtube
    async def _download_short(self, url: str) -> Path:
        raise NotImplementedError

    # Instagram
    async def _download_reel(self, url) -> Path:
        raise NotImplementedError

    # Tiktok
    async def _download_tiktok(self, url: str) -> Path:
        raise NotImplementedError

    # iFunny
    async def _download_if(self, url: str) -> Path:
        """Downloads a Video, Pulling the source URL from the <Video> HTML tags

        Args:
            url (str): The url of the video page

        Raises:
            ValueError: No video found

        Returns:
            Path: Path to saved file
        """
        HEADERS_IF = {
            'Host': 'ifunny.co',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'close'
        }
        PARAMS_IF = {'s': 'cl'}

        response = await self._make_get_request(url, data=PARAMS_IF, headers=HEADERS_IF)
        page_text = await response.text()

        match = re.search(r'<video.*?data-src="(.*?\.mp4)".*</video>', page_text)

        if not match:
            raise ValueError("No video found in the provided URL")

        video_url = match.group(1)
        outpath = MEDIA_DIRECTORY / f"{str(uuid.uuid4())}.mp4"

        video_response = await self._make_get_request(video_url)
        with open(outpath, 'wb') as file:
            file.write(await video_response.content.read())

        return outpath
   
    def remove_protocol_prefixes(self, url: str) -> str:
        """Removes 'http://', 'https://', and 'www.' from the start of the string"""
        pattern = r'^(https?://)?(www\.)?'
        return re.sub(pattern, '', url)
