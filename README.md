# 📊 Open-VSX Download Tracker

自动追踪 Open-VSX 插件下载量的工具，通过 GitHub Actions 每日定时运行，记录精确时间戳的下载量数据，统计增长并支持邮件通知（可选）。

## ✨ 功能特点

- 🔄 **自动化追踪**：GitHub Actions 每天定时自动运行
- 📈 **增长统计**：计算距离上次统计的下载量增长（灵活时间间隔）
- 📧 **邮件通知**：可选的精美 HTML 格式邮件报告
- 💾 **历史记录**：自动保存在 `download_history.json`，精确到秒的时间戳记录
- 🎨 **数据可视化**：总下载量、新增量、增长率、时间间隔等关键指标
- 🕐 **北京时间**：所有时间显示均使用北京时间（UTC+8）

## 🚀 30秒快速开始

### 1. Fork 本仓库

点击右上角的 **Fork** 按钮

### 2. 配置最小必需项（2个）

进入 `Settings` → `Secrets and variables` → `Actions`，添加：

| Secret 名称 | 说明 | 如何获取 |
|------------|------|---------|
| `EXTENSION_NAMESPACE` | 插件命名空间 | 访问你的插件页面 `https://open-vsx.org/extension/[namespace]/[name]`<br>取第一部分，如 `redhat` |
| `EXTENSION_NAME` | 插件名称 | 取第二部分，如 `vscode-yaml` |

### 3. 设置 Actions 权限 ⚠️

`Settings` → `Actions` → `General` → 滚动到底部：
- ✅ 选择 **"Read and write permissions"**
- ✅ 勾选 **"Allow GitHub Actions to create and approve pull requests"**
- 点击 **Save**

### 4. 启用并测试

1. 进入 `Actions` 标签
2. 启用 Workflows（如果被禁用）
3. 选择 "Open-VSX Download Tracker" → `Run workflow` 手动测试

✅ **完成！** 数据将保存在 `download_history.json`，每天自动更新。

## 📊 如何查看数据

### 方式 1：查看历史文件（推荐）

打开仓库中的 `download_history.json`（带时分秒的时间戳）：

```json
{
  "2025-11-01 05:00:15": "1000",
  "2025-11-02 05:00:23": "1050",
  "2025-11-03 05:00:18": "1120"
}
```

### 方式 2：查看 Actions 日志

`Actions` → 选择运行记录 → 查看输出：

```
✓ 成功获取下载量: 1180
上次统计时间: 2025-11-02 05:00:23
上次总下载量: 1,120
当前总下载量: 1,180
新增下载量: +60
```

### 方式 3：接收邮件报告（需额外配置）

如需每天收到邮件通知，查看 [完整设置指南](SETUP_GUIDE.md#邮件配置)

## 📅 运行时间

默认每天 **UTC 21:00**（北京时间 05:00）自动运行。

修改时间：编辑 `.github/workflows/daily-tracker.yml` 中的 cron 表达式。

**注意**：统计的是"距离上次统计的增长"而非固定24小时，首次运行或手动触发可能导致不同的统计间隔。

## 📚 文档导航

- 📖 **[完整设置指南](SETUP_GUIDE.md)** - 详细配置说明（包括邮件配置）
- 🔧 **[故障排查](TROUBLESHOOTING.md)** - 遇到问题时查看

## 🛠️ 本地测试

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量（必需）
export EXTENSION_NAMESPACE=your-namespace
export EXTENSION_NAME=your-extension-name

# 运行
python tracker.py
```

## 📁 项目结构

```
open-vsx-download-tracker/
├── .github/workflows/
│   └── daily-tracker.yml      # GitHub Actions 配置
├── tracker.py                 # 主程序
├── test_config.py             # 配置测试工具
├── requirements.txt           # Python 依赖
├── download_history.json      # 历史数据（自动生成）
├── README.md                  # 本文档
├── SETUP_GUIDE.md            # 详细设置指南
└── TROUBLESHOOTING.md        # 故障排查
```

## 💡 常见问题

<details>
<summary><b>Q: 必须配置邮件吗？</b></summary>

不需要！只配置 2 个必需项（插件信息）即可运行，数据保存在 `download_history.json`。
</details>

<details>
<summary><b>Q: GitHub Actions 报 403 错误？</b></summary>

需要设置 Actions 权限为 "Read and write permissions"。详见[故障排查](TROUBLESHOOTING.md#错误-2github-actions-权限错误-403)
</details>

<details>
<summary><b>Q: 如何添加邮件通知？</b></summary>

查看 [完整设置指南](SETUP_GUIDE.md#邮件配置)，需要额外配置 5 个邮件相关的 Secrets。
</details>

<details>
<summary><b>Q: 可以追踪多个插件吗？</b></summary>

可以！为每个插件 Fork 一个独立的仓库，分别配置不同的插件信息。
</details>

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 🌟 相关链接

- [Open-VSX Registry](https://open-vsx.org/)
- [Open-VSX API 文档](https://github.com/eclipse/openvsx/wiki)
- [GitHub Actions 文档](https://docs.github.com/en/actions)

---

**如果这个项目对你有帮助，请给个 ⭐️ Star！**
