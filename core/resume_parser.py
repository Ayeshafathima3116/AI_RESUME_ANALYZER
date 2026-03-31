"""
Resume file parser — extracts raw text from PDF and DOCX files.
"""

import io
import pdfplumber
from docx import Document


def parse_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file."""
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n\n".join(text_parts)


def parse_docx(file_bytes: bytes) -> str:
    """Extract text from a DOCX file."""
    doc = Document(io.BytesIO(file_bytes))
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs)


def parse_resume(uploaded_file) -> str:
    """
    Parse an uploaded Streamlit file object.
    Auto-detects format from the file name extension.
    Returns extracted plain text.
    """
    file_bytes = uploaded_file.read()
    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        return parse_pdf(file_bytes)
    elif name.endswith(".docx"):
        return parse_docx(file_bytes)
    else:
        raise ValueError(f"Unsupported file format: {name}. Please upload a PDF or DOCX file.")
