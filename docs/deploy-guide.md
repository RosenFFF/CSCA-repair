# 义务维修报名系统 — 华为云服务器部署教程

## 适用环境

- 服务器：华为云 ECS（推荐 1核2G 即可，20 人以内完全够用）
- 操作系统：Ubuntu 22.04 / CentOS 7+ 均可
- 本教程以 **Ubuntu 22.04** 为例
- 假设你已经有一个 Vue + FastAPI 项目在服务器上运行

---

## 第零步：检查服务器现有环境

连接服务器后，先确认当前状况：

```bash
# 查看系统信息
cat /etc/os-release

# 查看已安装的 Python 版本
python3 --version

# 查看已安装的 Node.js 版本（如果有）
node --version

# 查看当前正在运行的服务
systemctl list-units --type=service --state=running

# 查看哪些端口已被占用
netstat -tlnp
```

记录下已占用的端口（比如已有项目用的是 8000），后面新项目需要用一个**不同的端口**。

> **推荐：** 新项目使用 **8001** 端口，避免和已有项目冲突。

---

## 第一步：连接服务器

```bash
ssh root@你的服务器公网IP
```

输入密码后进入服务器终端。

---

## 第二步：确认 Python 环境

因为你之前已经部署过 Python 项目，大概率已经有 Python 和 pip 了，直接检查：

```bash
python3 --version
pip3 --version
```

如果版本 >= 3.10 就不用再装了。如果没装或者版本太低：

```bash
apt update && apt upgrade -y
apt install python3 python3-pip python3-venv -y
```

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

> **注意：** 路径 `/opt/repair-signup` 和你已有项目的路径是分开的，互不影响。

---

## 第四步：创建独立的虚拟环境

**每个项目的虚拟环境必须独立**，这样依赖不会冲突：

```bash
cd /opt/repair-signup/backend

# 创建独立的虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装这个项目自己的依赖
pip install -r requirements.txt

# 确认安装成功
pip list
```

> **为什么要独立虚拟环境？** 你已有项目的依赖可能和这个项目的版本不同。比如已有项目用的是 FastAPI 0.100，这个项目用的是 0.115，装在同一个环境里会互相覆盖导致出问题。虚拟环境就是给每个项目一个独立的"小房间"。

安装完后退出虚拟环境：

```bash
deactivate
```

---

## 第五步：配置环境变量

```bash
cd /opt/repair-signup/backend
cp .env.example .env
nano .env
```

修改内容：

```
ADMIN_PASSWORD=你的管理员密码
JWT_SECRET=换成一个随机字符串
```

**关于随机字符串：** 可以用以下命令生成：

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

把输出的字符串填到 `JWT_SECRET=` 后面。

保存退出（`Ctrl+O` → 回车 → `Ctrl+X`）。

---

## 第六步：构建前端

### 检查 Node.js

```bash
node --version
npm --version
```

如果已有 Node.js 且版本 >= 18 就不用装了。如果没有或版本太低：

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install nodejs -y
```

### 构建前端

```bash
cd /opt/repair-signup/frontend

# 安装依赖
npm install

# 构建生产版本
npm run build
```

构建完成后 `frontend/dist/` 目录就是前端静态文件，后端会自动托管。

确认构建成功：

```bash
ls -la dist/
```

应该能看到 `index.html` 和 `assets/` 目录。

---

## 第七步：测试运行

```bash
cd /opt/repair-signup/backend
source venv/bin/activate
python3 -m uvicorn main:app --host 0.0.0.0 --port 8001
```

> **这里用 8001 端口**，避免和你已有项目的 8000 端口冲突。如果你已有项目用的不是 8000，就选一个没被占用的端口。

打开浏览器访问 `http://你的服务器公网IP:8001`，确认能正常打开。

- 报名页：`http://你的服务器公网IP:8001/`
- 管理后台：`http://你的服务器公网IP:8001/admin`
- API 文档：`http://你的服务器公网IP:8001/docs`

测试完成后按 `Ctrl+C` 停止。

---

## 第八步：设置开机自启（systemd）

因为你已经有 systemd 服务了，再加一个**完全不会冲突**，它们是独立的服务文件。

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
ExecStart=/opt/repair-signup/backend/venv/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8001
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

> **注意 `ExecStart` 里的端口是 8001**，和第七步保持一致。如果你选了其他端口，这里也要改。

启用并启动服务：

```bash
# 重新加载 systemd 配置
systemctl daemon-reload

# 设置开机自启
systemctl enable repair-signup

# 启动服务
systemctl start repair-signup
```

检查状态：

```bash
systemctl status repair-signup
```

看到 `active (running)` 就成功了。

### 确认两个服务都在运行

