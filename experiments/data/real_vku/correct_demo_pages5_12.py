"""Apply OCR corrections checked against the QD1416 source PDF.

Only pages 5-12 are edited so any user's work on pages 1-4 is preserved.
The original file is backed up once before changes are written.
"""

from pathlib import Path
import re
import shutil
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


ROOT = Path(__file__).resolve().parent
DEMO = ROOT / "extracted" / "QD1416-demo.txt"
BACKUP = ROOT / "extracted" / "QD1416-demo.before_page5_12_corrections.bak"
MARKER = re.compile(r"(?m)^===== TRANG (\d+) =====[ \t]*\r?\n")

FIXES = {
    5: [
        ("kết quả học tập chí thực hiện", "kết quả học tập chỉ thực hiện"),
        ("một số học phân khác", "một số học phần khác"),
        ("bản gốc đề kiểm tra", "bản gốc để kiểm tra"),
    ],
    6: [
        ("đề cương chỉ tiết", "đề cương chi tiết"),
        ("gọi tăt là Hội đồng", "gọi tắt là Hội đồng"),
        ("Thành phân Hội đồng", "Thành phần Hội đồng"),
        ("phụ trách đào tạo:\r\n", "phụ trách đào tạo;\r\n"),
        ("Trưởng khoa/Tề trưởng", "Trưởng khoa/Tổ trưởng"),
        ("chât lượng giáo dục", "chất lượng giáo dục"),
        ("KT&ĐÐBCLGD", "KT&ĐBCLGD"),
        ("thành lập nhăm đảm bảo", "thành lập nhằm đảm bảo"),
        ("Hội đồng XMIH", "Hội đồng XMH"),
        ("được tô chức", "được tổ chức"),
        ("CÔNG NHẬN KÉT QUẢ HỌC TẠP VÀ CHUYÊN ĐỔI TÍN CHÍ", "CÔNG NHẬN KẾT QUẢ HỌC TẬP VÀ CHUYỂN ĐỔI TÍN CHỈ"),
        ("Người học chuyền trường", "Người học chuyển trường"),
        ("cấp có thắm quyên", "cấp có thẩm quyền"),
        ("gọi tăt là KT&ĐBCLGD", "gọi tắt là KT&ĐBCLGD"),
        ("và chuyền đổi tín chỉ", "và chuyển đổi tín chỉ"),
    ],
    7: [
        ("trao đối học thuật", "trao đổi học thuật"),
        ("ngoải nước", "ngoài nước"),
        ("chuyền đối tín chỉ", "chuyển đổi tín chỉ"),
        ("chuyền đổi tín chỉ", "chuyển đổi tín chỉ"),
        ("lớn hơn hoặc băng số tín chỉ", "lớn hơn hoặc bằng số tín chỉ"),
        ("chuyền đổi tín chỉ từ hai học phân trở lên: tông số tín chí", "chuyển đổi tín chỉ từ hai học phần trở lên: tổng số tín chỉ"),
        ("nhỏ hơn hoặc băng tông số tín chỉ của các học phân", "nhỏ hơn hoặc bằng tổng số tín chỉ của các học phần"),
        ("trung bình có trọng sô của các điểm học phân", "trung bình có trọng số của các điểm học phần"),
        ("số tín chí của các học", "số tín chỉ của các học"),
        ("quy đối về thang điểm", "quy đổi về thang điểm"),
        ("Việc quy đối do Hội đồng", "Việc quy đổi do Hội đồng"),
        ("kết quá học tập", "kết quả học tập"),
        ("Đề cương chỉ tiết", "Đề cương chi tiết"),
        ("Đại học Đà Năng", "Đại học Đà Nẵng"),
        ("cơ chê phôi hợp đào tạo (nêu có)", "cơ chế phối hợp đào tạo (nếu có)"),
        ("hoặc băng tông số tín chỉ của các học phân", "hoặc bằng tổng số tín chỉ của các học phần"),
        ("chuyền đổi tín chỉ", "chuyển đổi tín chỉ"),
        ("quy đối về thang điểm", "quy đổi về thang điểm"),
        ("tại Điều 98.", "tại Điều 8."),
    ],
    8: [
        ("các học phần găn liền", "các học phần gắn liền"),
        ("công nghệ. học thuật", "công nghệ, học thuật"),
        ("miễn thi vả công nhận", "miễn thi và công nhận"),
        ("học phần tương ứng:\r\n", "học phần tương ứng;\r\n"),
        ("điểm học phân hoặc điêm thành phân", "điểm học phần hoặc điểm thành phần"),
        ("theo kê hoạch", "theo kế hoạch"),
        ("điêm cao hơn sẽ được tính cho học phân", "điểm cao hơn sẽ được tính cho học phần"),
        ("Điêu 15. Tô chức và nhiệm vụ của Hội đồng xét công nhận điêm học phần", "Điều 15. Tổ chức và nhiệm vụ của Hội đồng xét công nhận điểm học phần"),
        ("KT&ÐĐBCLGD:", "KT&ĐBCLGD;"),
        ("có thê bô sung", "có thể bổ sung"),
        ("điểm học phân hoặc điểm thành phân", "điểm học phần hoặc điểm thành phần"),
        ("KT&ÐĐBCLGD", "KT&ĐBCLGD"),
    ],
    9: [
        ("KT&ÐBCLGD", "KT&ĐBCLGD"),
        ("kết quả thấm định", "kết quả thẩm định"),
        ("điêm học phần", "điểm học phần"),
        ("tương ứng: trường hợp cần thiết", "tương ứng; trường hợp cần thiết"),
        ("hỗ sơ cần có công văn để nghị", "hồ sơ cần có công văn đề nghị"),
        ("đề cương chỉ tiết", "đề cương chi tiết"),
    ],
    10: [
        ("cung cấp đây đủ", "cung cấp đầy đủ"),
        ("đ) Người học nộp hỗ sơ", "d) Người học nộp hồ sơ"),
        ("hỗ sơ có thể", "hồ sơ có thể"),
        ("KT&ĐÐBCLGD", "KT&ĐBCLGD"),
        ("đề cương chỉ tiết", "đề cương chi tiết"),
        ("ứng: xác minh tính xác thực", "ứng; xác minh tính xác thực"),
        ("(kế cả chứng chỉ", "(kể cả chứng chỉ"),
        ("không để xuất công nhận", "không đề xuất công nhận"),
        ("KT&@&ÐBCLGD", "KT&ĐBCLGD"),
        ("điêm học phân", "điểm học phần"),
        ("thành phân tương ứng nêu có căn cứ cho răng", "thành phần tương ứng nếu có căn cứ cho rằng"),
        ("KT&ÐBCLGD", "KT&ĐBCLGD"),
    ],
    11: [
        ("người học; phố\r\nbiến", "người học; phổ\r\nbiến"),
        ("được chuyền đổi", "được chuyển đổi"),
        ("kết quá học tập", "kết quả học tập"),
        ("điểm học phân", "điểm học phần"),
        ("đề nghị công nhận điêm học phân", "đề nghị công nhận điểm học phần"),
        ("có thể được bố sung", "có thể được bổ sung"),
        ("theo điêu kiện thực tê", "theo điều kiện thực tế"),
        ("những thay đôi", "những thay đổi"),
        ("Tắt cả các trường hợp", "Tất cả các trường hợp"),
        ("công tác chuyền đổi", "công tác chuyển đổi"),
        ("; phố\nbiến", "; phổ\nbiến"),
        ("KT&ĐÐBCLGD", "KT&ĐBCLGD"),
    ],
    12: [
        ("PHỤ LỤC 1 :", "PHỤ LỤC 1"),
        ("Xét miền học", "Xét miễn học"),
        ("học phân Pháp luật", "học phần Pháp luật"),
        ("Truyền  thông", "Truyền thông"),
        ("Loại văn bằng để xem xét được xét", "Loại văn bằng để xem xét"),
        ("Tôt nghiệp", "Tốt nghiệp"),
        ("Kinh tê chính trị", "Kinh tế chính trị"),
    ],
}


