import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def log_to_sheet(data_row, sheet_name=None, sheet_id=None):
    """Log data to Google Sheets
    Args:
        data_row: List containing [timestamp, user_name, username, activity_name, image_url, status]
        sheet_name: Name of the Google Sheet to write to (optional)
        sheet_id: ID of the Google Sheet to write to (optional, takes precedence over sheet_name)
    """
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        
        # Mở sheet bằng ID hoặc tên
        try:
            if sheet_id:
                # Sử dụng Sheet ID từ URL
                spreadsheet = client.open_by_key(sheet_id)
                sheet = spreadsheet.sheet1
                sheet_display_name = f"Sheet ID: {sheet_id[:10]}..."
            else:
                # Sử dụng tên sheet (cách cũ)
                sheet = client.open(sheet_name or "Thongke").sheet1
                sheet_display_name = sheet_name or "Thongke"
                
        except gspread.SpreadsheetNotFound:
            print(f"❌ Không tìm thấy Google Sheet: {sheet_name or sheet_id}")
            print(f"💡 Hãy đảm bảo sheet tồn tại và được chia sẻ với bot")
            return False
        except gspread.exceptions.APIError as e:
            print(f"❌ Lỗi API Google Sheets: {str(e)}")
            if "PERMISSION_DENIED" in str(e):
                print(f"💡 Sheet cần được đặt chế độ 'Anyone with the link can edit'")
            return False
        
        # Thêm header nếu sheet trống
        try:
            existing_data = sheet.get_all_values()
            if len(existing_data) == 0:
                headers = ['Thời gian', 'Tên người dùng', 'Username', 'Tên hoạt động', 'Link ảnh', 'Trạng thái']
                sheet.append_row(headers)
        except Exception as header_error:
            print(f"⚠️ Không thể thêm header: {str(header_error)}")
        
        # Thêm dữ liệu
        sheet.append_row(data_row)
        print(f"✅ Logged to sheet '{sheet_display_name}': {data_row}")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi ghi sheet: {str(e)}")
        return False

def log_to_sheet_simple(event_name, image_link):
    """Simple logging function for backward compatibility"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_to_sheet([now, '', '', event_name, image_link, 'Completed'])
