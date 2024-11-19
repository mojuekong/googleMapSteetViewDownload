import os
import shutil  # 用于文件操作，如移动文件


def move_jpg(oldpath, newpath):
    # 遍历源路径中的所有文件和子目录
    for root, dirs, files in os.walk(oldpath):
        for file in files:
            # 仅处理以 .jpg 结尾的文件
            if file.lower().endswith('.jpg'):
                # 构建旧文件的完整路径
                oldfile = os.path.join(root, file)
                # 构建新文件的完整路径
                newfile = os.path.join(newpath, file)

                # 如果目标路径中的文件已存在，添加编号以避免覆盖
                if os.path.exists(newfile):
                    base, ext = os.path.splitext(file)
                    count = 1
                    while os.path.exists(newfile):
                        newfile = os.path.join(newpath, f"{base}_{count}{ext}")
                        count += 1

                # 移动文件
                shutil.move(oldfile, newfile)
                print(f"Moved: {oldfile} -> {newfile}")


if __name__ == "__main__":
    oldpath = r"F:\postgraduateFiles\pyProject\crawler"  # 替换为源文件夹路径
    newpath = r"F:\postgraduateFiles\pyProject\crawler\googleStreetImgs"  # 替换为目标文件夹路径
    move_jpg(oldpath, newpath)
