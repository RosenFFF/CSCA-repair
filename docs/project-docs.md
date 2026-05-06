# 义务维修报名系统 — 项目文档

## 项目概述

本系统是为大学计算机协会开发的义务维修活动在线报名平台。每周三下午举办两个班次的义务维修活动，参与者通过手机端网页即可完成报名，管理员可通过后台查看统计数据、管理报名记录。

**核心特点：**
- 手机端优先，响应式设计
- 无需注册登录，填表即报
- 每班次最多 5 人，满员自动锁定
- 管理后台密码保护，支持数据统计与导出

---

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端框架 | Vue 3 + Vite | 组合式 API，快速构建 |
| UI 组件库 | Element Plus | 移动端适配的桌面组件 |
| 图表库 | ECharts (vue-echarts) | 数据可视化 |
| 状态管理 | Pinia | Vue 3 官方推荐 |
| 路由 | Vue Router | 单页应用路由 |
| HTTP 客户端 | Axios | API 请求 |
| 后端框架 | FastAPI | 高性能 Python API 框架 |
| 数据库 | SQLite | 轻量级，无需额外服务 |
| 认证 | JWT (python-jose) | 管理员登录凭证 |
| 导出 | openpyxl | Excel 文件生成 |

---

## 项目结构

```
义务维修统计/
├── backend/                    # 后端服务
│   ├── main.py                # FastAPI 应用入口
│   ├── database.py            # SQLite 数据库连接与初始化
│   ├── models.py              # Pydantic 数据模型
│   ├── auth.py                # JWT 认证模块
│   ├── requirements.txt       # Python 依赖
│   ├── .env.example           # 环境变量模板
│   └── routers/
│       ├── activities.py      # 活动列表 API
│       ├── signups.py         # 报名 API
│       └── admin.py           # 管理后台 API
├── frontend/                   # 前端应用
│   ├── src/
│   │   ├── main.js            # 应用入口
│   │   ├── App.vue            # 根组件
│   │   ├── api/
│   │   │   └── index.js       # API 接口封装
│   │   ├── router/
│   │   │   └── index.js       # 路由配置
│   │   ├── views/
│   │   │   ├── SignupPage.vue # 报名页
│   │   │   └── AdminPage.vue  # 管理后台
│   │   └── components/
│   │       ├── ActivityCard.vue   # 活动卡片
│   │       ├── StatsCards.vue     # 统计卡片
│   │       ├── TrendChart.vue     # 趋势图表
│   │       ├── Leaderboard.vue    # 排行榜
│   │       └── SignupList.vue     # 报名列表
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
└── docs/
    ├── deploy-guide.md        # 部署教程
    └── project-docs.md        # 项目文档（本文件）
```

---

## 功能说明

### 一、报名页（`/`）

**访问地址：** `http://服务器IP:8000/`

**功能：**

1. **本周活动展示**
   - 显示最近一个周三的两个班次
   - 每个班次显示当前报名人数/最大人数（如 3/5）
   - 班次标题：第一班次（13:30-15:30）、第二班次（15:30-17:30）
   - 标题格式：`X月X日 周三 义务维修`

2. **报名操作**
   - 点击"报名"按钮弹出对话框
   - 仅需填写姓名
   - 提交后实时更新人数
   - 达到 5 人上限后按钮变为"已满"，不可点击

3. **历史活动**
   - 折叠展示过往活动记录
   - 历史卡片为灰色，显示"已结束"按钮，不可报名

4. **提醒信息**
   - 底部黄色提示条："如果填错或误填，请及时联系部长删除"

5. **管理员入口**
   - 底部"管理员入口"链接，跳转至 `/admin`

### 二、管理后台（`/admin`）

**访问地址：** `http://服务器IP:8000/admin`

**登录：** 输入管理员密码（默认 `admin123`，建议部署时修改）

**功能标签页：**

#### 数据总览
- **统计卡片：** 本周报名数、累计参与人数、第一班次人数、第二班次人数
- **趋势图：** 近 8 周报名趋势柱状图，按班次分组
- **排行榜：** 参与次数 Top 20，前三名高亮显示

#### 报名列表
- 按日期、班次筛选报名记录
- 显示姓名、日期、班次、报名时间
- 支持删除单条记录（带姓名确认提示）
- 支持导出 Excel 文件

#### 排行榜
- 独立排行榜视图，与数据总览中的排行榜一致