```bash
# 查看你已有的服务
systemctl status 你的已有服务名

# 查看新服务
systemctl status repair-signup

# 确认两个端口都在监听
netstat -tlnp | grep -E "8000|8001"
```

---

## 第九步：开放防火墙端口

### 华为云安全组

1. 登录华为云控制台
2. 进入 ECS 实例 → 安全组
3. 添加入站规则：
   - 协议：TCP
   - 端口：**8001**
   - 来源：0.0.0.0/0

> 如果你之前已经放行了 8000 端口，只需要**再加一条 8001 的规则**就行，已有的规则不用动。

### 服务器防火墙（如果有）

```bash
ufw allow 8001/tcp
ufw reload
```

---

## 第十步：访问系统

| 页面 | 地址 |
|------|------|
| 报名页 | `http://你的服务器公网IP:8001/` |
| 管理后台 | `http://你的服务器公网IP:8001/admin` |
| API 文档 | `http://你的服务器公网IP:8001/docs` |

分享给部员的报名链接：`http://你的服务器公网IP:8001/`

---

## 两个项目共存对比

| 项目 | 服务名 | 端口 | 路径 |
|------|--------|------|------|
| 已有项目 | 你的已有服务名 | 8000 | 你的已有路径 |
| 义务维修系统 | repair-signup | 8001 | /opt/repair-signup |

两个项目互不干扰，各自有独立的：
- 代码目录
- Python 虚拟环境
- systemd 服务
- 端口号

---

## 常用运维命令

```bash
# ===== 义务维修系统 =====

# 查看服务状态
systemctl status repair-signup

# 启动/停止/重启
systemctl start repair-signup
systemctl stop repair-signup
systemctl restart repair-signup

# 查看实时日志（调试用）
journalctl -u repair-signup -f

# 查看最近 50 行日志
journalctl -u repair-signup -n 50

# 确认端口在监听
netstat -tlnp | grep 8001

# ===== 你已有的项目 =====

# 同样可以用这些命令，只是把 repair-signup 换成你的服务名
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

数据库文件位于 `/opt/repair-signup/backend/data.db`。

### 手动备份

```bash
mkdir -p /opt/backup
cp /opt/repair-signup/backend/data.db /opt/backup/repair_$(date +%Y%m%d).db
```

### 自动备份（crontab 每天凌晨 2 点）

```bash
crontab -e
```

在打开的编辑器末尾添加：

```
0 2 * * * cp /opt/repair-signup/backend/data.db /opt/backup/repair_$(date +\%Y\%m\%d).db
```

保存退出。

---

## 常见问题

**Q: 访问不了怎么办？**

按顺序排查：

1. **检查服务是否运行：**
   ```bash
   systemctl status repair-signup
   ```
   如果不是 `active (running)`，查看日志找原因：
   ```bash
   journalctl -u repair-signup -n 50
   ```

2. **检查端口是否在监听：**
   ```bash
   netstat -tlnp | grep 8001
   ```
   如果没有输出，说明服务没启动或绑错了端口。

3. **检查华为云安全组：**
   确认已放行 8001 端口（TCP 协议，来源 0.0.0.0/0）。

4. **检查服务器防火墙：**
   ```bash
   ufw status
   ```
   如果是 `active`，确认已放行 8001。

**Q: 端口被占用怎么办？**

```bash
# 查看谁在用这个端口
netstat -tlnp | grep 8001

# 换一个端口，比如 8002
# 修改 uvicorn 启动命令中的 --port 参数
# 修改 systemd 服务文件中的 --port
# 修改华为云安全组规则
```

**Q: 忘记管理员密码怎么办？**

```bash
nano /opt/repair-signup/backend/.env
# 修改 ADMIN_PASSWORD=新密码
systemctl restart repair-signup
```

**Q: 数据库损坏怎么办？**

```bash
# 停止服务
systemctl stop repair-signup

# 恢复备份
cp /opt/backup/repair_最新日期.db /opt/repair-signup/backend/data.db

# 启动服务
systemctl start repair-signup
```

**Q: 两个项目会不会互相影响？**

不会。每个项目有独立的：
- 代码目录（`/opt/repair-signup` vs 你的已有项目路径）
- Python 虚拟环境（各自的 `venv/`）
- systemd 服务文件（`repair-signup.service` vs 你的已有服务）
- 端口号（8001 vs 8000）
- 数据库文件（各自的 `data.db`）

**Q: 服务器内存不够用怎么办？**

1核2G 跑两个轻量项目一般没问题。如果确实紧张：
- 检查内存使用：`free -h`
- 检查各服务占用：`ps aux --sort=-%mem | head -10`
- 考虑升级到 2核4G
