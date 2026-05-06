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
