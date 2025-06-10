#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试extract_score_nodes函数的使用示例
"""

from process_data import extract_score_nodes

def test_single_file():
    """
    测试单个文件的score_nodes提取功能
    """
    # 测试文件路径
    test_file = "data/raw/slice/2022-500.json"
    
    print(f"正在测试文件: {test_file}")
    print("-" * 40)
    
    # 调用函数提取数据
    score_nodes = extract_score_nodes(test_file)
    
    if score_nodes:
        print(f"成功提取到 {len(score_nodes)} 条记录")
        print("\n前3条记录的大学信息:")
        for i, node in enumerate(score_nodes[:3]):
            print(f"{i+1}. {node.get('title', 'N/A')} - 排名: {node.get('rank', 'N/A')}")
    else:
        print("未能提取到数据")

if __name__ == "__main__":
    test_single_file() 