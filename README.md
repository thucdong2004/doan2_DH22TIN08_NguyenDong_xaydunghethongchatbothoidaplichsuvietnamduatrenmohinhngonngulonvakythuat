# 🇻🇳 Chatbot Lịch sử Việt Nam - Hệ thống RAG

Hệ thống chatbot hỏi đáp về Lịch sử Việt Nam sử dụng **Retrieval-Augmented Generation (RAG)** với **Ollama** (LLM chạy local miễn phí).

## ✨ Tính năng

- 📚 Trả lời câu hỏi về lịch sử Việt Nam dựa trên cơ sở tri thức
- 🔍 Trích xuất thông tin từ tài liệu và trích dẫn nguồn
- 💻 Chạy hoàn toàn local, không cần API key
- 🎨 Giao diện Gradio thân thiện và dễ sử dụng

## 📋 Yêu cầu hệ thống

1. **Python 3.10 trở lên**
2. **Ollama** đã cài đặt (tải tại [ollama.com](https://ollama.com))
3. Khoảng 4GB RAM trở lên

## 🚀 Cài đặt và chạy

### Bước 1: Cài đặt Ollama và tải model

```powershell
# Tải và cài đặt Ollama từ https://ollama.com

# Sau khi cài đặt, mở terminal và chạy:
ollama pull llama3.2
```

### Bước 2: Cài đặt thư viện Python

```powershell
cd d:\test1
pip install -r requirements.txt
```

### Bước 3: Khởi tạo cơ sở dữ liệu

```powershell
python init_db.py
```

### Bước 4: Chạy ứng dụng

```powershell
python app.py
```

Hoặc chỉ cần chạy file `run_chatbot.bat` để tự động thực hiện tất cả các bước!

## 💡 Sử dụng

1. Truy cập `http://localhost:7860` sau khi chạy `app.py`
2. Nhập câu hỏi về lịch sử Việt Nam
3. Hệ thống sẽ tìm kiếm trong cơ sở tri thức và trả lời

### Ví dụ câu hỏi:

- "Chiến thắng Điện Biên Phủ diễn ra năm nao?"
- "Ai là người lãnh đạo khởi nghĩa Lam Sơn?"
- "Kể tên các vua triều Nguyễn"
- "Võ Nguyên Giáp là ai?"

## 📁 Cấu trúc dữ liệu

Tài liệu lịch sử được lưu trong `data/vietnam_history/`:
- `cac_trieu_dai.txt` - Các triều đại phong kiến VN
- `khang_chien_chong_phap.txt` - Kháng chiến chống Pháp
- `khang_chien_chong_my.txt` - Kháng chiến chống Mỹ
- `lich_su_can_dai.txt` - Lịch sử cận đại và Đổi mới
- `cac_anh_hung_dan_toc.txt` - Các anh hùng dân tộc

## 🔧 Cấu hình

Chỉnh sửa file `config.py` để thay đổi:
- Model Ollama (mặc định: `llama3.2`)
- Kích thước chunk
- Số lượng kết quả truy xuất

## ⚠️ Khắc phục sự cố

**Nếu gặp lỗi "ModuleNotFoundError":**
```powershell
pip install -r requirements.txt --upgrade
```

**Nếu Ollama không kết nối:**
- Đảm bảo Ollama đang chạy (kiểm tra trong Task Manager)
- Thử chạy: `ollama serve` trong terminal riêng

**Nếu model chạy chậm:**
- Thử model nhỏ hơn: `ollama pull tinyllama` và sửa `OLLAMA_MODEL` trong `config.py`

## 📝 Ghi chú

- Lần chạy đầu sẽ tải model embedding (~100MB), có thể mất vài phút
- Database vector được lưu trong thư mục `chroma_db/`
- Để cập nhật kiến thức, thêm file `.txt` mới vào `data/vietnam_history/` và chạy lại `init_db.py`
