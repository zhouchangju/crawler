#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
油气公司市值排名爬虫
抓取 companiesmarketcap.com 网站上油气公司的名称和logo信息
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import os
from urllib.parse import urljoin

def get_page_data(page_num):
    """获取单页数据"""
    url = f"https://companiesmarketcap.com/oil-gas/largest-oil-and-gas-companies-by-market-cap/?page={page_num}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f"正在抓取第 {page_num} 页...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 查找marketcap-table表格
        table = soup.find('table', class_='marketcap-table')
        if not table:
            print(f"第 {page_num} 页未找到marketcap-table表格")
            return []
        
        companies = []
        
        # 遍历表格中的每一行
        rows = table.find_all('tr')
        for row in rows:
            # 查找包含公司信息的name-div
            name_div = row.find('div', class_='name-div')
            if not name_div:
                continue
            
            # 获取公司名称
            company_name_elem = name_div.find(class_='company-name')
            if not company_name_elem:
                continue
            
            company_name = company_name_elem.get_text(strip=True)
            
            # 获取公司logo - 查找class为company-logo的img标签
            logo_url = ""
            logo_elem = row.find('img', class_='company-logo')
            
            if logo_elem and logo_elem.get('src'):
                logo_url = logo_elem['src']
                
                # 处理相对路径
                if logo_url.startswith('/'):
                    logo_url = 'https://companiesmarketcap.com' + logo_url
                elif not logo_url.startswith('http'):
                    logo_url = 'https://companiesmarketcap.com/' + logo_url
            
            if company_name:
                companies.append({
                    'name': company_name,
                    'logo': logo_url
                })
                print(f"  找到公司: {company_name} | Logo: {logo_url.split('/')[-1] if logo_url else 'N/A'}")
        
        return companies
        
    except requests.RequestException as e:
        print(f"请求第 {page_num} 页时出错: {e}")
        return []
    except Exception as e:
        print(f"解析第 {page_num} 页时出错: {e}")
        return []

def save_html_for_debug(page_num, content):
    """保存HTML内容用于调试"""
    with open(f'debug_page_{page_num}.html', 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    """主函数"""
    all_companies = []
    
    # 抓取5个页面的数据
    for page in range(1, 6):
        companies = get_page_data(page)
        all_companies.extend(companies)
        
        # 添加延时，避免请求过于频繁
        if page < 5:
            time.sleep(2)
    
    print(f"\n总共抓取到 {len(all_companies)} 家公司的信息")
    
    # 保存到JSON文件
    output_file = 'oil_gas_companies.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_companies, f, ensure_ascii=False, indent=2)
    
    print(f"数据已保存到 {output_file}")
    
    # 统计有logo的公司数量
    companies_with_logo = [c for c in all_companies if c['logo']]
    print(f"其中有logo的公司: {len(companies_with_logo)} 家")
    
    # 打印前几个公司作为示例
    if all_companies:
        print("\n前5家公司示例:")
        for i, company in enumerate(all_companies[:5], 1):
            print(f"{i}. {company['name']}")
            print(f"   Logo: {company['logo']}")

if __name__ == "__main__":
    main() 