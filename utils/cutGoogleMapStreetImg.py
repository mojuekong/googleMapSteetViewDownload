import numpy as np
from PIL import Image
import os

import utils.convert_path_to_unix_style
import cv2
import glob


def crop_image_by_ratio_cv(input_path, output_path, top_ratio=0.4, bottom_ratio=0.2):
    """
    按照指定的高度比例裁剪图像，并将裁剪后的图像保存到新的路径。

    参数:
    - input_path (str): 原始图像文件的路径。
    - output_path (str): 保存裁剪后图像的路径。
    - top_ratio (float): 要去除的顶部比例（默认0.4，即40%）。
    - bottom_ratio (float): 要去除的底部比例（默认0.2，即20%）。

    示例:
    crop_image_by_ratio_cv("path/to/your/original_image.jpg", "path/to/save/cropped_image.jpg", 0.4, 0.2)
    """
    try:
        print("\n=== 开始按比例裁剪图像 ===")

        # 移除路径中的所有双引号
        input_path_clean = input_path.replace('"', '')
        output_path_clean = output_path.replace('"', '')

        # 打印原始和清理后的路径
        print(f"原始输入路径: {input_path}")
        print(f"原始输出路径: {output_path}")
        print(f"清理后的输入路径: {input_path_clean}")
        print(f"清理后的输出路径: {output_path_clean}")

        # 检查输入路径是否存在
        if not os.path.exists(input_path_clean):
            print(f"错误：无法找到文件 {input_path_clean}")
            return
        else:
            print(f"文件存在: {input_path_clean}")

        # 读取图像
        img = cv2.imread(input_path_clean)
        if img is None:
            print(f"错误：无法读取图像 {input_path_clean}")
            return
        else:
            print(f"图像读取成功: {input_path_clean}")
            print(f"图像尺寸: {img.shape}")  # (高度, 宽度, 通道数)

        # 获取图像高度和宽度
        height, width = img.shape[:2]
        print(f"图像高度: {height}")
        print(f"图像宽度: {width}")

        # 计算裁剪区域的起始和结束行
        start_row = int(height * top_ratio)
        end_row = int(height * (1 - bottom_ratio))
        print(f"裁剪区域起始行: {start_row} ({top_ratio * 100}%)")
        print(f"裁剪区域结束行: {end_row} ({(1 - bottom_ratio) * 100}%)")

        # 检查裁剪区域是否有效
        if start_row >= end_row:
            print("错误：裁剪区域无效。请检查裁剪比例。")
            return
        else:
            print(f"裁剪区域范围: 从第 {start_row} 行到第 {end_row} 行")

        # 裁剪图像
        cropped_img = img[start_row:end_row, :, :]
        print(f"裁剪后的图像尺寸: {cropped_img.shape}")  # (裁剪后高度, 宽度, 通道数)

        # 确保输出目录存在，如果不存在则创建
        output_dir = os.path.dirname(output_path_clean)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"已创建输出目录: {output_dir}")
        else:
            if output_dir:
                print(f"输出目录已存在: {output_dir}")
            else:
                print("输出路径中没有目录部分，直接保存到当前目录。")

        # 保存裁剪后的图像到输出路径
        success = cv2.imwrite(output_path_clean, cropped_img)
        if success:
            print(f"裁剪后的图像已保存至：{output_path_clean}")
        else:
            print(f"错误：无法保存裁剪后的图像至 {output_path_clean}")

    except FileNotFoundError:
        print(f"错误：未找到文件 {input_path}")
    except Exception as e:
        print(f"处理图像时发生错误：{e}")


