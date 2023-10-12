import os
import shutil

def delete_empty_folders(root_folder):
    # 获取目录下所有子文件夹
    subfolders = [f.path for f in os.scandir(root_folder) if f.is_dir()]

    # 遍历子文件夹，判断是否为空并删除空文件夹
    for folder in subfolders:
        if not os.listdir(folder):
            shutil.rmtree(folder)  # 删除空文件夹
            print(f"Deleted empty folder: {folder}")


# 示例：删除目录 "/path/to/your/folder" 下的空文件夹
delete_empty_folders("E:\\folder\\hotgirl\\")
