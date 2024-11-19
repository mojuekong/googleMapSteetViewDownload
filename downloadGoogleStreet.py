import os
import shutil

import requests
from PIL import Image
import subprocess
import hashlib
import sys
import zlib
import asyncio
import aiohttp
import re
import sys
from utils.get_location_info import get_location_info
from utils.extract_cunntry_and_city import extract_city_name,extract_country_name
from utils.remove_all_spaces import remove_all_spaces

googleStreetImgsFolderPath = "./googleStreetImgs"

# 设置代理（Clash代理）
proxies = {
    'http': 'http://127.0.0.1:7890',  # Clash代理的HTTP端口
    'https': 'http://127.0.0.1:7890'  # Clash代理的HTTPS端口
}

# OpId 类：处理 ID 的生成和管理
class OpId:
    def __init__(self, id):
        self.id_src = id
        self.id_op = self.make_id(id)

    def make_id(self, id):
        id_hash = hashlib.new('ripemd160', id.encode('utf-8')).hexdigest()
        id_crc = zlib.crc32(id.encode('utf-8'))
        return f"op{id_hash}{id_crc}"

    def get_id_src(self):
        return self.id_src

    def get_id_op(self):
        return self.id_op

# OpUrlList 类：处理 URL 列表和文件下载
class OpUrlList:
    def __init__(self):
        self.url_list = []

    def clear(self):
        self.url_list.clear()

    def add_url(self, url, file):
        self.url_list.append((url, file))

    def download_requests(self):
        for url, file in self.url_list:
            print(f"Downloading {url} to {file}...")
            try:
                response = requests.get(url, stream=True, proxies=proxies)
                if response.status_code == 200:
                    with open(file, 'wb') as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                else:
                    print(f"Failed to download {url}, status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error downloading {url}: {e}")

    async def download_aiohttp(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url, file in self.url_list:
                print(f"Downloading {url} to {file}...")
                tasks.append(self.download_file(session, url, file))
            await asyncio.gather(*tasks)

    async def download_file(self, session, url, file):
        try:
            async with session.get(url, proxy="http://127.0.0.1:7890") as response:
                if response.status == 200:
                    with open(file, 'wb') as f:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            f.write(chunk)
                else:
                    print(f"Failed to download {url}, status code: {response.status}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")

    def remove_files(self):
        for url, file in self.url_list:
            if os.path.exists(file):
                os.remove(file)
        print("Temporary files cleaned up.")

    def print_debug(self):
        for item in self.url_list:
            print(f"URL {item[0]} File {item[1]}")

# OpSt 类：处理主要的下载逻辑
class OpSt:
    def __init__(self, id, location_name = ""):
        self.op_id = OpId(id)
        self.op_url_list = OpUrlList()
        self.location_name = location_name

    def download(self):
        print("Downloading...")
        self.make_img_list()
        # 使用同步下载方法
        self.op_url_list.download_requests()
        # 如果你想使用异步下载，可以使用以下代码：
        # asyncio.run(self.op_url_list.download_aiohttp())
        print("Creating montage...")
        self.make_montage()
        print("Cleaning temp files...")
        self.op_url_list.remove_files()

    def make_img_list(self):
        self.op_url_list.clear()
        x_ini, x_fin = 0, 25
        y_ini, y_fin = 0, 12
        num_file = 1
        codigo = self.op_id.get_id_src()
        id = self.op_id.get_id_op()

        for y_act in range(y_ini, y_fin + 1):
            for x_act in range(x_ini, x_fin + 1):
                url = f"https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=maps_sv.tactile&panoid={codigo}&x={x_act}&y={y_act}&zoom=5&nbt=1&fover=2"
                file = f"tmp-f{id}_{num_file}.jpg"
                num_file += 1
                self.op_url_list.add_url(url, file)

    def make_montage(self):
        id = self.op_id.get_id_op()
        id_src = self.op_id.get_id_src()
        tile_width, tile_height = 500, 500  # 每个瓦片的大小

        # 定义拼接后的图像大小
        cols, rows = 26, 13
        montage_width = cols * tile_width
        montage_height = rows * tile_height

        # 创建一个新的空白图像
        montage_image = Image.new('RGB', (montage_width, montage_height))

        for i in range(1, 339):
            file = f"tmp-f{id}_{i}.jpg"
            if not os.path.exists(file):
                print(f"Warning: {file} does not exist.")
                continue
            try:
                tile = Image.open(file)
                # 计算瓦片的位置
                x = (i - 1) % cols * tile_width
                y = (i - 1) // cols * tile_height
                montage_image.paste(tile, (x, y))
            except Exception as e:
                print(f"Error processing {file}: {e}")

        # 保存拼接后的图像
        # montage_path = f"stl-{id_src}.jpg"
        montage_path = f"stl-{self.location_name}.jpg"
        montage_image.save(montage_path, quality=100)
        print(f"{montage_path} created.")

    def print_debug(self):
        self.make_img_list()
        self.op_url_list.print_debug()
        self.op_id.print_debug()

# 图片处理和修改 EXIF 信息
def resize_equi(path_src, path_dst, width):
    height = width // 2
    with Image.open(path_src) as img:
        img = img.resize((width, height), Image.LANCZOS)
        img.save(path_dst, quality=100)
    print(f"Resized {path_src} to {path_dst} with size {width}x{height}.")

def add_exif_equi(path, width):
    height = width // 2
    exiftool_cmd = (
        f"exiftool -overwrite_original "
        f"-UsePanoramaViewer=True "
        f"-ProjectionType=equirectangular "
        f"-PoseHeadingDegrees=180.0 "
        f"-CroppedAreaLeftPixels=0 "
        f"-FullPanoWidthPixels={width} "
        f"-CroppedAreaImageHeightPixels={height} "
        f"-FullPanoHeightPixels={height} "
        f"-CroppedAreaImageWidthPixels={width} "
        f"-CroppedAreaTopPixels=0 "
        f"-LargestValidInteriorRectLeft=0 "
        f"-LargestValidInteriorRectTop=0 "
        f"-LargestValidInteriorRectWidth={width} "
        f"-LargestValidInteriorRectHeight={height} "
        f"-Model='github fdd4s streetview-dl' "
        f"\"{path}\""
    )
    subprocess.run(exiftool_cmd, shell=True)
    print(f"Added EXIF tags to {path}.")

# 从 URL 获取 ID
def get_id_from_url(url):
    try:
        fields = url.split("!1s")
        fields2 = fields[1].split("!")
        return fields2[0]
    except IndexError:
        print("Error: Unable to extract ID from URL.")
        sys.exit(1)

# 最后保存的jpg图像 匹配中间的id 去创建文件夹
def match_substring(text):
    """
    使用正则表达式匹配以 '-' 开始，并以 '.jpg' 结尾的字符串，
    并提取 '-' 和 '.jpg' 之间的内容。

    参数:
    - text (str): 要匹配的文本。

    返回:
    - list: 匹配的子字符串列表。

    示例:
    >>> match_substring("image-tmp-fop<hash>_1.jpg")
    ['tmp-fop<hash>_1']
    """
    # 正则表达式：匹配以 '-' 开始，以 '.jpg' 结尾的字符串，中间可以是任意字符
    pattern = r'-(.*?)\.jpg$'  # (.*?) 表示非贪婪匹配中间的任何字符，\.jpg$ 确保以 .jpg 结尾
    matches = re.findall(pattern, text, re.IGNORECASE)  # re.IGNORECASE 忽略大小写

    return matches


def create_folder(name):
    # 获取文件夹名称
    folder_name = match_substring(name)  # 确保这是单一的字符串
    if isinstance(folder_name, list):
        folder_name = folder_name[0]  # 取第一个匹配的文件夹名称

    target_folder = os.path.join(googleStreetImgsFolderPath, folder_name)  # 拼接目标文件夹路径

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)  # 创建文件夹
        print(f"Created folder {folder_name} in {googleStreetImgsFolderPath}")
    else:
        print(f"Folder {folder_name} already exists in {googleStreetImgsFolderPath}.")

    return target_folder


