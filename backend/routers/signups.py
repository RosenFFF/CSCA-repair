from fastapi import APIRouter, HTTPException
from models import SignupRequest
from database import get_db

router = APIRouter()

MAX_SIGNUP = 5

@router.post("/signups", status_code=201)
def create_signup(req: SignupRequest):
    db = get_db()
    # Check if full
    row = db.execute(
        "SELECT COUNT(*) as cnt FROM signups WHERE date=? AND shift=?",
        (req.date, req.shift)
    ).fetchone()
    if row["cnt"] >= MAX_SIGNUP:
        db.close()
        raise HTTPException(status_code=400, detail="该班次已满")
    # Check duplicate
    existing = db.execute(
        "SELECT id FROM signups WHERE name=? AND date=? AND shift=?",
        (req.name, req.date, req.shift)
    ).fetchone()
    if existing:
        db.close()
        raise HTTPException(status_code=409, detail="你已经报名了这个班次")
    # Insert
    db.execute(
        "INSERT INTO signups (name, date, shift) VALUES (?, ?, ?)",
        (req.name, req.date, req.shift)
    )
    db.commit()
    db.close()
    return {"message": "报名成功"}