def process_folder(input_folder, output_folder, top_ratio=0.4, bottom_ratio=0.2):
    """
    遍历输入文件夹中的所有 JPG 图像，按指定比例裁剪，并保存到输出文件夹中。

    参数:
    - input_folder (str): 包含待处理 JPG 图像的输入文件夹路径。
    - output_folder (str): 保存裁剪后图像的输出文件夹路径。
    - top_ratio (float): 要去除的顶部比例（默认0.4，即40%）。
    - bottom_ratio (float): 要去除的底部比例（默认0.2，即20%）。

    示例:
    process_folder("path/to/input_folder", "path/to/output_folder", 0.4, 0.2)
    """
    try:
        print("\n=== 开始批量处理文件夹中的图像 ===")
        print(f"输入文件夹路径: {input_folder}")
        print(f"输出文件夹路径: {output_folder}")

        # 检查输入文件夹是否存在
        if not os.path.exists(input_folder):
            print(f"错误：无法找到输入文件夹 {input_folder}")
            return

        # 获取所有 JPG 图像路径（包括子文件夹）
        image_paths = glob.glob(os.path.join(input_folder, '**', '*.jpg'), recursive=True)
        print(f"找到 {len(image_paths)} 张 JPG 图像需要处理。")

        if not image_paths:
            print("没有找到任何 JPG 图像。")
            return

        for img_path in image_paths:
            # 构建相对路径
            relative_path = os.path.relpath(img_path, input_folder)
            print(f"\n处理图像: {img_path}")

            # 构建输出路径
            output_path = os.path.join(output_folder, relative_path)
            print(f"对应的输出路径: {output_path}")

            # 调用裁剪函数
            crop_image_by_ratio_cv(img_path, output_path, top_ratio, bottom_ratio)

    except Exception as e:
        print(f"批量处理时发生错误：{e}")

def remove_black_rows_binary(input_path, output_path, threshold=127):
    """
    移除图像顶部和底部的全黑色行，并将裁剪后的图像保存到新的路径。
    通过二值化图像检测黑色像素。

    参数:
    - input_path (str): 原始图像文件的路径。
    - output_path (str): 保存裁剪后图像的路径。
    - threshold (int): 二值化的阈值，默认为127。

    示例:
    remove_black_rows_cv("path/to/your/original_image.jpg", "path/to/save/cropped_image.jpg")
    """
    try:
        print("\n=== 开始处理图像 ===")

        # 移除路径中的所有双引号
        input_path_clean = input_path.replace('"', '')
        output_path_clean = output_path.replace('"', '')

        # 打印原始和清理后的路径
        print(f"原始输入路径: {input_path}")
        print(f"原始输出路径: {output_path}")
        print(f"清理后的输入路径: {input_path_clean}")
        print(f"清理后的输出路径: {output_path_clean}")

        # 检查输入路径是否存在
        if not os.path.exists(input_path_clean):
            print(f"错误：无法找到文件 {input_path_clean}")
            return
        else:
            print(f"文件存在: {input_path_clean}")

        # 读取图像
        img = cv2.imread(input_path_clean)
        if img is None:
            print(f"错误：无法读取图像 {input_path_clean}")
            return
        else:
            print(f"图像读取成功: {input_path_clean}")
            print(f"图像尺寸: {img.shape}")  # (高度, 宽度, 通道数)

        # 转换为灰度图像
        grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print("图像已转换为灰度图像。")

        # 检查灰度图像是否为空
        if grayscale.size == 0:
            print("错误：灰度图像为空。")
            return
        else:
            print(f"灰度图像尺寸: {grayscale.shape}")  # (高度, 宽度)

        # 二值化图像
        _, binary = cv2.threshold(grayscale, threshold, 255, cv2.THRESH_BINARY)
        print(f"图像已二值化，使用的阈值: {threshold}")

        # 显示二值化图像尺寸
        print(f"二值化图像尺寸: {binary.shape}")

        # 统计黑色像素（在二值化图像中，黑色为0，白色为255）
        total_pixels = binary.shape[0] * binary.shape[1]
        black_pixels = np.sum(binary == 0)
        white_pixels = np.sum(binary == 255)
        print(f"总像素数: {total_pixels}")
        print(f"黑色像素数: {black_pixels}")
        print(f"白色像素数: {white_pixels}")
        print(f"黑色像素占比: {black_pixels / total_pixels * 100:.2f}%")

        # 创建一个布尔数组，标记每一行是否全黑（所有像素为0）
        all_black_rows = np.all(binary == 0, axis=1)
        num_total_rows = binary.shape[0]
        num_all_black = np.sum(all_black_rows)
        print(f"总行数: {num_total_rows}")
        print(f"全黑行数: {num_all_black}")

        # 如果图像全黑，输出提示并返回
        if np.all(all_black_rows):
            print("图像全黑，无需处理。")
            return
        else:
            print("图像包含非全黑行，需要进行裁剪。")

        # 找到第一个非全黑的行索引
        first_non_black = np.argmax(~all_black_rows)
        print(f"第一个非全黑的行索引: {first_non_black}")

        # 找到最后一个非全黑的行索引
        last_non_black = num_total_rows - 1 - np.argmax(~all_black_rows[::-1])
        print(f"最后一个非全黑的行索引: {last_non_black}")

        # 检查索引是否有效
        if first_non_black > last_non_black:
            print("错误：未找到有效的裁剪区域。")
            return
        else:
            print(f"裁剪区域范围: {first_non_black} 到 {last_non_black} 行")

        # 裁剪图像：从 first_non_black 到 last_non_black 行（包含）
        cropped_img = img[first_non_black:last_non_black + 1, :, :]
        print(f"裁剪后的图像尺寸: {cropped_img.shape}")  # (裁剪后高度, 宽度, 通道数)

        # 确保输出目录存在，如果不存在则创建
        output_dir = os.path.dirname(output_path_clean)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"已创建输出目录: {output_dir}")
        else:
            if output_dir:
                print(f"输出目录已存在: {output_dir}")
            else:
                print("输出路径中没有目录部分，直接保存到当前目录。")

        # 保存裁剪后的图像到输出路径
        success = cv2.imwrite(output_path_clean, cropped_img)
        if success:
            print(f"已移除顶部和底部的全黑色行，裁剪后的图像已保存至：{output_path_clean}")
        else:
            print(f"错误：无法保存裁剪后的图像至 {output_path_clean}")

    except FileNotFoundError:
        print(f"错误：未找到文件 {input_path}")
    except Exception as e:
        print(f"处理图像时发生错误：{e}")

