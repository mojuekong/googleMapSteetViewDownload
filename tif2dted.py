from osgeo import gdal

def tiff_to_geotiff(input_tiff, output_geotiff):
    # 打开 TIFF 文件
    dataset = gdal.Open(input_tiff)
    if not dataset:
        print("无法打开 TIFF 文件。")
        return

    # 获取输入文件的投影信息和地理坐标
    projection = dataset.GetProjection()
    geo_transform = dataset.GetGeoTransform()

    # 创建一个输出文件（GeoTIFF 格式）
    driver = gdal.GetDriverByName('GTiff')
    if not driver:
        print("GDAL 不支持 GeoTIFF 格式。")
        return

    # 创建 GeoTIFF 输出文件
    output_ds = driver.Create(output_geotiff, dataset.RasterXSize, dataset.RasterYSize, 1, gdal.GDT_Float32)

    # 设置投影信息和地理坐标
    output_ds.SetProjection(projection)
    output_ds.SetGeoTransform(geo_transform)

    # 将 TIFF 中的高程数据复制到输出文件
    band = dataset.GetRasterBand(1)  # 获取第一个波段（假设高程数据在第一个波段）
    data = band.ReadAsArray()  # 读取数据
    output_band = output_ds.GetRasterBand(1)
    output_band.WriteArray(data)  # 将数据写入 GeoTIFF 文件

    # 清理
    output_ds = None
    dataset = None

    print(f"成功将 TIFF 文件转换为 GeoTIFF 格式: {output_geotiff}")


# 示例：将 input.tif 转换为 output.tif
tiff_to_geotiff(r'C:\Users\50505\Documents\WeChat Files\wxid_s7s2s0kx1vi422\FileStorage\File\2024-11\n00_e009_1arc_v3.tif', r'C:\Users\50505\Documents\WeChat Files\wxid_s7s2s0kx1vi422\FileStorage\File\2024-11\n00_e009_1arc_v3_output.tif')
