# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import requests  # 用requests库来获取网页
import xlwt  # 进行excel操作
import time  # 用于设置延时

# 正则表达式规则
findLink = re.compile(r'<a href="(.*?)">')  # 影片详情链接
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # 影片图片链接
findTitle = re.compile(r'<span class="title">(.*)</span>')  # 影片标题
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')  # 评分
findJudge = re.compile(r'<span>(\d*)人评价</span>')  # 评价人数
findInq = re.compile(r'<span class="inq">(.*)</span>')  # 影片一句话简介
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)  # 影片简介

def main():
    # 获取 IP 和地区信息
    get_ip_and_location()

    baseurl = "https://movie.douban.com/top250?start="  # 要爬取的网页链接
    datalist = getData(baseurl)  # 爬取网页
    savepath = "豆瓣电影Top250.xls"  # 存储的Excel文件路径
    saveData(datalist, savepath)  # 保存数据到Excel


def get_ip_and_location():
    try:
        # 设置代理（Clash代理）
        proxies = {
            'http': 'http://127.0.0.1:7890',  # Clash代理的HTTP端口
            'https': 'http://127.0.0.1:7890'  # Clash代理的HTTPS端口
        }
        # 获取公共 IP 地址
        ip_response = requests.get('https://api.ipify.org?format=json', proxies=proxies)
        ip_data = ip_response.json()
        ip_address = ip_data.get('ip')
        print(f"Your public IP address is: {ip_address}")

        # 获取地理位置 (根据 IP 地址查询)
        location_response = requests.get(f'https://ipinfo.io/{ip_address}/json', proxies=proxies)
        location_data = location_response.json()
        region = location_data.get('region', 'Unknown')
        city = location_data.get('city', 'Unknown')
        country = location_data.get('country', 'Unknown')

        print(f"Location: {city}, {region}, {country}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP or location: {e}")


def askURL(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Referer': 'https://movie.douban.com/top250'
    }
    # 设置代理（Clash代理）
    proxies = {
        'http': 'http://127.0.0.1:7890',  # Clash代理的HTTP端口
        'https': 'http://127.0.0.1:7890'  # Clash代理的HTTPS端口
    }

    try:
        # 发送请求并添加延时
        response = requests.get(url, proxies=proxies, headers=headers)  # 使用代理
        response.raise_for_status()  # 如果请求失败，抛出异常
        response.encoding = response.apparent_encoding  # 自动设置编码
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def getData(baseurl):
    datalist = []  # 用来存储爬取的网页信息
    for i in range(0, 10):  # 获取10页数据
        url = baseurl + str(i * 25)  # 每次翻页，URL中的start=0, 25, 50...
        html = askURL(url)  # 获取网页源码
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            for item in soup.find_all('div', class_='item'):
                data = []
                item_str = str(item)

                # 获取影片详情链接
                link = re.findall(findLink, item_str)[0]
                # 获取影片图片链接
                img_src = re.findall(findImgSrc, item_str)[0]
                # 获取影片标题
                title = re.findall(findTitle, item_str)
                # 获取影片评分
                rating = re.findall(findRating, item_str)
                # 获取影片评价人数
                judge = re.findall(findJudge, item_str)
                # 获取影片一句话简介
                inq = re.findall(findInq, item_str)
                # 获取影片简介
                bd = re.findall(findBd, item_str)

                # 存储数据
                data.append(link)
                data.append(img_src)
                data.append(title[0] if title else '')
                data.append(rating[0] if rating else '')
                data.append(judge[0] if judge else '')
                data.append(inq[0] if inq else '')
                data.append(bd[0] if bd else '')

                # 将数据添加到列表
                datalist.append(data)

        # 延时，避免请求过快
        time.sleep(2)

    return datalist


def saveData(datalist, savepath):
    # 创建Excel文件，写入数据
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet("豆瓣电影Top250", cell_overwrite_ok=True)

    # 写入表头
    headers = ['电影详情链接', '图片链接', '电影标题', '评分', '评价人数', '一句话简介', '影片简介']
    for col, header in enumerate(headers):
        sheet.write(0, col, header)

    # 写入数据
    for i, data in enumerate(datalist, start=1):
        for j, item in enumerate(data):
            sheet.write(i, j, item)

    # 保存文件
    workbook.save(savepath)


if __name__ == '__main__':
    main()
