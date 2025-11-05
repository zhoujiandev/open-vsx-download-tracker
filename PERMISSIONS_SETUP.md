# 🔑 GitHub Actions 权限设置指南

## ⚠️ 重要：必须设置权限

如果不设置此权限，会遇到 **403 错误**，导致无法自动保存下载历史数据。

## 📋 设置步骤（图文详解）

### 1. 进入仓库设置

点击仓库顶部的 **Settings**（设置）按钮

```
你的仓库页面
├── Code
├── Issues
├── Pull requests
├── Actions
└── Settings  ← 点击这里
```

### 2. 找到 Actions 设置

在左侧菜单中：

```
Settings 菜单
├── General
├── Access
│   ├── Collaborators
│   └── Moderation
├── Code and automation
│   ├── Branches
│   ├── Tags
│   ├── Actions  ← 点击这里
│   │   └── General  ← 然后点击这里
│   └── Webhooks
```

### 3. 滚动到页面底部

找到 **Workflow permissions** 区域

### 4. 选择正确的权限

你会看到两个选项：

```
( ) Read repository contents and packages permissions
    ↑ 这是默认选项，但不够用！

(●) Read and write permissions  ← 选择这个！
    ↑ 允许 Actions 推送代码
```

**选择：** ✅ **Read and write permissions**

### 5. 勾选额外选项

在下方还有一个复选框：

```
[✓] Allow GitHub Actions to create and approve pull requests
    ↑ 也要勾选这个
```

### 6. 保存设置

点击绿色的 **Save** 按钮

## ✅ 验证设置是否生效

### 方法 1：检查设置页面

返回 Settings → Actions → General，确认：
- ✅ "Read and write permissions" 已选中
- ✅ "Allow GitHub Actions to create and approve pull requests" 已勾选

### 方法 2：运行 Workflow

1. 进入 **Actions** 标签
2. 选择 "Open-VSX Download Tracker"
3. 点击 "Run workflow"
4. 等待运行完成

**成功的标志：**
- ✅ Actions 显示绿色勾号
- ✅ 仓库中出现 `download_history.json` 文件
- ✅ Git 历史中有来自 `github-actions[bot]` 的提交

**失败的标志：**
- ❌ 错误信息包含 "Permission denied" 或 "403"
- ❌ 没有自动创建 `download_history.json` 文件

## 🔍 常见问题

### Q: 为什么需要这个权限？

**A:** 程序需要自动将 `download_history.json` 文件提交到仓库保存，这需要写入权限。

### Q: 这个权限安全吗？

**A:** 
- ✅ 安全。这个权限只授予你自己仓库的 Actions
- ✅ Actions 只能修改你的仓库，不能访问其他仓库
- ✅ 代码是开源的，你可以查看它做了什么
- ✅ 你可以随时在 Actions 页面查看所有运行记录

### Q: 我不想授予写入权限怎么办？

**A:** 有两个替代方案：

**方案 1：手动查看数据**
- 不授予权限
- 修改 workflow，删除 `git push` 步骤
- 只在 Actions 日志中查看数据（不保存历史）

**方案 2：使用 Artifacts**
- 使用 GitHub Actions Artifacts 上传文件
- 需要修改 workflow（我可以帮你）
- 数据保存 90 天后自动删除

### Q: 设置后仍然报错怎么办？

**检查清单：**

1. ✅ 确认选择了 "Read and write permissions"
2. ✅ 确认勾选了 "Allow GitHub Actions to..."
3. ✅ 确认点击了 Save 按钮
4. ✅ 尝试重新运行 workflow
5. ✅ 查看 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) 获取更多帮助

## 📸 期望的设置截图描述

应该看到：

```
Workflow permissions

Choose the default permissions granted to the GITHUB_TOKEN when 
running workflows in this repository.

(●) Read and write permissions
    Workflows have read and write permissions in the repository 
    for all scopes.

( ) Read repository contents and packages permissions
    Workflows have read permissions in the repository for the 
    contents and packages scopes only.

[✓] Allow GitHub Actions to create and approve pull requests

                                          [Cancel] [Save]
```

## 🆘 需要帮助？

如果按照以上步骤设置后仍有问题：

1. 查看 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) 
2. 在 GitHub 上提交 Issue
3. 确保提供完整的错误日志

---

**设置完成后，你就可以享受自动化的下载量追踪了！** 🎉

