# 配置示例说明

## GitHub Secrets 配置

在你的 GitHub 仓库设置中添加以下 Secrets（Settings → Secrets and variables → Actions → New repository secret）：

### 必需的配置项

#### 1. EXTENSION_NAMESPACE（插件命名空间）

这是你的插件发布者名称。

**如何查找：**
- 访问你的插件页面，例如：`https://open-vsx.org/extension/redhat/vscode-yaml`
- URL 中 `/extension/` 后的第一部分就是 namespace
- 在上面的例子中，`EXTENSION_NAMESPACE` = `redhat`

**示例值：**
```
redhat
microsoft
vscode
```

#### 2. EXTENSION_NAME（插件名称）

这是你的插件的具体名称。

**如何查找：**
- 在同样的插件页面 URL 中
- `/extension/` 后的第二部分就是插件名称
- 在 `https://open-vsx.org/extension/redhat/vscode-yaml` 中，`EXTENSION_NAME` = `vscode-yaml`

**示例值：**
```
vscode-yaml
python
prettier-vscode
```

#### 3. SMTP_SERVER（邮件服务器）

SMTP 服务器地址。

**常用服务器：**

| 邮件服务商 | SMTP 服务器地址 |
|-----------|----------------|
| Gmail | smtp.gmail.com |
| Outlook/Hotmail | smtp-mail.outlook.com |
| QQ邮箱 | smtp.qq.com |
| 163邮箱 | smtp.163.com |
| 阿里云企业邮箱 | smtp.aliyun.com |
| 腾讯企业邮箱 | smtp.exmail.qq.com |

**示例值：**
```
smtp.gmail.com
```

#### 4. SMTP_PORT（邮件端口）

SMTP 服务器端口号。

**常用端口：**
- `587` - TLS 加密（推荐，大多数服务器支持）
- `465` - SSL 加密（某些服务器使用）
- `25` - 无加密（不推荐，可能被屏蔽）

**示例值：**
```
587
```

#### 5. SENDER_EMAIL（发件人邮箱）

用于发送邮件的邮箱地址。

**注意事项：**
- 必须与 SMTP 服务器匹配（例如使用 Gmail SMTP 就要用 Gmail 邮箱）
- 需要开启 SMTP 发送权限

**示例值：**
```
your-email@gmail.com
myname@outlook.com
```

#### 6. SENDER_PASSWORD（发件人密码）

邮箱的密码或应用专用密码。

**重要：**
- **Gmail 用户必须使用"应用专用密码"，不是你的邮箱登录密码！**
- QQ邮箱、163邮箱等也需要使用"授权码"

**Gmail 应用专用密码设置步骤：**

**方法 1（推荐）：直接访问**
1. 直接访问：https://myaccount.google.com/apppasswords
2. 登录你的 Google 账号（如果还未登录）
3. 如果提示需要启用两步验证，请先启用
4. 在"应用专用密码"页面，输入应用名称（如"Open-VSX Tracker"）
5. 点击"创建"
6. 复制生成的 16 位密码（格式类似：`abcd efgh ijkl mnop`）
7. 将这个密码作为 `SENDER_PASSWORD`

**方法 2：通过安全设置**
1. 访问 https://myaccount.google.com/security
2. 找到并启用"两步验证"（2-Step Verification）
3. 启用两步验证后，在同一页面向下滚动
4. 找到"应用专用密码"（App passwords）选项
5. 点击进入后按照方法 1 的步骤 4-7 操作

**注意：**
- 只有启用了两步验证后，才能看到"应用专用密码"选项
- 如果找不到此选项，请确认你的账号已启用两步验证

**QQ邮箱授权码设置：**

1. 登录 QQ 邮箱
2. 点击"设置" → "账户"
3. 找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
4. 开启"SMTP服务"
5. 按照提示发送短信获取授权码
6. 使用授权码作为 `SENDER_PASSWORD`

**示例值：**
```
abcdefghijklmnop
(这只是示例，使用你实际生成的密码)
```

#### 7. RECEIVER_EMAIL（收件人邮箱）

接收下载量报告的邮箱地址。

**注意事项：**
- 可以与发件人邮箱相同
- 可以是任何有效的邮箱地址
- 可以设置多个邮箱（用逗号分隔，需要修改代码）

**示例值：**
```
receiver@example.com
your-personal-email@gmail.com
```

## 完整配置示例

假设你的插件是 `https://open-vsx.org/extension/mycompany/awesome-extension`，你使用 Gmail 发送邮件：

```
EXTENSION_NAMESPACE: mycompany
EXTENSION_NAME: awesome-extension
SMTP_SERVER: smtp.gmail.com
SMTP_PORT: 587
SENDER_EMAIL: myemail@gmail.com
SENDER_PASSWORD: abcd efgh ijkl mnop
RECEIVER_EMAIL: myemail@gmail.com
```

## 本地测试配置

如果想在本地测试，可以设置环境变量：

### macOS/Linux:

```bash
export EXTENSION_NAMESPACE=mycompany
export EXTENSION_NAME=awesome-extension
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SENDER_EMAIL=myemail@gmail.com
export SENDER_PASSWORD="your-app-password"
export RECEIVER_EMAIL=myemail@gmail.com

python tracker.py
```

### Windows (PowerShell):

```powershell
$env:EXTENSION_NAMESPACE="mycompany"
$env:EXTENSION_NAME="awesome-extension"
$env:SMTP_SERVER="smtp.gmail.com"
$env:SMTP_PORT="587"
$env:SENDER_EMAIL="myemail@gmail.com"
$env:SENDER_PASSWORD="your-app-password"
$env:RECEIVER_EMAIL="myemail@gmail.com"

python tracker.py
```

## 故障排查

### 找不到插件

**错误提示：** API 请求失败，404 错误

**解决方法：**
1. 确认插件已发布到 Open-VSX
2. 访问 `https://open-vsx.org/extension/你的namespace/你的插件名` 确认可以访问
3. 检查 namespace 和 extension name 的拼写是否正确

### 邮件发送失败

**错误提示：** 发送邮件失败，认证错误

**解决方法：**
1. Gmail 用户确认使用的是应用专用密码，不是登录密码
2. 确认 SMTP 服务器和端口配置正确
3. 检查邮箱是否开启了 SMTP 服务
4. 查看 GitHub Actions 运行日志获取详细错误信息

### GitHub Actions 权限问题

**错误提示：** 无法提交 download_history.json

**解决方法：**
1. 确认仓库的 Actions 权限设置正确
2. 前往 Settings → Actions → General → Workflow permissions
3. 选择 "Read and write permissions"
4. 保存设置

