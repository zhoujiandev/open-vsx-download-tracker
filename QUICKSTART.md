# 🚀 快速开始指南

5分钟内完成配置，开始追踪你的 Open-VSX 插件下载量！

## 📋 前置要求

- 一个 GitHub 账号
- 一个已发布到 Open-VSX 的插件
- 一个邮箱账号（用于发送和接收报告）

## 🎯 配置步骤

### 步骤 1：Fork 项目

1. 点击本页面右上角的 **Fork** 按钮
2. 等待 Fork 完成

### 步骤 2：找到你的插件信息

访问你的插件页面，例如：

```
https://open-vsx.org/extension/redhat/vscode-yaml
```

从 URL 中提取信息：
- **namespace**（命名空间）= `redhat`（第一个斜杠后的部分）
- **extension name**（插件名）= `vscode-yaml`（第二个斜杠后的部分）

### 步骤 3：准备邮箱配置

#### 使用 Gmail（推荐）

1. 访问 https://myaccount.google.com/security
2. 启用"两步验证"
3. 搜索"应用专用密码"（App passwords）
4. 创建新的应用专用密码：
   - 应用：选择"邮件"
   - 设备：选择"其他"，输入"VSX Tracker"
5. 记下生成的 16 位密码（格式：`xxxx xxxx xxxx xxxx`）

你需要的配置：
```
SMTP_SERVER: smtp.gmail.com
SMTP_PORT: 587
SENDER_EMAIL: 你的Gmail地址
SENDER_PASSWORD: 刚才生成的16位密码（去掉空格）
RECEIVER_EMAIL: 接收报告的邮箱（可以是同一个）
```

#### 使用 QQ 邮箱

1. 登录 QQ 邮箱
2. 设置 → 账户 → POP3/SMTP 服务
3. 开启 SMTP 服务
4. 发送短信获取授权码

你需要的配置：
```
SMTP_SERVER: smtp.qq.com
SMTP_PORT: 587
SENDER_EMAIL: 你的QQ邮箱
SENDER_PASSWORD: 获取的授权码
RECEIVER_EMAIL: 接收报告的邮箱
```

### 步骤 4：在 GitHub 添加 Secrets

1. 进入你 fork 的仓库
2. 点击 **Settings**（设置）
3. 左侧菜单选择 **Secrets and variables** → **Actions**
4. 点击 **New repository secret** 按钮
5. 依次添加以下 7 个 secrets：

| Name | Value | 示例 |
|------|-------|------|
| `EXTENSION_NAMESPACE` | 你的插件命名空间 | `redhat` |
| `EXTENSION_NAME` | 你的插件名称 | `vscode-yaml` |
| `SMTP_SERVER` | SMTP服务器地址 | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP端口 | `587` |
| `SENDER_EMAIL` | 发件人邮箱 | `your@gmail.com` |
| `SENDER_PASSWORD` | 邮箱密码/授权码 | `your-app-password` |
| `RECEIVER_EMAIL` | 收件人邮箱 | `your@gmail.com` |

**提示：** 每次添加一个 secret，点击 "Add secret" 后再添加下一个。

### 步骤 5：设置 GitHub Actions 权限

1. 在仓库设置中，点击左侧的 **Actions** → **General**
2. 滚动到最下方的 **Workflow permissions**
3. 选择 **Read and write permissions**
4. 勾选 **Allow GitHub Actions to create and approve pull requests**
5. 点击 **Save** 保存

### 步骤 6：启用 GitHub Actions

1. 点击仓库顶部的 **Actions** 标签
2. 如果看到提示，点击 **I understand my workflows, go ahead and enable them**
3. 在左侧找到 **Open-VSX Download Tracker** workflow

### 步骤 7：测试运行

1. 点击左侧的 **Open-VSX Download Tracker**
2. 点击右侧的 **Run workflow** 按钮
3. 点击绿色的 **Run workflow** 确认
4. 等待几秒钟，刷新页面
5. 点击新出现的运行记录查看进度

### 步骤 8：检查结果

运行完成后（大约 30 秒到 1 分钟）：

1. ✅ GitHub Actions 显示绿色勾号（成功）
2. 📧 你的邮箱收到下载量报告
3. 📁 仓库中出现 `download_history.json` 文件

如果失败了：
- 点击失败的运行记录
- 查看红色叉号的步骤
- 点击展开查看错误信息
- 参考 `config.example.md` 中的故障排查部分

## 🎊 完成！

配置成功后，系统会：

- ⏰ **每天早上 9:00**（北京时间）自动运行
- 📊 统计过去 24 小时的下载量增长
- 📧 发送漂亮的 HTML 邮件报告到你的邮箱
- 💾 自动保存历史数据

## 📱 接下来做什么？

### 查看历史数据

查看仓库中的 `download_history.json` 文件，可以看到每天的下载量记录。

### 修改运行时间

编辑 `.github/workflows/daily-tracker.yml`，修改 cron 表达式：

```yaml
schedule:
  - cron: '0 1 * * *'  # 当前是 UTC 1:00 (北京时间 9:00)
```

常用时间对照：
- `0 0 * * *` - 北京时间 8:00
- `0 1 * * *` - 北京时间 9:00（默认）
- `0 2 * * *` - 北京时间 10:00
- `30 1 * * *` - 北京时间 9:30

### 本地测试

```bash
# 克隆你的仓库
git clone https://github.com/你的用户名/open-vsx-download-tracker
cd open-vsx-download-tracker

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export EXTENSION_NAMESPACE=你的namespace
export EXTENSION_NAME=你的插件名
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SENDER_EMAIL=你的邮箱
export SENDER_PASSWORD=你的密码
export RECEIVER_EMAIL=接收邮箱

# 测试配置
python test_config.py

# 运行追踪器
python tracker.py
```

## ❓ 常见问题

### Q: 收不到邮件怎么办？

1. 检查垃圾邮件文件夹
2. 确认 Gmail 使用的是应用专用密码，不是登录密码
3. 查看 Actions 运行日志中的错误信息

### Q: 显示插件不存在？

1. 确认插件已发布到 Open-VSX
2. 访问 `https://open-vsx.org/extension/namespace/name` 确认可以访问
3. 检查 namespace 和 name 的拼写

### Q: Actions 无法提交文件？

1. 确认已设置 "Read and write permissions"
2. 重新运行 workflow

### Q: 想追踪多个插件怎么办？

可以 fork 多个仓库，每个仓库配置不同的插件信息。

## 🆘 需要帮助？

- 📖 查看详细文档：`README.md`
- ⚙️ 配置说明：`config.example.md`
- 🐛 遇到问题：提交 Issue

---

**祝你使用愉快！** 🎉

