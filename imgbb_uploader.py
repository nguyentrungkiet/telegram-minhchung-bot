import requests
import os
import json

def upload_to_imgbb(image_path, api_key=None):
    """Upload ảnh lên ImgBB và trả về URL"""
    
    # Ưu tiên API key từ parameter, sau đó từ env, cuối cùng từ file
    if api_key is None:
        # Thử đọc từ environment variable trước
        api_key = os.getenv('IMGBB_API_KEY')
        
        # Nếu không có env var, thử đọc từ file (cho local development)
        if api_key is None:
            try:
                with open("config.json", "r") as f:
                    config = json.load(f)
                    api_key = config.get("IMGBB_API_KEY")
            except FileNotFoundError:
                pass
    
    if not api_key:
        raise ValueError("IMGBB_API_KEY not found in environment variables or config.json")
    
    # Upload logic
    try:
        with open(image_path, 'rb') as image_file:
            url = "https://api.imgbb.com/1/upload"
            payload = {
                "key": api_key,
            }
            files = {
                "image": image_file
            }
            
            response = requests.post(url, data=payload, files=files)
            response.raise_for_status()
            
            result = response.json()
            if result.get("success"):
                return result["data"]["url"]
            else:
                raise Exception(f"ImgBB upload failed: {result}")
                
    except Exception as e:
        print(f"❌ Error uploading to ImgBB: {e}")
        return None
