# HƯỚNG DẪN DÀNH CHO THÀNH VIÊN NHÓM A10 KHI SỬ DỤNG ANTIGRAVITY

> **Tài liệu bàn giao nội bộ:** Đồ án Bảo mật và An toàn HTTT (4) – VKU  
> **Đề tài:** Nghiên cứu tấn công Data Poisoning trên hệ thống RAG & Cơ chế giám sát, phát hiện dữ liệu độc hại  
> **Người biên soạn:** Nguyễn Thành Sinh (MSSV: 23IT.B188)

---

## 1. TỔNG QUAN HỆ THỐNG ĐÃ HOÀN THIỆN
Dự án đã được Nguyễn Thành Sinh hoàn thiện các phần nền tảng cốt lõi:
- **Corpus toàn văn 27 trang:** 104 chunks quy chế thật QĐ 1416/QĐ-ĐHVH (`QD1416-full-corpus.jsonl`).
- **Chỉ mục vector FAISS:** Tự động build và cache tại `.rag_index/real_vku_qd1416_full/`.
- **Kịch bản tấn công A3 & Phòng thủ D3:** Đã hoàn chỉnh tại `experiments/data/real_vku/` với TPR = 100%, FPR = 0%.
- **Giao diện Web 3 chế độ (`web.py`):** Chatbot tra cứu, Phòng thí nghiệm an ninh (Security Lab), và Dashboard đồ án.
- **Tập lệnh 1-Click:** `setup.bat` (tự cài thư viện), `run.bat` (tự mở web `http://localhost:8501`).
- **Cơ chế Fallback thông minh:** Dù thành viên có API key hay không, chatbot vẫn tự động trích xuất các điều khoản quy định QĐ1416 chính xác kèm số trang, **hoàn toàn không bị lỗi/crash**.

---

## 2. CÁCH KHỞI CHẠY DỰ ÁN TRÊN MÁY BẠN

### Cách 1: Chạy tự động (Khuyến nghị cho mọi thành viên)
1. Clone hoặc tải project về máy:
   ```bash
   git clone https://github.com/ThanhSinh-910/RAGChatbot-SecurityLab.git
   cd RAGChatbot-SecurityLab
   ```
2. Nhấp đúp chuột vào file **`setup.bat`** để tự động tạo môi trường `.venv` và cài thư viện.
3. Nhấp đúp chuột vào file **`run.bat`** để khởi chạy Web UI tại `http://localhost:8501`.

