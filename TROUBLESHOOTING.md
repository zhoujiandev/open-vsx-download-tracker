# 🔧 故障排查指南

遇到问题？本指南帮你快速定位和解决常见错误。

## 📋 目录

- [常见错误](#常见错误)
  - [错误 1：ValueError - 空端口号](#错误-1valueerror---空端口号)
  - [错误 2：GitHub Actions 权限错误 (403)](#错误-2github-actions-权限错误-403)
  - [错误 3：插件不存在 (404)](#错误-3插件不存在-404)
  - [错误 4：SMTP 认证失败](#错误-4smtp-认证失败)
  - [错误 5：收不到邮件](#错误-5收不到邮件)
  - [错误 6：环境变量未设置](#错误-6环境变量未设置)
- [调试技巧](#调试技巧)
- [提交 Issue 指南](#提交-issue-指南)

---

## 常见错误

### 错误 1：ValueError - 空端口号

**错误信息：**
```
ValueError: invalid literal for int() with base 10: ''
```

**原因：**
添加了 `SMTP_PORT` Secret 但值为空，或者只配置了部分邮件 Secrets。

**解决方案：**

**方案 A：删除邮件配置（推荐，如果不需要邮件）**

1. 进入 `Settings` → `Secrets and variables` → `Actions`
2. 删除以下所有邮件相关的 Secrets：
   - `SMTP_SERVER`
   - `SMTP_PORT`
   - `SENDER_EMAIL`
   - `SENDER_PASSWORD`
   - `RECEIVER_EMAIL`
3. 重新运行 workflow

> 💡 删除后，程序会正常运行，数据保存在 `download_history.json` 中。

**方案 B：正确配置邮件 Secrets（如果需要邮件）**

1. 确保 `SMTP_PORT` 的值是数字：`587` 或 `465`
2. 确保所有 5 个邮件 Secrets 都有正确的值，不能为空
3. 参考 [设置指南 - 邮件配置](SETUP_GUIDE.md#邮件配置)

---

### 错误 2：GitHub Actions 权限错误 (403)

**错误信息：**
```
remote: Permission to xxx/open-vsx-download-tracker.git denied to github-actions[bot].
fatal: unable to access 'https://github.com/xxx/': The requested URL returned error: 403
Error: Process completed with exit code 128
```

**原因：**
GitHub Actions 没有权限推送代码到仓库。

**解决方案：**

1. 进入仓库的 **Settings**
2. 左侧菜单：**Actions** → **General**
3. 滚动到页面最下方 **Workflow permissions**
4. 选择 ✅ **"Read and write permissions"**
5. 勾选 ✅ **"Allow GitHub Actions to create and approve pull requests"**
6. 点击 **Save** 保存
7. 重新运行 workflow

**验证成功：**
- ✅ Actions 运行成功（绿色勾号）
- ✅ 仓库中出现或更新了 `download_history.json`
- ✅ Git 历史中有 `github-actions[bot]` 的提交

> 📖 详细图文说明：[设置指南 - Actions 权限设置](SETUP_GUIDE.md#github-actions-权限设置)

---

### 错误 3：插件不存在 (404)

**错误信息：**
```
✗ API 返回错误状态码: 404
```

**原因：**
- 插件名称或命名空间配置错误
- 插件未发布到 Open-VSX

**解决方案：**

1. **验证插件 URL**
   
   访问 `https://open-vsx.org/extension/[你的namespace]/[你的插件名]`
   
   确认页面可以正常打开

2. **检查配置**
   
   比对 URL 和你的 Secrets：
   ```
   https://open-vsx.org/extension/redhat/vscode-yaml
                                    ↑         ↑
                        EXTENSION_NAMESPACE  EXTENSION_NAME
   ```

3. **常见错误**
   - ❌ 拼写错误（大小写敏感）
   - ❌ 多余的空格
   - ❌ 使用了显示名称而不是实际 ID

**示例：**
```
正确：EXTENSION_NAMESPACE=redhat
错误：EXTENSION_NAMESPACE=Red Hat
错误：EXTENSION_NAMESPACE= redhat （前面有空格）
```

---

### 错误 4：SMTP 认证失败

**错误信息：**
```
✗ SMTP 连接失败: SMTPAuthenticationError
✗ 发送邮件失败: (535, b'5.7.8 Username and Password not accepted.')
```

**原因：**
- Gmail 使用了普通密码而不是应用专用密码
- QQ/163 邮箱使用了登录密码而不是授权码
- 密码输入错误或过期

**解决方案：**

**Gmail 用户：**

必须使用应用专用密码！

1. 访问 https://myaccount.google.com/apppasswords
2. 启用两步验证（如果还未启用）
3. 创建新的应用专用密码
4. 复制生成的 16 位密码（去掉空格）
5. 更新 `SENDER_PASSWORD` Secret

> 📖 详细步骤：[设置指南 - Gmail 配置](SETUP_GUIDE.md#使用-gmail推荐)

**QQ 邮箱用户：**

1. 登录 QQ 邮箱
2. 设置 → 账户 → POP3/SMTP 服务
3. 开启 SMTP 服务并获取授权码
4. 使用授权码更新 `SENDER_PASSWORD`

**163/126 邮箱用户：**

1. 登录邮箱
2. 设置 → POP3/SMTP/IMAP
3. 开启 SMTP 服务
4. 获取授权码（可能需要发送短信验证）
5. 使用授权码更新 `SENDER_PASSWORD`

**其他检查项：**
- ✅ `SMTP_SERVER` 和 `SMTP_PORT` 配置正确
- ✅ `SENDER_EMAIL` 与 SMTP 服务器匹配
- ✅ 密码/授权码没有过期

---

### 错误 5：收不到邮件

**现象：**
- Actions 运行成功
- 没有错误提示
- 但是没有收到邮件

**排查步骤：**

**1. 检查垃圾邮件文件夹**

自动发送的邮件可能被误判为垃圾邮件。

**2. 查看 Actions 日志**

```
Actions → 选择运行记录 → 查看 "运行下载量追踪器" 步骤
```

查找：
- ✅ "邮件已发送成功" - 表示已发送
- ❌ 任何错误信息 - 表示发送失败

**3. 验证邮件配置**

本地测试邮件功能：

```bash
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SENDER_EMAIL=your@gmail.com
export SENDER_PASSWORD=your-app-password
export RECEIVER_EMAIL=your@gmail.com

python test_config.py
```

**4. 检查常见配置错误**

| 配置项 | 常见错误 | 正确示例 |
|-------|---------|---------|
| SMTP_SERVER | 多余空格或错误地址 | `smtp.gmail.com` |
| SMTP_PORT | 字符串或错误端口 | `587` |
| SENDER_EMAIL | 格式错误 | `user@gmail.com` |
| RECEIVER_EMAIL | 格式错误 | `user@example.com` |

**5. 延迟接收**

某些邮件服务器可能有延迟，等待 5-10 分钟再检查。

---

### 错误 6：环境变量未设置

**错误信息：**
```
错误: 请设置 EXTENSION_NAMESPACE 和 EXTENSION_NAME 环境变量
```

**原因：**
必需的 GitHub Secrets 未正确配置。

**解决方案：**

**1. 检查 Secret 是否存在**

`Settings` → `Secrets and variables` → `Actions`

必须有：
- `EXTENSION_NAMESPACE`
- `EXTENSION_NAME`

**2. 检查 Secret 名称**

Secret 名称**必须完全匹配**，区分大小写：

```
✅ 正确：EXTENSION_NAMESPACE
❌ 错误：extension_namespace
❌ 错误：Extension_Namespace
❌ 错误：EXTENSION NAMESPACE（有空格）
```

**3. 检查 Secret 值**

- 不能为空字符串
- 不能有前后空格
- 区分大小写

**4. 重新添加 Secrets**

如果不确定，删除并重新添加：
1. 点击 Secret 名称
2. 点击 "Remove secret"
3. 重新添加新的 Secret

---

## 调试技巧

### 1. 本地测试

本地运行可以更快地发现问题：

```bash
# 克隆仓库
git clone https://github.com/你的用户名/open-vsx-download-tracker
cd open-vsx-download-tracker

# 安装依赖
pip install -r requirements.txt

# 设置环境变量（最小配置）
export EXTENSION_NAMESPACE=your-namespace
export EXTENSION_NAME=your-extension-name

# 测试配置
python test_config.py

# 运行追踪器
python tracker.py
```

### 2. 查看详细日志

**在 GitHub Actions 中：**

1. 进入 `Actions` 标签
2. 点击失败的运行记录
3. 展开每个步骤查看详细输出
4. 红色 ❌ 标记的步骤包含错误信息
5. 可以搜索关键词：`error`、`failed`、`✗`

**关键步骤：**
- "Set up job" - 环境配置
- "运行下载量追踪器" - 主程序运行
- "提交下载历史记录" - Git 提交

### 3. 测试邮件配置

单独测试邮件功能：

```bash
# 设置邮件相关环境变量
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SENDER_EMAIL=your@gmail.com
export SENDER_PASSWORD=your-app-password
export RECEIVER_EMAIL=your@gmail.com

# 运行配置测试
python test_config.py
```

### 4. 分步排查

按顺序检查：

1. ✅ 必需配置是否正确（插件信息）
2. ✅ Actions 权限是否设置
3. ✅ Workflow 是否启用
4. ✅ 邮件配置是否完整（如果需要）
5. ✅ Secret 名称是否完全匹配

### 5. 使用 test_config.py

项目包含配置测试工具：

```bash
python test_config.py
```

它会检查：
- ✅ 环境变量是否设置
- ✅ Open-VSX API 是否可访问
- ✅ 插件信息是否正确
- ✅ 邮件配置是否有效（如果配置了）

---

## 提交 Issue 指南

如果以上方法都无法解决问题，请在 GitHub 提交 Issue。

### 请提供以下信息：

**1. 错误描述**
- 简洁描述问题
- 预期行为 vs 实际行为

**2. 错误截图/日志**
- GitHub Actions 运行日志（完整）
- 具体的错误信息
- 相关步骤的输出

**3. 配置信息（隐藏敏感内容）**

```
已配置的 Secrets（只列出名称，不要包含实际值）：
- EXTENSION_NAMESPACE: ✓
- EXTENSION_NAME: ✓
- SMTP_SERVER: ✓（或 ✗）
- ...

插件 URL：https://open-vsx.org/extension/...
```

**4. 环境信息**
- 是否在本地测试过？结果如何？
- 是否首次运行？还是曾经成功过？
- 使用的邮箱服务商（如果相关）

**5. 已尝试的解决方案**
- 列出你已经尝试过的步骤
- 避免重复建议

### Issue 标题示例

好的标题：
- ✅ "GitHub Actions 权限错误 403，已设置 write permissions"
- ✅ "Gmail SMTP 认证失败，已使用应用专用密码"
- ✅ "插件 404 错误，但 URL 可以访问"

不好的标题：
- ❌ "不工作"
- ❌ "错误"
- ❌ "帮帮我"

---

## 快速检查清单

遇到问题时，按此清单逐项检查：

- [ ] Fork 了项目到自己的仓库
- [ ] 添加了 `EXTENSION_NAMESPACE` Secret
- [ ] 添加了 `EXTENSION_NAME` Secret
- [ ] Secret 名称完全匹配（大小写）
- [ ] Secret 值正确，无空格
- [ ] 设置了 Actions "Read and write permissions"
- [ ] 勾选了 "Allow GitHub Actions to..."
- [ ] 启用了 GitHub Actions
- [ ] 插件 URL 可以在浏览器中访问
- [ ] （可选）邮件配置完整或全部删除

---

## 相关文档

- 📖 [完整设置指南](SETUP_GUIDE.md) - 详细配置步骤
- 📋 [README](README.md) - 项目概览

---

**大多数问题都可以通过仔细检查配置解决！** 🎯

如果本指南帮助你解决了问题，欢迎给项目一个 ⭐️ Star！
