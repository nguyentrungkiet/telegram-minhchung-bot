from telegram.ext import Application, CommandHandler, MessageHandler, filters
from imgbb_uploader import upload_to_imgbb
from sheet_logger import log_to_sheet
import os
import logging
import re

# Cấu hình logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Lưu trạng thái người dùng
user_state = {}

# Bot token - đọc từ environment variable
TOKEN = os.getenv('TOKEN') or "8294341746:AAFnqVsvoFK9Gg8htYyAP9RgbH0tXYa5IDY"

def extract_sheet_id_from_url(url):
    """Trích xuất Sheet ID từ Google Sheets URL"""
    pattern = r'/spreadsheets/d/([a-zA-Z0-9-_]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

async def start(update, context):
    """Gửi thông báo chào mừng"""
    user_id = update.effective_user.id
    user_state[user_id] = {'step': 'waiting_sheet_info'}
    
    await update.message.reply_text(
        "👋 Chào bạn!\n\n"
        "📊 Hãy cho tôi biết Google Sheet mà bạn muốn ghi dữ liệu:\n\n"
        "🔗 *Cách 1: Gửi link Google Sheet*\n"
        "Ví dụ: `https://docs.google.com/spreadsheets/d/1ABC.../edit`\n\n"
        "📝 *Cách 2: Gửi tên sheet (cách cũ)*\n"
        "Ví dụ: `HoatDongCuaToi`\n\n"
        "💡 *Lưu ý:* Sheet phải được đặt chế độ 'Anyone with the link can edit' để bot có thể ghi được.",
        parse_mode='Markdown'
    )

