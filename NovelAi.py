import requests
import base64
import uuid
import io
from PIL import Image
from time import sleep

class NovelAi:
 
    def generate_image(self, prompt_positive, seed, nsfw):
        
        
        headers = {
            'Host': 'novel.local',
            # 'Content-Length': '370',
            'Authorization': 'Bearer',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.63 Safari/537.36',
            # Already added when you pass json=
            # 'Content-Type': 'application/json',
            'Accept': '*/*',
            'Origin': 'http://novel.local',
            # 'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'close',
        }
        
        json_data = {
            'prompt': 'masterpiece, best quality,' + prompt_positive,
            'width': 512,
            'height': 512,
            'scale': 12,
            'sampler': 'k_euler',
            'steps': 22,
            'seed': str(seed),
            'n_samples': 1,
            'ucPreset': 0,
            'uc': 'lowres, bad anatomy, text, error, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry'
        }
        
        # Send Request
        response = requests.post('http://192.168.50.11/generate-stream', headers=headers, json=json_data, verify=False)
        raw = response.content.decode("utf-8")
        data = raw[raw.find("data")+5:]
            
        # Generate Random Filename
        path = "Images/" + str(uuid.uuid4()) + ".png"
        
        with open(path, "wb") as f:
            f.write(base64.b64decode(data))
        
        return path  
