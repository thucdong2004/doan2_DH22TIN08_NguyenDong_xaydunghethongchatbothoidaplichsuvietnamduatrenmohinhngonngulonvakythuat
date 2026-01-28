# HƯỚNG DẪN DEMO CHATBOT LỊCH SỬ VIỆT NAM

## Chuẩn bị
1.  Đảm bảo **Ollama** đã đang chạy (`ollama serve`).
2.  Mở terminal tại thư mục dự án (`d:\test1`).
3.  Chạy script demo tự động:
    ```powershell
    demo.bat
    ```
    Script này sẽ tự động kiểm tra database, chạy test và mở giao diện web.

## Kịch bản Demo

### PHẦN 1: Giới thiệu (1 phút)
*   Mở file `REPORT.md` giới thiệu nhanh về mục tiêu và kiến trúc RAG.
*   Khoe cấu trúc thư mục `data/` chứa các file text lịch sử.

### PHẦN 2: Demo Chức năng (3 phút)
Khi giao diện Gradio hiện lên (`http://localhost:7860`), thực hiện các câu hỏi sau theo thứ tự:

**1. Hỏi về sự kiện cụ thể (Kiểm tra độ chính xác):**
*   *Câu hỏi:* `Chiến thắng Điện Biên Phủ diễn ra năm nào?`
*   *Kết quả mong đợi:* Năm 1954, nhắc đến chiến thắng lừng lẫy năm châu.

**2. Hỏi về triều đại (Kiểm tra khả năng phân biệt context):**
*   *Câu hỏi:* `Nhà Trần ra đời năm bao nhiêu?`
*   *Kết quả mong đợi:* Năm 1225 (Không được nhầm sang nhà Tiền Lê hay Lý). Có nhắc đến việc thay thế nhà Lý.

**3. Hỏi về nhân vật (Kiểm tra tổng hợp thông tin):**
*   *Câu hỏi:* `Trần Hưng Đạo có công lao gì?`
*   *Kết quả mong đợi:* 3 lần thắng quân Nguyên Mông, trận Bạch Đằng 1288.

**4. Hỏi câu hỏi KHÔNG có trong dữ liệu (Kiểm tra Hallucination):**
*   *Câu hỏi:* `Ai là tổng thống đầu tiên của Mỹ?`
*   *Kết quả mong đợi:* Chatbot nên trả lời dựa trên kiến thức có sẵn hoặc nói không biết (tùy prompt), nhưng quan trọng nhất là không được bịa ra thông tin sai lệch liên quan đến lịch sử VN.

### PHẦN 3: Giải thích kỹ thuật (Nếu được hỏi)
*   Cho xem file `src/llm_chain.py` để thấy Prompt Template đã được tối ưu.
*   Cho xem logs trong terminal để thấy các documents được retrieve về.

## Xử lý sự cố khi Demo
*   **Nếu lỗi "Connection failed":** Kiểm tra lại Ollama (`ollama list`).
*   **Nếu trả lời sai:** Nhấn nút "Retry" hoặc clear history.
*   **Nếu app không chạy:** Chạy file `fix_database.bat` để reset lại DB sạch sẽ.
