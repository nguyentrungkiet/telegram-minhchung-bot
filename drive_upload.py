from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import re
import os

# OAuth2 cho My Drive cá nhân
def init_oauth2():
    """Khởi tạo OAuth2 authentication"""
    gauth = GoogleAuth('settings.yaml')
    
    # Kiểm tra credentials đã lưu
    if os.path.exists('saved_credentials.json'):
        gauth.LoadCredentialsFile('saved_credentials.json')
    
    if gauth.credentials is None:
        # Lần đầu: mở browser để authorize
        print("🔓 First time setup - opening browser for authorization...")
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Token hết hạn: refresh
        print("🔄 Refreshing expired token...")
        gauth.Refresh()
    else:
        # Token còn hiệu lực: authorize
        gauth.Authorize()
    
    # Lưu credentials
    gauth.SaveCredentialsFile('saved_credentials.json')
    
    return GoogleDrive(gauth)

# Khởi tạo drive với OAuth2
try:
    drive = init_oauth2()
    print("✅ Using OAuth2 authentication for My Drive")
except Exception as e:
    print(f"❌ OAuth2 initialization failed: {e}")
    drive = None

def slugify(text):
    """Chuyển tên sự kiện thành tên thư mục đơn giản"""
    return re.sub(r'[^\w\s-]', '', text).strip().replace(' ', '')

def create_subfolder(event_name, parent_folder_id):
    """Tạo thư mục con bên trong thư mục gốc"""
    slug = slugify(event_name)
    folder_metadata = {
        'title': slug,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [{'id': parent_folder_id}]
    }
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    return folder['id'], slug

def upload_to_drive(filename, filepath, folder_id):
    """Upload ảnh vào thư mục con đã tạo"""
    try:
        print(f"🔧 Starting upload process...")
        print(f"📄 File: {filename}")
        print(f"📂 Folder ID: {folder_id}")
        print(f"📍 File path: {filepath}")
        
        if drive is None:
            return None, "Drive authentication failed"
        
        # Kiểm tra file tồn tại
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return None, f"File không tồn tại: {filepath}"
        
        print(f"📏 File size: {os.path.getsize(filepath)} bytes")
        
        # Tạo file object
        print(f"🔧 Creating Drive file object...")
        file = drive.CreateFile({'title': filename, 'parents': [{'id': folder_id}]})
        
        # Set content
        print(f"🔧 Setting file content...")
        file.SetContentFile(filepath)
        
        # Upload
        print(f"⬆️ Uploading to Google Drive...")
        file.Upload()
        
        link = file['alternateLink']
        print(f"✅ Upload successful: {link}")
        return link, None
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Upload error: {error_msg}")
        return None, error_msg
