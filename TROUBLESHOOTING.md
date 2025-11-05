# 🔧 故障排查指南

## ❌ 常见错误及解决方案

### 错误 1：ValueError: invalid literal for int() with base 10: ''

**错误信息：**
```
ValueError: invalid literal for int() with base 10: ''
```

**原因：**
你添加了 `SMTP_PORT` Secret 但值为空字符串。

**解决方案：**

**方案 A**：删除邮件相关的 Secrets（推荐，如果不需要邮件）
1. 进入 Settings → Secrets and variables → Actions
2. 删除以下所有邮件相关的 Secrets：
   - `SMTP_SERVER`
   - `SMTP_PORT`
   - `SENDER_EMAIL`
   - `SENDER_PASSWORD`
   - `RECEIVER_EMAIL`

**方案 B**：正确配置邮件 Secrets（如果需要邮件）
1. 确保 `SMTP_PORT` 的值是数字，如 `587` 或 `465`
2. 确保所有 5 个邮件 Secrets 都有正确的值
3. 参考 [config.example.md](config.example.md) 了解正确配置

---

### 错误 2：插件不存在 (404)

**错误信息：**
```
✗ API 返回错误状态码: 404
```

**原因：**
- 插件名称或命名空间配置错误
- 插件未发布到 Open-VSX

**解决方案：**
1. 访问 `https://open-vsx.org/extension/你的namespace/你的插件名` 确认页面存在
2. 检查 `EXTENSION_NAMESPACE` 和 `EXTENSION_NAME` 是否拼写正确
3. 确认插件已成功发布到 Open-VSX

---

### 错误 3：SMTP 认证失败

**错误信息：**
```
✗ SMTP 连接失败: SMTPAuthenticationError
```

**原因：**
- Gmail 用户使用了普通密码而不是应用专用密码
- QQ 邮箱等使用了登录密码而不是授权码
- 密码输入错误

**解决方案：**

**Gmail 用户：**
1. 访问 https://myaccount.google.com/security
2. 启用"两步验证"
3. 搜索"应用专用密码"（App passwords）
4. 生成新的应用专用密码
5. 使用生成的 16 位密码更新 `SENDER_PASSWORD`

**QQ 邮箱用户：**
1. 登录 QQ 邮箱
2. 设置 → 账户 → POP3/SMTP 服务
3. 开启 SMTP 服务并获取授权码
4. 使用授权码更新 `SENDER_PASSWORD`

---

### 错误 4：GitHub Actions 无法提交文件

**错误信息：**
```
refusing to allow a GitHub App to create or update workflow
```

**原因：**
GitHub Actions 权限不足

**解决方案：**
1. 进入 Settings → Actions → General
2. 滚动到 "Workflow permissions"
3. 选择 "Read and write permissions"
4. 勾选 "Allow GitHub Actions to create and approve pull requests"
5. 点击 Save

---

### 错误 5：收不到邮件

**现象：**
- Actions 运行成功
- 但是没有收到邮件

**可能原因及解决方案：**

**1. 查看垃圾邮件文件夹**
- 邮件可能被误判为垃圾邮件

**2. 检查 Actions 日志**
- 查看是否有"邮件已发送"的提示
- 查看是否有错误信息

**3. 验证邮件配置**
```bash
# 本地测试邮件配置
python test_config.py
```

**4. 检查 SMTP 服务器配置**
- Gmail: `smtp.gmail.com:587`
- QQ: `smtp.qq.com:587`
- 163: `smtp.163.com:465`

---

### 错误 6：环境变量未设置

**错误信息：**
```
错误: 请设置 EXTENSION_NAMESPACE 和 EXTENSION_NAME 环境变量
```

**原因：**
GitHub Secrets 未正确配置

**解决方案：**
1. 确认已在 Settings → Secrets and variables → Actions 中添加
2. 检查 Secret 名称是否完全匹配（区分大小写）：
   - `EXTENSION_NAMESPACE`（不是 extension_namespace）
   - `EXTENSION_NAME`（不是 extension_name）
3. 确认 Secret 有值（不是空字符串）

---

## 💡 调试技巧

### 1. 本地测试

```bash
# 克隆仓库
git clone https://github.com/你的用户名/open-vsx-download-tracker
cd open-vsx-download-tracker

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export EXTENSION_NAMESPACE=你的namespace
export EXTENSION_NAME=你的插件名

# 测试配置（不需要邮件）
python test_config.py

# 运行追踪器
python tracker.py
```

### 2. 查看详细日志

在 GitHub Actions 中：
1. 进入 Actions 标签
2. 点击失败的运行记录
3. 展开每个步骤查看详细输出
4. 红色 X 标记的步骤包含错误信息

### 3. 测试邮件配置

```bash
# 只测试邮件功能
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SENDER_EMAIL=your@gmail.com
export SENDER_PASSWORD=your-app-password
export RECEIVER_EMAIL=your@gmail.com

python test_config.py
```

---

## 🆘 仍然无法解决？

### 提交 Issue 时请提供：

1. **错误截图**
   - GitHub Actions 运行日志
   - 完整的错误信息

2. **配置信息**（隐藏敏感信息）
   - 使用的 Secrets（不要包含实际值）
   - 插件 URL

3. **环境信息**
   - 是否在本地测试过
   - 是否首次运行

4. **已尝试的解决方案**
   - 避免重复建议

---

## 📚 相关文档

- [最小配置指南](MINIMAL_SETUP.md) - 只配置 2 个必需项
- [快速开始](QUICKSTART.md) - 完整配置步骤
- [配置示例](config.example.md) - 详细配置说明
- [完整文档](README.md) - 项目总览

---

**大多数问题都可以通过正确配置 Secrets 解决！** 🎯

