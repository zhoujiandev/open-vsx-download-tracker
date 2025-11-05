#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置测试脚本
用于验证 Open-VSX Tracker 的配置是否正确
"""

import os
import sys
import requests


def check_env_vars():
    """检查环境变量是否设置"""
    print("=" * 60)
    print("检查环境变量配置")
    print("=" * 60)
    
    required_vars = [
        'EXTENSION_NAMESPACE',
        'EXTENSION_NAME',
        'SMTP_SERVER',
        'SMTP_PORT',
        'SENDER_EMAIL',
        'SENDER_PASSWORD',
        'RECEIVER_EMAIL'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # 隐藏密码
            if 'PASSWORD' in var:
                display_value = '*' * 8
            else:
                display_value = value
            print(f"✓ {var}: {display_value}")
        else:
            print(f"✗ {var}: 未设置")
            missing_vars.append(var)
    
    print()
    
    if missing_vars:
        print(f"❌ 缺少 {len(missing_vars)} 个必需的环境变量")
        return False
    else:
        print("✅ 所有环境变量都已设置")
        return True


def test_openvsx_api():
    """测试 Open-VSX API 连接"""
    print("=" * 60)
    print("测试 Open-VSX API 连接")
    print("=" * 60)
    
    namespace = os.getenv('EXTENSION_NAMESPACE')
    extension_name = os.getenv('EXTENSION_NAME')
    
    if not namespace or not extension_name:
        print("✗ 跳过测试（缺少插件信息）")
        return False
    
    try:
        url = f"https://open-vsx.org/api/{namespace}/{extension_name}"
        print(f"请求 URL: {url}")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ API 连接成功")
            print(f"  插件名称: {data.get('displayName', 'N/A')}")
            print(f"  版本: {data.get('version', 'N/A')}")
            print(f"  总下载量: {data.get('downloadCount', 0):,}")
            print()
            print("✅ Open-VSX API 测试通过")
            return True
        elif response.status_code == 404:
            print(f"✗ 插件不存在 (404)")
            print(f"  请检查 namespace 和 extension name 是否正确")
            print(f"  访问 https://open-vsx.org/extension/{namespace}/{extension_name} 确认")
            return False
        else:
            print(f"✗ API 返回错误状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ API 请求失败: {e}")
        return False


def test_smtp_connection():
    """测试 SMTP 连接"""
    print("=" * 60)
    print("测试 SMTP 连接")
    print("=" * 60)
    
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    if not all([smtp_server, smtp_port, sender_email, sender_password]):
        print("✗ 跳过测试（缺少 SMTP 配置）")
        return False
    
    try:
        import smtplib
        
        print(f"连接到 {smtp_server}:{smtp_port}...")
        
        with smtplib.SMTP(smtp_server, int(smtp_port), timeout=10) as server:
            server.starttls()
            print(f"✓ TLS 连接成功")
            
            server.login(sender_email, sender_password)
            print(f"✓ SMTP 认证成功")
        
        print()
        print("✅ SMTP 连接测试通过")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("✗ SMTP 认证失败")
        print("  可能的原因：")
        print("  1. Gmail 用户需要使用应用专用密码，不是邮箱登录密码")
        print("  2. QQ邮箱等需要使用授权码")
        print("  3. 密码输入错误")
        return False
    except Exception as e:
        print(f"✗ SMTP 连接失败: {e}")
        return False


def main():
    """主函数"""
    print("\n🔍 Open-VSX Download Tracker - 配置测试工具\n")
    
    results = []
    
    # 测试环境变量
    results.append(check_env_vars())
    print()
    
    # 测试 API
    results.append(test_openvsx_api())
    print()
    
    # 测试 SMTP
    results.append(test_smtp_connection())
    print()
    
    # 总结
    print("=" * 60)
    print("测试总结")
    print("=" * 60)
    
    if all(results):
        print("🎉 所有测试通过！配置正确，可以正常运行。")
        print()
        print("下一步：")
        print("1. 将配置添加到 GitHub Secrets")
        print("2. 启用 GitHub Actions")
        print("3. 手动运行一次工作流进行测试")
        return 0
    else:
        print("❌ 部分测试失败，请检查配置。")
        print()
        print("详细帮助请查看 config.example.md 文件")
        return 1


if __name__ == "__main__":
    sys.exit(main())

