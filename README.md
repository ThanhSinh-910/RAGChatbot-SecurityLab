# RAGChatbot – Nghiên cứu Data Poisoning trên RAG & Cơ chế Giám sát An toàn

Dự án gồm chatbot RAG tra cứu Quyết định 1416/QĐ-ĐHVH của VKU và bộ thử nghiệm cục bộ đánh giá tấn công Data Poisoning (A1, A3) cùng các cơ chế phòng thủ (D1, D2, D3).

**Lớp học phần:** Bảo mật & An toàn HTTT (4) – VKU  
**Nhóm thực hiện:** A10

| Thành viên | MSSV | Phân công |
|---|---|---|
| Nguyễn Văn Tài | 23IT.EB087 | Trưởng nhóm: Pipeline, A1, D2 |
| Phùng Đức Tài | 23IT.B193 | Embedding, Top-k, A2, D1 |
| Nguyễn Thành Sinh | 23IT.B188 | Data Ingestion, A3, D3, Demo UI |
| Võ Văn Tài | 23IT.B194 | LLM connection, Baseline, ASR/TPR/FPR |

> 🤖 **Dành cho thành viên dùng Antigravity:** Xem file hướng dẫn và mẫu prompt chi tiết tại: [HUONG_DAN_CHO_NHOM_ANTIGRAVITY.md](HUONG_DAN_CHO_NHOM_ANTIGRAVITY.md)

---

## ⚡ Cài đặt nhanh (Dành cho thành viên mới)

### Cách 1: Dùng script tự động (Khuyến nghị)

1. Mở thư mục dự án `RAGChatbot-main`
2. Nhấp đúp chuột vào file **`setup.bat`**
3. Script sẽ tự động:
   - Tạo virtual environment (`.venv`)
   - Cài tất cả thư viện cần thiết
   - Hướng dẫn cấu hình API key
   - Khởi chạy ứng dụng

### Cách 2: Cài đặt thủ công (PowerShell)

```powershell
cd RAGChatbot-main
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## 🔑 Cấu hình Google Gemini API Key

> **⚠️ BẮT BUỘC** để sử dụng tính năng Chatbot trả lời bằng AI.  
> Nếu không có API key, chatbot vẫn hoạt động ở chế độ "retrieval" (chỉ truy xuất trích đoạn).

### Bước 1: Lấy API key miễn phí

1. Truy cập: https://aistudio.google.com/api-keys
2. Đăng nhập bằng tài khoản Google
3. Nhấn **"Create API key"** → Chọn project → **Copy key**

### Bước 2: Tạo file `.env`

1. Sao chép file `.env.example` → đổi tên thành `.env`
2. Mở file `.env` bằng Notepad
3. Thay `your_google_api_key_here` bằng API key vừa copy

```
GOOGLE_API_KEY=AIzaSy...key_cua_ban...
RAG_EXPERIMENT_MODEL=gemini-2.0-flash-lite
```

> **🔒 LƯU Ý BẢO MẬT:**
> - File `.env` **KHÔNG** được commit lên Git (đã có trong `.gitignore`)
> - **Không** chia sẻ API key qua chat, email hay bất kỳ đâu
> - Mỗi thành viên tự tạo API key và file `.env` riêng

---

## 🚀 Chạy ứng dụng

```powershell
.\.venv\Scripts\streamlit.exe run web.py
```

Truy cập: **http://localhost:8501**

Ứng dụng có 3 chế độ:
- **💬 Chatbot Tra cứu QĐ1416** — Hỏi đáp quy định VKU
- **🧪 Phòng Thí nghiệm** — Mô phỏng tấn công A1/A3 và phòng thủ D2/D3
- **📊 Dashboard** — Báo cáo tổng hợp kết quả đồ án

---

## Phạm vi dữ liệu

- **Corpus Demo** (66 chunks, trang 1–12): Quy chế cốt lõi
- **Corpus Toàn văn** (104 chunks, trang 1–27): Đầy đủ kèm Phụ lục Ngoại ngữ, Tin học
- Bộ câu hỏi gồm 18 câu tại `experiments/data/real_vku/questions.csv`
- Chỉ mục FAISS sẽ tự động build lần đầu chạy (mất khoảng 1–2 phút)

## Chạy thử nghiệm

### Đánh giá Retrieval cơ bản (18 câu, không cần Gemini API)

```powershell
.\.venv\Scripts\python.exe experiments\data\real_vku\run_qa.py
```

### Sinh câu trả lời bằng Gemini

```powershell
.\.venv\Scripts\python.exe experiments\data\real_vku\run_qa.py --generate
```

### Thử nghiệm A1 + D2

```powershell
.\.venv\Scripts\python.exe experiments\data\real_vku\run_a1.py --scenario A1 --defense D2 --all-questions --top-k 5
```

### Thử nghiệm A3 + D3 (Nguyễn Thành Sinh)

```powershell
# A3 không phòng thủ — trên corpus toàn văn
.\.venv\Scripts\python.exe experiments\data\real_vku\run_a3.py --defense none --corpus full

# A3 + D3 — phòng thủ 3 tầng
.\.venv\Scripts\python.exe experiments\data\real_vku\run_a3.py --defense D3 --corpus full
```

Kết quả CSV lưu tại `experiments/data/real_vku/results/`.

---

## Cấu trúc dự án

```
RAGChatbot-main/
├── web.py                  # Giao diện Streamlit (3 chế độ)
├── rag.py                  # Pipeline RAG (FAISS + embedding)
├── app.py                  # Entry point gốc
├── requirements.txt        # Danh sách thư viện
├── setup.bat               # Script cài đặt tự động
├── .env.example            # Mẫu cấu hình môi trường
├── .gitignore              # Loại trừ .env, .venv, cache
│
├── experiments/data/real_vku/
│   ├── chunks/             # Corpus JSONL (demo + full)
│   ├── attacks/A3/         # File tấn công A3 (HTML poison)
│   ├── defense_d3.py       # Module phòng thủ D3 (3 tầng)
│   ├── run_qa.py           # Đánh giá retrieval baseline
│   ├── run_a1.py           # Thử nghiệm A1 + D2
│   ├── run_a3.py           # Thử nghiệm A3 + D3
│   ├── build_full_corpus.py# Build corpus toàn văn 27 trang
│   ├── questions.csv       # 18 câu hỏi + đáp án chuẩn
│   └── results/            # Kết quả CSV
│
└── .rag_index/             # FAISS indexes (tự động tạo)
```

## Cộng tác qua GitHub

1. Tạo repository **Private** cho nhóm
2. Mỗi người tạo nhánh riêng: `feature/a2`, `feature/d1`, v.v.
3. Commit, push rồi tạo Pull Request để nhóm review
4. Tránh nhiều người sửa cùng một file CSV kết quả

## Ghi chú

- Embedding model (`paraphrase-multilingual-MiniLM-L12-v2`) tải từ Hugging Face lần đầu (~500MB), sau đó cached tại `~/.cache/huggingface/`
- Script OCR (`ocr_scanned_pdfs.py`) cần thêm PyMuPDF, pytesseract, Pillow — không cần cho chatbot thường
- Python tối thiểu: 3.11+ (đã test trên 3.13.7)
