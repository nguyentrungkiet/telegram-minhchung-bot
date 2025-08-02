import gspread
import json
import os
from datetime import datetime

def get_credentials():
    """Lấy credentials từ environment hoặc file"""
    
    # Thử đọc từ environment variables trước
    creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
    if creds_json:
        return json.loads(creds_json)
    
    # Fallback: đọc từ file (cho local development)
    try:
        with open('credentials.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError("Google credentials not found in environment or credentials.json file")

def log_to_sheet(sheet_name, user_data, sheet_id=None):
    """Ghi dữ liệu vào Google Sheet"""
    try:
        # Lấy credentials
        credentials = get_credentials()
        
        # Kết nối Google Sheets
        gc = gspread.service_account_from_dict(credentials)
        
        # Mở sheet
        if sheet_id:
            # Nếu có sheet_id từ URL
            spreadsheet = gc.open_by_key(sheet_id)
            try:
                worksheet = spreadsheet.worksheet(sheet_name)
            except:
                # Tạo sheet mới nếu không tồn tại
                worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="20")
        else:
            # Mở sheet theo tên (cách cũ)
            worksheet = gc.open(sheet_name).sheet1
        
        # Thêm header nếu sheet trống
        if len(worksheet.get_all_records()) == 0:
            worksheet.append_row([
                'Timestamp', 'User', 'Username', 'Activity', 'All_Images', 'Status'
            ])
        
        # Thêm dữ liệu
        worksheet.append_row(user_data)
        
        print(f"✅ Logged to sheet: {user_data}")
        return True
        
    except Exception as e:
        print(f"❌ Error logging to sheet: {e}")
        return False

def log_to_sheet_simple(event_name, image_link):
    """Simple logging function for backward compatibility"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_to_sheet('', [now, '', '', event_name, image_link, 'Completed'])
