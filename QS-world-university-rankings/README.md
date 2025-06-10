QS World University Rankings

## 数据来源
来自QS官网抓取。
接口不能一次返回所有数据，因此需要分页抓取，每页数据设置为500条。
先访问网页，比如： 
```shell
https://www.topuniversities.com/world-university-rankings/2024?items_per_page=10
```

然后F12抓包查看分页请求，将其复制为curl命令，自行修改参数，类似这样：

```shell
curl 'https://www.topuniversities.com/rankings/endpoint?nid=3740566&page=2&items_per_page=500&tab=indicators&region=&countries=&cities=&search=&star=&sort_by=&order_by=&program_type=&scholarship=&fee=&english_score=&academic_score=&mix_student=&loggedincache=6775058-1749267250836' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: zh-CN,zh;q=0.9' \
  -b '_cfuvid=XTF6ORscVd4APFNMqwDkcSZs4cwUh4l50fBJapA8bfA-1749266310198-0.0.1.1-604800000; cookie-agreed-version=1.0.0; cookie-agreed-categories=[%22necessary%22%2C%22analytics%22%2C%22marketing%22]; cookie-agreed=2; STYXKEY-user_survey=other; STYXKEY-social_login_go=6442863; STYXKEY-flexregStep2Content=yes; SSESSd0b453299ef9c5a888765d3401caf373=bO-meYSlnvG966Qj1WG5mXrzUxK1wWUYpULwSdJIUdPcNZMX; STYXKEY-show-step2=1; STYXKEY-qs_new_user=true; STYXKEY-user-name=Leo; STYXKEY-user-communications-optin=No; STYXKEY-user-thirdparty-optin=No; STYXKEY-user_survey_submitted=yes; STYXKEY_current_pageURL=https%3A%2F%2Fwww.topuniversities.com%2Fworld-university-rankings%2F2022%3Fitems_per_page%3D10; STYXKEY_pageVisitCount=16' \
  -H 'priority: u=0, i' \
  -H 'sec-ch-ua: "Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: none' \
  -H 'sec-fetch-user: ?1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'  -o 2022-1500.json
```

## 数据处理

### 合并分割的年份数据
Prompt:
```shell
写脚本实现如下功能：
1、写一个函数，根据传入的文件路径(比如data/raw/slice/2022-500.json)，解析文件内容，提取里面的score_nodes属性的值，进行返回
2、遍历data/raw/slice下的文件，调用第一步的函数对其进行处理，并且把年份相同的数据(即文件名第一段数字相同的文件的数据)合并到一起，写入data/raw/merge目录下，比如data/raw/merge/2022.json
```

```shell
python QS-world-university-rankings/merge_data.py 
```

### 提取国内数据
Prompt:
```shell
写脚本实现如下功能：
1、写一个函数，根据传入的文件路径(比如data/raw/merge/2022.json)，解析文件内容
2、过滤出符合以下条件的学校：
- country字段包含“China (Mainland)”、“Hong Kong SAR”、“Macau SAR”、“Taiwan”
3、把符合条件的学校数据写入data/parsed/目录下，比如data/parsed/2022.json
```

```shell
python QS-world-university-rankings/extract_domestic_data.py 
```

## 翻译大学英文名
**功能：** 批量翻译 `data/parsed/` 目录下所有文件中的大学英文名为中文名

**方案：**
通过包含582所中国大学信息的数据库：[Chinese_Universities](https://github.com/xioajiumi/Chinese_Universities)，构建基础的预定义映射表。
使用创建的 UniversityNameTranslator 类，它结合了预定义映射和在线翻译
- 对于QS排名中的大学：大部分已经预定义好了中文翻译
- 对于未知大学：自动回退到在线翻译

**功能特性：**
- 自动处理 `data/parsed/` 目录下的所有JSON文件
- 排除已翻译的文件（文件名以 `_with_chinese.json` 结尾）
- 支持Unicode字符标准化（如右单引号转换）
- 对每个文件生成对应的中文翻译版本

```shell
python QS-world-university-rankings/translate_university_names.py 
```

**生成的文件格式：**
- 输入：`2022.json` → 输出：`2022_with_chinese.json`
- 在原有数据基础上添加 `title_zh` 字段保存中文校名

### 找出翻译失败的大学

```shell
# 查看所有翻译失败的大学
python QS-world-university-rankings/find_untranslated.py

# 导出到文件
python QS-world-university-rankings/find_untranslated.py --export
```
## 生成展示数据
> 注意：QS500名之后，是没有overall_score值的。
Prompt:
```shell
写脚本实现如下功能：
读取data/parsed目录下的所有with_chinese.json文件，解析文件内容，提取每个元素的title_zh、rank、overall_score、logo字段，生成展示数据，类似这样：
{
    name: title_zh字段,
    value: overall_score字段,
    rank: rank字段,
    date: 文件名的第一个数字，比如2022,
    logo: logo字段
},
将生成的所有数据写入data/display/rank.json文件中
```

```shell
python QS-world-university-rankings/generate_display_data.py 
```
