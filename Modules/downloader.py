import requests
import wget
import pathlib
import re
import urllib3

urllib3.disable_warnings()

headers = {
    'Host': 'ifunny.co',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'close',
}

params = {
    's': 'cl',
}


def get(url: str):
    print("Downloading ", url)

    response = requests.get(url, params=params, headers=headers, verify=False).text

    # Search for the video tags
    result = re.search('{start}(.*){end}'.format(start='<video', end='</video>'), response).group(1)

    # Now filter down to the data-src link
    video_url = result[result.index("data-src=\"") + 10:result.index(".mp4\"") + 4]

    # Download the video
    return pathlib.Path(wget.download(video_url, out="videos/"))
