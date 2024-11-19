import reverse_geocoder as rg
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
from utils.getProxyParameter import get_clash_proxy

def get_location_info_offline(latitude, longitude):
    '''
    根据经纬度获取地理信息，使用离线数据  --------- 暂时不好用
    :param latitude: 经度
    :param longitude: 纬度
    :return:
    '''
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
    '''
    根据经纬度获取地理信息，使用在线数据  --------- 推荐使用
    :param latitude:
    :param longitude:
    :return:
    '''
    geolocator = Nominatim(user_agent="geoapiExercises", proxies=get_clash_proxy())
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