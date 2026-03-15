import os
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.retriever import retrieve_documents
from config import OLLAMA_MODEL, OLLAMA_BASE_URL

# Prompt — strict: CHỈ dùng context, không suy đoán, không dùng kiến thức ngoài
PROMPT_TEMPLATE = """Bạn là chatbot chuyên trả lời câu hỏi về lịch sử Việt Nam.

Nhiệm vụ của bạn là trả lời câu hỏi CHỈ dựa trên thông tin trong CONTEXT được cung cấp.

Quy tắc bắt buộc:
1. Chỉ sử dụng thông tin trong CONTEXT.
2. Không sử dụng kiến thức bên ngoài.
3. Không suy đoán hoặc tạo thêm thông tin.
4. Nếu CONTEXT không chứa câu trả lời, hãy trả lời:
   "Câu hỏi này không thuộc phạm vi dữ liệu của hệ thống. Chatbot chỉ hỗ trợ trả lời các câu hỏi liên quan đến lịch sử Việt Nam dựa trên cơ sở dữ liệu đã được cung cấp."
5. Nếu có nhiều thông tin liên quan, hãy chọn thông tin chính xác nhất.
6. Trả lời rõ ràng, ngắn gọn và đúng sự kiện lịch sử (nêu năm hoặc nhân vật nếu có).

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:"""


def get_llm():
    """
    Initialize Ollama LLM with temperature=0 for deterministic, factual answers
    """
    llm = OllamaLLM(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0,  # Zero temperature for maximum determinism — no randomness
    )
    return llm


def get_prompt_template():
    """
    Get the strict prompt template
    """
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )
    return prompt


def format_context(docs_with_scores):
    """
    Format retrieved documents into a context string.
    """
    if not docs_with_scores:
        return ""
    return "\n\n---\n\n".join(doc.page_content for doc, score in docs_with_scores)


def ask_question(question):
    """
    Full RAG pipeline:
    1. Retrieve relevant documents
    2. Build context from top chunks
    3. Send to LLM with strict prompt
    4. Return answer + source documents

    Returns:
        tuple: (answer_text, docs_with_scores, context_text)
    """
    # Step 1: Retrieve
    docs_with_scores = retrieve_documents(question)

    # Step 2: Build context
    context_text = format_context(docs_with_scores)

    # Debug: print context sent to LLM
    print(f"\n📝 [LLM] Context length: {len(context_text)} chars")
    if context_text:
        preview = context_text[:200].replace('\n', ' ')
        print(f"📝 [LLM] Context preview: {preview}...")
    else:
        print("📝 [LLM] Context is EMPTY — will return fallback answer")

    # Step 3: If no relevant context, return fallback immediately
    if not context_text:
        fallback = "Câu hỏi này không thuộc phạm vi dữ liệu của hệ thống. Chatbot chỉ hỗ trợ trả lời các câu hỏi liên quan đến lịch sử Việt Nam dựa trên cơ sở dữ liệu đã được cung cấp."
        return fallback, docs_with_scores, context_text

    # Step 4: Send to LLM
    llm = get_llm()
    prompt = get_prompt_template()

    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({
        "context": context_text,
        "question": question
    })

    print(f"✅ [LLM] Answer: {answer[:200]}")

    return answer, docs_with_scores, context_text
