#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成展示数据脚本
功能：从data/parsed目录下的*_with_chinese.json文件中提取展示所需的字段，生成统一的展示数据文件
"""

import json
import os
from pathlib import Path


def generate_display_data():
    """
    生成展示数据
    """
    script_dir = Path(__file__).parent
    parsed_dir = script_dir / "data" / "parsed"
    display_dir = script_dir / "data" / "display"
    
    # 确保输出目录存在
    display_dir.mkdir(parents=True, exist_ok=True)
    
    if not parsed_dir.exists():
        print(f"解析数据目录 {parsed_dir} 不存在")
        return
    
    # 查找所有带中文翻译的JSON文件
    chinese_files = list(parsed_dir.glob("*_with_chinese.json"))
    
    if not chinese_files:
        print("未找到翻译文件")
        return
    
    print(f"找到 {len(chinese_files)} 个翻译文件")
    
    all_display_data = []
    
    for file_path in sorted(chinese_files):
        # 从文件名提取年份
        year = file_path.stem.replace("_with_chinese", "")
        print(f"处理 {year} 年数据...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                universities = json.load(f)
            
            count = 0
            for university in universities:
                # 提取所需字段
                title_zh = university.get('title_zh')
                rank = university.get('rank', '')
                overall_score = university.get('overall_score', '')
                logo = university.get('logo', '')
                
                # 只有中文名存在的才加入展示数据
                if title_zh and title_zh != "":
                    display_item = {
                        "name": title_zh,
                        "value": overall_score,
                        "rank": rank,
                        "date": year,
                        "logo": logo
                    }
                    all_display_data.append(display_item)
                    count += 1
            
            print(f"  - 成功提取 {count} 所大学的展示数据")
                    
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")
    
    # 对数据进行排序：按年份，然后按排名
    def get_sort_key(item):
        """
        生成排序键：先按年份，再按排名
        """
        year = item['date']
        rank_str = item['rank']
        
        # 处理排名字段，提取数字
        if rank_str and rank_str.isdigit():
            rank_num = int(rank_str)
        elif rank_str and '-' in rank_str:
            # 处理范围排名如 "501-510"，取第一个数字
            try:
                rank_num = int(rank_str.split('-')[0])
            except:
                rank_num = 9999
        else:
            rank_num = 9999  # 无排名的放到最后
        
        return (year, rank_num)
    
    # 排序数据
    all_display_data.sort(key=get_sort_key)
    
    # 保存展示数据
    output_file = display_dir / "rank.json"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_display_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 展示数据生成成功！")
        print(f"输出文件: {output_file}")
        print(f"总计: {len(all_display_data)} 条记录")
        
        # 统计各年份数据量
        year_counts = {}
        for item in all_display_data:
            year = item['date']
            year_counts[year] = year_counts.get(year, 0) + 1
        
        print("\n各年份数据统计:")
        for year in sorted(year_counts.keys()):
            print(f"  {year}年: {year_counts[year]} 所大学")
            
    except Exception as e:
        print(f"保存展示数据时出错: {e}")


def preview_display_data(limit=5):
    """
    预览展示数据
    
    Args:
        limit (int): 预览条数
    """
    script_dir = Path(__file__).parent
    display_file = script_dir / "data" / "display" / "rank.json"
    
    if not display_file.exists():
        print("展示数据文件不存在，请先运行生成功能")
        return
    
    try:
        with open(display_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 优先显示有具体分数的记录（最新年份）
        latest_year = max(item['date'] for item in data)
        scored_data = [item for item in data 
                      if item['date'] == latest_year and item['value'] != 'n/a' and item['value'] != '']
        
        # 按排名排序
        def get_rank_num(item):
            rank_str = item['rank']
            if rank_str and rank_str.isdigit():
                return int(rank_str)
            return 9999
        
        scored_data_sorted = sorted(scored_data, key=get_rank_num)
        
        print(f"展示数据预览（{latest_year}年有具体分数的前{limit}条）:")
        print("="*60)
        
        for i, item in enumerate(scored_data_sorted[:limit]):
            print(f"{i+1}. {item['name']} ({item['date']}年)")
            print(f"   排名: {item['rank']}")
            print(f"   分数: {item['value']}")
            print(f"   Logo: {item['logo'][:50]}..." if len(item['logo']) > 50 else f"   Logo: {item['logo']}")
            print()
        
        print(f"总计: {len(data)} 条记录")
        print(f"其中有具体分数的: {len([item for item in data if item['value'] != 'n/a' and item['value'] != ''])} 条")
        print(f"分数为n/a的: {len([item for item in data if item['value'] == 'n/a'])} 条")
        
    except Exception as e:
        print(f"预览展示数据时出错: {e}")


def analyze_display_data():
    """
    分析展示数据
    """
    script_dir = Path(__file__).parent
    display_file = script_dir / "data" / "display" / "rank.json"
    
    if not display_file.exists():
        print("展示数据文件不存在，请先运行生成功能")
        return
    
    try:
        with open(display_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("展示数据分析报告")
        print("="*50)
        
        # 按年份统计
        year_stats = {}
        for item in data:
            year = item['date']
            if year not in year_stats:
                year_stats[year] = 0
            year_stats[year] += 1
        
        print("各年份数据统计:")
        for year in sorted(year_stats.keys()):
            print(f"  {year}年: {year_stats[year]} 所大学")
        
        # 统计有分数的数据
        scored_data = [item for item in data if item['value'] and item['value'] != '']
        print(f"\n有分数的记录: {len(scored_data)} / {len(data)} ({len(scored_data)/len(data)*100:.1f}%)")
        
        # 统计有Logo的数据
        logo_data = [item for item in data if item['logo'] and item['logo'] != '']
        print(f"有Logo的记录: {len(logo_data)} / {len(data)} ({len(logo_data)/len(data)*100:.1f}%)")
        
        # 找出排名最高的几所大学（最近年份）
        latest_year = max(year_stats.keys())
        latest_data = [item for item in data if item['date'] == latest_year]
        
        print(f"\n{latest_year}年排名前10的大学:")
        # 按排名排序（处理可能的字符串格式）
        def get_rank_num(item):
            rank_str = item['rank']
            if rank_str and rank_str.isdigit():
                return int(rank_str)
            return 9999  # 无排名的放到最后
        
        latest_data_sorted = sorted(latest_data, key=get_rank_num)
        
        for i, item in enumerate(latest_data_sorted[:10]):
            print(f"  {item['rank']:>3}. {item['name']}")
        
    except Exception as e:
        print(f"分析展示数据时出错: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--preview":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            preview_display_data(limit)
        elif sys.argv[1] == "--analyze":
            analyze_display_data()
        else:
            print("使用方法:")
            print("  python generate_display_data.py          # 生成展示数据")
            print("  python generate_display_data.py --preview [数量]  # 预览数据")
            print("  python generate_display_data.py --analyze # 分析数据")
    else:
        generate_display_data() 