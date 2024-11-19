import requests

# 图像URL
url = "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2614988097.webp"

# 设置代理（Clash代理）
proxies = {
    'http': 'http://127.0.0.1:7890',  # Clash代理的HTTP端口
    'https': 'http://127.0.0.1:7890'  # Clash代理的HTTPS端口
}

# 发送HTTP GET请求
response = requests.get(url, proxies=proxies)

# 检查请求是否成功
if response.status_code == 200:
    # 以二进制模式写入文件
    with open("jingshi_chuanjie.webp", "wb") as file:
        file.write(response.content)
    print("图像下载成功！")
else:
    print(f"下载失败，状态码：{response.status_code}")
