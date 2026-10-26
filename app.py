from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from rag import (
    format_docs,
    get_api_key,
    get_real_vku_fingerprint,
    get_real_vku_retriever,
    make_source_list,
)


SYSTEM_PROMPT = """Bạn là trợ lý tra cứu các tài liệu PDF được cung cấp.
Chỉ dùng thông tin trong phần ngữ cảnh để trả lời. Nếu tài liệu không có câu trả lời,
hãy nói rõ: 'Tôi không tìm thấy thông tin này trong tài liệu.' Không tự suy đoán.
Trả lời ngắn gọn bằng tiếng Việt và giữ lại tên riêng, con số, thời hạn chính xác.

Ngữ cảnh:
{context}"""


def main():
    api_key = get_api_key()
    retriever = get_real_vku_retriever(get_real_vku_fingerprint())
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        temperature=0,
        google_api_key=api_key,
    )
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", SYSTEM_PROMPT), ("human", "{input}")]
    )
    output_parser = StrOutputParser()

    print("Chatbot tra cứu tài liệu đã sẵn sàng. Gõ 'thoát' để kết thúc.")
    while True:
        question = input("\nBạn: ").strip()
        if question.lower() in {"thoát", "thoat", "exit", "quit"}:
            print("Tạm biệt!")
            break
        if not question:
            continue
        if question.lower() in {"xin chào", "chào", "hello", "hi"}:
            print("\nTrợ lý: Xin chào! Bạn muốn tra cứu nội dung nào trong các tài liệu PDF?")
            continue

        try:
            docs = retriever.invoke(question)
            prompt_value = prompt_template.invoke(
                {"context": format_docs(docs), "input": question}
            )
            print("\nTrợ lý: ", end="", flush=True)
            for part in output_parser.transform(llm.stream(prompt_value)):
                print(part, end="", flush=True)
            sources = make_source_list(docs)
            if sources:
                print("\n\nNguồn: " + "; ".join(sources))
            else:
                print()
        except Exception as exc:
            print(f"\nKhông thể tạo câu trả lời: {exc}")


if __name__ == "__main__":
    main()
