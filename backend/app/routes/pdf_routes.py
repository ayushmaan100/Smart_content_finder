"""
PDF-related API routes.

This module exposes endpoints for uploading a PDF and receiving an AI-generated
summary. It delegates the heavy lifting to the PDF service layer.
"""

# APIRouter is used to group routes that can be mounted in the main app with a prefix.
from fastapi import APIRouter, UploadFile, File, Depends

# Business logic for processing and summarizing PDF files lives in the service.
from app.services.pdf_service import process_pdf_file
from app.routes.auth.auth_routes import get_current_user

# Create a router instance dedicated to PDF endpoints.
router = APIRouter()

from app.db.models import Summary
from app.db.database import get_db
from uuid import uuid4
from sqlalchemy.orm import Session


@router.post("/summarize")
async def summarize_pdf(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Summarize an uploaded PDF file.

    Request:
    - Content-Type: multipart/form-data
    - Form field "file": the PDF to summarize

    Parameters:
    - file: FastAPI's UploadFile wrapper provides async file interface and metadata.
      The `File(...)` dependency marks it as a required uploaded file parameter.

    Returns:
    - JSON object with a single key "summary" containing the generated summary text.
    """
    # Delegate PDF parsing and summarization to the service layer.
    summary_text = await process_pdf_file(file)

    summary_obj = Summary(
        id=str(uuid4()),
        user_id=user["id"] if isinstance(user, dict) and "id" in user else getattr(user, "id", None),
        source_type="pdf",
        title=file.filename,
        summary_text=summary_text
    )

    db.add(summary_obj)
    db.commit()

    return {"id": summary_obj.id, "summary": summary_text}
    # Respond with a simple JSON payload for easy consumption on the   
