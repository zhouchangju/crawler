#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QS世界大学排名数据处理脚本
功能：
1. 从JSON文件中提取score_nodes数据
2. 按年份合并相同年份的数据
"""

import json
import os
import re
from collections import defaultdict
from pathlib import Path


def extract_score_nodes(file_path):
    """
    根据传入的文件路径，解析文件内容，提取score_nodes属性的值
    
    Args:
        file_path (str): JSON文件的路径
        
    Returns:
        list: score_nodes的数据列表，如果文件不存在或解析失败则返回空列表
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 提取score_nodes属性
        score_nodes = data.get('score_nodes', [])
        print(f"从文件 {file_path} 提取到 {len(score_nodes)} 条记录")
        return score_nodes
        
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 不存在")
        return []
    except json.JSONDecodeError as e:
        print(f"错误：解析JSON文件 {file_path} 失败: {e}")
        return []
    except Exception as e:
        print(f"错误：处理文件 {file_path} 时发生异常: {e}")
        return []


def merge_data_by_year():
    """
    遍历data/raw/slice下的文件，按年份合并数据并写入data/raw/merge目录
    """
    # 设置路径
    slice_dir = Path("data/raw/slice")
    merge_dir = Path("data/raw/merge")
    
    # 创建merge目录（如果不存在）
    merge_dir.mkdir(parents=True, exist_ok=True)
    
    # 检查slice目录是否存在
    if not slice_dir.exists():
        print(f"错误：目录 {slice_dir} 不存在")
        return
    
    # 用于存储按年份分类的数据
    yearly_data = defaultdict(list)
    
    # 遍历slice目录下的所有JSON文件
    for file_path in slice_dir.glob("*.json"):
        print(f"正在处理文件: {file_path}")
        
        # 从文件名中提取年份
        filename = file_path.stem  # 获取不带扩展名的文件名
        year_match = re.match(r'^(\d{4})', filename)
        
        if not year_match:
            print(f"警告：无法从文件名 {filename} 中提取年份，跳过该文件")
            continue
            
        year = year_match.group(1)
        
        # 提取score_nodes数据
        score_nodes = extract_score_nodes(file_path)
        
        if score_nodes:
            yearly_data[year].extend(score_nodes)
    
    # 将合并后的数据写入merge目录
    for year, combined_data in yearly_data.items():
        output_file = merge_dir / f"{year}.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(combined_data, f, ensure_ascii=False, indent=2)
            
            print(f"成功将 {year} 年的数据（共 {len(combined_data)} 条记录）写入 {output_file}")
            
        except Exception as e:
            print(f"错误：写入文件 {output_file} 时发生异常: {e}")


def main():
    """
    主函数
    """
    print("开始处理QS世界大学排名数据...")
    print("=" * 50)
    
    # 切换到脚本所在目录
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # 执行数据合并
    merge_data_by_year()
    
    print("=" * 50)
    print("数据处理完成！")


if __name__ == "__main__":
    main() 