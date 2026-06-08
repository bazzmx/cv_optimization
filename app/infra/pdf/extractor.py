import fitz
from app.core.logger import logger


def extract_pdf_text(pdf_bytes: bytes) -> str:
    """Extract text from a PDF file."""
    logger.info("Extracting text from PDF")
    document = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = ""

    for page in document:
        text += page.get_text()
    logger.info("Text extraction completed")
    return text
