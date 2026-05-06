# 义务维修活动报名系统 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a mobile-friendly web app for tracking weekly repair activity signups, with a public signup page and admin dashboard.

**Architecture:** Vue 3 SPA frontend served as static files by FastAPI backend. SQLite database for storage. Dynamic activity date generation (no pre-seeded records). Admin auth via JWT token from fixed password.

**Tech Stack:** Vue 3, Vite, Element Plus, ECharts, Python FastAPI, SQLite, openpyxl

---

## File Structure

```
义务维修统计/
├── backend/
│   ├── main.py              # FastAPI app entry, CORS, static file serving
│   ├── database.py          # SQLite connection, table creation
│   ├── models.py            # Pydantic request/response models
│   ├── auth.py              # Password verification, JWT token
│   ├── routers/
│   │   ├── activities.py    # GET /api/activities
│   │   ├── signups.py       # POST /api/signups
│   │   └── admin.py         # All /api/admin/* endpoints
│   └── requirements.txt
├── frontend/
│   ├── vite.config.js
│   ├── package.json
│   ├── index.html
│   └── src/
│       ├── main.js
│       ├── App.vue
│       ├── router/index.js
│       ├── api/index.js     # Axios instance + API functions
│       ├── views/
│       │   ├── SignupPage.vue
│       │   └── AdminPage.vue
│       └── components/
│           ├── ActivityCard.vue
│           ├── SignupDialog.vue
│           ├── StatsCards.vue
│           ├── TrendChart.vue
│           ├── SignupList.vue
│           └── Leaderboard.vue
└── docs/
```

---