def move_jpg(folder, newfolder):
    """
    Move JPG files from folder to newfolder. \n
    folder: 原文件夹路径                       \n
    newfolder: 新文件夹路径
    """
    move_jpg_list = []

    # 获取源文件夹下所有 JPG 文件
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith('.jpg'):
                file_abspath = os.path.join(root, file)
                move_jpg_list.append(file_abspath)

    # 确保目标文件夹存在
    if not os.path.exists(newfolder):
        os.makedirs(newfolder)

    for file_abspath in move_jpg_list:
        file_name = os.path.basename(file_abspath)
        new_file_abspath = os.path.join(newfolder, file_name)

        # 如果目标文件夹中已有同名文件，则进行重命名
        if os.path.exists(new_file_abspath):
            base, ext = os.path.splitext(file_name)
            count = 1
            while os.path.exists(new_file_abspath):
                new_file_abspath = os.path.join(newfolder, f"{base}_{count}{ext}")
                count += 1

        shutil.move(file_abspath, new_file_abspath)  # 移动文件
        print(f"Moved img [{file_abspath}] -> [{new_file_abspath}]")

def run_streetview_download(id, latitude, longitude):
    if len(id) < 10 or len(id) > 30:
        print("Wrong ID.")
        return

    print(f"Pano ID: {id}")

    location_info = get_location_info(latitude, longitude)

    state = location_info.get('国家', '未知国家')
    simplified_state = extract_country_name(state)
    city = location_info.get('地区', '未知地区')
    simplified_city = extract_city_name(city)

    location_name = f"{latitude}_{longitude}_{simplified_state}_{simplified_city}"
    location_name = remove_all_spaces(location_name)

    op_st = OpSt(id, location_name=location_name)
    op_st.download()

    pathL = f"stl-{location_name}.jpg"
    print(f"{pathL} created.")
    create_folder(pathL)

    print("Resizing...")
    pathM = f"stm-{location_name}.jpg"
    resize_equi(pathL, pathM, 8192)

    print(f"{pathM} created.")

    pathS = f"sts-{location_name}.jpg"
    resize_equi(pathM, pathS, 1300)

    print(f"{pathS} created.")

    print("Adding equirectangular pano EXIF tags...")
    add_exif_equi(pathL, 13000)
    add_exif_equi(pathM, 8192)
    add_exif_equi(pathS, 1300)

    move_jpg(".", os.path.join("./googleStreetImgs", location_name))

    print("Done.")