**返回首页：** 页面顶部"← 返回报名页"链接

---

## 数据模型

### signups 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| name | TEXT | 报名者姓名 |
| date | TEXT | 活动日期（格式：YYYY-MM-DD） |
| shift | TEXT | 班次（13:30-15:30 或 15:30-17:30） |
| created_at | TIMESTAMP | 报名时间 |

**约束：** `UNIQUE(name, date, shift)` — 同一人同一天同一班次不可重复报名

---

## API 文档

启动后端后访问 `http://服务器IP:8000/docs` 可查看 Swagger 自动生成的 API 文档。

### 公开接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/activities` | 获取活动列表（含报名人数） |
| POST | `/api/signups` | 提交报名 |

### 管理接口（需 JWT Token）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/login` | 管理员登录，返回 JWT |
| GET | `/api/signups` | 查询报名列表（支持 date/shift 筛选） |
| DELETE | `/api/signups/{id}` | 删除报名记录 |
| GET | `/api/stats` | 获取统计数据 |
| GET | `/api/export` | 导出 Excel 文件 |

### 请求/响应示例

**报名：**
```json
POST /api/signups
{
  "name": "张三",
  "date": "2026-05-06",
  "shift": "13:30-15:30"
}

// 成功
{ "message": "报名成功" }

// 失败（满员）
{ "detail": "该班次已满" }

// 失败（重复）
{ "detail": "你已经报名了该班次" }
```

**管理员登录：**
```json
POST /api/login
{ "password": "your_password" }

// 成功
{ "token": "eyJhbGciOiJIUzI1NiIs..." }
```

**统计：**
```json
GET /api/stats

{
  "week_count": 8,
  "total_count": 156,
  "shift1_count": 5,
  "shift2_count": 3,
  "weekly_trend": [
    { "date": "2026-03-11", "shift1": 4, "shift2": 3 },
    ...
  ],
  "leaderboard": [
    { "name": "张三", "count": 12 },
    ...
  ]
}
```

---

## 活动日期逻辑

系统自动识别每周三活动，无需手动创建：

1. **当前是周三且未到 18:00** → 显示今天的活动
2. **当前是周三且已过 18:00** → 显示下周三的活动
3. **其他日期** → 显示最近的下一个周三

报名页默认展示 4 周数据（1 个本周 + 3 个历史周），历史活动自动折叠。

---

## 配置说明

### 环境变量（`backend/.env`）

```env
ADMIN_PASSWORD=admin123        # 管理员密码，部署时务必修改
JWT_SECRET=your-random-string  # JWT 签名密钥，建议使用随机字符串
```

### 前端配置

- **API 代理：** 开发模式下 Vite 自动将 `/api` 请求代理到 `http://localhost:8000`
- **Element Plus：** 使用中文语言包
- **构建输出：** `frontend/dist/` 目录，后端自动托管

---

## 本地开发

### 启动后端

```bash
cd backend
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn main:app --reload --port 8000
```

### 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端开发服务器运行在 `http://localhost:5173`，API 请求自动代理到后端。

### 构建生产版本

```bash
cd frontend
npm run build
```

构建产物在 `frontend/dist/`，后端启动后会自动托管这些静态文件。

---

## 生产部署

详见 [deploy-guide.md](./deploy-guide.md)。

**快速流程：**
1. 安装 Python 3.10+ 和 Node.js 20+
2. 上传项目到服务器 `/opt/repair-signup`
3. 安装后端依赖并配置 `.env`
4. 构建前端 (`npm run build`)
5. 配置 systemd 开机自启
6. 开放 8000 端口

---

## 常见问题

**Q: 同一人能否重复报名同一班次？**
A: 不能。数据库有唯一约束，重复报名会返回"你已经报名了该班次"提示。

**Q: 报错"该班次已满"怎么办？**
A: 每班次最多 5 人，满员后需选择其他班次，或联系管理员删除误填记录。

**Q: 如何修改管理员密码？**
A: 编辑 `backend/.env` 中的 `ADMIN_PASSWORD`，重启服务生效。

**Q: 如何备份数据？**
A: 定期复制 `backend/data.db` 文件即可。详见部署文档中的备份章节。

**Q: 前端修改后需要重新部署吗？**
A: 是的。修改前端代码后需要重新 `npm run build`，后端会自动加载新的静态文件。
