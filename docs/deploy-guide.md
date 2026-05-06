# 义务维修报名系统 — 华为云服务器部署教程

## 适用环境

- 服务器：华为云 ECS（推荐 1核2G 即可，20 人以内完全够用）
- 操作系统：Ubuntu 22.04 / CentOS 7+ 均可
- 本教程以 **Ubuntu 22.04** 为例

---

## 第一步：连接服务器

```bash
ssh root@你的服务器公网IP
```

输入密码后进入服务器终端。

---

## 第二步：安装 Python 3.10+

```bash
apt update && apt upgrade -y
apt install python3 python3-pip python3-venv -y
python3 --version
```

确保版本号 >= 3.10。

---

## 第三步：上传项目文件

### 方式一：用 scp 上传（推荐）

在你**本地电脑**的终端执行：

```bash
scp -r "C:/Users/LENOVO/Desktop/义务维修统计" root@你的服务器IP:/opt/repair-signup
```

### 方式二：用 Git 上传

先把项目推到 GitHub/Gitee，然后在服务器上：

```bash
cd /opt
git clone https://你的仓库地址.git repair-signup
```

### 方式三：用 FileZilla 等 SFTP 工具

把整个项目文件夹拖到服务器的 `/opt/repair-signup` 目录。

---

## 第四步：安装后端依赖

```bash
cd /opt/repair-signup/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 第五步：配置环境变量

```bash
cp .env.example .env
nano .env
```

修改内容：

```
ADMIN_PASSWORD=你的管理员密码
JWT_SECRET=换成一个随机字符串
```

保存退出（`Ctrl+O` → 回车 → `Ctrl+X`）。

---

## 第六步：构建前端

```bash
# 安装 Node.js（如果没有）
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install nodejs -y

# 构建前端
cd /opt/repair-signup/frontend
npm install
npm run build
```

构建完成后 `frontend/dist/` 目录就是前端静态文件，后端会自动托管。

---

## 第七步：测试运行

```bash
cd /opt/repair-signup/backend
source venv/bin/activate
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

打开浏览器访问 `http://你的服务器IP:8000`，确认能正常打开。

测试完成后按 `Ctrl+C` 停止。

---

## 第八步：设置开机自启（systemd）

创建服务文件：

```bash
nano /etc/systemd/system/repair-signup.service
```

写入以下内容：

```ini
[Unit]
Description=Repair Signup System
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/repair-signup/backend
Environment=PATH=/opt/repair-signup/backend/venv/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=/opt/repair-signup/backend/venv/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

启用并启动服务：

```bash
systemctl daemon-reload
systemctl enable repair-signup
systemctl start repair-signup
```

检查状态：

```bash
systemctl status repair-signup
```

看到 `active (running)` 就成功了。

---

## 第九步：开放防火墙端口

### 华为云安全组

1. 登录华为云控制台
2. 进入 ECS 实例 → 安全组
3. 添加入站规则：
   - 协议：TCP
   - 端口：8000
   - 来源：0.0.0.0/0

### 服务器防火墙（如果有）

```bash
ufw allow 8000/tcp
ufw reload
```

---

## 第十步：访问系统

- 报名页：`http://你的服务器IP:8000/`
- 管理后台：`http://你的服务器IP:8000/admin`
- API 文档：`http://你的服务器IP:8000/docs`

---

## 常用运维命令

```bash
# 查看服务状态
systemctl status repair-signup

# 重启服务
systemctl restart repair-signup

# 查看日志
journalctl -u repair-signup -f

# 停止服务
systemctl stop repair-signup
```

---

## 更新部署

当代码有更新时：

```bash
# 拉取最新代码
cd /opt/repair-signup
git pull

# 重新构建前端
cd frontend
npm install
npm run build

# 重启后端
systemctl restart repair-signup
```

---

## 数据备份

数据库文件位于 `/opt/repair-signup/backend/data.db`，定期备份：

```bash
cp /opt/repair-signup/backend/data.db /opt/backup/data_$(date +%Y%m%d).db
```

可以加到 crontab 每天自动备份：

```bash
crontab -e
# 添加：
0 2 * * * cp /opt/repair-signup/backend/data.db /opt/backup/data_$(date +\%Y\%m\%d).db
```

---

## 常见问题

**Q: 访问不了怎么办？**
- 检查华为云安全组是否放行 8000 端口
- 检查服务是否运行：`systemctl status repair-signup`
- 检查日志：`journalctl -u repair-signup -n 50`

**Q: 忘记管理员密码怎么办？**
- 修改 `/opt/repair-signup/backend/.env` 中的 `ADMIN_PASSWORD`
- 重启服务：`systemctl restart repair-signup`

**Q: 数据库损坏怎么办？**
- 停止服务：`systemctl stop repair-signup`
- 恢复备份：`cp /opt/backup/data_最新日期.db /opt/repair-signup/backend/data.db`
- 启动服务：`systemctl start repair-signup`
