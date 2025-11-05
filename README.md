# 📊 Open-VSX Download Tracker

一个自动追踪 Open-VSX 插件下载量的工具，通过 GitHub Actions 每日定时运行，统计过去 24 小时的下载增长并发送邮件报告。

## ✨ 功能特点

- 🔄 **自动化追踪**：通过 GitHub Actions 每天早上 9 点（北京时间）自动运行
- 📈 **增长统计**：计算过去 24 小时的下载量增长
- 📧 **邮件通知**：生成精美的 HTML 格式报告并发送到指定邮箱
- 💾 **历史记录**：自动保存历史数据，便于长期追踪
- 🎨 **可视化报告**：包含总下载量、新增下载量、增长率等关键指标

## 🚀 快速开始

### 1. Fork 本仓库

点击右上角的 Fork 按钮，将本项目 fork 到你的 GitHub 账户。

### 2. 配置 GitHub Secrets

在你的仓库中，进入 `Settings` → `Secrets and variables` → `Actions`，添加以下 Secrets：

#### 🔴 必需配置（最小配置）

| Secret 名称 | 说明 | 示例 |
|------------|------|------|
| `EXTENSION_NAMESPACE` | 插件的命名空间（发布者名称） | `redhat` |
| `EXTENSION_NAME` | 插件名称 | `vscode-yaml` |

#### 📧 可选配置（邮件通知）

如果需要每天收到邮件报告，还需要配置以下 Secrets：

| Secret 名称 | 说明 | 示例 |
|------------|------|------|
| `SMTP_SERVER` | SMTP 服务器地址 | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP 端口 | `587` |
| `SENDER_EMAIL` | 发件人邮箱 | `your-email@gmail.com` |
| `SENDER_PASSWORD` | 发件人邮箱密码或应用专用密码 | `your-app-password` |
| `RECEIVER_EMAIL` | 收件人邮箱 | `receiver@example.com` |

> 💡 **提示**：不配置邮件也能正常运行！数据会保存在 `download_history.json` 文件中，你可以随时在仓库中查看。

#### 📝 如何找到你的插件信息？

访问你的插件页面，例如：`https://open-vsx.org/extension/redhat/vscode-yaml`

- `EXTENSION_NAMESPACE` = `redhat`（URL 中 `/extension/` 后的第一部分）
- `EXTENSION_NAME` = `vscode-yaml`（URL 中的第二部分）

#### 🔐 Gmail 应用专用密码设置

如果使用 Gmail，需要生成应用专用密码：

