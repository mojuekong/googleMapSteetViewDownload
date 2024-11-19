import reverse_geocoder as rg

import utils.getProxyParameter
from utils.getLatitudeAndLongitudeFromUrl import extract_coordinates_from_url
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError

def get_location_info_offline(latitude, longitude):
    coordinates = (latitude, longitude)
    results = rg.search(coordinates)  # 返回一个包含地理信息的列表
    if results:
        result = results[0]
        country = result.get('cc', '未知国家')
        admin1 = result.get('admin1', '未知地区')
        name = result.get('name', '未知城市')
        return {
            '国家代码': country,
            '地区': admin1,
            '城市': name
        }
    else:
        return {'国家代码': '未知', '地区': '未知', '城市': '未知'}


# 获取经纬度对应的国家和地区
def get_location_info(latitude, longitude):
    geolocator = Nominatim(user_agent="geoapiExercises", proxies=utils.getProxyParameter.get_clash_proxy())
    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True, language='zh')
        if location:
            address = location.raw.get('address', {})
            country = address.get('country', '未知国家')
            state = address.get('state', '未知地区')
            city = address.get('city', address.get('town', address.get('village', '未知城市')))
            return {
                '国家': country,
                '地区': state,
                '城市': city
            }
        else:
            return {'国家': '未知', '地区': '未知', '城市': '未知'}
    except GeocoderServiceError as e:
        print(f"Geocoding 服务错误: {e}")
        return {'国家': '错误', '地区': '错误', '城市': '错误'}

# 示例使用
# 测试函数
url = "https://www.google.com/maps/@43.1831701,-89.2121317,3a,75y,210.21h,93.47t/data=!3m7!1e1!3m5!1sHpdRhYQCda0PKGEjFaYBNA!2e0!6shttps:%2F%2Fstreetviewpixels-pa.googleapis.com%2Fv1%2Fthumbnail%3Fcb_client%3Dmaps_sv.tactile%26w%3D900%26h%3D600%26pitch%3D-3.4725287897017836%26panoid%3DHpdRhYQCda0PKGEjFaYBNA%26yaw%3D210.20506529051855!7i16384!8i8192?entry=ttu&g_ep=EgoyMDI0MTExMy4xIKXMDSoASAFQAw%3D%3D"
latitude, longitude = extract_coordinates_from_url(url)

print(f"Latitude: {latitude}, Longitude: {longitude}")

location_info = get_location_info(latitude, longitude)
print(location_info)
