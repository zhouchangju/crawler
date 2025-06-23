#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载公司logo图片
从油气公司JSON文件中读取logo URL并下载到本地
"""

import requests
import json
import os
import time
import re
from urllib.parse import urlparse
from pathlib import Path

def sanitize_filename(filename):
    """清理文件名，移除不合法的字符"""
    # 移除或替换不合法的文件名字符
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # 移除前后空格和点号
    filename = filename.strip(' .')
    # 限制长度
    if len(filename) > 200:
        filename = filename[:200]
    return filename

def get_file_extension(url):
    """从URL获取文件扩展名"""
    parsed_url = urlparse(url)
    path = parsed_url.path
    if '.' in path:
        return os.path.splitext(path)[1].lower()
    return '.png'  # 默认为PNG

def download_logo(company_name, logo_url, output_dir):
    """下载单个logo"""
    if not logo_url:
        print(f"  跳过 {company_name}：无logo URL")
        return False
    
    try:
        # 清理公司名称作为文件名
        safe_name = sanitize_filename(company_name)
        file_extension = get_file_extension(logo_url)
        filename = f"{safe_name}{file_extension}"
        filepath = os.path.join(output_dir, filename)
        
        # 如果文件已存在，跳过
        if os.path.exists(filepath):
            print(f"  跳过 {company_name}：文件已存在")
            return True
        
        # 下载图片
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://companiesmarketcap.com/'
        }
        
        response = requests.get(logo_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 保存文件
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"  ✓ 下载成功: {company_name} -> {filename}")
        return True
        
    except requests.RequestException as e:
        print(f"  ✗ 下载失败 {company_name}: 网络错误 - {e}")
        return False
    except Exception as e:
        print(f"  ✗ 下载失败 {company_name}: {e}")
        return False

def main():
    """主函数"""
    # 读取JSON文件
    json_file = 'oil_gas_companies.json'
    if not os.path.exists(json_file):
        print(f"错误：找不到文件 {json_file}")
        return
    
    with open(json_file, 'r', encoding='utf-8') as f:
        companies = json.load(f)
    
    print(f"从 {json_file} 读取到 {len(companies)} 家公司")
    
    # 创建输出目录
    output_dir = 'logo'
    os.makedirs(output_dir, exist_ok=True)
    
    # 统计变量
    success_count = 0
    failed_count = 0
    skipped_count = 0
    
    print(f"\n开始下载logo到 {output_dir} 目录...")
    
    for i, company in enumerate(companies, 1):
        company_name = company.get('name', f'Unknown_{i}')
        logo_url = company.get('logo', '')
        
        print(f"\n[{i:3d}/{len(companies)}] {company_name}")
        
        if not logo_url:
            print(f"  跳过：无logo URL")
            skipped_count += 1
            continue
        
        # 检查文件是否已存在
        safe_name = sanitize_filename(company_name)
        file_extension = get_file_extension(logo_url)
        filename = f"{safe_name}{file_extension}"
        filepath = os.path.join(output_dir, filename)
        
        if os.path.exists(filepath):
            print(f"  跳过：文件已存在")
            skipped_count += 1
            continue
        
        # 下载
        if download_logo(company_name, logo_url, output_dir):
            success_count += 1
        else:
            failed_count += 1
        
        # 添加延时避免请求过于频繁
        if i % 10 == 0:  # 每10个文件后稍作停顿
            time.sleep(0.1)
        else:
            time.sleep(0.05)
    
    # 显示结果统计
    print(f"\n" + "="*50)
    print(f"下载完成！")
    print(f"成功下载: {success_count} 个")
    print(f"下载失败: {failed_count} 个")
    print(f"跳过文件: {skipped_count} 个")
    print(f"总计处理: {len(companies)} 个")
    
    # 检查输出目录
    downloaded_files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
    print(f"\n{output_dir} 目录中共有 {len(downloaded_files)} 个文件")

if __name__ == "__main__":
    main() 