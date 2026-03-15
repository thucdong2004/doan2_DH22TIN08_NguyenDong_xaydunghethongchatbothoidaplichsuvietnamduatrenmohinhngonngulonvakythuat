import streamlit as st
import os
import time
from src.llm_chain import ask_question
from config import MAX_QUESTIONS_PER_SESSION, RATE_LIMIT_SECONDS, MAX_CONCURRENT_USERS

# Page config
st.set_page_config(
    page_title="Chatbot Lịch sử Việt Nam",
    page_icon="🇻🇳",
    layout="wide"
)

# --- Rate Limiting & Session Management ---
# Initialize session counters
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "last_question_time" not in st.session_state:
    st.session_state.last_question_time = 0

def check_rate_limit():
    """
    Check if the user can ask a question.
    Returns (allowed: bool, message: str)
    """
    # Check session question limit
    if st.session_state.question_count >= MAX_QUESTIONS_PER_SESSION:
        return False, (
            f"⚠️ Bạn đã đạt giới hạn **{MAX_QUESTIONS_PER_SESSION} câu hỏi** "
            f"cho phiên này. Vui lòng tải lại trang để bắt đầu phiên mới."
        )

    # Check cooldown between questions
    elapsed = time.time() - st.session_state.last_question_time
    if elapsed < RATE_LIMIT_SECONDS and st.session_state.last_question_time > 0:
        remaining = int(RATE_LIMIT_SECONDS - elapsed)
        return False, (
            f"⏳ Vui lòng chờ **{remaining} giây** trước khi hỏi câu tiếp theo."
        )

    return True, ""


# Chat input — must be called unconditionally every render
chat_prompt = st.chat_input("Đặt câu hỏi về lịch sử Việt Nam...")

# If user typed a question in chat input, store it and rerun
if chat_prompt:
    st.session_state["pending_question"] = chat_prompt
    st.rerun()

# Handle pending question (from sidebar button or chat input)
if "pending_question" in st.session_state:
    prompt = st.session_state.pop("pending_question")
else:
    prompt = None

# If there's a prompt, process rate limits BEFORE rendering the sidebar
allowed = True
limit_msg = ""
if prompt:
    allowed, limit_msg = check_rate_limit()
    if allowed:
        st.session_state.question_count += 1
        st.session_state.last_question_time = time.time()

# --- Sidebar ---
with st.sidebar:
    st.title("🇻🇳 Chatbot Lịch sử Việt Nam")
    st.markdown("Hệ thống sử dụng **RAG** + **LLM** để trả lời câu hỏi dựa trên dữ liệu lịch sử.")
    st.divider()

    # Session info
    remaining = MAX_QUESTIONS_PER_SESSION - st.session_state.question_count
    st.markdown(f"### 📊 Phiên hiện tại")
    st.markdown(f"- Câu hỏi đã dùng: **{st.session_state.question_count}/{MAX_QUESTIONS_PER_SESSION}**")
    st.markdown(f"- Còn lại: **{remaining}** câu hỏi")
    st.progress(st.session_state.question_count / MAX_QUESTIONS_PER_SESSION)

    st.divider()
    st.markdown("### 💡 Câu hỏi mẫu")
    example_questions = [
        "Chiến thắng Điện Biên Phủ diễn ra năm nào?",
        "Nhà Trần thành lập năm nào?",
        "Nguyễn Trãi là ai?",
        "Ai là người đọc bản Tuyên ngôn Độc lập?",
        "Hiệp định Paris được ký năm nào?",
    ]
    for q in example_questions:
        if st.button(q, key=f"ex_{q}", use_container_width=True):
            st.session_state["pending_question"] = q
            st.rerun()

    st.divider()
    st.caption(f"⚙️ Giới hạn: {MAX_QUESTIONS_PER_SESSION} câu/phiên · "
               f"{RATE_LIMIT_SECONDS}s cooldown · {MAX_CONCURRENT_USERS} user")

# --- Main area ---
st.title("🇻🇳 Chatbot Hỏi - Đáp Lịch sử Việt Nam")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("📚 Nguồn tài liệu & Chunks đã truy xuất"):
                st.markdown(message["sources"])

# Process question
if prompt:
    if not allowed:
        st.warning(limit_msg)
    else:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Đang tìm kiếm và phân tích..."):
                try:
                    answer, docs_with_scores, context_text = ask_question(prompt)

                    st.markdown(answer)

                    # Build sources display
                    sources_md = ""
                    if docs_with_scores:
                        sources_md += "**Tài liệu được truy xuất:**\n\n"
                        for i, (doc, score) in enumerate(docs_with_scores, 1):
                            source_name = os.path.basename(
                                doc.metadata.get('source', 'Unknown'))
                            sources_md += f"- **{source_name}** (Score: {score:.4f})\n"

                        sources_md += "\n---\n\n**Nội dung chunks:**\n\n"
                        for i, (doc, score) in enumerate(docs_with_scores, 1):
                            source_name = os.path.basename(
                                doc.metadata.get('source', 'Unknown'))
                            sources_md += (f"**Chunk {i}** — `{source_name}` "
                                           f"(Score: {score:.4f})\n\n")
                            sources_md += f"```\n{doc.page_content}\n```\n\n"

                        with st.expander("📚 Nguồn tài liệu & Chunks đã truy xuất"):
                            st.markdown(sources_md)
                    else:
                        sources_md = "*Không tìm thấy tài liệu liên quan.*"

                    # Save to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources_md
                    })

                except Exception as e:
                    error_msg = f"⚠️ Có lỗi xảy ra: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
