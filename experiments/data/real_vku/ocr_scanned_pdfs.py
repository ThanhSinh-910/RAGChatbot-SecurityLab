"""OCR scanned PDFs in source_pdfs into page-separated UTF-8 text files."""

from io import BytesIO
import os
from pathlib import Path

import fitz
import pytesseract
from PIL import Image


ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "source_pdfs"
OUTPUT_DIR = ROOT / "extracted"

# Optional: set TESSERACT_CMD to the full path to tesseract.exe if it is not on PATH.
if os.getenv("TESSERACT_CMD"):
    pytesseract.pytesseract.tesseract_cmd = os.environ["TESSERACT_CMD"]


def main() -> None:
    pdf_files = sorted(SOURCE_DIR.glob("*.pdf"))
    if not pdf_files:
        raise SystemExit(f"No PDF files found in {SOURCE_DIR}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for pdf_path in pdf_files:
        pdf = fitz.open(pdf_path)
        output_path = OUTPUT_DIR / f"{pdf_path.stem}.txt"
        with output_path.open("w", encoding="utf-8") as output:
            for page_number, page in enumerate(pdf, start=1):
                pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
                image = Image.open(BytesIO(pixmap.tobytes("png")))
                text = pytesseract.image_to_string(
                    image,
                    lang="vie+eng",
                    config="--psm 6",
                )
                output.write(f"\n\n===== TRANG {page_number} =====\n{text}")
        print(f"OCR complete: {len(pdf)} pages -> {output_path}")


if __name__ == "__main__":
    main()
