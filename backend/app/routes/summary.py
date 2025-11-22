"""Summary retrieval API routes.

Provides endpoints to list and fetch individual summary records for the
authenticated user. All routes depend on a `get_current_user` function
which should return a dict-like object containing the user's `id`.

Endpoints:
    GET /summary/list
        Returns all Summary rows belonging to the current user.
    GET /summary/{summary_id}
        Returns a single Summary by ID if it belongs to the current user,
        otherwise 404.

Security considerations:
    - Each query filters by `user_id` ensuring users cannot access others' data.
    - If `get_current_user` changes to return a Pydantic model or ORM object,
      adjust property access accordingly (e.g. user.id instead of user['id']).
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models import Summary
from app.db.database import get_db
from app.routes.auth import get_current_user
from app.services.utils import generate_flashcards, generate_mcqs


# Router is prefixed so all endpoints are mounted under /summary
router = APIRouter(prefix="/summary")

@router.get("/{summary_id}/flashcards")
def get_flashcards(summary_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.query(Summary).filter(
        Summary.id == summary_id, Summary.user_id == user["id"]
    ).first()

    if not row:
        raise HTTPException(404, "Summary not found")

    cards = generate_flashcards(row.summary_text)
    return {"flashcards": cards}



@router.get("/{summary_id}/mcqs")
def get_mcqs(summary_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.query(Summary).filter(
        Summary.id == summary_id, Summary.user_id == user["id"]
    ).first()

    if not row:
        raise HTTPException(404, "Summary not found")

    mcqs = generate_mcqs(row.summary_text)
    return {"mcqs": mcqs}



@router.get("/list")
def list_summaries(
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return all summaries belonging to the authenticated user."""
    return db.query(Summary).filter(Summary.user_id == user["id"]).all()

@router.get("/{summary_id}")
def get_summary(
    summary_id: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    
    
    
    """Return a single summary by id if owned by the current user, else 404."""
    row = (
        db.query(Summary)
        .filter(Summary.id == summary_id, Summary.user_id == user["id"])
        .first()
    )
    if not row:
        # Raise 404 to indicate the resource does not exist or isn't accessible.
        raise HTTPException(404, "Not found")
    return row