def remove_black_rows(input_path, output_path):
    """
    移除图像顶部和底部的全黑色行，并将裁剪后的图像保存到新的路径。

    参数:
    - input_path (str): 原始图像文件的路径。
    - output_path (str): 保存裁剪后图像的路径。

    示例:
    remove_black_rows_cv("path/to/your/original_image.jpg", "path/to/save/cropped_image.jpg")
    """
    try:
        print("开始处理图像...")

        # 移除路径中的所有双引号
        input_path_clean = input_path.replace('"', '')
        output_path_clean = output_path.replace('"', '')

        # 打印原始和清理后的路径
        print(f"原始输入路径: {input_path}")
        print(f"原始输出路径: {output_path}")
        print(f"清理后的输入路径: {input_path_clean}")
        print(f"清理后的输出路径: {output_path_clean}")

        # 检查输入路径是否存在
        if not os.path.exists(input_path_clean):
            print(f"错误：无法找到文件 {input_path_clean}")
            return
        else:
            print(f"文件存在: {input_path_clean}")

        # 读取图像
        img = cv2.imread(input_path_clean)
        if img is None:
            print(f"错误：无法读取图像 {input_path_clean}")
            return
        else:
            print(f"图像读取成功: {input_path_clean}")
            print(f"图像尺寸: {img.shape}")  # (高度, 宽度, 通道数)

        # 转换为灰度图像
        grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print("图像已转换为灰度图像。")

        # 检查灰度图像是否为空
        if grayscale.size == 0:
            print("错误：灰度图像为空。")
            return
        else:
            print(f"灰度图像尺寸: {grayscale.shape}")  # (高度, 宽度)

        # 创建一个布尔数组，标记每一行是否全黑（灰度值为0）
        all_black_rows = np.all(grayscale == 0, axis=1)
        num_total_rows = grayscale.shape[0]
        num_all_black = np.sum(all_black_rows)
        print(f"总行数: {num_total_rows}")
        print(f"全黑行数: {num_all_black}")

        # 如果图像全黑，输出提示并返回
        if np.all(all_black_rows):
            print("图像全黑，无需处理。")
            return
        else:
            print("图像包含非全黑行，需要进行裁剪。")

        # 找到第一个非全黑的行索引
        first_non_black = np.argmax(~all_black_rows)
        print(f"第一个非全黑的行索引: {first_non_black}")

        # 找到最后一个非全黑的行索引
        last_non_black = num_total_rows - 1 - np.argmax(~all_black_rows[::-1])
        print(f"最后一个非全黑的行索引: {last_non_black}")

        # 检查索引是否有效
        if first_non_black > last_non_black:
            print("错误：未找到有效的裁剪区域。")
            return
        else:
            print(f"裁剪区域范围: {first_non_black} 到 {last_non_black} 行")

        # 裁剪图像：从 first_non_black 到 last_non_black 行（包含）
        cropped_img = img[first_non_black:last_non_black + 1, :, :]
        print(f"裁剪后的图像尺寸: {cropped_img.shape}")  # (裁剪后高度, 宽度, 通道数)

        # 确保输出目录存在，如果不存在则创建
        output_dir = os.path.dirname(output_path_clean)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"已创建输出目录: {output_dir}")
        else:
            if output_dir:
                print(f"输出目录已存在: {output_dir}")
            else:
                print("输出路径中没有目录部分，直接保存到当前目录。")

        # 保存裁剪后的图像到输出路径
        success = cv2.imwrite(output_path_clean, cropped_img)
        if success:
            print(f"已移除顶部和底部的全黑色行，裁剪后的图像已保存至：{output_path_clean}")
        else:
            print(f"错误：无法保存裁剪后的图像至 {output_path_clean}")

    except FileNotFoundError:
        print(f"错误：未找到文件 {input_path}")
    except Exception as e:
        print(f"处理图像时发生错误：{e}")


