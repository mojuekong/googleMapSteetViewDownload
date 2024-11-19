def get_clash_proxy():
    proxies = {
        'http': 'http://127.0.0.1:7890',  # Clash代理的HTTP端口
        'https': 'http://127.0.0.1:7890'  # Clash代理的HTTPS端口
    }
    return proxies

# 调用函数并打印代理设置
proxies = get_clash_proxy()
print(proxies)
