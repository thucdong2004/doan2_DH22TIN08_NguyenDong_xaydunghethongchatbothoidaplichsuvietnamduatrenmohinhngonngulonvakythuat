# 🔧 Hướng dẫn khắc phục sự cố - Chatbot Lịch sử Việt Nam

## ⚠️ Lỗi thường gặp

### 1. Lỗi: "The process cannot access the file" khi chạy init_db.py

**Nguyên nhân:** Database đang được sử dụng bởi process khác (thường là `app.py` đang chạy)

**Giải pháp:**

#### Cách 1: Đóng app.py trước khi chạy init_db.py (Khuyên dùng)
```powershell
# 1. Đóng terminal đang chạy app.py (Ctrl+C)
# 2. Sau đó chạy:
python init_db.py --clear
```

#### Cách 2: Sử dụng script tự động
```powershell
# File này sẽ tự động đóng Python processes và recreate database
.\fix_database.bat
```

#### Cách 3: Đóng thủ công qua Task Manager
1. Mở Task Manager (Ctrl+Shift+Esc)
2. Tìm tất cả process `python.exe`
3. End Task tất cả
4. Chạy lại `python init_db.py --clear`

---

### 2. Lỗi: "ModuleNotFoundError" hoặc "No module named..."

**Nguyên nhân:** Thiếu dependencies hoặc cài đặt không đầy đủ

**Giải pháp:**
```powershell
# Cài đặt lại tất cả dependencies
pip install -r requirements.txt --upgrade

# Hoặc cài từng package bị thiếu
pip install langchain langchain-community chromadb gradio
```

---

### 3. Lỗi: "Connection to Ollama failed"

**Nguyên nhân:** Ollama chưa chạy hoặc model chưa được tải

**Giải pháp:**
```powershell
# Kiểm tra Ollama có chạy không
ollama list

# Nếu không chạy, start Ollama service
ollama serve

# Tải model (mở terminal mới)
ollama pull llama3.2

# Hoặc thử model nhẹ hơn
ollama pull tinyllama
```

---

### 4. Chatbot chạy rất chậm

**Nguyên nhân:** Model quá lớn cho máy tính hoặc thiếu RAM

**Giải pháp:**

#### Option 1: Dùng model nhỏ hơn
```powershell
# Tải model nhẹ hơn
ollama pull tinyllama

# hoặc
ollama pull phi3:mini
```

Sau đó sửa file `config.py`:
```python
OLLAMA_MODEL = "tinyllama"  # thay vì "llama3.2"
```

#### Option 2: Giảm số lượng documents retrieve
Sửa file `config.py`:
```python
TOP_K_RESULTS = 2  # giảm từ 4 xuống 2
CHUNK_SIZE = 800   # giảm từ 1000 xuống 800
```

---

### 5. Lỗi: "Port 7860 already in use"

**Nguyên nhân:** Có Gradio app khác đang chạy ở port đó

**Giải pháp:**

Sửa file `app.py`, dòng cuối cùng:
```python
demo.launch(share=False, server_port=7861)  # Đổi port
```

Hoặc tìm và đóng process đang dùng port 7860:
```powershell
netstat -ano | findstr :7860
taskkill /PID <PID_NUMBER> /F
```

---

### 6. Câu trả lời không chính xác hoặc không liên quan

**Nguyên nhân:** Thiếu dữ liệu hoặc RAG không hoạt động tốt

**Giải pháp:**

#### Thêm dữ liệu mới:
1. Tạo file `.txt` mới trong `data/vietnam_history/`
2. Copy nội dung lịch sử vào file
3. Chạy lại: `python init_db.py --clear`

#### Cải thiện prompt:
Sửa file `src/llm_chain.py`, chỉnh template trong hàm `get_prompt_template()`

#### Tăng số lượng documents:
Sửa `config.py`:
```python
TOP_K_RESULTS = 6  # tăng từ 4 lên 6
```

---

### 7. Lỗi: "Out of Memory" hoặc "MemoryError"

**Nguyên nhân:** Máy tính không đủ RAM

**Giải pháp:**

1. **Dùng model nhỏ hơn** (xem phần 4)

2. **Giảm embedding batch size:**
Sửa `src/embeddings.py`:
```python
embedding_function = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    model_kwargs={'device': 'cpu'},
    encode_kwargs={
        'normalize_embeddings': False,
        'batch_size': 16  # thêm dòng này, giảm từ 32
    }
)
```

3. **Giảm chunk size:** (xem phần 4)

---

### 8. Database bị corrupt hoặc lỗi lạ

**Giải pháp:** Xóa và tạo lại database

```powershell
# Cách 1: Dùng script
.\fix_database.bat

# Cách 2: Thủ công
# Đóng tất cả Python processes
# Xóa thư mục chroma_db
rmdir /s /q chroma_db

# Tạo lại
python init_db.py
```

---

## 🆘 Vẫn gặp lỗi?

Nếu các giải pháp trên không giúp được, hãy thử:

1. **Restart lại máy tính** - Đôi khi processes bị treo

2. **Kiểm tra phiên bản Python:**
```powershell
python --version  # Nên là 3.10 hoặc cao hơn
```

3. **Tạo virtual environment mới:**
```powershell
python -m venv venv_new
.\venv_new\Scripts\activate
pip install -r requirements.txt
```

4. **Kiểm tra logs** (nếu có):
```powershell
# Xem file logs để biết lỗi chi tiết
type logs\chatbot.log
```

---

## 📊 Performance Tuning

### Để chatbot chạy nhanh nhất:

1. **Model:** `tinyllama` hoặc `phi3:mini`
2. **TOP_K_RESULTS:** 2-3
3. **CHUNK_SIZE:** 800
4. **Temperature:** 0.2 (giảm creativity, tăng tốc độ)

### Để chatbot chính xác nhất:

1. **Model:** `llama3.2` hoặc `mistral`
2. **TOP_K_RESULTS:** 5-6
3. **CHUNK_SIZE:** 1000-1200
4. **Temperature:** 0.3-0.5
5. **Thêm nhiều dữ liệu training**

---

## ✅ Best Practices

1. **Luôn đóng app.py trước khi chạy init_db.py**
2. **Backup thư mục `data/` thường xuyên**
3. **Không xóa `chroma_db/` khi app đang chạy**
4. **Dùng virtual environment để tránh conflict dependencies**
5. **Update Ollama và models thường xuyên**

```powershell
# Update Ollama
ollama pull llama3.2  # Pull latest version
```