### Task 1: Backend Project Setup

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/main.py`
- Create: `backend/database.py`

- [ ] **Step 1: Create requirements.txt**

```
fastapi==0.115.0
uvicorn==0.30.0
pydantic==2.9.0
python-jose[cryptography]==3.3.0
openpyxl==3.1.5
python-dotenv==1.0.1
```

- [ ] **Step 2: Create database.py**

```python
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS signups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            shift TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(name, date, shift)
        );
    """)
    conn.commit()
    conn.close()
```

Note: Simplified schema — signups table directly stores `date` and `shift` instead of a separate activities table, since activities are dynamically generated.

- [ ] **Step 3: Create main.py**

```python
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
```

- [ ] **Step 4: Create routers directory**

Create empty `backend/routers/__init__.py` file.

- [ ] **Step 5: Verify backend starts**

```bash
cd backend && pip install -r requirements.txt && python -c "from database import init_db; init_db(); print('DB OK')"
```

Expected: `DB OK` printed, `data.db` file created.

- [ ] **Step 6: Commit**

```bash
git add backend/
git commit -m "feat: backend project setup with FastAPI and SQLite"
```

---

### Task 2: Backend Models and Auth

**Files:**
- Create: `backend/models.py`
- Create: `backend/auth.py`

- [ ] **Step 1: Create models.py**

```python
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
```

- [ ] **Step 2: Create auth.py**

```python
import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = os.getenv("JWT_SECRET", "repair-activity-secret-key-change-in-prod")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24

security = HTTPBearer()

def verify_password(password: str) -> bool:
    return password == ADMIN_PASSWORD

def create_token() -> str:
    expire = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    return jwt.encode({"exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except JWTError:
        raise HTTPException(status_code=401, detail="无效的认证令牌")
```

- [ ] **Step 3: Commit**

```bash
git add backend/models.py backend/auth.py
git commit -m "feat: add Pydantic models and JWT auth"
```

---

### Task 3: Backend API — Activities and Signups

**Files:**
- Create: `backend/routers/activities.py`
- Create: `backend/routers/signups.py`

- [ ] **Step 1: Create activities.py**

```python
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
```

- [ ] **Step 2: Create signups.py**

```python
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
```

- [ ] **Step 3: Test API manually**

```bash
cd backend && python -m uvicorn main:app --reload --port 8000
```

Then in another terminal:
```bash
curl http://localhost:8000/api/activities
curl -X POST http://localhost:8000/api/signups -H "Content-Type: application/json" -d '{"name":"测试","date":"2026-05-07","shift":"13:30-15:30"}'
```

Expected: First returns activity list, second returns `{"message":"报名成功"}`.

- [ ] **Step 4: Commit**

```bash
git add backend/routers/activities.py backend/routers/signups.py
git commit -m "feat: add activities and signups API endpoints"
```

---

### Task 4: Backend API — Admin Endpoints

**Files:**
- Create: `backend/routers/admin.py`

- [ ] **Step 1: Create admin.py**

```python
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
```

- [ ] **Step 2: Test admin endpoints**

```bash
# Login
curl -X POST http://localhost:8000/api/admin/login -H "Content-Type: application/json" -d '{"password":"admin123"}'
# Use returned token:
curl http://localhost:8000/api/admin/stats -H "Authorization: Bearer <token>"
```

Expected: Login returns token, stats returns JSON with counts and trend data.

- [ ] **Step 3: Commit**

```bash
git add backend/routers/admin.py
git commit -m "feat: add admin API endpoints (login, stats, CRUD, export)"
```

---

### Task 5: Frontend Project Setup

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.js`
- Create: `frontend/index.html`
- Create: `frontend/src/main.js`
- Create: `frontend/src/App.vue`
- Create: `frontend/src/router/index.js`
- Create: `frontend/src/api/index.js`

- [ ] **Step 1: Initialize Vue project**

```bash
cd frontend && npm create vite@latest . -- --template vue
npm install
npm install element-plus @element-plus/icons-vue vue-router@4 pinia axios echarts vue-echarts
```

- [ ] **Step 2: Configure vite.config.js**

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
```

- [ ] **Step 3: Create src/main.js**

```javascript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(ElementPlus, { locale: zhCn })
app.mount('#app')
```

- [ ] **Step 4: Create src/router/index.js**

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import SignupPage from '../views/SignupPage.vue'
import AdminPage from '../views/AdminPage.vue'

const routes = [
  { path: '/', component: SignupPage },
  { path: '/admin', component: AdminPage },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
```

- [ ] **Step 5: Create src/api/index.js**

```javascript
import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

// Add admin token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token')
  if (token && config.url.startsWith('/admin')) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const getActivities = () => api.get('/activities')
export const createSignup = (data) => api.post('/signups', data)
export const adminLogin = (password) => api.post('/admin/login', { password })
export const getAdminSignups = (params) => api.get('/admin/signups', { params })
export const deleteSignup = (id) => api.delete(`/admin/signups/${id}`)
export const getAdminStats = () => api.get('/admin/stats')
export const exportExcel = (params) =>
  api.get('/admin/export', { params, responseType: 'blob' })
```

- [ ] **Step 6: Create src/App.vue**

```vue
<template>
  <router-view />
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f5f7fa;
  -webkit-font-smoothing: antialiased;
}
</style>
```

- [ ] **Step 7: Verify frontend starts**

```bash
cd frontend && npm run dev
```

Expected: Dev server starts on http://localhost:5173

- [ ] **Step 8: Commit**

```bash
git add frontend/
git commit -m "feat: frontend project setup with Vue 3, Element Plus, Router"
```

---

### Task 6: Signup Page — Activity List

**Files:**
- Create: `frontend/src/views/SignupPage.vue`
- Create: `frontend/src/components/ActivityCard.vue`

- [ ] **Step 1: Create ActivityCard.vue**

```vue
<template>
  <div class="activity-card" :class="{ full: activity.is_full }">
    <div class="card-header">
      <span class="shift-label">{{ activity.shift }}</span>
      <span class="count" :class="{ 'count-full': activity.is_full }">
        {{ activity.signup_count }}/{{ activity.max_signup }}
      </span>
    </div>
    <el-button
      v-if="!activity.is_full"
      type="primary"
      size="large"
      round
      @click="$emit('signup', activity)"
    >
      报名
    </el-button>
    <el-button v-else type="info" size="large" round disabled>
      已满
    </el-button>
  </div>
</template>

<script setup>
defineProps({ activity: Object })
defineEmits(['signup'])
</script>

<style scoped>
.activity-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.activity-card.full {
  opacity: 0.6;
}
.card-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.shift-label {
  font-size: 15px;
  font-weight: 500;
  color: #333;
}
.count {
  font-size: 13px;
  color: #999;
}
.count-full {
  color: #f56c6c;
}
</style>
```

- [ ] **Step 2: Create SignupPage.vue**

```vue
<template>
  <div class="signup-page">
    <div class="page-header">
      <div class="logo">🔧</div>
      <h1>义务维修报名</h1>
      <p class="subtitle">计算机协会 · 每周三下午</p>
    </div>

    <!-- This week -->
    <div class="section" v-if="currentWeekActivities.length">
      <h2 class="section-title">本周活动</h2>
      <div class="card-list">
        <ActivityCard
          v-for="item in currentWeekActivities"
          :key="item.date + item.shift"
          :activity="item"
          @signup="openSignupDialog"
        />
      </div>
    </div>

    <!-- History -->
    <div class="section" v-if="historyActivities.length">
      <el-collapse v-model="expandedHistory">
        <el-collapse-item title="历史活动" name="history">
          <div v-for="(week, idx) in historyGrouped" :key="idx" class="history-week">
            <div class="history-date">{{ formatDate(week.date) }}</div>
            <div class="card-list">
              <ActivityCard
                v-for="item in week.items"
                :key="item.shift"
                :activity="item"
                @signup="openSignupDialog"
              />
            </div>
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>

    <!-- Signup Dialog -->
    <el-dialog v-model="dialogVisible" title="报名" width="90%" :show-close="false">
      <el-form @submit.prevent="submitSignup">
        <el-form-item label="姓名">
          <el-input v-model="signupName" placeholder="请输入你的姓名" maxlength="20" clearable />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitSignup" :loading="submitting">确认报名</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getActivities, createSignup } from '../api'
import ActivityCard from '../components/ActivityCard.vue'

const activities = ref([])
const dialogVisible = ref(false)
const selectedActivity = ref(null)
const signupName = ref('')
const submitting = ref(false)
const expandedHistory = ref([])

const currentWeekDate = computed(() => {
  if (!activities.value.length) return ''
  return activities.value[0].date
})

const currentWeekActivities = computed(() =>
  activities.value.filter((a) => a.date === currentWeekDate.value)
)

const historyActivities = computed(() =>
  activities.value.filter((a) => a.date !== currentWeekDate.value)
)

const historyGrouped = computed(() => {
  const groups = {}
  historyActivities.value.forEach((a) => {
    if (!groups[a.date]) groups[a.date] = []
    groups[a.date].push(a)
  })
  return Object.entries(groups).map(([date, items]) => ({ date, items }))
})

function formatDate(dateStr) {
  const d = new Date(dateStr)
  return `${d.getMonth() + 1}月${d.getDate()}日 周三`
}

async function loadActivities() {
  const { data } = await getActivities()
  activities.value = data
}

function openSignupDialog(activity) {
  selectedActivity.value = activity
  signupName.value = ''
  dialogVisible.value = true
}

async function submitSignup() {
  if (!signupName.value.trim()) {
    ElMessage.warning('请输入姓名')
    return
  }
  submitting.value = true
  try {
    await createSignup({
      name: signupName.value.trim(),
      date: selectedActivity.value.date,
      shift: selectedActivity.value.shift,
    })
    ElMessage.success('报名成功！')
    dialogVisible.value = false
    await loadActivities()
  } catch (err) {
    const msg = err.response?.data?.detail || '报名失败'
    ElMessage.error(msg)
  } finally {
    submitting.value = false
  }
}

onMounted(loadActivities)
</script>

<style scoped>
.signup-page {
  max-width: 480px;
  margin: 0 auto;
  padding: 20px 16px;
  min-height: 100vh;
}
.page-header {
  text-align: center;
  margin-bottom: 24px;
}
.logo {
  font-size: 36px;
  margin-bottom: 8px;
}
h1 {
  font-size: 22px;
  font-weight: 600;
  color: #1a1a1a;
}
.subtitle {
  font-size: 13px;
  color: #666;
  margin-top: 4px;
}
.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
}
.card-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 16px;
}
.history-week {
  margin-bottom: 12px;
}
.history-date {
  font-size: 13px;
  color: #999;
  margin-bottom: 8px;
}
</style>
```

- [ ] **Step 3: Test signup page**

Start backend (`cd backend && python -m uvicorn main:app --reload --port 8000`) and frontend (`cd frontend && npm run dev`). Open http://localhost:5173, verify activity list loads, try signing up.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/views/SignupPage.vue frontend/src/components/ActivityCard.vue
git commit -m "feat: signup page with activity list and dialog"
```

---

### Task 7: Admin Page — Login and Stats Cards

**Files:**
- Create: `frontend/src/views/AdminPage.vue`
- Create: `frontend/src/components/StatsCards.vue`

- [ ] **Step 1: Create StatsCards.vue**

```vue
<template>
  <div class="stats-grid">
    <div class="stat-card blue">
      <div class="stat-label">本周报名</div>
      <div class="stat-value">{{ stats.week_count }}</div>
    </div>
    <div class="stat-card purple">
      <div class="stat-label">累计参与</div>
      <div class="stat-value">{{ stats.total_count }}</div>
    </div>
    <div class="stat-card orange">
      <div class="stat-label">第一班</div>
      <div class="stat-value">{{ stats.shift1_count }}</div>
      <div class="stat-sub">13:30-15:30</div>
    </div>
    <div class="stat-card teal">
      <div class="stat-label">第二班</div>
      <div class="stat-value">{{ stats.shift2_count }}</div>
      <div class="stat-sub">15:30-17:30</div>
    </div>
  </div>
</template>

<script setup>
defineProps({ stats: Object })
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 16px;
}
.stat-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.stat-label {
  font-size: 12px;
  color: #999;
}
.stat-value {
  font-size: 32px;
  font-weight: 700;
  margin-top: 4px;
}
.stat-sub {
  font-size: 11px;
  color: #999;
  margin-top: 2px;
}
.blue .stat-value { color: #1890ff; }
.purple .stat-value { color: #722ed1; }
.orange .stat-value { color: #fa8c16; }
.teal .stat-value { color: #13c2c2; }
</style>
```

- [ ] **Step 2: Create AdminPage.vue (login + stats tab)**

```vue
<template>
  <div class="admin-page">
    <!-- Login -->
    <div v-if="!isLoggedIn" class="login-container">
      <div class="login-card">
        <h2>管理后台</h2>
        <el-form @submit.prevent="handleLogin">
          <el-form-item>
            <el-input
              v-model="password"
              type="password"
              placeholder="请输入管理员密码"
              show-password
              size="large"
            />
          </el-form-item>
          <el-button type="primary" size="large" @click="handleLogin" :loading="loggingIn" style="width:100%">
            登录
          </el-button>
        </el-form>
      </div>
    </div>

    <!-- Dashboard -->
    <div v-else class="dashboard">
      <div class="dash-header">
        <h2>管理后台</h2>
        <el-button text @click="logout">退出</el-button>
      </div>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="数据总览" name="stats">
          <StatsCards :stats="stats" />
          <TrendChart :trend="stats.weekly_trend" />
        </el-tab-pane>
        <el-tab-pane label="报名列表" name="list">
          <SignupList />
        </el-tab-pane>
        <el-tab-pane label="排行榜" name="rank">
          <Leaderboard :data="stats.leaderboard" />
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { adminLogin, getAdminStats } from '../api'
import StatsCards from '../components/StatsCards.vue'
import TrendChart from '../components/TrendChart.vue'
import SignupList from '../components/SignupList.vue'
import Leaderboard from '../components/Leaderboard.vue'

const isLoggedIn = ref(!!localStorage.getItem('admin_token'))
const password = ref('')
const loggingIn = ref(false)
const activeTab = ref('stats')
const stats = ref({
  week_count: 0,
  total_count: 0,
  shift1_count: 0,
  shift2_count: 0,
  weekly_trend: [],
  leaderboard: [],
})

async function handleLogin() {
  if (!password.value) return
  loggingIn.value = true
  try {
    const { data } = await adminLogin(password.value)
    localStorage.setItem('admin_token', data.token)
    isLoggedIn.value = true
    await loadStats()
  } catch {
    ElMessage.error('密码错误')
  } finally {
    loggingIn.value = false
  }
}

function logout() {
  localStorage.removeItem('admin_token')
  isLoggedIn.value = false
}

async function loadStats() {
  try {
    const { data } = await getAdminStats()
    stats.value = data
  } catch {
    // Token expired
    logout()
  }
}

onMounted(() => {
  if (isLoggedIn.value) loadStats()
})
</script>

<style scoped>
.admin-page {
  max-width: 480px;
  margin: 0 auto;
  padding: 20px 16px;
  min-height: 100vh;
}
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 80vh;
}
.login-card {
  background: white;
  border-radius: 16px;
  padding: 32px 24px;
  width: 100%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
.login-card h2 {
  text-align: center;
  margin-bottom: 24px;
  font-size: 20px;
}
.dash-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.dash-header h2 {
  font-size: 20px;
}
</style>
```

- [ ] **Step 3: Test admin login**

Open http://localhost:5173/admin, enter password `admin123`, verify login works and stats display.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/views/AdminPage.vue frontend/src/components/StatsCards.vue
git commit -m "feat: admin page with login and stats cards"
```

---

### Task 8: Admin Page — Trend Chart and Leaderboard

**Files:**
- Create: `frontend/src/components/TrendChart.vue`
- Create: `frontend/src/components/Leaderboard.vue`

- [ ] **Step 1: Create TrendChart.vue**

```vue
<template>
  <div class="chart-container">
    <h3 class="chart-title">每周报名趋势</h3>
    <v-chart :option="chartOption" autoresize style="height: 250px" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

use([BarChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

const props = defineProps({ trend: Array })

const chartOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  legend: { data: ['第一班', '第二班'], bottom: 0 },
  grid: { left: 40, right: 16, top: 16, bottom: 40 },
  xAxis: {
    type: 'category',
    data: props.trend?.map((t) => {
      const d = new Date(t.date)
      return `${d.getMonth() + 1}/${d.getDate()}`
    }) || [],
  },
  yAxis: { type: 'value', minInterval: 1 },
  series: [
    {
      name: '第一班',
      type: 'bar',
      data: props.trend?.map((t) => t.shift1) || [],
      itemStyle: { color: '#1890ff', borderRadius: [4, 4, 0, 0] },
    },
    {
      name: '第二班',
      type: 'bar',
      data: props.trend?.map((t) => t.shift2) || [],
      itemStyle: { color: '#13c2c2', borderRadius: [4, 4, 0, 0] },
    },
  ],
}))
</script>

<style scoped>
.chart-container {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.chart-title {
  font-size: 15px;
  font-weight: 500;
  color: #333;
  margin-bottom: 12px;
}
</style>
```

- [ ] **Step 2: Create Leaderboard.vue**

```vue
<template>
  <div class="leaderboard">
    <div v-if="!data || data.length === 0" class="empty">暂无数据</div>
    <div v-else>
      <div
        v-for="(item, index) in data"
        :key="item.name"
        class="lb-item"
      >
        <div class="lb-rank" :class="{ top3: index < 3 }">{{ index + 1 }}</div>
        <div class="lb-name">{{ item.name }}</div>
        <div class="lb-count">{{ item.count }} 次</div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ data: Array })
</script>

<style scoped>
.leaderboard {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.empty {
  text-align: center;
  color: #999;
  padding: 32px;
}
.lb-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f5f5f5;
}
.lb-item:last-child {
  border-bottom: none;
}
.lb-rank {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  color: #666;
  margin-right: 12px;
}
.lb-rank.top3 {
  background: #fff7e6;
  color: #fa8c16;
}
.lb-name {
  flex: 1;
  font-size: 15px;
  color: #333;
}
.lb-count {
  font-size: 14px;
  color: #1890ff;
  font-weight: 500;
}
</style>
```

- [ ] **Step 3: Test charts and leaderboard**

Open admin page, verify trend chart renders with bar chart, leaderboard shows names ranked by participation count.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/components/TrendChart.vue frontend/src/components/Leaderboard.vue
git commit -m "feat: trend chart and leaderboard components"
```

---

### Task 9: Admin Page — Signup List with Filter and Export

**Files:**
- Create: `frontend/src/components/SignupList.vue`

- [ ] **Step 1: Create SignupList.vue**

```vue
<template>
  <div class="signup-list">
    <div class="filters">
      <el-date-picker
        v-model="filterDate"
        type="date"
        placeholder="选择日期"
        value-format="YYYY-MM-DD"
        size="small"
        clearable
        @change="loadSignups"
      />
      <el-select v-model="filterShift" placeholder="选择班次" size="small" clearable @change="loadSignups">
        <el-option label="13:30-15:30" value="13:30-15:30" />
        <el-option label="15:30-17:30" value="15:30-17:30" />
      </el-select>
    </div>

    <div class="list">
      <div v-if="signups.length === 0" class="empty">暂无数据</div>
      <div v-for="item in signups" :key="item.id" class="list-item">
        <div class="item-info">
          <div class="item-name">{{ item.name }}</div>
          <div class="item-meta">{{ item.date }} · {{ item.shift }}</div>
        </div>
        <el-button type="danger" text size="small" @click="handleDelete(item.id)">删除</el-button>
      </div>
    </div>

    <el-button type="success" size="large" style="width: 100%; margin-top: 12px" @click="handleExport">
      📥 导出 Excel
    </el-button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAdminSignups, deleteSignup, exportExcel } from '../api'

const signups = ref([])
const filterDate = ref('')
const filterShift = ref('')

async function loadSignups() {
  const params = {}
  if (filterDate.value) params.date = filterDate.value
  if (filterShift.value) params.shift = filterShift.value
  const { data } = await getAdminSignups(params)
  signups.value = data
}

async function handleDelete(id) {
  try {
    await ElMessageBox.confirm('确定删除这条记录？', '提示', { type: 'warning' })
    await deleteSignup(id)
    ElMessage.success('删除成功')
    await loadSignups()
  } catch {
    // cancelled
  }
}

async function handleExport() {
  try {
    const params = {}
    if (filterDate.value) params.start_date = filterDate.value
    if (filterDate.value) params.end_date = filterDate.value
    const { data } = await exportExcel(params)
    const url = URL.createObjectURL(data)
    const a = document.createElement('a')
    a.href = url
    a.download = `repair_signups_${new Date().toISOString().slice(0, 10)}.xlsx`
    a.click()
    URL.revokeObjectURL(url)
  } catch {
    ElMessage.error('导出失败')
  }
}

onMounted(loadSignups)
</script>

<style scoped>
.signup-list {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.filters {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}
.empty {
  text-align: center;
  color: #999;
  padding: 32px;
}
.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f5f5f5;
}
.list-item:last-child {
  border-bottom: none;
}
.item-name {
  font-size: 15px;
  font-weight: 500;
  color: #333;
}
.item-meta {
  font-size: 12px;
  color: #999;
  margin-top: 2px;
}
</style>
```

- [ ] **Step 2: Test full admin flow**

Login → verify stats cards, chart, leaderboard → switch to signup list tab → filter by date → delete a record → export Excel.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/components/SignupList.vue
git commit -m "feat: signup list with filter, delete, and Excel export"
```

---

### Task 10: Build and Integration

**Files:**
- Modify: `backend/main.py` (verify static file serving)

- [ ] **Step 1: Build frontend**

```bash
cd frontend && npm run build
```

Expected: `frontend/dist/` directory created with built files.

- [ ] **Step 2: Test production mode**

```bash
cd backend && python -m uvicorn main:app --port 8000
```

Open http://localhost:8000 — should serve the Vue app. Open http://localhost:8000/admin — admin page. Verify all features work.

- [ ] **Step 3: Create .env file for configuration**

```
ADMIN_PASSWORD=admin123
JWT_SECRET=your-secret-key-change-this
```

- [ ] **Step 4: Create .gitignore additions**

Ensure these are in `.gitignore`:
```
backend/data.db
backend/__pycache__/
frontend/node_modules/
frontend/dist/
.env
.superpowers/
```

- [ ] **Step 5: Final commit**

```bash
git add .gitignore
git commit -m "chore: add gitignore and env config"
```

---

### Task 11: README and Documentation

**Files:**
- Create: `README.md`

- [ ] **Step 1: Create README.md**

```markdown
# 义务维修活动报名系统

计算机协会每周三义务维修活动的在线报名与数据管理工具。

## 快速开始

### 1. 启动后端

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # 修改管理员密码
python -m uvicorn main:app --reload --port 8000
```

### 2. 启动前端（开发模式）

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173

### 3. 生产部署

```bash
cd frontend && npm run build
cd ../backend && python -m uvicorn main:app --port 8000
```

访问 http://localhost:8000

## 功能

- **报名页**：选择班次 → 输入姓名 → 完成报名（每班次限 5 人）
- **管理后台**：/admin → 输入密码 → 查看统计、趋势图、排行榜、导出 Excel

## 配置

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| ADMIN_PASSWORD | 管理员密码 | admin123 |
| JWT_SECRET | JWT 签名密钥 | 内置默认值 |
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add README with setup instructions"
```
