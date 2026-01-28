import gradio as gr
from src.llm_chain import get_qa_chain
import os

# Initialize QA chain
print("⏳ Initializing RAG pipeline...")
try:
    qa_chain, retriever = get_qa_chain()
    print("✅ RAG pipeline initialized successfully!")
except Exception as e:
    print(f"❌ Error initializing pipeline: {e}")
    qa_chain = None
    retriever = None

def chat_response(message, history):
    if not qa_chain:
        return "⚠️ Hệ thống chưa được khởi tạo thành công. Vui lòng kiểm tra lại cấu hình."
    
    try:
        # Get response from RAG chain
        answer = qa_chain.invoke(message)
        
        # Get source documents
        source_documents = retriever.invoke(message)
        
        # Format sources
        sources_text = "\n\n**Nguồn tham khảo:**\n"
        seen_sources = set()
        for doc in source_documents:
            source_name = os.path.basename(doc.metadata.get('source', 'Unknown'))
            if source_name not in seen_sources:
                sources_text += f"- {source_name}\n"
                seen_sources.add(source_name)
        
        return answer + sources_text
    except Exception as e:
        return f"⚠️ Có lỗi xảy ra: {str(e)}"

# Define custom CSS
custom_css = """
.gradio-container {
    font-family: 'Roboto', sans-serif;
}
.chat-message {
    font-size: 16px;
}
"""

# Create Gradio interface
with gr.Blocks(title="Chatbot Lịch sử Việt Nam") as demo:
    gr.Markdown(
        """
        # 🇻🇳 Chatbot Hỏi - Đáp Lịch sử Việt Nam
        Hệ thống sử dụng mô hình ngôn ngữ lớn (LLM) và kỹ thuật RAG để trả lời câu hỏi dựa trên dữ liệu lịch sử.
        """
    )
    
    chatbot = gr.ChatInterface(
        fn=chat_response,
        chatbot=gr.Chatbot(height=600),
        textbox=gr.Textbox(placeholder="Đặt câu hỏi về lịch sử Việt Nam (ví dụ: Chiến thắng Điện Biên Phủ năm nào?)", container=False, scale=7),
        title=None,
        description=None,
        examples=[
            "Chiến thắng Điện Biên Phủ diễn ra vào năm nào?",
            "Ai là người đọc bản Tuyên ngôn Độc lập?",
            "Trận Bạch Đằng năm 938 có ý nghĩa gì?",
            "Kể tên các triều đại phong kiến Việt Nam?"
        ],
        cache_examples=False,
    )
    
    gr.Markdown(
        """
        ---
        **Lưu ý:** Thông tin được trích xuất từ cơ sở dữ liệu có sẵn. Đôi khi mô hình có thể đưa ra thông tin chưa chính xác hoàn toàn.
        """
    )

if __name__ == "__main__":
    demo.launch(share=False, css=custom_css)
