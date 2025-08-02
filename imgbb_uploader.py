import requests
import base64
import json
import os

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

IMGBB_API_KEY = config["IMGBB_API_KEY"]

def upload_to_imgbb(image_path, api_key=None):
    """Upload image to ImgBB and return URL"""
    try:
        # Use provided API key or default from config
        key = api_key if api_key else IMGBB_API_KEY
        
        with open(image_path, "rb") as file:
            encoded = base64.b64encode(file.read())
        
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": key,
            "image": encoded
        }
        
        res = requests.post(url, data=payload)
        if res.status_code == 200:
            return res.json()["data"]["url"]
        else:
            print("Upload lỗi:", res.text)
            return None
    except Exception as e:
        print(f"Lỗi upload ImgBB: {str(e)}")
        return None
