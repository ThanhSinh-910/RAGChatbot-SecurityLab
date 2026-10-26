"""Script kiem tra nhanh ket noi Google Gemini API cho thanh vien nhom A10."""
import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
load_dotenv()

key = os.getenv("GOOGLE_API_KEY", "").strip()

if not key or key in {"your_google_api_key_here", "DAN_API_KEY_CUA_BAN"}:
    print("[THONG BAO] Chua co GOOGLE_API_KEY trong file .env.")
    print("Ung dung web.py van hoat dong o che do tra cuu trich doan truc tiep.")
    sys.exit(0)

print(f"[1] Da tim thay API Key: {key[:8]}...{key[-5:]} (Do dai: {len(key)})")

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    model_name = os.getenv("RAG_EXPERIMENT_MODEL", "gemini-3.5-flash")
    print(f"[2] Dang ket noi toi model: {model_name}...")

    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0, google_api_key=key)
    prompt = ChatPromptTemplate.from_template("Tra loi ngan gon: {q}")
    chain = prompt | llm | StrOutputParser()

    res = chain.invoke({"q": "VKU la truong gi?"})
    print(f"[3] Ket noi THANH CONG!")
    print(f"    Phan hoi tu Gemini: {res.strip()}")
except Exception as e:
    print(f"[CANH BAO] Khong the ket noi API: {e}")