async def help_command(update, context):
    """Hiển thị hướng dẫn sử dụng"""
    help_text = """
🤖 *HƯỚNG DẪN SỬ DỤNG BOT*

📋 *Quy trình:*
1️⃣ Gửi /start
2️⃣ Gửi link Google Sheet hoặc tên sheet
3️⃣ Nhập tên hoạt động
4️⃣ Gửi ảnh minh chứng (có thể gửi nhiều ảnh)
5️⃣ Gõ "xong" để hoàn thành

🔗 *Sử dụng link Google Sheet:*
• Copy link từ Google Sheets
• Paste vào bot
• Sheet sẽ tự động được nhận diện

📸 *Upload nhiều ảnh:*
• Gửi ảnh thứ 1 → Bot xác nhận
• Gửi ảnh thứ 2 → Bot xác nhận  
• Gửi ảnh thứ 3 → Bot xác nhận
• Gõ "xong" → Bot ghi vào Google Sheets

💡 *Lệnh hữu ích:*
• /start - Bắt đầu ghi hoạt động mới
• /help - Xem hướng dẫn này

📊 *Dữ liệu được ghi:*
• Thời gian
• Tên & username
• Tên hoạt động
• Tất cả link ảnh
• Trạng thái hoàn thành

Gửi /start để bắt đầu! 🚀
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def handle_photo(update, context):
    """Xử lý ảnh được gửi"""
    user_id = update.effective_user.id
    
    # Kiểm tra xem user đã nhập tên hoạt động chưa
    if user_id not in user_state or user_state[user_id].get('step') != 'waiting_photo':
        await update.message.reply_text(
            "⚠️ Vui lòng gửi lệnh /start và nhập thông tin sheet + hoạt động trước khi gửi ảnh!"
        )
        return
    
    try:
        activity_name = user_state[user_id]['activity_name']
        
        # Khởi tạo danh sách ảnh nếu chưa có
        if 'image_urls' not in user_state[user_id]:
            user_state[user_id]['image_urls'] = []
        
        await update.message.reply_text("📤 Đang xử lý ảnh của bạn...")
        
        # Lấy thông tin file ảnh
        photo = update.message.photo[-1]  # Lấy ảnh có độ phân giải cao nhất
        file_id = photo.file_id
        
        # Tải file về
        file = await context.bot.get_file(file_id)
        
        # Tạo tên file unique
        image_count = len(user_state[user_id]['image_urls']) + 1
        filename = f"photo_{update.message.date.strftime('%Y%m%d_%H%M%S')}_{user_id}_{image_count}.jpg"
        
        # Tải file về máy
        await file.download_to_drive(filename)
        
        # Upload lên ImgBB
        logger.info(f"📤 User {user_id} đang upload ảnh {image_count} cho hoạt động: {activity_name}")
        image_url = upload_to_imgbb(filename)
        
        if image_url:
            # Thêm link ảnh vào danh sách
            user_state[user_id]['image_urls'].append(image_url)
            current_count = len(user_state[user_id]['image_urls'])
            
            logger.info(f"✅ Upload ảnh {current_count} thành công: {image_url}")
            
            await update.message.reply_text(
                f"✅ Ảnh {current_count} đã upload thành công!\n\n"
                f"📋 Hoạt động: *{activity_name}*\n"
                f"🔗 Link ảnh {current_count}: {image_url}\n\n"
                f"📸 Tiếp tục gửi thêm ảnh hoặc gõ *'xong'* để hoàn thành!",
                parse_mode='Markdown'
            )
                
        else:
            logger.error("❌ Upload ImgBB thất bại")
            await update.message.reply_text("❌ Có lỗi khi tải ảnh lên ImgBB. Vui lòng thử lại!")
        
        # Xóa file tạm
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        logger.error(f"❌ Lỗi xử lý ảnh: {str(e)}")
        await update.message.reply_text(f"❌ Có lỗi xảy ra: {str(e)}")
        
        # Reset trạng thái user khi có lỗi
        if user_id in user_state:
            del user_state[user_id]

async def handle_text(update, context):
    """Xử lý tin nhắn văn bản"""
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    # Bỏ qua các command
    if text.startswith('/'):
        return
    
    # Kiểm tra trạng thái user
    if user_id not in user_state:
        await update.message.reply_text(
            "ℹ️ Hãy gửi lệnh /start để bắt đầu!"
        )
        return
    
    current_step = user_state[user_id].get('step')
    
    if current_step == 'waiting_sheet_info':
        # Kiểm tra xem có phải là link Google Sheets không
        if 'docs.google.com/spreadsheets' in text:
            sheet_id = extract_sheet_id_from_url(text)
            if sheet_id:
                user_state[user_id]['sheet_id'] = sheet_id
                user_state[user_id]['sheet_url'] = text
                user_state[user_id]['sheet_name'] = f"Sheet từ link (ID: {sheet_id[:10]}...)"
                
                await update.message.reply_text(
                    f"🔗 Đã nhận link Google Sheet!\n"
                    f"📊 Sheet ID: `{sheet_id}`\n\n"
                    f"📝 Bây giờ hãy cho tôi biết *tên hoạt động* mà bạn đã thực hiện:\n"
                    f"Ví dụ: 'Tham gia seminar AI', 'Hoàn thành bài tập lập trình', v.v.",
                    parse_mode='Markdown'
                )
                
                user_state[user_id]['step'] = 'waiting_activity'
                logger.info(f"👤 User {user_id} đã gửi Google Sheets link: {sheet_id}")
            else:
                await update.message.reply_text(
                    "❌ Link Google Sheets không hợp lệ!\n\n"
                    "Hãy đảm bảo link có dạng:\n"
                    "`https://docs.google.com/spreadsheets/d/[ID]/edit`"
                )
        else:
            # Cách cũ: tên sheet
            user_state[user_id]['sheet_name'] = text
            user_state[user_id]['step'] = 'waiting_activity'
            
            await update.message.reply_text(
                f"📊 Đã chọn Google Sheet: *{text}*\n\n"
                f"📝 Bây giờ hãy cho tôi biết *tên hoạt động* mà bạn đã thực hiện:\n"
                f"Ví dụ: 'Tham gia seminar AI', 'Hoàn thành bài tập lập trình', v.v.",
                parse_mode='Markdown'
            )
            
            logger.info(f"👤 User {user_id} ({update.effective_user.first_name}) đã chọn sheet: {text}")
        
    elif current_step == 'waiting_activity':
        # Lưu tên hoạt động
        user_state[user_id]['activity_name'] = text
        user_state[user_id]['step'] = 'waiting_photo'
        
        await update.message.reply_text(
            f"📝 Đã ghi nhận hoạt động: *{text}*\n\n"
            f"📸 Bây giờ hãy gửi ảnh minh chứng cho hoạt động này!\n"
            f"💡 Bạn có thể gửi nhiều ảnh, sau đó gõ *'xong'* để hoàn thành.",
            parse_mode='Markdown'
        )
        
        logger.info(f"👤 User {user_id} ({update.effective_user.first_name}) đã nhập hoạt động: {text}")
        
    elif current_step == 'waiting_photo':
        # Kiểm tra lệnh hoàn thành
        if text.lower() in ['xong', 'done', 'finish', 'complete']:
            # Kiểm tra xem đã có ảnh chưa
            if 'image_urls' not in user_state[user_id] or len(user_state[user_id]['image_urls']) == 0:
                await update.message.reply_text(
                    "⚠️ Bạn chưa gửi ảnh nào! Hãy gửi ít nhất một ảnh minh chứng."
                )
                return
            
            # Hoàn thành và ghi vào Google Sheets
            activity_name = user_state[user_id]['activity_name']
            sheet_info = user_state[user_id].get('sheet_name', 'Unknown')
            sheet_id = user_state[user_id].get('sheet_id')
            image_urls = user_state[user_id]['image_urls']
            image_count = len(image_urls)
            
            # Gộp tất cả link ảnh thành một chuỗi
            all_images = ' | '.join(image_urls)
            
            # Chuẩn bị dữ liệu cho Google Sheets
            sheet_data = [
                update.message.date.strftime('%Y-%m-%d %H:%M:%S'),
                update.effective_user.first_name or '',
                update.effective_user.username or '',
                activity_name,
                all_images,  # Tất cả link ảnh cách nhau bằng " | "
                f'Completed - {image_count} images'
            ]
            
            logger.info(f"📝 User {user_id} hoàn thành hoạt động với {image_count} ảnh: {activity_name} → Sheet: {sheet_info}")
            
            # Ghi nhật ký vào Google Sheets
            if sheet_id:
                success = log_to_sheet(sheet_data, sheet_id=sheet_id)
            else:
                success = log_to_sheet(sheet_data, sheet_name=sheet_info)
            
            if not success:
                await update.message.reply_text(
                    f"❌ Không thể ghi vào Google Sheet\n\n"
                    f"💡 Hãy kiểm tra:\n"
                    f"• Sheet có tồn tại không?\n"
                    f"• Sheet có được đặt chế độ 'Anyone with the link can edit' không?\n"
                    f"• Link có chính xác không?\n\n"
                    f"Gửi /start để thử lại!",
                    parse_mode='Markdown'
                )
                # Không reset user_state để user có thể thử lại
                return
            
            # Tạo tin nhắn tổng kết
            summary_message = f"✅ Hoàn thành!\n\n"
            summary_message += f"📊 Google Sheet: *{sheet_info}*\n"
            summary_message += f"📋 Hoạt động: *{activity_name}*\n"
            summary_message += f"📸 Số ảnh: {image_count}\n\n"
            
            for i, url in enumerate(image_urls, 1):
                summary_message += f"🔗 Ảnh {i}: {url}\n"
            
            summary_message += f"\n📊 Đã ghi vào Google Sheets\n\n"
            summary_message += f"Gửi /start để thêm hoạt động mới!"
            
            await update.message.reply_text(summary_message, parse_mode='Markdown')
            
            # Reset trạng thái user
            del user_state[user_id]
            
        else:
            await update.message.reply_text(
                f"📸 Tôi đang chờ bạn gửi ảnh minh chứng.\n\n"
                f"📊 Google Sheet: *{user_state[user_id].get('sheet_name', 'Unknown')}*\n"
                f"📋 Hoạt động hiện tại: *{user_state[user_id]['activity_name']}*\n"
                f"📊 Đã có: {len(user_state[user_id].get('image_urls', []))} ảnh\n\n"
                f"💡 Gửi ảnh hoặc gõ *'xong'* để hoàn thành\n"
                f"🔄 Gửi /start để bắt đầu lại",
                parse_mode='Markdown'
            )
    else:
        await update.message.reply_text(
            "🤔 Tôi không hiểu. Hãy gửi /start để bắt đầu!"
        )

async def error_handler(update, context):
    """Xử lý lỗi"""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.message:
        await update.message.reply_text(
            "❌ Đã xảy ra lỗi. Vui lòng thử lại sau."
        )

def main():
    """Chạy bot"""
    # Tạo Application
    application = Application.builder().token(TOKEN).build()
    
    # Thêm handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Thêm error handler
    application.add_error_handler(error_handler)
    
    # Log khởi động
    logger.info("🤖 Bot đang khởi động...")
    
    # Chạy bot  
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
