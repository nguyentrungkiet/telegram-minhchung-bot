# 📋 HƯỚNG DẪN SETUP BOT CHO BẠN BÈ

## 🎯 Tính năng mới: Hỗ trợ Google Sheets URL

Bot hiện hỗ trợ **2 cách** ghi vào Google Sheet:
1. 🔗 **Gửi link Google Sheet** (Khuyến nghị - Dễ nhất!)
2. 📝 **Gửi tên sheet** (Cách cũ)

## � Cách 1: Sử dụng Link Google Sheet (KHUYẾN NGHỊ)

### Bước 1: Tạo Google Sheet
1. Truy cập https://sheets.google.com
2. Tạo sheet mới với tên bất kỳ

### Bước 2: Chia sẻ Sheet (Cực đơn giản!)
1. Trong Google Sheet, nhấn nút **"Chia sẻ"** (góc trên bên phải)
2. Nhấn **"Thay đổi thành ai có liên kết"**
3. Chọn **"Editor"** (Người chỉnh sửa)
4. Nhấn **"Xong"**
5. **Copy link** được tạo ra

### Bước 3: Sử dụng Bot
1. Gửi `/start` trong Telegram
2. **Paste link** vào bot (ví dụ: `https://docs.google.com/spreadsheets/d/1ABC...`)
3. Bot tự động nhận diện sheet
4. Tiếp tục như bình thường

## � Cách 2: Sử dụng Tên Sheet (Cách cũ)

### Bước 1: Tạo & Chia sẻ với Service Account
1. Tạo Google Sheet với tên cụ thể
2. Chia sẻ với email: `botminhchung@botminhchung.iam.gserviceaccount.com`
3. Cấp quyền **"Editor"**

### Bước 2: Sử dụng Bot
1. Gửi `/start`
2. Nhập **tên sheet** chính xác
3. Tiếp tục workflow

## 🤖 Workflow Bot (Hướng dẫn chi tiết)

### Bước 1: Khởi động
- Gửi `/start` trong Telegram

### Bước 2: Chọn Sheet
**Cách A - Link Google Sheet (Dễ nhất - Khuyến nghị):**
- Paste link Google Sheet: `https://docs.google.com/spreadsheets/d/1ABC.../edit`
- Bot tự động nhận diện và lấy tên sheet

**Cách B - Tên Sheet (Cách cũ):**
- Nhập tên sheet chính xác: `HoatDongCuaToi`

### Bước 3: Nhập hoạt động
- Nhập tên hoạt động: `Học Python cơ bản`

### Bước 4: Upload hình ảnh
- Gửi **nhiều hình** liên tiếp (không giới hạn số lượng)
- Upload ảnh, video, file đều được
- Bot hiển thị tiến độ: "✅ Ảnh 1 đã upload!", "✅ Ảnh 2 đã upload!"

### Bước 5: Hoàn thành
- Gửi `xong` để kết thúc và lưu vào sheet
- Bot hiển thị tóm tắt kết quả

## 📝 Kết quả trong Google Sheet

Bot sẽ tự động tạo các cột:
- **Thời gian**: Ngày giờ thực hiện  
- **Hoạt động**: Tên hoạt động đã nhập
- **Hình ảnh**: Links ImgBB của tất cả hình đã upload (cách nhau bởi dấu phẩy)
- **Tổng hình**: Số lượng hình ảnh

## 📋 Ví dụ thực tế:

**Cách A - Sử dụng Link (Khuyến nghị):**
```
👤 User: /start
🤖 Bot: Hãy gửi tên Google Sheet hoặc link...

👤 User: https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
🤖 Bot: ✅ Đã chọn sheet: "Class Data"
🤖 Bot: Bây giờ hãy nhập tên hoạt động...

👤 User: Tham gia workshop Machine Learning  
🤖 Bot: Đã ghi nhận hoạt động, hãy gửi ảnh...

👤 User: [Upload ảnh chứng chỉ]
🤖 Bot: ✅ Ảnh 1 đã upload thành công!

👤 User: [Upload ảnh check-in]
🤖 Bot: ✅ Ảnh 2 đã upload thành công!

👤 User: xong
🤖 Bot: ✅ Hoàn thành!
🤖 Bot: 📊 Google Sheet: Class Data
🤖 Bot: 📋 Hoạt động: Tham gia workshop Machine Learning
🤖 Bot: 📸 Số ảnh: 2
🤖 Bot: 📊 Đã ghi vào Google Sheets
```

**Cách B - Sử dụng Tên Sheet:**
```
👤 User: /start
🤖 Bot: Hãy gửi tên Google Sheet hoặc link...

👤 User: HoatDongCuaToi
🤖 Bot: ✅ Đã chọn sheet: "HoatDongCuaToi"
🤖 Bot: Bây giờ hãy nhập tên hoạt động...
(Tiếp tục như trên...)
```

## 💡 Lưu ý quan trọng:

### Đối với Cách A (Link - Khuyến nghị):
- ✅ **Dễ dàng**: Chỉ cần copy-paste link
- ✅ **Không cần nhớ tên**: Bot tự lấy tên từ link
- ✅ **Ít lỗi**: Không gõ sai tên sheet
- ⚠️ **Cần chia sẻ public**: Chọn "Ai có liên kết" → "Editor"

### Đối với Cách B (Tên sheet):
- ⚠️ **Tên sheet phải chính xác** (phân biệt hoa thường)
- ⚠️ **Không được có khoảng trống thừa**
- ✅ Ví dụ đúng: `HoatDongCuaToi`
- ❌ Ví dụ sai: `hoat dong cua toi`, ` HoatDongCuaToi `
- ⚠️ **Phải chia sẻ với service account**: `botminhchung@botminhchung.iam.gserviceaccount.com`

### Chung:
- 📱 Sử dụng `/help` để xem hướng dẫn trong bot
- 🔄 Gửi `/start` để bắt đầu ghi hoạt động mới
- 🚫 Nếu gặp lỗi permission, kiểm tra lại bước chia sẻ

## 🎉 Lợi ích mới:

- 🎯 **Linh hoạt**: Hỗ trợ cả link và tên sheet
- 🔗 **Dễ chia sẻ**: Gửi link cho bạn bè là xong
- 📊 **Tổ chức tốt**: Mỗi người/nhóm có sheet riêng  
- 🤝 **Đa người dùng**: Nhiều người dùng cùng bot
- 📈 **Theo dõi**: Dễ quản lý và thống kê

## 🎉 HOÀN THÀNH!

Bot đã sẵn sàng với tính năng mới! Chỉ cần:
1. **Tạo** Google Sheet bất kỳ
2. **Chia sẻ** public (Editor) hoặc với service account
3. **Gửi link/tên** cho bot
4. **Bắt đầu** log hoạt động ngay!

---

*💡 Khuyến nghị: Sử dụng **Cách A (Link)** vì đơn giản và ít lỗi hơn!*
