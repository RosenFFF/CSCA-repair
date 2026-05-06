from fastapi import APIRouter
from datetime import datetime, timedelta
from database import get_db

router = APIRouter()

MAX_SIGNUP = 5

def get_wednesday_dates(weeks: int = 4) -> list[str]:
    """Return Wednesday dates: the next upcoming one + previous weeks."""
    today = datetime.now().date()
    # Days until next Wednesday (0 = today is Wednesday)
    days_until_wed = (2 - today.weekday()) % 7
    # If it's Wednesday and before 18:00, use today; otherwise use next Wednesday
    if days_until_wed == 0 and datetime.now().hour < 18:
        next_wednesday = today
    elif days_until_wed == 0:
        next_wednesday = today + timedelta(days=7)
    else:
        next_wednesday = today + timedelta(days=days_until_wed)
    # Return: next_wednesday, then (weeks-1) previous Wednesdays
    return [(next_wednesday - timedelta(weeks=i)).isoformat() for i in range(weeks)]

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