def count_min_grayscale_pixels(image_path):
    """
    读取JPG RGB图像，转换为灰度图像，并打印灰度值最大的像素数量。

    :param image_path: 图像文件的路径
    """
    try:
        # 打开图像文件
        with Image.open(image_path) as img:
            # 将图像转换为灰度图
            grayscale = img.convert('L')
            print(f" 图像的总像素的个数是 ：  {grayscale.size[0] * grayscale.size[1]}")

            # 获取所有像素的灰度值并转换为列表
            pixels = list(grayscale.getdata())

            # 找到最大灰度值
            max_gray = min(pixels)

            # 计算具有最大灰度值的像素数量
            count = pixels.count(max_gray)

            # 打印结果
            print(f"灰度值最小的像素数量为: {count}， 最小的灰度值是: {min(pixels)}")

    except FileNotFoundError:
        print(f"文件未找到: {image_path}")
    except Exception as e:
        print(f"发生错误: {e}")

def count_black_rows(image_path):
    """
    读取JPG RGB图像，转换为灰度图像，并计算每一行全部为黑色像素的行数。

    :param image_path: 图像文件的路径
    """
    try:
        # 打开图像文件
        with Image.open(image_path) as img:
            # 将图像转换为灰度图
            grayscale = img.convert('L')
            print(f"图像的总像素的个数是: {grayscale.size[0] * grayscale.size[1]}")

            # 获取所有像素的灰度值并转换为列表
            pixels = list(grayscale.getdata())

            # 获取图像的宽度和高度
            width, height = grayscale.size

            # 统计每一行全为0的行数
            black_row_count = 0

            # 遍历每一行
            for y in range(height):
                # 获取当前行的像素数据
                row = pixels[y * width:(y + 1) * width]
                # 如果这一行的所有像素值都是0，说明这一行是黑色的
                if all(pixel == 0 for pixel in row):
                    black_row_count += 1

            # 打印结果
            print(f"完全是黑色的行数为: {black_row_count}")

    except FileNotFoundError:
        print(f"文件未找到: {image_path}")
    except Exception as e:
        print(f"发生错误: {e}")

