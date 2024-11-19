import requests
from bs4 import BeautifulSoup

# 要爬取的网页 URL
url = 'https://example.com'  # 请替换为您想要爬取的网址

# 发起 HTTP 请求
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    print(f"成功访问: {url}")

    # 解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取网页中的所有标题和链接
    titles = soup.find_all(['h1', 'h2', 'h3'])  # 提取所有标题标签
    links = soup.find_all('a', href=True)  # 提取所有带 href 属性的链接

    # 输出所有标题
    print("\n网页中的标题:")
    for title in titles:
        print(title.get_text())

    # 输出所有链接
    print("\n网页中的链接:")
    for link in links:
        print(link['href'])

else:
    print(f"访问网页失败, 状态码: {response.status_code}")
