"""
Test script cho Vietnamese History Chatbot
Kiểm tra độ chính xác của các câu trả lời
"""

from src.llm_chain import get_qa_chain
from src.retriever import get_retriever
import time

def print_separator():
    print("\n" + "="*80 + "\n")

def test_question(qa_chain, retriever, question, expected_keywords=None):
    """
    Test một câu hỏi và kiểm tra kết quả
    """
    print(f"❓ Câu hỏi: {question}")
    print("-" * 80)
    
    start_time = time.time()
    
    try:
        # Get answer
        answer = qa_chain.invoke(question)
        
        # Get sources
        source_docs = retriever.invoke(question)
        
        elapsed = time.time() - start_time
        
        print(f"✅ Trả lời ({elapsed:.2f}s):\n{answer}")
        
        # Show sources
        print("\n📚 Nguồn tài liệu được sử dụng:")
        for i, doc in enumerate(source_docs, 1):
            source = doc.metadata.get('source', 'Unknown')
            preview = doc.page_content[:150].replace('\n', ' ')
            print(f"  {i}. {source}")
            print(f"     Preview: {preview}...")
        
        # Check expected keywords if provided
        if expected_keywords:
            print("\n🔍 Kiểm tra từ khóa mong đợi:")
            for keyword in expected_keywords:
                if keyword.lower() in answer.lower():
                    print(f"  ✓ Tìm thấy: '{keyword}'")
                else:
                    print(f"  ✗ THIẾU: '{keyword}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def main():
    print("🎬 Khởi động test chatbot...")
    print_separator()
    
    # Initialize
    try:
        qa_chain, retriever = get_qa_chain()
        print("✅ RAG pipeline đã sẵn sàng!")
    except Exception as e:
        print(f"❌ Không thể khởi tạo pipeline: {e}")
        return
    
    print_separator()
    
    # Test cases về các triều đại
    test_cases = [
        {
            "question": "Nhà Trần ra đời năm nao?",
            "keywords": ["1225", "Trần", "nhà Lý"]
        },
        {
            "question": "Nhà Tiền Lê được thành lập năm nào?",
            "keywords": ["980", "Lê Hoàn", "Lê Đại Hành"]
        },
        {
            "question": "Ai là người lãnh đạo khởi nghĩa Lam Sơn?",
            "keywords": ["Lê Lợi", "1418", "1427", "Minh"]
        },
        {
            "question": "Chiến thắng Điện Biên Phủ diễn ra năm nào?",
            "keywords": ["1954", "Điện Biên Phủ"]
        },
        {
            "question": "Trận Bạch Đằng năm 938 do ai lãnh đạo?",
            "keywords": ["Ngô Quyền", "938", "Nam Hán"]
        },
        {
            "question": "Võ Nguyên Giáp là ai?",
            "keywords": ["Đại tướng", "Điện Biên Phủ"]
        },
        {
            "question": "Kể tên các vua triều Nguyễn",
            "keywords": ["Gia Long", "Minh Mạng", "Thiệu Trị", "Tự Đức"]
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 TEST CASE {i}/{len(test_cases)}")
        print_separator()
        
        result = test_question(
            qa_chain, 
            retriever, 
            test["question"],
            test.get("keywords")
        )
        
        if result:
            passed += 1
        else:
            failed += 1
        
        print_separator()
        time.sleep(1)  # Pause between tests
    
    # Summary
    print("\n" + "="*80)
    print("📊 KẾT QUẢ TEST")
    print("="*80)
    print(f"✅ Thành công: {passed}/{len(test_cases)}")
    print(f"❌ Thất bại: {failed}/{len(test_cases)}")
    print(f"📈 Tỷ lệ: {(passed/len(test_cases)*100):.1f}%")
    print("="*80)

if __name__ == "__main__":
    main()
