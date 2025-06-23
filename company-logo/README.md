# 油气公司市值排名爬虫

这个项目用于抓取 [Companies Market Cap](https://companiesmarketcap.com) 网站上油气公司的名称和logo信息，并下载logo图片到本地。

## 功能

- 抓取 5 个页面的油气公司数据（按市值排名）
- 解析公司名称和logo图片地址
- 将数据保存为JSON格式
- 批量下载所有公司的logo图片

## 文件说明

### 主要文件

- `crawl_oil_gas_companies.py` - 主要的爬虫程序
- `download_logos.py` - logo下载程序
- `oil_gas_companies.json` - 抓取到的数据文件（413家公司）
- `requirements.txt` - Python依赖包列表

### 数据目录

- `logo/` - 存放下载的logo图片（413个PNG文件）

## 使用方法

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 抓取公司数据

```bash
python3 crawl_oil_gas_companies.py
```

### 3. 下载logo图片

```bash
python3 download_logos.py
```

### 4. 查看结果

- 公司数据：`oil_gas_companies.json` 文件
- Logo图片：`logo/` 目录

## 数据格式

生成的JSON文件格式如下：

```json
[
  {
    "name": "Saudi Aramco",
    "logo": "https://companiesmarketcap.com/img/company-logos/64/2222.SR.png"
  },
  {
    "name": "Exxon Mobil",
    "logo": "https://companiesmarketcap.com/img/company-logos/64/XOM.png"
  }
]
```

## 抓取和下载结果

- **总计**: 413家油气公司
- **页面范围**: 第1页到第5页
- **数据完整性**: 所有公司都包含名称和logo信息
- **Logo下载**: 413个PNG图片文件，以公司名称命名

## 技术细节

### 数据抓取
- 使用 `requests` 库发送HTTP请求
- 使用 `BeautifulSoup` 解析HTML
- 通过CSS选择器定位数据元素
- 自动处理相对路径转绝对路径
- 包含请求延时避免频繁访问

### Logo下载
- 批量下载所有公司logo
- 自动清理文件名中的特殊字符
- 支持断点续传（跳过已存在文件）
- 包含下载进度显示和统计
- 错误处理和重试机制

## 注意事项

1. 请求间隔设置为合理时间，避免对服务器造成过大压力
2. 使用了真实的浏览器User-Agent来模拟正常访问
3. 包含错误处理机制，确保程序稳定运行
4. Logo图片尺寸为64x64像素
5. 文件名已清理特殊字符，适合各种操作系统

## 示例Logo文件

下载的logo文件示例：
- `Saudi Aramco.png`
- `Exxon Mobil.png`
- `Chevron.png`
- `Shell.png`
- `BP.png`

所有文件都保存在 `logo/` 目录下，使用公司名称命名。 