@router.get("/{summary_id}/mcqs")
def get_mcqs(summary_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.query(Summary).filter(
        Summary.id == summary_id, Summary.user_id == user["id"]
    ).first()

    if not row:
        raise HTTPException(404, "Summary not found")

    mcqs = generate_mcqs(row.summary_text)
    return {"mcqs": mcqs}
