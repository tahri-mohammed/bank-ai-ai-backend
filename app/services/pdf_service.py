import pdfplumber
import pytesseract
from pdf2image import convert_from_path


def extract_text_from_pdf(file_path: str) -> str:
    extracted_text = []

    with pdfplumber.open(file_path) as pdf:
        for page_index, page in enumerate(pdf.pages):
            text = page.extract_text()

            if text and len(text.strip()) > 50:
                extracted_text.append(text)
            else:
                images = convert_from_path(
                    file_path,
                    first_page=page_index + 1,
                    last_page=page_index + 1
                )

                for image in images:
                    ocr_text = pytesseract.image_to_string(
                        image,
                        lang="fra+ara+eng"
                    )

                    if ocr_text.strip():
                        extracted_text.append(ocr_text)

    return "\n".join(extracted_text)
