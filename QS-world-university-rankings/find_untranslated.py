#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查找翻译失败的大学名称
功能：从data/parsed目录下的*_with_chinese.json文件中找出title_zh为null的记录，输出其title
"""

import json
from pathlib import Path


def find_untranslated_universities():
    """
    查找所有翻译失败的大学名称
    """
    script_dir = Path(__file__).parent
    parsed_dir = script_dir / "data" / "parsed"
    
    if not parsed_dir.exists():
        print(f"解析数据目录 {parsed_dir} 不存在")
        return
    
    # 查找所有带中文翻译的JSON文件
    chinese_files = list(parsed_dir.glob("*_with_chinese.json"))
    
    if not chinese_files:
        print("未找到翻译文件")
        return
    
    print(f"找到 {len(chinese_files)} 个翻译文件")
    
    all_untranslated = []
    
    for file_path in sorted(chinese_files):
        year = file_path.stem.replace("_with_chinese", "")
        print(f"\n=== {year}年 翻译失败的大学 ===")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                universities = json.load(f)
            
            untranslated_in_file = []
            
            for university in universities:
                title = university.get('title', '')
                title_zh = university.get('title_zh')
                
                # 检查title_zh是否为null或空
                if title_zh is None or title_zh == "":
                    untranslated_in_file.append(title)
                    all_untranslated.append((year, title))
            
            if untranslated_in_file:
                for i, title in enumerate(untranslated_in_file, 1):
                    print(f"{i:2d}. {title}")
                print(f"小计：{len(untranslated_in_file)} 所大学")
            else:
                print("无翻译失败的大学")
                
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")
    
    # 输出总结
    print(f"\n{'='*60}")
    print(f"总结：共找到 {len(all_untranslated)} 所翻译失败的大学")
    print(f"{'='*60}")
    
    if all_untranslated:
        print("\n所有翻译失败的大学名称：")
        for i, (year, title) in enumerate(all_untranslated, 1):
            print(f"{i:2d}. [{year}] {title}")
        
        # 统计重复出现的大学
        title_counts = {}
        for year, title in all_untranslated:
            if title not in title_counts:
                title_counts[title] = []
            title_counts[title].append(year)
        
        repeated_titles = {title: years for title, years in title_counts.items() if len(years) > 1}
        
        if repeated_titles:
            print(f"\n重复出现的大学（在多个年份都翻译失败）：")
            for title, years in repeated_titles.items():
                print(f"• {title} (出现年份: {', '.join(years)})")


def export_untranslated_list():
    """
    导出翻译失败的大学名称列表到文本文件
    """
    script_dir = Path(__file__).parent
    parsed_dir = script_dir / "data" / "parsed"
    
    chinese_files = list(parsed_dir.glob("*_with_chinese.json"))
    
    all_untranslated = set()  # 使用set去重
    
    for file_path in chinese_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                universities = json.load(f)
            
            for university in universities:
                title = university.get('title', '')
                title_zh = university.get('title_zh')
                
                if title_zh is None or title_zh == "":
                    all_untranslated.add(title)
                    
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")
    
    # 导出到文件
    output_file = script_dir / "untranslated_universities.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("翻译失败的大学名称列表\n")
        f.write("="*50 + "\n\n")
        for i, title in enumerate(sorted(all_untranslated), 1):
            f.write(f"{i:2d}. {title}\n")
    
    print(f"\n翻译失败的大学名称已导出到: {output_file}")
    print(f"共 {len(all_untranslated)} 所大学（去重后）")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--export":
        export_untranslated_list()
    else:
        find_untranslated_universities()
        print(f"\n提示：使用 '--export' 参数可以将结果导出到文件") 