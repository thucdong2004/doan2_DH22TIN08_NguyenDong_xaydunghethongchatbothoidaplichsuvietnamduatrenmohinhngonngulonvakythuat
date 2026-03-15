"""
Test script cho Vietnamese History Chatbot
Kiểm tra độ chính xác của các câu trả lời
"""

from src.llm_chain import ask_question
import time


def print_separator():
    print("\n" + "=" * 80 + "\n")


def test_question(question, expected_keywords=None):
    """
    Test một câu hỏi và kiểm tra kết quả
    """
    print(f"❓ Câu hỏi: {question}")
    print("-" * 80)

    start_time = time.time()

    try:
        # Get answer + sources from the new pipeline
        answer, docs_with_scores, context_text = ask_question(question)

        elapsed = time.time() - start_time

        print(f"\n✅ Trả lời ({elapsed:.2f}s):\n{answer}")

        # Show sources
        print("\n📚 Nguồn tài liệu được sử dụng:")
        if docs_with_scores:
            for i, (doc, score) in enumerate(docs_with_scores, 1):
                import os
                source = os.path.basename(doc.metadata.get('source', 'Unknown'))
                preview = doc.page_content[:150].replace('\n', ' ')
                print(f"  {i}. {source} (score={score:.4f})")
                print(f"     Preview: {preview}...")
        else:
            print("  (Không có tài liệu liên quan)")

        # Check expected keywords if provided
        if expected_keywords:
            print("\n🔍 Kiểm tra từ khóa mong đợi:")
            all_found = True
            for keyword in expected_keywords:
                if keyword.lower() in answer.lower():
                    print(f"  ✓ Tìm thấy: '{keyword}'")
                else:
                    print(f"  ✗ THIẾU: '{keyword}'")
                    all_found = False
            return all_found

        return True

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False


def main():
    print("🎬 Khởi động test chatbot...")
    print_separator()

    # Test cases
    test_cases = [
        {
            "question": "Nhà Trần thành lập năm nào?",
            "keywords": ["1225"]
        },
        {
            "question": "Chiến thắng Điện Biên Phủ diễn ra năm nào?",
            "keywords": ["1954"]
        },
        {
            "question": "Nguyễn Trãi là ai?",
            "keywords": ["Nguyễn Trãi"]
        },
        {
            "question": "Ai là người đọc bản Tuyên ngôn Độc lập?",
            "keywords": ["Hồ Chí Minh"]
        },
        {
            "question": "Hiệp định Paris được ký năm nào?",
            "keywords": ["1973"]
        },
    ]

    passed = 0
    failed = 0

    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 TEST CASE {i}/{len(test_cases)}")
        print_separator()

        result = test_question(
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
    print("\n" + "=" * 80)
    print("📊 KẾT QUẢ TEST")
    print("=" * 80)
    print(f"✅ Thành công: {passed}/{len(test_cases)}")
    print(f"❌ Thất bại: {failed}/{len(test_cases)}")
    print(f"📈 Tỷ lệ: {(passed / len(test_cases) * 100):.1f}%")
    print("=" * 80)


if __name__ == "__main__":
    main()
