"""
Service functions for handling PDF processing and summarization.

Flow:
1) Read the uploaded PDF file and extract text from all pages
2) Send the concatenated text to the AI layer to produce a summary

Notes/limitations to be aware of (not handled here):
- Scanned PDFs or image-only pages may yield little/no text with `extract_text()`.
- Encrypted PDFs may require a password before reading.
- Very large PDFs could exceed model token limits; consider chunking if needed.
"""

# PDF parsing library used to open and iterate pages and extract text.
# We import lazily and raise a clear runtime error if the dependency is missing
# so the API returns a helpful message instead of a generic 500 trace.
try:
    import PyPDF2  # type: ignore
except ModuleNotFoundError as e:  # pragma: no cover
    raise RuntimeError(
        "PyPDF2 is not installed. Activate your virtual environment and run 'pip install -r backend/requirements.txt'"
    ) from e
# App's AI service responsible for turning raw text into a concise summary
from app.services.ai_service import generate_summary
from typing import Optional
from fastapi import UploadFile

async def process_pdf_file(uploaded_pdf: UploadFile) -> str:
    """
    Read an uploaded PDF and return an AI-generated summary of its contents.

    Parameters
    ----------
    uploaded_pdf : UploadFile
        The file object provided by FastAPI's file upload mechanism. Its `.file`
        attribute exposes a file-like object suitable for libraries like PyPDF2.

    Returns
    -------
    str
        The generated summary text.

    Implementation details
    ----------------------
    - Uses PyPDF2.PdfReader to iterate each page and call `extract_text()`.
    - Concatenates page texts separated by newlines.
    - Delegates summarization to `generate_summary(full_text)`.

    Edge cases (not explicitly handled here)
    ---------------------------------------
    - If a page is image-only, `extract_text()` may return None; we coerce to empty string.
    - If the PDF is encrypted, PdfReader may raise; caller should handle exceptions.
    - For very long documents, consider chunking before summarization to avoid token limits.
    """

    # Initialize the PDF reader over the uploaded file's underlying file-like object.
    reader = PyPDF2.PdfReader(uploaded_pdf.file)
    full_text = ""

    for page in reader.pages:
        # `extract_text()` may return None for non-textual (scanned) pages; default to "".
        page_text: Optional[str] = page.extract_text()
        full_text += (page_text or "") + "\n"

    # Hand off the raw text to the AI service to generate a concise summary.
    summary = generate_summary(full_text)
    return summary
