import re

def extract_country_name(text):
    # 使用正则表达式匹配并提取 `/` 前面的部分
    match = re.match(r'([^/]+)', text)
    if match:
        return match.group(1)  # 返回第一个匹配到的部分
    else:
        return text  # 如果没有 `/`，返回原始字符串

def extract_city_name(text):
    # 使用正则表达式匹配并提取 `/` 前面的部分
    match = re.match(r'([^/]+)', text)
    if match:
        return match.group(1)  # 返回第一个匹配到的部分
    else:
        return text  # 如果没有 `/`，返回原始字符串

print(extract_country_name('美利坚合众国/美利堅合眾國'))  # 输出: 美利坚合众国
print(extract_city_name('威斯康星州 / 威斯康辛州'))  # 输出: 美利坚合众国