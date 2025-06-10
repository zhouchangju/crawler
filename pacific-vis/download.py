'''
下载arXiv论文
arXiv: https://arxiv.org/help/api/user-manual#query_details
github：https://github.com/lukasschwab/arxiv.py
'''

import json
import arxiv
import os


def sanitize_filename(text, max_length=50):
    """清理文本，使其成为有效的文件名"""
    # 替换不允许在文件名中使用的字符
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        text = text.replace(char, '-')
    
    # 替换其他可能有问题的字符
    text = text.replace(' ', '_')
    text = text.replace('&', 'and')
    
    # 截断长文本以控制文件名长度，但保留文本的开头部分
    if len(text) > max_length:
        text = text[:max_length]
    
    return text


def download(raw_title, paper_type=None, category=None):
    """下载论文"""
    client = arxiv.Client()

    # 注意，有空格的关键词，必须加上引号和转义符(一般通过完整标题搜索，都必须加这个)
    escaped_title = "\"{}\"".format(raw_title)
    search = arxiv.Search(query=f"ti:{escaped_title}")

    try:
        paper = next(client.results(search))
        print(paper)
        
        # 清理标题、类型和分类，生成有效的文件名
        valid_title = sanitize_filename(raw_title)
        
        # 构建文件名
        if category and paper_type:
            valid_category = sanitize_filename(category, 30)
            filename = f"{valid_category}-{paper_type}-{valid_title}.pdf"
        else:
            filename = f"{valid_title}.pdf"
        
        try:
            paper.download_pdf(dirpath="./arxiv/papers/2025", filename=filename)
            return True
        except arxiv.DownloadFailed:
            print(f"下载失败： {raw_title}")
            return False
    except StopIteration:
        print(f"没有搜索到结果: {raw_title}")
        return False
    except Exception as e:
        print(f"下载时出错: {e}")
        return False


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


def parse_pvis_2025(file):
    """解析PacificVis 2025论文数据"""
    count = 0
    success_count = 0
    
    # 确保保存目录存在
    save_dir = "./arxiv/papers/2025"
    os.makedirs(save_dir, exist_ok=True)
    
    with open(file, 'r', encoding='utf-8') as f:
        papers = json.load(f)
    
    # 按类型和分类整理论文
    papers_by_category = {}
    for paper in papers:
        category = paper['category']
        if category not in papers_by_category:
            papers_by_category[category] = []
        papers_by_category[category].append(paper)
    
    # 逐个下载论文
    for category, category_papers in papers_by_category.items():
        print(f"\n开始下载分类: {category}，共{len(category_papers)}篇论文")
        
        for idx, paper in enumerate(category_papers):
            title = paper['title']
            paper_type = paper['type']
            
            print(f"    [{idx+1}/{len(category_papers)}] [{paper_type}] {title}")
            try:
                success = download(title, paper_type, category)
                if success:
                    success_count += 1
            except Exception as e:
                print(f"    下载出错: {e}")
            
            count += 1
            print(f"处理进度: {count}/{len(papers)}，成功下载: {success_count}")
    
    print(f"\n下载完成，共处理{count}篇论文，成功下载{success_count}篇")


def main():
    """主流程"""
    # 使用新的解析函数处理PacificVis 2025论文数据
    parse_pvis_2025('PVIS-2025-Technical-Sessions.json')


if __name__ == "__main__":
    main()
