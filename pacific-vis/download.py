'''
下载arXiv论文
arXiv: https://arxiv.org/help/api/user-manual#query_details
github：https://github.com/lukasschwab/arxiv.py
'''

import json
import arxiv


def download(raw_title):
    """下载论文"""
    client = arxiv.Client()

    # 注意，有空格的关键词，必须加上引号和转义符(一般通过完整标题搜索，都必须加这个)
    escaped_title = "\"{}\"".format(raw_title)
    search = arxiv.Search(query=f"ti:{escaped_title}")

    try:
        paper = next(client.results(search))
        print(paper)
        validTitle = raw_title.replace(': ', '-').replace(':', '-')

        try:
            paper.download_pdf(dirpath="./arxiv/papers/2023",
                               filename=f"{validTitle}.pdf")
        except arxiv.DownloadFailed:
            print(f"下载失败： {raw_title}")
    except arxiv.PaperNotFound:
        print("没有搜索到结果")


def parse_map(file):
    """解析不同类型的论文"""
    count = 0
    with open(file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for key, value in data.items():
        print(f"开始下载分类: {key}, {value}")
        if isinstance(value, list):
            for idx, item in enumerate(value):
                print(f"    Item {idx}: {item}")
                download(item)
                count += 1
                print(f"已下载【{count}】篇论文")
        else:
            print(f"无效的list: {value}")
    print(f"下载完成，共下载【{count}】篇论文")


def parse_list(file):
    """解析返回的paper列表"""
    count = 0
    with open(file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if isinstance(data, list):
        for idx, item in enumerate(data):
            print(f"    Item {idx}: {item}")
            download(item)
            count += 1
            print(f"已下载【{count}】篇论文")
        print(f"下载完成，共下载【{count}】篇论文")
    else:
        print(f"无效的list: {data}")


def main():
    """主流程"""
    parse_list('./arxiv/titles.json')


main()
