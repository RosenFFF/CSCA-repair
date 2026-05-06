from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from dotenv import load_dotenv
from database import init_db
from routers import activities, signups, admin

load_dotenv()

app = FastAPI(title="义务维修报名系统")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(activities.router, prefix="/api")
app.include_router(signups.router, prefix="/api")
app.include_router(admin.router, prefix="/api/admin")

# Serve frontend static files
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="static")

@app.on_event("startup")
def startup():
    init_db()
