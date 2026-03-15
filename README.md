# 🇻🇳 Chatbot Lịch sử Việt Nam - Hệ thống RAG

Hệ thống chatbot hỏi đáp về Lịch sử Việt Nam sử dụng **Retrieval-Augmented Generation (RAG)** với **Ollama** (LLM chạy local miễn phí).

## ✨ Tính năng

- 📚 Trả lời câu hỏi về lịch sử Việt Nam dựa trên cơ sở tri thức
- 🔍 Trích xuất thông tin từ tài liệu và trích dẫn nguồn
- 💻 Chạy hoàn toàn local, không cần API key
- 🎨 Giao diện **Streamlit** thân thiện và dễ sử dụng

## 📋 Yêu cầu hệ thống

1. **Python 3.10 trở lên**
2. **Ollama** đã cài đặt (tải tại [ollama.com](https://ollama.com))
3. Khoảng **4GB RAM** trở lên

## 🚀 Cài đặt và chạy

### Cách 1: Chạy nhanh bằng file `.bat` (khuyên dùng)

Chỉ cần nhấn đúp vào file `run_chatbot.bat` — sẽ tự động cài thư viện, khởi tạo database và chạy chatbot.

### Cách 2: Chạy thủ công từng bước

#### Bước 1: Cài đặt Ollama và tải model

```powershell
# Tải và cài đặt Ollama từ https://ollama.com

# Sau khi cài đặt, mở terminal và chạy:
ollama pull llama3.2
```

#### Bước 2: Cài đặt thư viện Python

```powershell
pip install -r requirements.txt
```

#### Bước 3: Khởi tạo cơ sở dữ liệu vector (ChromaDB)

```powershell
python init_db.py
```

> **Lưu ý:** Lần chạy đầu sẽ tải model embedding (~100MB), có thể mất vài phút.

#### Bước 4: Chạy ứng dụng

```powershell
streamlit run app.py
```

Trình duyệt sẽ tự động mở tại: **http://localhost:8501**

### Cách 3: Chạy demo đầy đủ (kiểm tra + chatbot)

```powershell
demo.bat
```

File `demo.bat` sẽ lần lượt: kiểm tra Ollama → khởi tạo database → chạy test tự động → khởi chạy chatbot.

## 💡 Sử dụng

1. Truy cập **http://localhost:8501** sau khi chạy `app.py`
2. Nhập câu hỏi về lịch sử Việt Nam vào ô chat
3. Hệ thống sẽ tìm kiếm trong cơ sở tri thức và trả lời kèm nguồn tài liệu

### Ví dụ câu hỏi:

- "Chiến thắng Điện Biên Phủ diễn ra năm nào?"
- "Ai là người lãnh đạo khởi nghĩa Lam Sơn?"
- "Kể tên các vua triều Nguyễn"
- "Võ Nguyên Giáp là ai?"

## 📁 Cấu trúc dự án

```
├── app.py                  # Ứng dụng Streamlit (giao diện chatbot)
├── config.py               # Cấu hình hệ thống
├── init_db.py              # Script khởi tạo cơ sở dữ liệu vector
├── requirements.txt        # Danh sách thư viện Python
├── run_chatbot.bat          # Script chạy nhanh
├── demo.bat                # Script demo đầy đủ
├── src/
│   ├── document_loader.py  # Tải và xử lý tài liệu
│   ├── embeddings.py       # Tạo embeddings
│   ├── vector_store.py     # Quản lý ChromaDB
│   ├── retriever.py        # Truy xuất tài liệu liên quan
│   └── llm_chain.py        # Chuỗi xử lý LLM (RAG pipeline)
├── data/vietnam_history/   # Dữ liệu lịch sử (43 file Markdown)
│   ├── chronology/         # 15 file theo dòng thời gian (Văn Lang → Đổi Mới)
│   └── entities/           # 28 file nhân vật & sự kiện lịch sử
└── chroma_db/              # Cơ sở dữ liệu vector (tự động tạo)
```

## 🔧 Cấu hình

Chỉnh sửa file `config.py` để thay đổi:

| Tham số | Mặc định | Mô tả |
|---|---|---|
| `OLLAMA_MODEL` | `llama3.2` | Model LLM sử dụng |
| `EMBEDDING_MODEL` | `paraphrase-multilingual-MiniLM-L12-v2` | Model embedding đa ngôn ngữ |
| `TOP_K_RESULTS` | `8` | Số tài liệu truy xuất |
| `CHUNK_SIZE` | `500` | Kích thước chunk tài liệu |
| `MAX_QUESTIONS_PER_SESSION` | `20` | Giới hạn câu hỏi mỗi phiên |
| `RATE_LIMIT_SECONDS` | `10` | Thời gian chờ giữa các câu hỏi |

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

**Nếu database bị lỗi:**
```powershell
fix_database.bat
```

## 📝 Ghi chú

- Database vector được lưu trong thư mục `chroma_db/`
- Để cập nhật kiến thức, thêm file `.txt` mới vào `data/vietnam_history/` và chạy lại `python init_db.py`
