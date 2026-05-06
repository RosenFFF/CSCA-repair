from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import StreamingResponse
from models import LoginRequest, StatsResponse, SignupRecord
from auth import verify_password, create_token, verify_token
from database import get_db
from datetime import datetime, timedelta
from io import BytesIO
from openpyxl import Workbook

router = APIRouter()

@router.post("/login")
def admin_login(req: LoginRequest):
    if not verify_password(req.password):
        raise HTTPException(status_code=401, detail="密码错误")
    return {"token": create_token()}

@router.get("/signups", dependencies=[Depends(verify_token)])
def list_signups(
    date: str = Query(None, description="按日期筛选"),
    shift: str = Query(None, description="按班次筛选"),
):
    db = get_db()
    query = "SELECT id, name, date, shift, created_at FROM signups WHERE 1=1"
    params = []
    if date:
        query += " AND date=?"
        params.append(date)
    if shift:
        query += " AND shift=?"
        params.append(shift)
    query += " ORDER BY created_at DESC"
    rows = db.execute(query, params).fetchall()
    db.close()
    return [dict(r) for r in rows]

@router.delete("/signups/{signup_id}", dependencies=[Depends(verify_token)])
def delete_signup(signup_id: int):
    db = get_db()
    result = db.execute("DELETE FROM signups WHERE id=?", (signup_id,))
    db.commit()
    db.close()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="记录不存在")
    return {"message": "删除成功"}

@router.get("/stats", dependencies=[Depends(verify_token)])
def get_stats():
    db = get_db()
    today = datetime.now().date()
    days_since_wed = (today.weekday() - 2) % 7
    this_wednesday = (today - timedelta(days=days_since_wed)).isoformat()

    # This week count
    week_row = db.execute(
        "SELECT COUNT(*) as cnt FROM signups WHERE date=?", (this_wednesday,)
    ).fetchone()
    week_count = week_row["cnt"]

    # Total count
    total_row = db.execute("SELECT COUNT(*) as cnt FROM signups").fetchone()
    total_count = total_row["cnt"]

    # Shift counts for this week
    s1 = db.execute(
        "SELECT COUNT(*) as cnt FROM signups WHERE date=? AND shift='13:30-15:30'",
        (this_wednesday,)
    ).fetchone()
    s2 = db.execute(
        "SELECT COUNT(*) as cnt FROM signups WHERE date=? AND shift='15:30-17:30'",
        (this_wednesday,)
    ).fetchone()

    # Weekly trend (last 8 weeks)
    trend = []
    for i in range(7, -1, -1):
        wed = (today - timedelta(days=days_since_wed, weeks=i)).isoformat()
        r1 = db.execute(
            "SELECT COUNT(*) as cnt FROM signups WHERE date=? AND shift='13:30-15:30'", (wed,)
        ).fetchone()
        r2 = db.execute(
            "SELECT COUNT(*) as cnt FROM signups WHERE date=? AND shift='15:30-17:30'", (wed,)
        ).fetchone()
        trend.append({"date": wed, "shift1": r1["cnt"], "shift2": r2["cnt"]})

    # Leaderboard
    lb = db.execute(
        "SELECT name, COUNT(*) as count FROM signups GROUP BY name ORDER BY count DESC LIMIT 20"
    ).fetchall()

    db.close()
    return {
        "week_count": week_count,
        "total_count": total_count,
        "shift1_count": s1["cnt"],
        "shift2_count": s2["cnt"],
        "weekly_trend": trend,
        "leaderboard": [dict(r) for r in lb],
    }

@router.get("/export", dependencies=[Depends(verify_token)])
def export_excel(
    start_date: str = Query(None),
    end_date: str = Query(None),
):
    db = get_db()
    query = "SELECT name, date, shift, created_at FROM signups WHERE 1=1"
    params = []
    if start_date:
        query += " AND date>=?"
        params.append(start_date)
    if end_date:
        query += " AND date<=?"
        params.append(end_date)
    query += " ORDER BY date DESC, shift, created_at"
    rows = db.execute(query, params).fetchall()
    db.close()

    wb = Workbook()
    ws = wb.active
    ws.title = "报名数据"
    ws.append(["姓名", "日期", "班次", "报名时间"])
    for r in rows:
        ws.append([r["name"], r["date"], r["shift"], r["created_at"]])

    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)

    filename = f"repair_signups_{datetime.now().strftime('%Y%m%d')}.xlsx"
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
