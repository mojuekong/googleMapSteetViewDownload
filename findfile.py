import os
import fnmatch

# 设置要搜索的目录路径
# search_dir = r'D:\BaiduNetdiskDownload\GDAL_Development_Kits(VS2008_2017)'

search_dir = r'D:\\'

# 设置要查找的文件名
target_file = 'gdal1202.dll'

# 遍历目录查找文件
def find_file_in_directory(directory, filename):
    # 遍历目录及子目录
    for root, dirs, files in os.walk(directory):
        # 使用 fnmatch 查找匹配的文件
        for file in fnmatch.filter(files, filename):
            # 输出找到的文件路径
            return os.path.join(root, file)
    return None

# 调用函数
file_path = find_file_in_directory(search_dir, target_file)

# 输出结果
if file_path:
    print(f'文件 {target_file} 找到: {file_path}')
else:
    print(f'未找到文件 {target_file}')
