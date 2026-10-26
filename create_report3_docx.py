"""Script tạo tệp Word Báo cáo tiến độ Lần 3 chuẩn đẹp cho Nhóm A10."""
import sys
import os
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn


def set_cell_background(cell, hex_color: str):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def format_table_header(row, col_widths, hex_color="1F4E79"):
    for idx, cell in enumerate(row.cells):
        cell.width = col_widths[idx]
        set_cell_background(cell, hex_color)
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(10.5)
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)


def format_table_row(row, col_widths, is_even=False, alignments=None):
    bg_color = "F7F9FB" if is_even else "FFFFFF"
    for idx, cell in enumerate(row.cells):
        cell.width = col_widths[idx]
        set_cell_background(cell, bg_color)
        set_cell_margins(cell, top=90, bottom=90, left=130, right=130)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        align = alignments[idx] if alignments and idx < len(alignments) else WD_ALIGN_PARAGRAPH.LEFT
        for p in cell.paragraphs:
            p.alignment = align
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(10)
                run.font.color.rgb = RGBColor(40, 40, 40)


def create_report3():
    doc = docx.Document()

    # Căn lề chuẩn văn bản: Top=2cm, Bottom=2cm, Left=2.5cm, Right=2cm
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.79)
        section.bottom_margin = Inches(0.79)
        section.left_margin = Inches(0.98)
        section.right_margin = Inches(0.79)

    # 1. TIÊU ĐỀ ĐẦU TRANG
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst = p_inst.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO — ĐẠI HỌC ĐÀ NẴNG\nTRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ TRUYỀN THÔNG VIỆT - HÀN")
    r_inst.font.name = "Times New Roman"
    r_inst.font.size = Pt(10.5)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(31, 78, 121)

    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line.paragraph_format.space_after = Pt(14)
    r_line = p_line.add_run("-----------------------***-----------------------")
    r_line.font.name = "Times New Roman"
    r_line.font.size = Pt(10)
    r_line.font.color.rgb = RGBColor(120, 120, 120)

    # 2. TÊN BÁO CÁO
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("BÁO CÁO TIẾN ĐỘ ĐỒ ÁN")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(17)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(192, 0, 0)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub = p_sub.add_run("Lần: 3 (Từ ngày 23/10/2026 đến ngày 05/11/2026)")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(11.5)
    r_sub.font.italic = True
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(40, 40, 40)

    # 3. THÔNG TIN HỌC PHẦN & ĐỀ TÀI
    p_info = doc.add_paragraph()
    p_info.paragraph_format.space_after = Pt(4)
    p_info.paragraph_format.line_spacing = 1.25

    def add_meta_line(label, value):
        r1 = p_info.add_run(f"• {label}: ")
        r1.font.name = "Times New Roman"
        r1.font.bold = True
        r1.font.size = Pt(11)
        r2 = p_info.add_run(f"{value}\n")
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11)

    add_meta_line("Môn học / Lớp học phần", "Bảo mật và An toàn hệ thống thông tin (4)")
    add_meta_line("Tên đề tài", "Nghiên cứu tấn công Data Poisoning trên hệ thống RAG (Retrieval-Augmented Generation) và xây dựng cơ chế giám sát, phát hiện dữ liệu đầu vào độc hại")
    add_meta_line("Nhóm thực hiện", "A10")
    add_meta_line("Trưởng nhóm", "Nguyễn Văn Tài (MSSV: 23IT.EB087)")

    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(2)
    p_div.paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # MỤC 1: CÔNG VIỆC ĐÃ HOÀN THÀNH
    # -------------------------------------------------------------
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(10)
    h1.paragraph_format.space_after = Pt(4)
    r_h1 = h1.add_run("1. Công việc đã hoàn thành (trong giai đoạn Báo cáo Lần 3)")
    r_h1.font.name = "Times New Roman"
    r_h1.font.size = Pt(13)
    r_h1.font.bold = True
    r_h1.font.color.rgb = RGBColor(31, 78, 121)

    t1_headers = ["STT", "Nội dung công việc", "Người thực hiện", "Kết quả đạt được", "Ngày xong"]
    t1_widths = [Inches(0.45), Inches(2.35), Inches(1.15), Inches(2.20), Inches(0.85)]
    t1_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER]

    t1_data = [
        (
            "1",
            "Mở rộng và chuẩn hóa kho dữ liệu quy chế thật QĐ1416/QĐ-ĐHVH từ 12 trang pilot lên toàn văn 27 trang.",
            "Nguyễn Thành Sinh chủ trì; nhóm hỗ trợ",
            "Xây dựng thành công QD1416-full-corpus.jsonl (104 chunks, tăng 38 chunks so với pilot), bổ sung đầy đủ Phụ lục Ngoại ngữ, Tin học, GDTC; tạo chỉ mục FAISS riêng real_vku_qd1416_full.",
            "24/10/2026"
        ),
        (
            "2",
            "Đóng băng và chốt bộ đánh giá Baseline sạch (18 câu hỏi); khắc phục các câu hỏi tồn đọng (QVKU12, QVKU17).",
            "Võ Văn Tài, Nguyễn Văn Tài",
            "Bộ baseline đạt Recall@5 = 18/18 (100%), MRR@5 = 0,898; độ chính xác sinh đáp án sạch đạt 16/18 câu (88,9%).",
            "25/10/2026"
        ),
        (
            "3",
            "Kết nối mô hình LLM thế hệ mới (Gemini 3.5 Flash) vào pipeline sinh câu trả lời RAG qua API chính thức.",
            "Võ Văn Tài, Nguyễn Thành Sinh",
            "Tích hợp thành công SDK Gemini API với model gemini-3.5-flash; quản lý khóa an toàn qua .env và hỗ trợ nạp key động từ giao diện.",
            "26/10/2026"
        ),
        (
            "4",
            "Thiết kế và kiểm thử kịch bản tấn công A3 (Đầu độc qua bước nạp tài liệu HTML/PDF).",
            "Nguyễn Thành Sinh",
            "Tạo 3 payload kiểm thử: HTML chứa CSS ẩn (display:none, font-size:0) làm tròn điểm sai; giả mạo quy định miễn thi Ngoại ngữ (TOEIC 200) và Tin học. ASR đạt 100% khi không phòng thủ.",
            "25/10/2026"
        ),
        (
            "5",
            "Xây dựng và đánh giá thực nghiệm cơ chế phòng thủ D3 (Làm sạch & Thẩm định khi nạp - Ingestion Defense).",
            "Nguyễn Thành Sinh",
            "Hoàn thành module defense_d3.py với 3 tầng lọc: Xác thực nguồn gốc (Allowlist), Bóc tách CSS ẩn, Đối chiếu mâu thuẫn quy chế. Đạt TPR = 100% (ngăn chặn toàn bộ A3), FPR = 0%.",
            "26/10/2026"
        ),
        (
            "6",
            "Hoàn thiện thử nghiệm tấn công A1 và phòng thủ D2 trên bản sao corpus thật QĐ1416.",
            "Nguyễn Văn Tài, Võ Văn Tài",
            "Dữ liệu độc làm tròn điểm bị cô lập hoàn toàn sau tầng D2 (Claim Registry); ASR giảm về 0% ở câu mục tiêu.",
            "26/10/2026"
        ),
        (
            "7",
            "Nâng cấp toàn diện giao diện Web Demo Streamlit (web.py) thành RAG Security Lab.",
            "Nguyễn Thành Sinh",
            "Tích hợp 3 chế độ: (1) Chatbot tra cứu QĐ1416 tùy chọn 12/27 trang; (2) Phòng thí nghiệm an toàn mô phỏng trực quan A1/A3 đối chiếu D2/D3; (3) Dashboard báo cáo số liệu đồ án.",
            "26/10/2026"
        ),
        (
            "8",
            "Đóng gói hệ thống phân phối nội bộ và cơ chế chống lỗi tự động cho nhóm.",
            "Nguyễn Thành Sinh",
            "Tạo kịch bản tự động 1-click setup.bat và run.bat; xây dựng cơ chế Fallback thông minh giúp hệ thống vẫn tra cứu chính xác trích đoạn văn bản ngay cả khi không có API key.",
            "26/10/2026"
        ),
    ]

    table1 = doc.add_table(rows=len(t1_data) + 1, cols=len(t1_headers))
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table1)

    for i, h_text in enumerate(t1_headers):
        table1.rows[0].cells[i].text = h_text
    format_table_header(table1.rows[0], t1_widths)

    for row_idx, row_data in enumerate(t1_data):
        row = table1.rows[row_idx + 1]
        for col_idx, cell_value in enumerate(row_data):
            row.cells[col_idx].text = cell_value
        format_table_row(row, t1_widths, is_even=(row_idx % 2 == 1), alignments=t1_aligns)

    # -------------------------------------------------------------
    # MỤC 2: CÔNG VIỆC SẼ LÀM TRONG THỜI GIAN TỚI
    # -------------------------------------------------------------
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(4)
    r_h2 = h2.add_run("2. Công việc sẽ làm trong thời gian tới (Kế hoạch Giai đoạn cuối: 06/11 – 02/12)")
    r_h2.font.name = "Times New Roman"
    r_h2.font.size = Pt(13)
    r_h2.font.bold = True
    r_h2.font.color.rgb = RGBColor(31, 78, 121)

    t2_headers = ["STT", "Nội dung công việc", "Người phụ trách", "Kết quả cần có", "Hạn"]
    t2_widths = [Inches(0.45), Inches(2.35), Inches(1.20), Inches(2.15), Inches(0.85)]
    t2_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER]

    t2_data = [
        ("1", "Cài đặt và đo lường kịch bản tấn công A2 (Thao túng thứ hạng truy xuất top-k) trên dữ liệu thật.", "Phùng Đức Tài", "Script tấn công A2, bảng đo độ lệch cosine và tỷ lệ can thiệp top-k.", "08/11/2026"),
        ("2", "Cài đặt cơ chế phòng thủ D1 (Phát hiện vector bất thường) và tinh chỉnh ngưỡng khoảng cách/mật độ.", "Phùng Đức Tài", "Module D1 chạy độc lập, bảng chỉ số TPR và FPR của D1.", "11/11/2026"),
        ("3", "Tích hợp toàn diện pipeline phòng thủ đa tầng (D1 + D2 + D3) và tiến hành đánh giá cắt bỏ (Ablation Study).", "Cả nhóm (Võ Văn Tài & Nguyễn Văn Tài chủ trì)", "Ma trận kết quả tổng hợp: ASR, TPR, FPR khi chạy đơn lẻ và khi kết hợp đa tầng phòng thủ.", "15/11/2026"),
        ("4", "Tổ chức vòng thử nghiệm chéo Red-team / Blue-team nội bộ giữa các thành viên.", "Cả nhóm", "Báo cáo kiểm thử chéo, danh sách kịch bản tấn công thích ứng (adaptive attacks).", "18/11/2026"),
        ("5", "Quay video clip demo trực quan (thời lượng 3–5 phút) trên nền tảng RAG Security Lab đã xây dựng.", "Nguyễn Thành Sinh phụ trách kịch bản & quay", "Video minh chứng hoàn chỉnh (MP4 Full HD), kịch bản demo rõ ràng.", "22/11/2026"),
        ("6", "Tổng hợp toàn bộ số liệu, viết Báo cáo tổng kết đồ án, thiết kế Slide thuyết trình và tập dượt.", "Cả nhóm (Nguyễn Văn Tài điều phối)", "Báo cáo đồ án hoàn chỉnh (Word/PDF), Slide bảo vệ (PowerPoint), sẵn sàng bảo vệ cuối kỳ.", "02/12/2026"),
    ]

    table2 = doc.add_table(rows=len(t2_data) + 1, cols=len(t2_headers))
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table2)

    for i, h_text in enumerate(t2_headers):
        table2.rows[0].cells[i].text = h_text
    format_table_header(table2.rows[0], t2_widths)

    for row_idx, row_data in enumerate(t2_data):
        row = table2.rows[row_idx + 1]
        for col_idx, cell_value in enumerate(row_data):
            row.cells[col_idx].text = cell_value
        format_table_row(row, t2_widths, is_even=(row_idx % 2 == 1), alignments=t2_aligns)

    # -------------------------------------------------------------
    # MỤC 3: TIẾN ĐỘ CHUNG
    # -------------------------------------------------------------
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(4)
    r_h3 = h3.add_run("3. Tiến độ chung của đồ án")
    r_h3.font.name = "Times New Roman"
    r_h3.font.size = Pt(13)
    r_h3.font.bold = True
    r_h3.font.color.rgb = RGBColor(31, 78, 121)

    t3_headers = ["Hạng mục", "Tỉ trọng (%)", "Đã xong (%)", "Ghi chú so với Báo cáo lần 2"]
    t3_widths = [Inches(2.50), Inches(0.95), Inches(0.95), Inches(2.60)]
    t3_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]

    t3_data = [
        ("Nghiên cứu nền tảng và mô hình mối đe dọa", "10", "100", "Hoàn tất đầy đủ lý thuyết PoisonedRAG, MITRE ATLAS, OWASP LLM."),
        ("Xây dựng RAG baseline & Corpus dữ liệu thật", "20", "100", "Vượt tiến độ: Đã mở rộng 27 trang toàn văn (104 chunks), Recall@5 = 100%."),
        ("Thực nghiệm các kịch bản tấn công (A1, A2, A3)", "20", "80", "A1 và A3 đã hoàn thành thực nghiệm trên dữ liệu thật; đang hoàn thiện A2."),
        ("Xây dựng các cơ chế phòng thủ (D1, D2, D3)", "20", "75", "D2 và D3 đã hoàn thành với hiệu quả cao (TPR 100%); đang tích hợp D1."),
        ("Đánh giá tổng hợp, Ablation & Thử nghiệm chéo", "15", "30", "Đã có số liệu đơn lẻ của A1+D2, A3+D3; chuẩn bị chạy ma trận tích hợp."),
        ("Giao diện Demo, Báo cáo & Slide thuyết trình", "15", "75", "Vượt tiến độ: Web Streamlit 3 chế độ chạy tốt; đã có báo cáo chi tiết từng phần."),
    ]

    table3 = doc.add_table(rows=len(t3_data) + 1, cols=len(t3_headers))
    table3.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table3)

    for i, h_text in enumerate(t3_headers):
        table3.rows[0].cells[i].text = h_text
    format_table_header(table3.rows[0], t3_widths)

    for row_idx, row_data in enumerate(t3_data):
        row = table3.rows[row_idx + 1]
        for col_idx, cell_value in enumerate(row_data):
            row.cells[col_idx].text = cell_value
        format_table_row(row, t3_widths, is_even=(row_idx % 2 == 1), alignments=t3_aligns)

    p_prog = doc.add_paragraph()
    p_prog.paragraph_format.space_before = Pt(6)
    p_prog.paragraph_format.space_after = Pt(8)
    r_p1 = p_prog.add_run("Tiến độ tổng cộng: ")
    r_p1.font.name = "Times New Roman"
    r_p1.font.bold = True
    r_p1.font.size = Pt(11)
    r_p2 = p_prog.add_run("78 %  ")
    r_p2.font.name = "Times New Roman"
    r_p2.font.bold = True
    r_p2.font.size = Pt(12)
    r_p2.font.color.rgb = RGBColor(192, 0, 0)
    r_p3 = p_prog.add_run("(Lần 1: 25% | Lần 2: 52% | Mục tiêu đề ra: 70–75% — Đạt và vượt kế hoạch)")
    r_p3.font.name = "Times New Roman"
    r_p3.font.italic = True
    r_p3.font.size = Pt(10.5)

    # -------------------------------------------------------------
    # MỤC 4: MỨC ĐỘ ĐÓNG GÓP CỦA THÀNH VIÊN (ĐÃ BỎ CỘT ĐÁNH GIÁ)
    # -------------------------------------------------------------
    h4 = doc.add_paragraph()
    h4.paragraph_format.space_before = Pt(14)
    h4.paragraph_format.space_after = Pt(4)
    r_h4 = h4.add_run("4. Mức độ đóng góp của thành viên (Tính đến thời điểm báo cáo Lần 3)")
    r_h4.font.name = "Times New Roman"
    r_h4.font.size = Pt(13)
    r_h4.font.bold = True
    r_h4.font.color.rgb = RGBColor(31, 78, 121)

    t4_headers = ["STT", "MSSV", "Họ và tên", "Công việc chính", "Đóng góp (%)", "Ghi chú"]
    t4_widths = [Inches(0.45), Inches(1.00), Inches(1.25), Inches(2.40), Inches(0.90), Inches(1.00)]
    t4_aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]

    t4_data = [
        ("1", "23IT.EB087", "Nguyễn Văn Tài", "Trưởng nhóm: Điều phối dự án, chuẩn hóa pipeline, hoàn thiện runner A1, kiểm thử D2 trên bản sao corpus QĐ1416.", "25", "Phụ trách tiếp: tích hợp pipeline đa tầng, điều phối báo cáo cuối kỳ"),
        ("2", "23IT.B193", "Phùng Đức Tài", "Phụ trách phân tích không gian vector, nghiên cứu module phát hiện bất thường D1 và chuẩn bị kịch bản A2.", "25", "Phụ trách tiếp: hoàn thiện thực nghiệm A2 và module phòng thủ D1"),
        ("3", "23IT.B188", "Nguyễn Thành Sinh", "Chủ trì mở rộng kho dữ liệu 27 trang (104 chunks); kịch bản tấn công A3; module phòng thủ D3 (TPR 100%, FPR 0%); giao diện Web Security Lab; kịch bản tự động setup.bat/run.bat.", "25", "Phụ trách tiếp: hỗ trợ kiểm thử đa tầng, chuẩn bị kịch bản và quay video demo"),
        ("4", "23IT.B194", "Võ Văn Tài", "Phụ trách đo lường baseline 18 câu; tích hợp LLM Gemini 3.5 Flash; chuẩn hóa rubric đáp án và kiểm tra độc lập các chỉ số ASR/TPR/FPR.", "25", "Phụ trách tiếp: chủ trì đánh giá ablation study và vòng red-team chéo"),
        ("", "", "Tổng cộng", "", "100", ""),
    ]

    table4 = doc.add_table(rows=len(t4_data) + 1, cols=len(t4_headers))
    table4.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table4)

    for i, h_text in enumerate(t4_headers):
        table4.rows[0].cells[i].text = h_text
    format_table_header(table4.rows[0], t4_widths)

    for row_idx, row_data in enumerate(t4_data):
        row = table4.rows[row_idx + 1]
        for col_idx, cell_value in enumerate(row_data):
            row.cells[col_idx].text = cell_value
        is_total = (row_idx == len(t4_data) - 1)
        format_table_row(row, t4_widths, is_even=(row_idx % 2 == 1), alignments=t4_aligns)
        if is_total:
            for cell in row.cells:
                set_cell_background(cell, "EAECEF")
                for p in cell.paragraphs:
                    for run in p.runs:
                        run.font.bold = True

    # -------------------------------------------------------------
    # MỤC 5: KHÓ KHĂN VÀ KIẾN NGHỊ
    # -------------------------------------------------------------
    h5 = doc.add_paragraph()
    h5.paragraph_format.space_before = Pt(14)
    h5.paragraph_format.space_after = Pt(4)
    r_h5 = h5.add_run("5. Khó khăn đã giải quyết và Kiến nghị")
    r_h5.font.name = "Times New Roman"
    r_h5.font.size = Pt(13)
    r_h5.font.bold = True
    r_h5.font.color.rgb = RGBColor(31, 78, 121)

    p_dif = doc.add_paragraph()
    p_dif.paragraph_format.line_spacing = 1.25
    p_dif.paragraph_format.space_after = Pt(4)
    r_d1 = p_dif.add_run("• Khó khăn đã giải quyết:\n")
    r_d1.font.bold = True
    r_d1.font.name = "Times New Roman"
    r_d1_text = (
        "  - Ban đầu corpus chỉ có 12 trang đầu nên thiếu các quy định miễn giảm chứng chỉ ngoại ngữ/tin học. "
        "Nhóm đã xử lý OCR và phân đoạn toàn văn 27 trang của QĐ 1416/QĐ-ĐHVH thành 104 chunks có metadata rõ ràng.\n"
        "  - Xử lý thành công việc kết nối với mô hình LLM mới gemini-3.5-flash và xây dựng cơ chế Fallback tự động, "
        "giúp chatbot hoạt động ổn định và trích xuất đúng ngữ cảnh kể cả khi không có kết nối internet hoặc API key.\n"
        "  - Chuẩn hóa môi trường thực thi với các tập lệnh setup.bat và run.bat giúp tất cả thành viên trong nhóm khởi chạy đồng nhất không phát sinh lỗi."
    )
    p_dif.add_run(r_d1_text).font.name = "Times New Roman"

    p_prop = doc.add_paragraph()
    p_prop.paragraph_format.line_spacing = 1.25
    p_prop.paragraph_format.space_after = Pt(14)
    r_p1 = p_prop.add_run("• Kiến nghị và Đề xuất:\n")
    r_p1.font.bold = True
    r_p1.font.name = "Times New Roman"
    r_p1_text = (
        "  - Nhóm kiến nghị giữ phạm vi thử nghiệm dữ liệu thật trên Quyết định 1416/QĐ-ĐHVH (toàn văn 27 trang) "
        "kết hợp dữ liệu độc lập do nhóm tự tạo trên bản sao cục bộ, không thử nghiệm trên môi trường trực tuyến để đảm bảo an toàn thông tin theo chuẩn đạo đức nghiên cứu.\n"
        "  - Kính mong thầy/cô góp ý thêm về ma trận kiểm thử kết hợp đa tầng phòng thủ (D1 + D2 + D3) để nhóm hoàn thiện phần thực nghiệm tổng hợp trong giai đoạn tới."
    )
    p_prop.add_run(r_p1_text).font.name = "Times New Roman"

    # CHỮ KÝ TRƯỞNG NHÓM
    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign.paragraph_format.space_before = Pt(10)
    p_sign.paragraph_format.line_spacing = 1.2

    r_date = p_sign.add_run("Đà Nẵng, ngày 27 tháng 10 năm 2026\n")
    r_date.font.name = "Times New Roman"
    r_date.font.italic = True
    r_date.font.size = Pt(11)

    r_role = p_sign.add_run("Trưởng nhóm\n")
    r_role.font.name = "Times New Roman"
    r_role.font.bold = True
    r_role.font.size = Pt(11)

    r_note = p_sign.add_run("(Ký và ghi rõ họ tên)\n\n\n\n")
    r_note.font.name = "Times New Roman"
    r_note.font.italic = True
    r_note.font.size = Pt(10)

    r_name = p_sign.add_run("Nguyễn Văn Tài")
    r_name.font.name = "Times New Roman"
    r_name.font.bold = True
    r_name.font.size = Pt(12)

    # LƯU FILE
    out_dir_1 = Path(r"c:\Users\ACER\OneDrive\Desktop\AT_BMTT\CK ATBM")
    out_file_1 = out_dir_1 / "Báo cáo tiến độ lần 3 - Nhóm A10.docx"
    doc.save(str(out_file_1))
    print(f"Đã tạo: {out_file_1}")

    out_dir_2 = Path(r"c:\Users\ACER\OneDrive\Desktop\AT_BMTT\CK ATBM\RAGChatbot-main\RAGChatbot-main")
    out_file_2 = out_dir_2 / "Bao_cao_tien_do_lan_3_nhom_A10.docx"
    doc.save(str(out_file_2))
    print(f"Đã tạo: {out_file_2}")


if __name__ == "__main__":
    create_report3()
