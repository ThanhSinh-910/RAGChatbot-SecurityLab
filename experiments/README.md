# Thử nghiệm Data Poisoning trên RAG

Đọc và duyệt `../EXPERIMENT_SPEC.md` trước khi tạo dữ liệu hoặc chạy phép thử.

## Chuẩn bị dữ liệu và chạy pilot

Mở PowerShell tại thư mục gốc dự án, bảo đảm `.venv` đã kích hoạt, rồi chạy:

```powershell
$env:PYTHONIOENCODING = "utf-8"
.\.venv\Scripts\python.exe experiments\prepare_dataset.py
.\.venv\Scripts\python.exe experiments\run_experiment.py --scenario A1 --poison-count 1 --defense none --top-k 3 --query-class target --limit 2 --repeats 1 --retrieval-only
```

Lượt đầu chỉ kiểm tra truy xuất cục bộ, không gọi Gemini và không đo ASR. Sau khi nhóm duyệt dữ liệu/configuration và key API hoạt động, chạy câu trả lời thật bằng cách bỏ `--retrieval-only`; ví dụ:

```powershell
$env:GOOGLE_API_KEY = "KEY_MOI_CUA_BAN"
.\.venv\Scripts\python.exe experiments\run_experiment.py --scenario baseline --defense none --top-k 3 --query-class clean --repeats 3
.\.venv\Scripts\python.exe experiments\run_experiment.py --scenario A1 --poison-count 1 --defense none --top-k 3 --query-class target --repeats 3
```

Để thử phòng thủ, thay `--defense none` bằng `D1`, `D2`, `D3` hoặc `all`. Dùng `--scenario A2`/`A3` để chọn kịch bản khác. Đừng chạy toàn bộ ma trận trước pilot: mỗi câu hỏi lặp là một lần gọi model và có thể tiêu tốn quota.

Kết quả được thêm vào `results/results.csv` và `results/document_audit.csv`; mỗi lượt có `run_id` riêng. Chỉ số từ lượt `--retrieval-only` không đại diện cho ASR hay độ đúng câu trả lời.

- `data/clean/`: chỉ chứa corpus sạch tổng hợp.
- `data/poisoned/`: các bản corpus thử có tài liệu canary; giữ riêng theo mã kịch bản. A3 hiện thử đường nạp HTML hiển thị văn bản.
- `questions/`: câu hỏi, đáp án chuẩn, nhãn clean/target và ID ổn định.
- `results/`: log CSV thô và bảng kết quả; không lưu API key.

Không đặt dữ liệu thử vào thư mục `../data/` của chatbot hiện tại. Với mỗi cấu hình, tạo lại FAISS index từ đúng corpus đã ghi trong đặc tả.
