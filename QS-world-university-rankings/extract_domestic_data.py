#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取国内大学数据脚本
功能：从合并后的数据中提取中国大陆、香港、澳门、台湾的大学数据
"""

import json
import os
from pathlib import Path


def parse_merge_file(file_path):
    """
    解析合并后的文件内容
    
    Args:
        file_path (str): 文件路径，如 data/raw/merge/2022.json
        
    Returns:
        list: 解析后的大学数据列表
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"解析文件 {file_path} 时出错: {e}")
        return []


def filter_domestic_universities(universities):
    """
    过滤出国内大学（中国大陆、香港、澳门、台湾）
    
    Args:
        universities (list): 大学数据列表
        
    Returns:
        list: 符合条件的国内大学数据
    """
    domestic_countries = [
        "China (Mainland)",
        "Hong Kong SAR", 
        "Macau SAR",
        "Taiwan"
    ]
    
    domestic_universities = []
    
    for university in universities:
        if 'country' in university and university['country'] in domestic_countries:
            domestic_universities.append(university)
    
    return domestic_universities


def save_domestic_data(domestic_universities, output_file):
    """
    保存国内大学数据到文件
    
    Args:
        domestic_universities (list): 国内大学数据列表
        output_file (str): 输出文件路径
    """
    try:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(domestic_universities, f, ensure_ascii=False, indent=2)
        
        print(f"成功保存 {len(domestic_universities)} 所国内大学数据到 {output_file}")
    except Exception as e:
        print(f"保存文件 {output_file} 时出错: {e}")


def process_all_merge_files():
    """
    处理所有合并后的文件，提取国内大学数据
    """
    # 获取脚本文件所在目录，然后构建数据目录的相对路径
    script_dir = Path(__file__).parent
    merge_dir = script_dir / "data" / "raw" / "merge"
    parsed_dir = script_dir / "data" / "parsed"
    
    if not merge_dir.exists():
        print(f"合并数据目录 {merge_dir} 不存在")
        return
    
    # 遍历所有合并后的文件
    for merge_file in merge_dir.glob("*.json"):
        print(f"处理文件: {merge_file}")
        
        # 解析文件内容
        universities = parse_merge_file(merge_file)
        if not universities:
            continue
        
        # 过滤国内大学
        domestic_universities = filter_domestic_universities(universities)
        
        # 生成输出文件名
        output_file = parsed_dir / merge_file.name
        
        # 保存国内大学数据
        save_domestic_data(domestic_universities, output_file)
        
        # 打印统计信息
        print(f"原始数据: {len(universities)} 所大学")
        print(f"国内大学: {len(domestic_universities)} 所大学")
        print(f"输出文件: {output_file}")
        print("-" * 50)


def main():
    """
    主函数
    """
    print("开始提取国内大学数据...")
    process_all_merge_files()
    print("数据提取完成！")


if __name__ == "__main__":
    main() 