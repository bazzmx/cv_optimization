import fitz
from app.infra.pdf.extractor import extract_pdf_text


def test_extract_pdf_text():

    doc = fitz.open()

    lorem_ipsum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do 
                    eiusmod tempor incididunt ut labore et dolore magna aliqua.
                    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi 
                    ut aliquip ex ea commodo consequat.
                    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore 
                    eu fugiat nulla pariatur.
                    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia 
                    deserunt mollit anim id est laborum."""

    page = doc.new_page()
    page.insert_text((50, 50), lorem_ipsum)

    pdf_bytes = doc.tobytes()

    text = extract_pdf_text(pdf_bytes)

    assert lorem_ipsum in text
