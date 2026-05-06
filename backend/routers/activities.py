from fastapi import APIRouter
from datetime import datetime, timedelta
from database import get_db

router = APIRouter()

MAX_SIGNUP = 5

def get_wednesday_dates(weeks: int = 4) -> list[str]:
    """Return the last `weeks` Wednesday dates (including today if Wednesday)."""
    today = datetime.now().date()
    # Find this week's Wednesday (weekday 2 = Wednesday)
    days_since_wed = (today.weekday() - 2) % 7
    this_wednesday = today - timedelta(days=days_since_wed)
    return [(this_wednesday - timedelta(weeks=i)).isoformat() for i in range(weeks)]

@router.get("/activities")
def list_activities():
    dates = get_wednesday_dates(4)
    shifts = ["13:30-15:30", "15:30-17:30"]
    db = get_db()
    result = []
    for date in dates:
        for shift in shifts:
            row = db.execute(
                "SELECT COUNT(*) as cnt FROM signups WHERE date=? AND shift=?",
                (date, shift)
            ).fetchone()
            count = row["cnt"]
            result.append({
                "date": date,
                "shift": shift,
                "signup_count": count,
                "max_signup": MAX_SIGNUP,
                "is_full": count >= MAX_SIGNUP,
            })
    db.close()
    return result
