# ⚡ 最小配置指南

只需 **2 个配置项**即可运行！

## 🎯 最小配置（无需邮箱）

### 必需的 2 个 GitHub Secrets

1. **EXTENSION_NAMESPACE** - 你的插件命名空间
2. **EXTENSION_NAME** - 你的插件名称

### 如何获取这 2 个值？

访问你的插件页面，例如：
```
https://open-vsx.org/extension/redhat/vscode-yaml
                                 ↑         ↑
                           namespace  extension name
```

- `EXTENSION_NAMESPACE` = `redhat`
- `EXTENSION_NAME` = `vscode-yaml`

### 配置步骤

1. **Fork 本仓库**

2. **添加 Secrets**
   - 进入 Settings → Secrets and variables → Actions
   - 添加 2 个 Secrets：
     - Name: `EXTENSION_NAMESPACE`，Value: 你的 namespace
     - Name: `EXTENSION_NAME`，Value: 你的插件名

3. **设置 Actions 权限** ⚠️ 重要！
   - Settings → Actions → General
   - 滚动到 "Workflow permissions"
   - 选择 ✅ "Read and write permissions"
   - 勾选 ✅ "Allow GitHub Actions to create and approve pull requests"
   - 点击 Save

4. **手动运行测试**
   - 进入 Actions 标签
   - 选择 workflow 并手动运行一次

### 数据查看方式

运行成功后，查看下载量数据有 2 种方式：

#### 方式 1：查看历史文件

打开仓库中的 `download_history.json`：

```json
{
  "2025-11-05": 1000,
  "2025-11-06": 1050,
  "2025-11-07": 1120
}
```

#### 方式 2：查看 Actions 日志

进入 Actions → 选择运行记录 → 查看输出：

```
✓ 成功获取下载量: 1120
昨日总下载量: 1,050
今日总下载量: 1,120
24小时新增: +70
```

## 📧 想要邮件通知？

如果以后想收邮件，随时可以添加这 5 个 Secrets：

- `SMTP_SERVER`
- `SMTP_PORT`
- `SENDER_EMAIL`
- `SENDER_PASSWORD`
- `RECEIVER_EMAIL`

⚠️ **重要提示**：
- 如果不需要邮件功能，**不要添加**这些 Secrets
- 如果已经添加了但值为空，请**删除**它们
- 要么全部配置完整，要么全部不配置

详细配置方法见 [config.example.md](config.example.md)

## ✅ 优势

**最小配置的好处：**
- ✅ 配置简单，30 秒搞定
- ✅ 无需邮箱账号
- ✅ 数据永久保存在 GitHub
- ✅ 随时可以查看历史趋势
- ✅ 以后可以随时添加邮件功能

## 🚀 立即开始

只需 3 步：

1. **Fork** 本仓库
2. **添加** 2 个 Secrets（插件信息）
3. **运行** workflow 测试

就这么简单！🎉

---

**完整文档**：[README.md](README.md) | **快速开始**：[QUICKSTART.md](QUICKSTART.md)

