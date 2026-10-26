"""Extract page-separated text from PDFs in source_pdfs into extracted."""

from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "source_pdfs"
OUTPUT_DIR = ROOT / "extracted"


def main() -> None:
    pdf_files = sorted(SOURCE_DIR.glob("*.pdf"))
    if not pdf_files:
        raise SystemExit(f"No PDF files found in {SOURCE_DIR}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for pdf_path in pdf_files:
        reader = PdfReader(str(pdf_path))
        output_path = OUTPUT_DIR / f"{pdf_path.stem}.txt"
        page_texts = []
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            page_texts.append(f"\n\n===== TRANG {page_number} =====\n{text}")

        output_path.write_text("".join(page_texts), encoding="utf-8")
        nonempty_pages = sum(bool((page.extract_text() or "").strip()) for page in reader.pages)
        print(
            f"{pdf_path.name}: {len(reader.pages)} pages, "
            f"{nonempty_pages} pages with text -> {output_path}"
        )


if __name__ == "__main__":
    main()
