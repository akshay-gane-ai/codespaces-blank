from pypdf import PdfReader

def extract_text_from_pdf(file) -> str:
    """
    Extracts text from a PDF file.

    Args:
        file :  PDF file.
        Example: "path/to/document.pdf"

    Returns:
        str: The extracted text from the PDF.
    """
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
            text += page.extract_text() or ""
    return text