@router.get("/{summary_id}/flashcards")
def get_flashcards(summary_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.query(Summary).filter(
        Summary.id == summary_id, Summary.user_id == user["id"]
    ).first()

    if not row:
        raise HTTPException(404, "Summary not found")

    cards = generate_flashcards(row.summary_text)
    return {"flashcards": cards}
