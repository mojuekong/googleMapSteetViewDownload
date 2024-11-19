import re

def extract_coordinates_from_url(url):
    # 使用正则表达式提取经纬度
    match = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)", url)

    if match:
        latitude = float(match.group(1))  # 获取纬度
        longitude = float(match.group(2))  # 获取经度
        return latitude, longitude
    else:
        return None, None  # 如果没有找到经纬度


# 测试函数
url = "https://www.google.com/maps/@43.1831701,-89.2121317,3a,75y,210.21h,93.47t/data=!3m7!1e1!3m5!1sHpdRhYQCda0PKGEjFaYBNA!2e0!6shttps:%2F%2Fstreetviewpixels-pa.googleapis.com%2Fv1%2Fthumbnail%3Fcb_client%3Dmaps_sv.tactile%26w%3D900%26h%3D600%26pitch%3D-3.4725287897017836%26panoid%3DHpdRhYQCda0PKGEjFaYBNA%26yaw%3D210.20506529051855!7i16384!8i8192?entry=ttu&g_ep=EgoyMDI0MTExMy4xIKXMDSoASAFQAw%3D%3D"
latitude, longitude = extract_coordinates_from_url(url)

print(f"Latitude: {latitude}, Longitude: {longitude}")
