import downloadGoogleStreet
import json
from utils.getLatitudeAndLongitudeFromUrl import extract_coordinates_from_url
from utils.get_location_info import get_location_info
import os
from utils.extract_cunntry_and_city import extract_city_name,extract_country_name
from utils.remove_all_spaces import remove_all_spaces

def get_existing_folders(folder_path):
    try:
        return set(os.listdir(folder_path))
    except FileNotFoundError:
        print(f"Error: The folder {folder_path} does not exist.")
        return set()

def call_streetview_script(url, existing_folders):
    id = downloadGoogleStreet.get_id_from_url(url)
    print(f"id = {id}")
    latitude, longitude = extract_coordinates_from_url(url)  # 得到 经纬度
    location_info = get_location_info(latitude, longitude)
    state = location_info.get('国家', '未知国家')
    simplified_state = extract_country_name(state)
    city = location_info.get('地区', '未知地区')
    simplified_city = extract_city_name(city)
    print(f"经纬度是 ： {latitude}, {longitude} ， 国家是：{simplified_state}， 地区是： {simplified_city}")
    folderName = f"{latitude}_{longitude}_{simplified_state}_{simplified_city}"
    folderName = remove_all_spaces(folderName)
    print(f"Folder ---> {folderName} ")

    # 检查并处理
    if folderName in existing_folders:
        print(f"Folder '{folderName}' 已经存在，已遍历过。")
    else:
        # 调用下载脚本
        downloadGoogleStreet.run_streetview_download(id, latitude, longitude)


if __name__ == "__main__":
    # 读取 JSON 文件
    with open('googleStreetHtml.json', 'r') as file:
        data = json.load(file)

    # 获取现有的文件夹名称
    existing_folders = get_existing_folders("./googleStreetImgs")
    print(f"Existing folders: {existing_folders}")

    # 遍历所有 URL
    for url in data["urls"]:
        print(url)
        call_streetview_script(str(url), existing_folders)

