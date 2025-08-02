import requests
import os
import json
import time

def upload_to_imgbb(image_path, api_key=None, max_retries=3):
    """Upload ảnh lên ImgBB và trả về URL với retry mechanism"""
    
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
    
    # Upload logic với retry
    for attempt in range(max_retries):
        try:
            print(f"🔄 Attempt {attempt + 1}/{max_retries} uploading to ImgBB...")
            
            with open(image_path, 'rb') as image_file:
                url = "https://api.imgbb.com/1/upload"
                payload = {
                    "key": api_key,
                }
                files = {
                    "image": image_file
                }
                
                # Tăng timeout lên 30 giây
                response = requests.post(url, data=payload, files=files, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                if result.get("success"):
                    print(f"✅ ImgBB upload successful: {result['data']['url']}")
                    return result["data"]["url"]
                else:
                    raise Exception(f"ImgBB upload failed: {result}")
                    
        except requests.exceptions.Timeout:
            print(f"⏰ ImgBB timeout on attempt {attempt + 1}")
            if attempt < max_retries - 1:
                print(f"🔄 Retrying in 2 seconds...")
                time.sleep(2)
            continue
            
        except requests.exceptions.RequestException as e:
            print(f"🌐 Network error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                print(f"🔄 Retrying in 2 seconds...")
                time.sleep(2)
            continue
                
        except Exception as e:
            print(f"❌ Error uploading to ImgBB on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                print(f"🔄 Retrying in 2 seconds...")
                time.sleep(2)
            continue
    
    print(f"❌ Failed to upload after {max_retries} attempts")
    return None
