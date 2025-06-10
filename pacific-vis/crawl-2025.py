import requests
from bs4 import BeautifulSoup
import json
import re

def crawl_pacific_vis_2025():
    url = "https://pacificvis2025.github.io/pages/TechnicalSessions.html"
    
    # 发送HTTP请求
    response = requests.get(url)
    if response.status_code != 200:
        print(f"请求失败，状态码: {response.status_code}")
        return None
    
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 存储所有论文信息的列表
    papers = []
    
    # 查找所有的时间段和分类标题
    sections = soup.find_all(lambda tag: tag.name == 'h3' and 'April' in tag.text)
    
    for section in sections:
        current_time = section.text.strip()
        # 查找下一个h5标签，它包含分类信息
        category_tag = section.find_next('h5')
        if not category_tag:
            continue
            
        current_category = category_tag.text.strip()
        
        # 查找所有的论文（每篇论文都有一个 badge-tvcg/conf/note 和 strong 标签）
        # 从当前分类标签开始，直到下一个时间段
        next_section = category_tag.find_next(lambda tag: tag.name == 'h3' and 'April' in tag.text)
        
        # 查找所有带有论文类型badge的p标签
        current_tag = category_tag
        while current_tag and (not next_section or current_tag != next_section):
            if current_tag.name == 'p' and current_tag.find(class_=re.compile(r'badge-(tvcg|conf|note)')):
                paper_type_tag = current_tag.find(class_=re.compile(r'badge-(tvcg|conf|note)'))
                paper_type = paper_type_tag.text.strip()
                
                title_tag = current_tag.find('strong')
                if title_tag:
                    paper_title = title_tag.text.strip()
                    
                    # 查找作者列表（通常在下一个ul标签中）
                    authors = []
                    author_list = current_tag.find_next('ul')
                    if author_list:
                        for li in author_list.find_all('li'):
                            author = li.text.strip()
                            if author:
                                authors.append(author)
                    
                    papers.append({
                        'title': paper_title,
                        'type': paper_type,
                        'category': current_category,
                        'time': current_time,
                        'authors': authors
                    })
            
            current_tag = current_tag.find_next()
            if current_tag and (next_section and current_tag == next_section):
                break
    
    return papers

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    print("开始抓取PacificVis 2025论文信息...")
    papers = crawl_pacific_vis_2025()
    
    if papers:
        print(f"共抓取到 {len(papers)} 篇论文")
        save_to_json(papers, "PVIS-2025-Technical-Sessions.json")
        print("数据已保存到 PVIS-2025-Technical-Sessions.json")
    else:
        print("抓取失败，未获取到论文信息")
