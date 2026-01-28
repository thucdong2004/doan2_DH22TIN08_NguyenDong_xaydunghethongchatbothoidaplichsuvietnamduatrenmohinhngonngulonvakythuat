# BÁO CÁO ĐỀ TÀI: CHATBOT HỎI ĐÁP LỊCH SỬ VIỆT NAM SỬ DỤNG RAG VÀ LLM

## 1. Giới thiệu

### 1.1. Đặt vấn đề
Lịch sử Việt Nam có bề dày hàng nghìn năm với nhiều triều đại, sự kiện và nhân vật hào hùng. Tuy nhiên, việc tra cứu thông tin lịch sử đôi khi gặp khó khăn do dữ liệu phân tán. Mô hình ngôn ngữ lớn (LLM) có khả năng trả lời câu hỏi tốt nhưng thường thiếu kiến thức chuyên sâu hoặc cập nhật về lịch sử cụ thể của một quốc gia, dẫn đến hiện tượng "ảo giác" (hallucination).

### 1.2. Mục tiêu đề tài
Xây dựng một hệ thống chatbot có khả năng:
- Trả lời chính xác các câu hỏi về Lịch sử Việt Nam.
- Sử dụng kỹ thuật **RAG (Retrieval-Augmented Generation)** để trích xuất thông tin từ tài liệu chính thống.
- Chạy hoàn toàn **offline (local)** để đảm bảo quyền riêng tư và không phụ thuộc vào API trả phí.
- Có giao diện trực quan, dễ sử dụng.

## 2. Kiến trúc hệ thống

Hệ thống được xây dựng theo mô hình RAG tiêu chuẩn:

1.  **Dữ liệu đầu vào:** Các file văn bản (.txt) chứa thông tin về các triều đại, cuộc kháng chiến, nhân vật lịch sử.
2.  **Indexing (Đánh chỉ mục):**
    *   **Document Loader:** Đọc dữ liệu từ folder `data/`.
    *   **Text Splitter:** Chia nhỏ văn bản thành các chunks (đoạn nhỏ) kích thước 1000 ký tự.
    *   **Embeddings:** Sử dụng model `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` để chuyển văn bản thành vector.
    *   **Vector Store:** Lưu trữ vector vào ChromaDB.
3.  **Retrieval & Generation:**
    *   Người dùng đặt câu hỏi.
    *   Hệ thống tìm kiếm các chunks tương đồng nhất trong ChromaDB (Top-K retrieval).
    *   Các chunks này được đưa vào Prompt làm ngữ cảnh (Context).
    *   **LLM (Ollama - Llama 3.2)** nhận Prompt + Context và sinh câu trả lời.

## 3. Công nghệ sử dụng

*   **Ngôn ngữ lập trình:** Python 3.10+
*   **LLM Engine:** Ollama (chạy model Llama 3.2 hoặc Mistral).
*   **Framework RAG:** LangChain.
*   **Vector Database:** ChromaDB.
*   **Embeddings:** HuggingFace Embeddings (phẩm chất đa ngôn ngữ).
*   **Giao diện:** Gradio.

## 4. Kết quả thực nghiệm

### 4.1. Khả năng truy xuất (Retrieval)
Hệ thống có khả năng tìm kiếm chính xác các đoạn văn bản chứa thông tin liên quan đến câu hỏi.
*   *Ví dụ:* Hỏi về "Nhà Trần", hệ thống trích xuất được đúng đoạn văn bản về năm thành lập (1225) và các chiến công chống quân Nguyên Mông.

### 4.2. Chất lượng câu trả lời
Sau khi tinh chỉnh Prompt (Prompt Engineering), chatbot đã:
*   Bám sát ngữ cảnh document, giảm thiểu bịa đặt.
*   Trả lời đúng các câu hỏi dễ gây nhầm lẫn (ví dụ: phân biệt Nhà Lý và Nhà Trần).
*   Trích dẫn được nguồn tài liệu tham khảo.

### 4.3. Hiệu năng
*   Thời gian khởi tạo pipeline: ~1-2 giây.
*   Thời gian truy xuất: < 0.5 giây.
*   Thời gian sinh câu trả lời: 3-10 giây (tùy thuộc vào phần cứng máy tính).

## 5. Hướng phát triển

*   Mở rộng cơ sở dữ liệu với nhiều tài liệu chi tiết hơn.
*   Cải thiện giao diện Web với tính năng lưu lịch sử chat.
*   Tích hợp tính năng Speech-to-Text để hỏi bằng giọng nói.

## 6. Kết luận
Đề tài đã xây dựng thành công chatbot hỏi đáp lịch sử Việt Nam chạy local. Hệ thống hoạt động ổn định, đáp ứng được nhu cầu tra cứu thông tin cơ bản và minh họa hiệu quả việc ứng dụng kỹ thuật RAG vào bài toán thực tế.