1. 访问 [Google 账户安全设置](https://myaccount.google.com/security)
2. 启用两步验证
3. 在"应用专用密码"中生成新密码
4. 使用生成的密码作为 `SENDER_PASSWORD`

### 3. 设置 GitHub Actions 权限 ⚠️

**这一步非常重要！** 否则会遇到 403 权限错误。

1. 进入 `Settings` → `Actions` → `General`
2. 滚动到 **Workflow permissions**
3. 选择 ✅ **"Read and write permissions"**
4. 勾选 ✅ **"Allow GitHub Actions to create and approve pull requests"**
5. 点击 **Save** 保存

> 📖 详细图文教程：[PERMISSIONS_SETUP.md](PERMISSIONS_SETUP.md)

### 4. 启用 GitHub Actions

1. 进入仓库的 `Actions` 标签页
2. 如果 Actions 被禁用，点击 "I understand my workflows, go ahead and enable them"
3. 找到 "Open-VSX Download Tracker" workflow
4. 点击 "Enable workflow"

### 5. 手动测试（可选）

在 `Actions` 页面：

1. 选择 "Open-VSX Download Tracker" workflow
2. 点击 "Run workflow" 按钮
3. 点击 "Run workflow" 确认

这将立即运行一次追踪任务，你应该会收到一封测试邮件。

## 📅 运行时间

GitHub Actions 配置为每天 UTC 时间 1:00 AM 运行，即：

- 🇨🇳 北京时间：早上 9:00
- 🇺🇸 太平洋时间：下午 6:00（前一天）
- 🇪🇺 中欧时间：早上 2:00

如需修改时间，编辑 `.github/workflows/daily-tracker.yml` 中的 cron 表达式。

## 📧 邮件报告示例

邮件包含以下信息：

- 📦 插件名称
- 📊 当前总下载量
- 📈 过去 24 小时新增下载量
- 📉 增长率百分比
- 🔗 Open-VSX 插件页面链接

## 🛠️ 本地运行

### 安装依赖

```bash
pip install -r requirements.txt
```

### 设置环境变量

创建 `.env` 文件（或直接设置环境变量）：

```bash
export EXTENSION_NAMESPACE=your-namespace
export EXTENSION_NAME=your-extension-name
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SENDER_EMAIL=your-email@gmail.com
export SENDER_PASSWORD=your-app-password
export RECEIVER_EMAIL=receiver@example.com
```

### 运行脚本

```bash
python tracker.py
```

## 📁 项目结构

```
open-vsx-download-tracker/
├── .github/
│   └── workflows/
│       └── daily-tracker.yml    # GitHub Actions 工作流配置
├── tracker.py                   # 主程序脚本
├── requirements.txt             # Python 依赖
├── download_history.json        # 历史下载量数据（自动生成）
├── .gitignore                   # Git 忽略文件配置
└── README.md                    # 项目文档
```

## 📊 如何查看下载量数据

### 方式 1：查看历史数据文件（无需邮件配置）

每次运行后，数据会自动保存在仓库的 `download_history.json` 文件中：

```json
{
  "2025-11-01": 1000,
  "2025-11-02": 1050,
  "2025-11-03": 1120,
  "2025-11-04": 1180
}
```

你可以：
- 直接在 GitHub 仓库中查看该文件
- 下载后用 Excel 等工具分析
- 查看 Git 历史了解每天的变化

### 方式 2：查看 Actions 运行日志

进入 `Actions` → 选择任意一次运行 → 查看 "运行下载量追踪器" 步骤的输出：

```
昨日总下载量: 1,120
今日总下载量: 1,180
24小时新增: +60
```

### 方式 3：接收邮件报告（需配置邮件）

配置邮件后，每天会收到包含以下内容的精美 HTML 邮件：
- 📦 插件名称
- 📊 当前总下载量
- 📈 过去 24 小时新增
- 📉 增长率百分比

## 🔧 高级配置

### 修改运行时间

编辑 `.github/workflows/daily-tracker.yml`：

```yaml
schedule:
  - cron: '0 1 * * *'  # 修改这里的时间
```

Cron 表达式格式：`分钟 小时 日 月 星期`（UTC 时间）

### 自定义邮件模板

编辑 `tracker.py` 中的 `generate_report` 方法，修改 HTML 模板。

### 更换邮件服务商

常用 SMTP 配置：

| 服务商 | SMTP_SERVER | SMTP_PORT |
|--------|-------------|-----------|
| Gmail | smtp.gmail.com | 587 |
| Outlook | smtp-mail.outlook.com | 587 |
| QQ 邮箱 | smtp.qq.com | 587 |
| 163 邮箱 | smtp.163.com | 465 |
| 阿里云邮箱 | smtp.aliyun.com | 465 |

## 🐛 故障排查

### Actions 运行失败

1. 检查 Secrets 是否都正确配置
2. 查看 Actions 运行日志中的错误信息
3. 确认插件名称是否正确

### 未收到邮件

1. 检查邮件服务器配置是否正确
2. 查看垃圾邮件文件夹
3. 确认 SMTP 密码是否正确（Gmail 需使用应用专用密码）
4. 查看 Actions 日志中的邮件发送状态

### ValueError: invalid literal for int()

如果看到类似 `ValueError: invalid literal for int() with base 10: ''` 的错误：

1. **不需要邮件功能**：删除所有邮件相关的 Secrets（SMTP_SERVER、SMTP_PORT 等）
2. **需要邮件功能**：确保所有 5 个邮件 Secrets 都有正确的值，不能为空

### API 请求失败

1. 确认插件在 Open-VSX 上存在
2. 检查网络连接
3. 验证 `EXTENSION_NAMESPACE` 和 `EXTENSION_NAME` 是否正确

**更多问题**：查看 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## 📊 数据存储

历史下载量数据保存在 `download_history.json` 文件中，格式如下：

```json
{
  "2025-11-01": 1000,
  "2025-11-02": 1050,
  "2025-11-03": 1120
}
```

该文件会在每次运行后自动更新并提交到仓库。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🌟 相关链接

- [Open-VSX Registry](https://open-vsx.org/)
- [Open-VSX API 文档](https://github.com/eclipse/openvsx/wiki/Using-the-VS-Code-Extensions-Namespace)
- [GitHub Actions 文档](https://docs.github.com/en/actions)

---

**如果这个项目对你有帮助，请给个 ⭐️ Star！**