def test_count_min_grayscale_pixels():
    image_path = r"D:\postgraduateFiles\pyProject\crawler\googleStreetImgs\42.3969023_-94.6303308_美利坚合众国_艾奥瓦州\stl-42.395421_-94.6376329_美利坚合众国_艾奥瓦州_1.jpg"  # 替换为你的图像路径
    count_min_grayscale_pixels(image_path)

def test_remove_black_rows():
    image_path = "D:\\postgraduateFiles\\pyProject\\crawler\\googleStreetImgs\\42.3969023_-94.6303308_美利坚合众国_艾奥瓦州\\stl-42.951301_-91.8099438_美利坚合众国_艾奥瓦州_1_1_1_1_1_1_1_1.jpg"  # 替换为你的图像路径
    print(f" image_path:{image_path}")
    googleStreetImgsAfterCutFolder = "D:\\postgraduateFiles\\pyProject\\crawler\\googleStreetImgAfterCut\\stl-42.951301_-91.8099438_美利坚合众国_艾奥瓦州_1_1_1_1_1_1_1_1.jpg"
    print(f"googleStreetImgsAfterCutFolder :{googleStreetImgsAfterCutFolder} ")
    remove_black_rows(image_path, googleStreetImgsAfterCutFolder)

def test_count_black_rows():
    image_path = r"D:\postgraduateFiles\pyProject\crawler\googleStreetImgs\42.3969023_-94.6303308_美利坚合众国_艾奥瓦州\stl-42.395421_-94.6376329_美利坚合众国_艾奥瓦州_1.jpg"  # 替换为你的图像路径
    count_black_rows(image_path)

def test_remove_black_rows_binary():
    image_path = "D:\\postgraduateFiles\\pyProject\\crawler\\googleStreetImgs\\42.3969023_-94.6303308_美利坚合众国_艾奥瓦州\\stl-42.951301_-91.8099438_美利坚合众国_艾奥瓦州_1_1_1_1_1_1_1_1.jpg"  # 替换为你的图像路径
    print(f" image_path:{image_path}")
    googleStreetImgsAfterCutFolder = "D:\\postgraduateFiles\\pyProject\\crawler\\googleStreetImgAfterCut\\stl-42.951301_-91.8099438_美利坚合众国_艾奥瓦州_1_1_1_1_1_1_1_1.jpg"
    print(f"googleStreetImgsAfterCutFolder :{googleStreetImgsAfterCutFolder} ")
    remove_black_rows_binary(image_path, googleStreetImgsAfterCutFolder)

def test_crop_image_by_ratio_cv():
    image_path = "D:\\postgraduateFiles\\pyProject\\crawler\\googleStreetImgs\\42.3969023_-94.6303308_美利坚合众国_艾奥瓦州\\"  # 替换为你的图像路径
    print(f" image_path:{image_path}")
    googleStreetImgsAfterCutFolder = "D:\\postgraduateFiles\\pyProject\\crawler\\googleStreetImgAfterCut\\"
    print(f"googleStreetImgsAfterCutFolder :{googleStreetImgsAfterCutFolder} ")
    process_folder(image_path, googleStreetImgsAfterCutFolder)

# 示例使用
if __name__ == "__main__":
    # test_count_min_grayscale_pixels()

    # test_count_black_rows()

    # test_remove_black_rows()

    # test_remove_black_rows_binary()

    test_crop_image_by_ratio_cv()