### Cách 2: Cấu hình API Key (Nếu muốn dùng Gemini AI sinh câu trả lời)
- **Cách nhanh nhất:** Mở web `http://localhost:8501`, nhìn vào Sidebar bên trái có ô **"Google Gemini API Key"** ➜ Dán key của bạn vào là xong.
- **Cách lưu lâu dài:** Sao chép file `.env.example` thành file `.env` rồi điền key:
  ```env
  GOOGLE_API_KEY=your_key_here
  RAG_EXPERIMENT_MODEL=gemini-3.5-flash
  ```
  *(Lấy key miễn phí tại: https://aistudio.google.com/api-keys)*

---

## 3. PROMPT MẪU DÀNH CHO CÁC THÀNH VIÊN KHI NHỜ ANTIGRAVITY

Khi mở Antigravity trên máy của bạn, hãy **sao chép đúng prompt tương ứng với tên của bạn** dưới đây và gửi cho Antigravity:

---

### 🔹 Prompt dành cho NGUYỄN VĂN TÀI (Trưởng nhóm - Pipeline, A1, D2):
```text
Chào Antigravity, tôi là Nguyễn Văn Tài (MSSV: 23IT.EB087), trưởng nhóm A10 đồ án môn Bảo mật và An toàn HTTT (4) tại VKU.
Dự án của nhóm tôi nghiên cứu Data Poisoning trên RAG tra cứu QĐ 1416/QĐ-ĐHVH.
Thành viên Nguyễn Thành Sinh đã hoàn thiện kho dữ liệu toàn văn 27 trang (104 chunks), kịch bản A3, phòng thủ D3 và giao diện web 3 chế độ (web.py).

Nhiệm vụ của tôi là hoàn thiện kịch bản tấn công A1 (chèn dữ liệu sai lệch làm tròn điểm) và phòng thủ D2 (đối chiếu Claim Registry).
Hãy giúp tôi:
1. Đọc kỹ file README.md, experiments/data/real_vku/run_a1.py và experiments/data/real_vku/attacks/A1/claim_registry.json.
2. Kiểm tra môi trường .venv hiện tại và chạy thử nghiệm A1 + D2 trên 18 câu hỏi chuẩn với các cấu hình top-k (top-k=3, top-k=5).
3. Hướng dẫn tôi mở rộng ma trận poison (1/3/5 tài liệu độc) và kiểm tra khả năng cô lập dữ liệu độc hại của D2.
4. Chạy web.py để tôi kiểm tra chế độ "Phòng Thí nghiệm Tấn công & Phòng thủ" xem kịch bản A1 và D2 hiển thị như thế nào.
Lưu ý: Giữ nguyên cấu trúc code và corpus toàn văn mà Sinh đã xây dựng.
```

---

### 🔹 Prompt dành cho PHÙNG ĐỨC TÀI (Embedding, Top-k, A2, D1):
```text
Chào Antigravity, tôi là Phùng Đức Tài (MSSV: 23IT.B193), thành viên nhóm A10 đồ án Bảo mật và An toàn HTTT (4) tại VKU.
Nhóm tôi đang nghiên cứu Data Poisoning trên RAG QĐ 1416. Sinh đã hoàn thiện mở rộng corpus toàn văn 27 trang và runner A3/D3.

Nhiệm vụ của tôi là:
1. Kịch bản tấn công A2: Tối ưu hóa văn bản độc hại để thao túng thứ hạng truy xuất (rank/top-k manipulation) dựa trên độ tương đồng cosine của embedding `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.
2. Cơ chế phòng thủ D1: Phát hiện bất thường vector (Vector Anomaly Detection / Outlier Detection) dựa trên khoảng cách cụm và mật độ embedding trước khi nạp vào FAISS.

Hãy giúp tôi:
1. Đọc code rag.py và experiments/data/real_vku/ để nắm cấu trúc index FAISS hiện tại.
2. Viết file runner experiments/data/real_vku/run_a2.py để đo lường độ lệch thứ hạng (Rank Shift) khi có vector độc A2.
3. Xây dựng module defense_d1.py tính toán z-score hoặc cosine distance threshold để phát hiện outlier.
4. Chạy thử nghiệm và xuất kết quả ra file CSV trong experiments/data/real_vku/results/.
```

---

### 🔹 Prompt dành cho VÕ VĂN TÀI (LLM Connection, Baseline, Đánh giá số liệu):
```text
Chào Antigravity, tôi là Võ Văn Tài (MSSV: 23IT.B194), thành viên nhóm A10 đồ án Bảo mật và An toàn HTTT (4) tại VKU.
Dự án của nhóm tôi nghiên cứu Data Poisoning trên RAG QĐ 1416. 
Hiện tại mô hình Gemini 3.5 Flash đã được kết nối thành công trong .env và web.py.

Nhiệm vụ của tôi là chủ trì đánh giá thực nghiệm:
1. Chốt tập Baseline sạch 18 câu trong experiments/data/real_vku/questions.csv (chú ý kiểm tra câu QVKU12 và QVKU17).
2. Đo lường các chỉ số an toàn hệ thống: ASR (Attack Success Rate), Retrieval Hit Rate, TPR (True Positive Rate) và FPR (False Positive Rate) trên các kịch bản A1, A3 và các cơ chế phòng thủ D2, D3.
3. Xây dựng bảng đánh giá cắt bỏ (Ablation Study) tổng hợp cho Báo cáo tiến độ Lần 3 và Báo cáo cuối kỳ.

Hãy giúp tôi:
1. Chạy run_qa.py để kiểm tra lại Recall@5 và MRR trên baseline sạch.
2. Chạy run_a3.py với 2 chế độ: `--defense none` và `--defense D3` để lấy log so sánh ASR và Detection Rate.
3. Xuất bảng tổng hợp số liệu khoa học rõ ràng để tôi đưa vào báo cáo đồ án.
```

---

### 🔹 Prompt chung (Dành cho bất kỳ thành viên nào muốn Antigravity hỗ trợ chạy ngay):
```text
Chào Antigravity, tôi là thành viên nhóm A10 đồ án Bảo mật RAG VKU.
Hãy giúp tôi kiểm tra môi trường dự án này:
1. Kích hoạt môi trường ảo .venv hoặc chạy setup.bat nếu máy tôi chưa có thư viện.
2. Kiểm tra file .env xem đã có GOOGLE_API_KEY chưa (nếu chưa, hướng dẫn tôi cấu hình hoặc chạy chế độ tra cứu trực tiếp).
3. Khởi chạy giao diện Streamlit web.py và cho tôi đường link truy cập (http://localhost:8501).
4. Hướng dẫn tôi cách thử nghiệm từng chức năng trong 3 tab của giao diện: Chatbot, Security Lab và Dashboard.
```

---

## 4. QUY TẮC CỘNG TÁC QUA GITHUB CHO NHÓM A10
1. **Không commit file `.env`:** File `.env` chứa API key cá nhân, đã được ghi vào `.gitignore` để tránh rò rỉ key.
2. **Tạo nhánh riêng khi làm việc:**
   - Nguyễn Văn Tài: nhánh `feature/a1-d2`
   - Phùng Đức Tài: nhánh `feature/a2-d1`
   - Võ Văn Tài: nhánh `feature/evaluation-ablation`
3. **Giữ nguyên các file nền tảng:** Không sửa đè `QD1416-full-corpus.jsonl` và `defense_d3.py` để đảm bảo tính nhất quán của số liệu báo cáo.
