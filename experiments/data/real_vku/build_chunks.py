"""Build page-aware JSONL chunks from the manually reviewed QD1416 demo text."""

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "extracted" / "QD1416-demo.txt"
OUTPUT = ROOT / "chunks" / "QD1416-demo-corpus.jsonl"
MAX_CHARS = 700

PAGE_MARKER = re.compile(r"(?m)^===== TRANG (\d+) =====\s*$")
NEW_BLOCK = re.compile(
    r"^(?:Căn cứ\b|Theo đề nghị\b|QUYẾT ĐỊNH:?$|Điều\s+\d+\b|"
    r"Chương\s+[IVXLCDM]+\b|\d+\.\s|Nơi nhận:?$|KT\.\s|"
    r"Số:|PHÓ HIỆU TRƯỞNG$|HIỆU TRƯỞNG$)"
)


def split_long_text(text: str) -> list[str]:
    """Split only oversized blocks, preferring sentence and then word boundaries."""
    pieces = []
    remaining = text.strip()
    while len(remaining) > MAX_CHARS:
        cut = remaining.rfind(". ", 0, MAX_CHARS + 1)
        if cut < MAX_CHARS // 2:
            cut = remaining.rfind(" ", 0, MAX_CHARS + 1)
        if cut <= 0:
            cut = MAX_CHARS
        else:
            cut += 1
        pieces.append(remaining[:cut].strip())
        remaining = remaining[cut:].strip()
    if remaining:
        pieces.append(remaining)
    return pieces


def page_blocks(page_text: str) -> list[str]:
    blocks = []
    current = []

    def flush() -> None:
        if current:
            blocks.append(" ".join(current).strip())
            current.clear()

    for raw_line in page_text.splitlines():
        line = " ".join(raw_line.split())
        if not line:
            flush()
            continue
        is_heading = line.isupper() and len(line) < 120
        if current and (NEW_BLOCK.match(line) or is_heading):
            flush()
        current.append(line)
    flush()
    return [block for block in blocks if block]


def make_chunks(page_number: int, page_text: str) -> list[dict]:
    chunks = []
    current = ""

    if page_number == 1:
        # Keep the decree's identifier/date in a short, easy-to-retrieve chunk.
        blocks = page_blocks(page_text)
        chunks = [piece for block in blocks for piece in split_long_text(block)]
        chunks = [
            (
                "Thông tin số hiệu và ngày ban hành của quyết định: " + text
                if text.startswith("Số:")
                else "Tên và nội dung chính của Quy định được ban hành: " + text
                if text.startswith("QUYẾT ĐỊNH Về việc ban hành")
                else text
            )
            for text in chunks
        ]
        return [
            {
                "doc_id": f"VKU-QD1416-P{page_number:02d}-C{index:02d}",
                "text": text,
                "label": "clean",
                "scenario": "real_vku",
                "trusted_source": True,
                "source": "QD1416-demo.txt",
                "source_title": "Quyết định 1416/QĐ-ĐHVH ngày 15/06/2026",
                "page_number": page_number,
            }
            for index, text in enumerate(chunks, start=1)
        ]

    def flush() -> None:
        nonlocal current
        if current:
            chunks.append(current.strip())
            current = ""

    for block in page_blocks(page_text):
        for piece in split_long_text(block):
            candidate = f"{current}\n\n{piece}" if current else piece
            if current and len(candidate) > MAX_CHARS:
                flush()
                candidate = piece
            current = candidate
    flush()

    return [
        {
            "doc_id": f"VKU-QD1416-P{page_number:02d}-C{index:02d}",
            "text": text,
            "label": "clean",
            "scenario": "real_vku",
            "trusted_source": True,
            "source": "QD1416-demo.txt",
            "source_title": "Quyết định 1416/QĐ-ĐHVH ngày 15/06/2026",
            "page_number": page_number,
        }
        for index, text in enumerate(chunks, start=1)
    ]


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not INPUT.exists():
        raise SystemExit(f"Không tìm thấy file đầu vào: {INPUT}")

    original = INPUT.read_text(encoding="utf-8")
    markers = list(PAGE_MARKER.finditer(original))
    page_numbers = [int(match.group(1)) for match in markers]
    if page_numbers != list(range(1, 13)):
        raise SystemExit(
            "Mong đợi đúng các dấu trang từ 1 đến 12; không tạo corpus. "
            f"Đã tìm thấy: {page_numbers}"
        )

    rows = []
    for index, marker in enumerate(markers):
        start = marker.end()
        end = markers[index + 1].start() if index + 1 < len(markers) else len(original)
        rows.extend(make_chunks(page_numbers[index], original[start:end]))

    # Article 10 starts at the bottom of page 6 and continues on page 7.
    # Keep a clearly labeled combined excerpt so retrieval can answer its full list.
    rows.append(
        {
            "doc_id": "VKU-QD1416-P06-07-ARTICLE10",
            "text": (
                "Điều 10. Đối tượng được xét công nhận kết quả học tập và chuyển đổi tín chỉ: "
                "(1) Người học chuyển trường đến theo quyết định của cấp có thẩm quyền; "
                "(2) người học theo học cùng lúc hai chương trình đào tạo theo quy định; "
                "(3) người học tham gia chương trình trao đổi học thuật tại cơ sở đào tạo "
                "trong nước hoặc ngoài nước. Nội dung được tổng hợp từ trang 6–7 của QĐ1416."
            ),
            "label": "clean",
            "scenario": "real_vku",
            "trusted_source": True,
            "source": "QD1416-demo.txt",
            "source_title": "Quyết định 1416/QĐ-ĐHVH ngày 15/06/2026",
            "pages": [6, 7],
            "text_origin": "combined_excerpt_from_source_pages",
        }
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="\n") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Đã tạo {len(rows)} chunks: {OUTPUT}")
    print(f"Giới hạn: {MAX_CHARS} ký tự/chunk; mỗi chunk giữ số trang nguồn.")
    print(f"Kích thước lớn nhất: {max(len(row['text']) for row in rows)} ký tự.")


if __name__ == "__main__":
    main()
