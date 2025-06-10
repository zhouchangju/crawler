#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def check_extraction_results():
    """检查提取结果"""
    with open('data/parsed/2022.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print('提取的国内大学总数:', len(data))
    print('\n按地区分布:')
    regions = {}
    for univ in data:
        country = univ.get('country', 'Unknown')
        if country not in regions:
            regions[country] = []
        regions[country].append(univ['title'])

    for country, universities in regions.items():
        print(f'\n{country} ({len(universities)} 所):')
        for i, name in enumerate(universities[:5], 1):
            print(f'  {i}. {name}')
        if len(universities) > 5:
            print(f'  ... 还有 {len(universities) - 5} 所大学')

if __name__ == "__main__":
    check_extraction_results() 