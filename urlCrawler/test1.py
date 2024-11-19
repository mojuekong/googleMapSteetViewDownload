from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

from ..utils.getProxyParameter import get_clash_proxy


# 初始化浏览器
def init_driver():
    options = webdriver.ChromeOptions()

    # 设置代理
    options.add_argument(f'--proxy-server={get_clash_proxy()["http"]}')

    options.add_argument("--headless")  # 无头模式，不显示浏览器界面
    driver = webdriver.Chrome(options=options)
    return driver


# 打开地图页面并选取路段
def scrape_map_urls(driver, base_url, roads):
    driver.get(base_url)
    time.sleep(5)  # 等待页面加载

    urls = []
    for road in roads:
        try:
            # 在搜索框输入路段名
            search_box = driver.find_element(By.XPATH,
                                             '//*[@id="searchboxinput"]')  # 搜索框的XPath
            search_box.clear()
            search_box.send_keys(road)
            search_box.send_keys(Keys.ENTER)

            time.sleep(3)  # 等待搜索结果加载

            # 获取当前URL
            current_url = driver.current_url
            print(f"URL for {road}: {current_url}")
            urls.append((road, current_url))
        except Exception as e:
            print(f"Error processing road {road}: {e}")

    return urls


# 主函数
if __name__ == "__main__":
    # 初始参数
    base_url = "https://www.google.com/maps"
    roads = ["Main Street, Madison", "State Street, Chicago",
             "Wall Street, New York"]  # 路段名称列表

    # 初始化浏览器
    driver = init_driver()

    try:
        # 爬取地图URL
        urls = scrape_map_urls(driver, base_url, roads)

        # 输出或保存结果
        for road, url in urls:
            print(f"{road}: {url}")
    finally:
        driver.quit()
