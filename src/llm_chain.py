from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.retriever import get_retriever
from config import OLLAMA_MODEL, OLLAMA_BASE_URL

def get_llm():
    """
    Initialize Ollama LLM
    """
    llm = Ollama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0.3  # Lower temperature for more factual answers
    )
    return llm

def get_prompt_template():
    """
    Get prompt template for Vietnamese history
    """
    template = """
Bạn là một chuyên gia về Lịch sử Việt Nam, am hiểu sâu sắc về các triều đại, sự kiện và nhân vật lịch sử.

QUAN TRỌNG - Quy tắc trả lời:
1. ĐỌC KỸ ngữ cảnh được cung cấp dưới đây TRƯỚC KHI trả lời
2. CHỈ sử dụng thông tin có trong ngữ cảnh để trả lời
3. Nếu ngữ cảnh có thông tin, PHẢI trả lời dựa trên ngữ cảnh đó
4. Nếu ngữ cảnh KHÔNG có thông tin cần thiết, hãy nói rõ "Xin lỗi, tôi không tìm thấy thông tin này trong cơ sở dữ liệu"
5. TUYỆT ĐỐI KHÔNG nhầm lẫn thông tin giữa các triều đại, nhân vật, sự kiện
6. Kiểm tra kỹ năm tháng, tên người, tên triều đại trước khi trả lời
7. Trả lời ngắn gọn, chính xác, có trích dẫn cụ thể từ ngữ cảnh

Ngữ cảnh:
{context}

Câu hỏi: {question}

Trả lời (dựa trên ngữ cảnh):
"""
    prompt = PromptTemplate(
        template=template, 
        input_variables=["context", "question"]
    )
    return prompt

def format_docs(docs):
    """
    Format retrieved documents into a single string
    """
    return "\n\n".join(doc.page_content for doc in docs)

def get_qa_chain():
    """
    Build the QA chain using LCEL (LangChain Expression Language)
    """
    llm = get_llm()
    retriever = get_retriever()
    prompt = get_prompt_template()
    
    # Create the chain using LCEL
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain, retriever

