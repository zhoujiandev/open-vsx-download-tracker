#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Open-VSX 插件下载量追踪器
每日自动查询插件下载量并通过邮件发送统计报告
"""

import os
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path


class OpenVSXTracker:
    """Open-VSX 下载量追踪器"""
    
    def __init__(self, namespace, extension_name):
        """
        初始化追踪器
        
        Args:
            namespace: 插件的命名空间（发布者名称）
            extension_name: 插件名称
        """
        self.namespace = namespace
        self.extension_name = extension_name
        self.api_base_url = "https://open-vsx.org/api"
        self.data_file = Path("download_history.json")
        
    def get_download_count(self):
        """
        从 Open-VSX API 获取当前总下载量
        
        Returns:
            int: 总下载量，失败时返回 None
        """
        try:
            url = f"{self.api_base_url}/{self.namespace}/{self.extension_name}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            download_count = data.get('downloadCount', 0)
            
            print(f"✓ 成功获取下载量: {download_count}")
            return download_count
            
        except requests.exceptions.RequestException as e:
            print(f"✗ 获取下载量失败: {e}")
            return None
    
    def load_history(self):
        """
        加载历史下载量数据
        
        Returns:
            dict: 历史数据字典
        """
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"✗ 读取历史数据失败: {e}")
                return {}
        return {}
    
    def save_history(self, history):
        """
        保存历史下载量数据
        
        Args:
            history: 要保存的历史数据字典
        """
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            print(f"✓ 历史数据已保存")
        except Exception as e:
            print(f"✗ 保存历史数据失败: {e}")
    
    def calculate_daily_increase(self, current_count):
        """
        计算过去24小时的下载量增长
        
        Args:
            current_count: 当前总下载量
            
        Returns:
            tuple: (增长量, 昨日总下载量, 上次统计时间)
        """
        history = self.load_history()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 获取最近一次记录
        last_timestamp = None
        last_count = current_count
        
        if history:
            # 按时间戳排序，获取最近一次记录
            sorted_timestamps = sorted(history.keys())
            last_timestamp = sorted_timestamps[-1]
            last_count = int(history[last_timestamp])
            
            increase = current_count - last_count
        else:
            increase = 0
        
        # 保存今天的数据（新格式：时间戳为key，下载量字符串为value）
        history[current_time] = str(current_count)
        self.save_history(history)
        
        return increase, last_count, last_timestamp
    
    def send_email(self, subject, body):
        """
        发送邮件通知
        
        Args:
            subject: 邮件主题
            body: 邮件正文
        """
        # 从环境变量获取邮件配置
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com') or 'smtp.gmail.com'
        smtp_port_str = os.getenv('SMTP_PORT', '587') or '587'
        try:
            smtp_port = int(smtp_port_str)
        except ValueError:
            smtp_port = 587
        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('SENDER_PASSWORD')
        receiver_email = os.getenv('RECEIVER_EMAIL')
        
        # 检查必需的邮件配置
        if not sender_email or not sender_password or not receiver_email:
            print("✗ 邮件配置不完整，跳过发送")
            if sender_email:
                print(f"  发送方: {sender_email}")
            if receiver_email:
                print(f"  接收方: {receiver_email}")
            if not sender_email:
                print(f"  缺少: SENDER_EMAIL")
            if not sender_password:
                print(f"  缺少: SENDER_PASSWORD")
            if not receiver_email:
                print(f"  缺少: RECEIVER_EMAIL")
            return
        
        try:
            # 创建邮件
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = subject
            
            message.attach(MIMEText(body, 'html', 'utf-8'))
            
            # 发送邮件
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)
            
            print(f"✓ 邮件已发送至: {receiver_email}")
            
        except Exception as e:
            print(f"✗ 发送邮件失败: {e}")
    
    def generate_report(self, current_count, daily_increase, last_count, last_timestamp):
        """
        生成 HTML 格式的统计报告
        
        Args:
            current_count: 当前总下载量
            daily_increase: 24小时增长量
            last_count: 昨日总下载量
            last_timestamp: 上次统计时间
            
        Returns:
            str: HTML 格式的报告
        """
        today = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        # 计算增长百分比
        if last_count > 0:
            percentage = (daily_increase / last_count) * 100
        else:
            percentage = 0
        
        # 计算距离上次统计的时间
        time_elapsed = "首次统计"
        if last_timestamp:
            try:
                last_dt = datetime.strptime(last_timestamp, "%Y-%m-%d %H:%M:%S")
                current_dt = datetime.now()
                time_diff = current_dt - last_dt
                
                days = time_diff.days
                hours = time_diff.seconds // 3600
                minutes = (time_diff.seconds % 3600) // 60
                
                if days > 0:
                    time_elapsed = f"{days}天{hours}小时{minutes}分钟"
                elif hours > 0:
                    time_elapsed = f"{hours}小时{minutes}分钟"
                else:
                    time_elapsed = f"{minutes}分钟"
            except:
                time_elapsed = "未知"
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                           color: white; padding: 20px; border-radius: 5px; text-align: center; }}
                .stats {{ background: #f7f7f7; padding: 20px; margin: 20px 0; border-radius: 5px; }}
                .stat-item {{ margin: 15px 0; padding: 10px; background: white; border-radius: 3px; }}
                .stat-label {{ color: #666; font-size: 14px; }}
                .stat-value {{ font-size: 24px; font-weight: bold; color: #667eea; }}
                .increase {{ color: #10b981; }}
                .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Open-VSX 下载量读数</h1>
                    <p>{today}</p>
                </div>
                
                <div class="stats">
                    <div class="stat-item">
                        <div class="stat-label">插件名称</div>
                        <div class="stat-value">{self.namespace}.{self.extension_name}</div>
                    </div>
                    
                    <div class="stat-item">
                        <div class="stat-label">当前总下载量</div>
                        <div class="stat-value">{current_count:,}</div>
                    </div>
                    
                    <div class="stat-item">
                        <div class="stat-label">距离上次统计</div>
                        <div class="stat-value">{time_elapsed}</div>
                    </div>
                    
                    <div class="stat-item">
                        <div class="stat-label">新增下载量</div>
                        <div class="stat-value increase">+{daily_increase:,}</div>
                    </div>
                    
                    <div class="stat-item">
                        <div class="stat-label">增长率</div>
                        <div class="stat-value increase">{percentage:.2f}%</div>
                    </div>
                </div>
                
                <div class="footer">
                    <p>此邮件由 Open-VSX Download Tracker 自动生成</p>
                    <p>查看项目: <a href="https://open-vsx.org/extension/{self.namespace}/{self.extension_name}">
                        Open-VSX 页面</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def run(self):
        """
        执行主程序逻辑
        """
        print("=" * 60)
        print(f"Open-VSX Download Tracker - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print(f"正在追踪: {self.namespace}/{self.extension_name}")
        print()
        
        # 获取当前下载量
        current_count = self.get_download_count()
        
        if current_count is None:
            print("✗ 无法获取下载量，程序退出")
            return
        
        # 计算增长量
        daily_increase, last_count, last_timestamp = self.calculate_daily_increase(current_count)
        
        print(f"上次统计时间: {last_timestamp if last_timestamp else '首次统计'}")
        print(f"上次总下载量: {last_count:,}")
        print(f"当前总下载量: {current_count:,}")
        print(f"新增下载量: +{daily_increase:,}")
        print()
        
        # 生成并发送报告
        subject = f"📊 {self.namespace}.{self.extension_name} 下载量日报 - {datetime.now().strftime('%Y-%m-%d')}"
        body = self.generate_report(current_count, daily_increase, last_count, last_timestamp)
        
        self.send_email(subject, body)
        
        print("=" * 60)
        print("任务完成！")
        print("=" * 60)


def main():
    """主函数"""
    # 从环境变量获取插件信息
    namespace = os.getenv('EXTENSION_NAMESPACE')
    extension_name = os.getenv('EXTENSION_NAME')
    
    if not namespace or not extension_name:
        print("错误: 请设置 EXTENSION_NAMESPACE 和 EXTENSION_NAME 环境变量")
        print("示例: export EXTENSION_NAMESPACE=redhat")
        print("      export EXTENSION_NAME=vscode-yaml")
        exit(1)
    
    tracker = OpenVSXTracker(namespace, extension_name)
    tracker.run()


if __name__ == "__main__":
    main()

