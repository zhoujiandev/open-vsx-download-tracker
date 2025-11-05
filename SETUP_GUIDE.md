# 📖 完整设置指南

本指南涵盖从最小配置到完整功能的所有设置步骤。

## 目录

- [方案 A：最小配置（推荐新手）](#方案-a最小配置推荐新手)
- [方案 B：完整配置（含邮件通知）](#方案-b完整配置含邮件通知)
- [GitHub Actions 权限设置](#github-actions-权限设置)
- [配置项详解](#配置项详解)
- [本地测试](#本地测试)

---

## 方案 A：最小配置（推荐新手）

⚡ 只需 **2 个配置项**，30 秒完成！

### 优势

- ✅ 配置简单，快速上手
- ✅ 无需邮箱账号
- ✅ 数据永久保存在 GitHub
- ✅ 随时可以查看历史趋势
- ✅ 以后可以随时添加邮件功能

### 配置步骤

#### 1. Fork 本仓库

点击页面右上角的 **Fork** 按钮

#### 2. 找到你的插件信息

访问你的插件页面，例如：

```
https://open-vsx.org/extension/redhat/vscode-yaml
                                 ↑         ↑
                           namespace  extension name
```

- `EXTENSION_NAMESPACE` = `redhat`
- `EXTENSION_NAME` = `vscode-yaml`

#### 3. 添加 GitHub Secrets

1. 进入你 fork 的仓库
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加以下 2 个 Secrets：

| Name | Value | 你的值 |
|------|-------|--------|
| `EXTENSION_NAMESPACE` | 你的插件命名空间 | 如：`redhat` |
| `EXTENSION_NAME` | 你的插件名称 | 如：`vscode-yaml` |

⚠️ **注意**：Secret 名称必须完全匹配，区分大小写！

#### 4. 设置 Actions 权限 ⭐ 重要！

参见下方 [GitHub Actions 权限设置](#github-actions-权限设置)

#### 5. 启用并测试

1. 进入 **Actions** 标签
2. 如果看到提示，点击 "I understand my workflows, go ahead and enable them"
3. 选择 "Open-VSX Download Tracker"
4. 点击 **Run workflow** → **Run workflow** 测试

#### 6. 查看结果

运行成功后（约 30 秒）：

**✅ 成功标志：**
- Actions 显示绿色勾号 ✓
- 仓库中出现 `download_history.json` 文件
- Git 历史中有来自 `github-actions[bot]` 的提交

**📊 查看数据的 2 种方式：**

1. **查看历史文件**：打开 `download_history.json`
   ```json
   {
     "2025-11-05": 1000,
     "2025-11-06": 1050,
     "2025-11-07": 1120
   }
   ```

2. **查看 Actions 日志**：Actions → 选择运行记录 → 查看输出
   ```
   ✓ 成功获取下载量: 1,120
   昨日总下载量: 1,050
   今日总下载量: 1,120
   24小时新增: +70
   ```

🎉 **完成！** 现在每天早上 9 点（北京时间）会自动运行并更新数据。

---

## 方案 B：完整配置（含邮件通知）

在方案 A 的基础上，添加邮件通知功能。

### 前置要求

- 已完成方案 A 的基础配置
- 一个邮箱账号（用于发送报告）

### 邮件配置

需要额外添加 **5 个 Secrets**：

| Secret 名称 | 说明 | 示例值 |
|------------|------|--------|
| `SMTP_SERVER` | SMTP 服务器地址 | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP 端口 | `587` |
| `SENDER_EMAIL` | 发件人邮箱 | `your@gmail.com` |
| `SENDER_PASSWORD` | 邮箱密码或授权码 | `应用专用密码` |
| `RECEIVER_EMAIL` | 收件人邮箱 | `your@gmail.com` |

⚠️ **重要提示**：
- 要么全部配置完整，要么全部不配置
- 如果不需要邮件，**不要添加**这些 Secrets
- 如果已添加但值为空，请**删除**它们

### 常用邮箱配置

#### 使用 Gmail（推荐）

**1. 生成应用专用密码**

Gmail **必须**使用应用专用密码，不能使用登录密码！

**方法 1（推荐）：直接访问**
1. 访问 https://myaccount.google.com/apppasswords
2. 登录你的 Google 账号
3. 如果提示需要启用两步验证，请先启用
4. 输入应用名称（如 "Open-VSX Tracker"）
5. 点击"创建"
6. 复制生成的 16 位密码（格式：`abcd efgh ijkl mnop`）

**方法 2：通过安全设置**
1. 访问 https://myaccount.google.com/security
2. 启用"两步验证"（2-Step Verification）
3. 找到"应用专用密码"（App passwords）
4. 按照方法 1 的步骤 4-6 操作

**2. 配置 Secrets**

```
SMTP_SERVER: smtp.gmail.com
SMTP_PORT: 587
SENDER_EMAIL: your-email@gmail.com
SENDER_PASSWORD: abcdefghijklmnop （去掉空格的16位密码）
RECEIVER_EMAIL: your-email@gmail.com （可以是同一个）
```

#### 使用 QQ 邮箱

**1. 获取授权码**

1. 登录 QQ 邮箱
2. 设置 → 账户 → POP3/IMAP/SMTP 服务
3. 开启 "SMTP 服务"
4. 发送短信获取授权码
5. 保存授权码

**2. 配置 Secrets**

```
SMTP_SERVER: smtp.qq.com
SMTP_PORT: 587
SENDER_EMAIL: your@qq.com
SENDER_PASSWORD: 获取的授权码
RECEIVER_EMAIL: your@qq.com
```

#### 使用其他邮箱

| 邮件服务商 | SMTP_SERVER | SMTP_PORT |
|-----------|-------------|-----------|
| Outlook/Hotmail | smtp-mail.outlook.com | 587 |
| 163 邮箱 | smtp.163.com | 465 |
| 126 邮箱 | smtp.126.com | 465 |
| 阿里云企业邮箱 | smtp.aliyun.com | 465 |
| 腾讯企业邮箱 | smtp.exmail.qq.com | 587 |

### 邮件报告示例

配置成功后，每天会收到包含以下内容的 HTML 邮件：

- 📦 插件名称（namespace/name）
- 📊 当前总下载量
- 📈 过去 24 小时新增下载量
- 📉 增长率百分比
- 🔗 Open-VSX 插件页面链接

---

## GitHub Actions 权限设置

### ⚠️ 为什么需要设置？

如果不设置此权限，会遇到 **403 错误**，导致无法自动保存 `download_history.json` 文件。

### 设置步骤（重要！）

#### 1. 进入仓库设置

点击仓库顶部的 **Settings** 按钮

```
仓库页面顶部导航
├── Code
├── Issues
├── Pull requests
├── Actions
└── Settings  ← 点击这里
```

#### 2. 找到 Actions 设置

左侧菜单：

```
Settings 菜单
├── General
├── Access
│   └── Collaborators
├── Code and automation
│   ├── Branches
│   ├── Actions  ← 点击这里
│   │   └── General  ← 然后点击这里
│   └── Webhooks
```

#### 3. 滚动到页面底部

找到 **Workflow permissions** 区域

#### 4. 选择正确的权限

你会看到两个选项：

```
( ) Read repository contents and packages permissions
    ↑ 默认选项，但不够用！

(●) Read and write permissions  ← 选择这个！
    ↑ 允许 Actions 推送代码
```

**必须选择：** ✅ **Read and write permissions**

#### 5. 勾选额外选项

```
[✓] Allow GitHub Actions to create and approve pull requests
    ↑ 也要勾选这个
```

#### 6. 保存设置

点击绿色的 **Save** 按钮

### 验证设置

**方法 1：检查设置页面**

返回 Settings → Actions → General，确认：
- ✅ "Read and write permissions" 已选中
- ✅ "Allow GitHub Actions to create and approve pull requests" 已勾选

**方法 2：运行 Workflow 测试**

1. Actions → "Open-VSX Download Tracker" → Run workflow
2. 等待运行完成

**成功标志：**
- ✅ Actions 显示绿色勾号
- ✅ 仓库中出现/更新 `download_history.json`
- ✅ Git 历史中有 `github-actions[bot]` 的提交

**失败标志：**
- ❌ 错误信息包含 "Permission denied" 或 "403"
- ❌ 没有自动创建 `download_history.json`

### 安全性说明

**Q: 这个权限安全吗？**

✅ **完全安全：**
- 只授予你自己仓库的 Actions
- Actions 只能修改你的仓库，无法访问其他仓库
- 代码开源，可以查看它做了什么
- 可以随时在 Actions 页面查看所有运行记录

---

## 配置项详解

### 必需配置项

#### EXTENSION_NAMESPACE（插件命名空间）

**说明：** 你的插件发布者名称

**如何查找：**
1. 访问你的插件页面：`https://open-vsx.org/extension/redhat/vscode-yaml`
2. URL 中 `/extension/` 后的第一部分就是 namespace
3. 在上面的例子中，值为 `redhat`

**示例值：**
- `redhat`
- `microsoft`
- `vscode`

#### EXTENSION_NAME（插件名称）

**说明：** 你的插件的具体名称

**如何查找：**
1. 在同样的插件页面 URL 中
2. `/extension/` 后的第二部分就是插件名称
3. 在 `https://open-vsx.org/extension/redhat/vscode-yaml` 中，值为 `vscode-yaml`

**示例值：**
- `vscode-yaml`
- `python`
- `prettier-vscode`

### 可选配置项（邮件）

#### SMTP_SERVER（邮件服务器）

**说明：** SMTP 服务器地址

**常用值：**
- Gmail: `smtp.gmail.com`
- QQ: `smtp.qq.com`
- Outlook: `smtp-mail.outlook.com`
- 163: `smtp.163.com`

#### SMTP_PORT（邮件端口）

**说明：** SMTP 服务器端口号

**常用值：**
- `587` - TLS 加密（推荐，大多数服务器支持）
- `465` - SSL 加密（某些服务器使用）
- `25` - 无加密（不推荐，可能被屏蔽）

#### SENDER_EMAIL（发件人邮箱）

**说明：** 用于发送邮件的邮箱地址

**注意事项：**
- 必须与 SMTP 服务器匹配
- 需要开启 SMTP 发送权限

**示例：**
- `your-email@gmail.com`
- `myname@outlook.com`

#### SENDER_PASSWORD（发件人密码）

**说明：** 邮箱的密码或应用专用密码

**重要：**
- Gmail 必须使用"应用专用密码"
- QQ 邮箱、163 邮箱等需要使用"授权码"
- 不是邮箱的登录密码！

#### RECEIVER_EMAIL（收件人邮箱）

**说明：** 接收下载量报告的邮箱地址

**注意：**
- 可以与发件人邮箱相同
- 可以是任何有效的邮箱地址

---

## 本地测试

### 安装依赖

```bash
pip install -r requirements.txt
```

### 设置环境变量

**macOS/Linux:**

```bash
# 必需配置
export EXTENSION_NAMESPACE=mycompany
export EXTENSION_NAME=awesome-extension

# 可选：邮件配置
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SENDER_EMAIL=myemail@gmail.com
export SENDER_PASSWORD="your-app-password"
export RECEIVER_EMAIL=myemail@gmail.com

# 测试配置
python test_config.py

# 运行追踪器
python tracker.py
```

**Windows (PowerShell):**

```powershell
# 必需配置
$env:EXTENSION_NAMESPACE="mycompany"
$env:EXTENSION_NAME="awesome-extension"

# 可选：邮件配置
$env:SMTP_SERVER="smtp.gmail.com"
$env:SMTP_PORT="587"
$env:SENDER_EMAIL="myemail@gmail.com"
$env:SENDER_PASSWORD="your-app-password"
$env:RECEIVER_EMAIL="myemail@gmail.com"

# 测试配置
python test_config.py

# 运行追踪器
python tracker.py
```

### 配置测试工具

使用 `test_config.py` 验证配置：

```bash
# 测试基本配置（不发送邮件）
python test_config.py

# 测试完整配置（包括发送测试邮件）
python test_config.py
```

---

## 高级配置

### 修改运行时间

编辑 `.github/workflows/daily-tracker.yml`：

```yaml
schedule:
  - cron: '0 1 * * *'  # 修改这里
```

**常用时间对照（UTC → 北京时间）：**
- `0 0 * * *` - 北京时间 8:00
- `0 1 * * *` - 北京时间 9:00（默认）
- `0 2 * * *` - 北京时间 10:00
- `30 1 * * *` - 北京时间 9:30
- `0 12 * * *` - 北京时间 20:00

**Cron 表达式格式：** `分钟 小时 日 月 星期`（UTC 时间）

### 追踪多个插件

为每个插件创建一个独立的 fork 仓库，分别配置不同的 `EXTENSION_NAMESPACE` 和 `EXTENSION_NAME`。

---

## 完整配置示例

假设你的插件是 `https://open-vsx.org/extension/mycompany/awesome-extension`，使用 Gmail：

```
EXTENSION_NAMESPACE: mycompany
EXTENSION_NAME: awesome-extension
SMTP_SERVER: smtp.gmail.com
SMTP_PORT: 587
SENDER_EMAIL: myemail@gmail.com
SENDER_PASSWORD: abcdefghijklmnop
RECEIVER_EMAIL: myemail@gmail.com
```

---

## 🆘 遇到问题？

查看 [故障排查指南](TROUBLESHOOTING.md) 获取帮助。

---

**设置完成后，你就可以享受自动化的下载量追踪了！** 🎉