# 主程序
def main(location_name):
    if len(sys.argv) != 2:
        print("Syntax: python streetview_dl.py <url>\nRemember to put the URL between single quotes.")
        sys.exit(0)

    id = sys.argv[1]
    if "/" in id:
        id = get_id_from_url(id)
        print(f"id = {id}")

    if len(id) < 10 or len(id) > 30:
        print("Wrong ID.")
        sys.exit(0)

    print(f"Pano ID: {id}")

    op_st = OpSt(id)
    op_st.download()

    pathL = f"stl-{id}.jpg"
    print(f"{pathL} created.")
    create_folder(pathL)

    print("Resizing...")
    pathM = f"stm-{id}.jpg"
    resize_equi(pathL, pathM, 8192)

    print(f"{pathM} created.")

    pathS = f"sts-{id}.jpg"
    resize_equi(pathM, pathS, 1300)

    print(f"{pathS} created.")

    print("Adding equirectangular pano EXIF tags...")
    add_exif_equi(pathL, 13000)
    add_exif_equi(pathM, 8192)
    add_exif_equi(pathS, 1300)

    move_jpg("F:\postgraduateFiles\pyProject\crawler", f"F:/postgraduateFiles/pyProject/crawler/googleStreetImgs/{location_name}")

    print("Done.")

if __name__ == "__main__":
    # main(location_name=get_location_info(
    print(f"hello world!")