def main() -> None:
    original_bytes = DEMO.read_bytes()
    original = original_bytes.decode("utf-8")
    pages = list(MARKER.finditer(original))
    if [int(match.group(1)) for match in pages] != list(range(1, 13)):
        raise SystemExit("Expected page markers 1-12; no changes made.")

    page4_end = pages[4].start()
    protected_prefix = original[:page4_end]
    updated = original
    applied = []
    for index in range(len(pages) - 1, 3, -1):
        page_number = int(pages[index].group(1))
        start = pages[index].end()
        end = pages[index + 1].start() if index + 1 < len(pages) else len(updated)
        body = updated[start:end]
        for old, new in FIXES[page_number]:
            count = body.count(old)
            if count:
                body = body.replace(old, new)
                applied.append((page_number, old, new, count))
        if page_number == 6:
            body, count = re.subn(r"phụ trách đào tạo:[ \t]*(\r?\n)", r"phụ trách đào tạo;\1", body)
            if count:
                applied.append((6, "phụ trách đào tạo:", "phụ trách đào tạo;", count))
        if page_number == 8:
            body, count = re.subn(r"học phần tương ứng:[ \t]*(\r?\n)", r"học phần tương ứng;\1", body)
            if count:
                applied.append((8, "học phần tương ứng:", "học phần tương ứng;", count))
        if page_number == 5:
            body, count = re.subn(
                r"được phép chuyên ngành,\s*chuyền ngành",
                "được phép chuyển ngành, chuyên ngành",
                body,
            )
            if count:
                applied.append((5, "chuyên ngành, chuyền ngành", "chuyển ngành, chuyên ngành", count))
        if page_number == 7:
            body, count = re.subn(r"quy[ \t]*\r?\nđối về thang điểm", "quy đổi về thang điểm", body)
            if count:
                applied.append((7, "quy\\nđối về thang điểm", "quy đổi về thang điểm", count))
        if page_number == 11:
            body, count = re.subn(r"phố[ \t]*\r?\nbiến", "phổ biến", body)
            if count:
                applied.append((11, "phố\\nbiến", "phổ biến", count))
        updated = updated[:start] + body + updated[end:]

    if updated[:page4_end] != protected_prefix:
        raise SystemExit("Pages 1-4 preservation check failed; no changes made.")
    if not BACKUP.exists():
        shutil.copy2(DEMO, BACKUP)
    DEMO.write_bytes(updated.encode("utf-8"))
    print(f"Corrected pages 5-12 in {DEMO}")
    print(f"Pages 1-4 preserved. Backup: {BACKUP}")
    for page, old, new, count in applied:
        print(f"Page {page}: {count}x {old!r} -> {new!r}")


if __name__ == "__main__":
    main()
