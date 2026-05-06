from pydantic import BaseModel, Field
from typing import Optional

class SignupRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=20, description="参与者姓名")
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="活动日期 YYYY-MM-DD")
    shift: str = Field(..., pattern=r"^\d{2}:\d{2}-\d{2}:\d{2}$", description="班次时间")

class ActivityResponse(BaseModel):
    date: str
    shift: str
    signup_count: int
    max_signup: int = 5
    is_full: bool

class LoginRequest(BaseModel):
    password: str

class SignupRecord(BaseModel):
    id: int
    name: str
    date: str
    shift: str
    created_at: str

class StatsResponse(BaseModel):
    week_count: int
    total_count: int
    shift1_count: int
    shift2_count: int
    weekly_trend: list[dict]
    leaderboard: list[dict]
