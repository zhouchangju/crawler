"""
抓取PacificVis 2024网站上的论文列表，并将结果保存为JSON文件，便于批量下载
"""
import json
import requests
from bs4 import BeautifulSoup

type_urls = {
    'TVCG Papers': 'https://pacificvis.github.io/pvis2024/papers/jrnl/',
    #   'Conference papers': 'https://pacificvis.github.io/pvis2024/papers/conf/',
    #   'Visualization Notes': 'https://pacificvis.github.io/pvis2024/papers/notes/',
    #   'Visualization Meets AI Workshop': 'https://pacificvis.github.io/pvis2024/papers/visxai/',
    #   'Posters': 'https://pacificvis.github.io/pvis2024/papers/posters/',
}


def get_papers(url):
    """获取指定网页上的论文列表"""
    # 1. 抓取网页内容
    response = requests.get(url, timeout=5)  # Add timeout argument
    html_content = response.content

    # 2. 解析HTML并输出id="page-title"元素的innerHTML
    soup = BeautifulSoup(html_content, "html.parser")
    page_title = soup.find(id="page-title")
    if page_title:
        print("Page Title:", page_title.get_text(strip=True))
    else:
        print("Page Title element not found.")

    # 3. 解析class="page__content"元素下的所有li元素，生成一个数组并输出
    page_content = soup.find(class_="page__content")
    if page_content:
        li_elements = page_content.find_all("li")
        li_texts = [li.get_text(strip=True) for li in li_elements]
        print("\nList Items:")
        for text in li_texts:
            print("-", text)
        return li_texts
    else:
        print("Page content element not found.")


def main():
    """主函数"""
    papers_for_types = {}
    for key, value in type_urls.items():
        print(key)
        papers = get_papers(value)
        papers_for_types[key] = papers
        print("\n-----------------papers_for_types---------------------\n")
        print(papers_for_types)

    # 将字典转换为JSON字符串
    json_string = json.dumps(papers_for_types)
    # 写入文件
    file = open('./pacific-vis/papers_for_types.json',
                'w', encoding='utf-8')  # Specify encoding
    file.write(json_string)
    file.close()


main()
