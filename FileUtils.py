import os
import shutil

#按行读取文件数据
def read_file_by_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            return lines
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

#删除空文件夹数据
def delete_empty_folders(root_folder):
    # 获取目录下所有子文件夹
    subfolders = [f.path for f in os.scandir(root_folder) if f.is_dir()]

    # 遍历子文件夹，判断是否为空并删除空文件夹
    for folder in subfolders:
        if not os.listdir(folder):
            shutil.rmtree(folder)  # 删除空文件夹
            print(f"Deleted empty folder: {folder}")

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            print(f"Directory '{directory_path}' created successfully.")
        except OSError as e:
            print(f"Error creating directory '{directory_path}': {e}")
    else:
        print(f"Directory '{directory_path}' already exists.")

def svae_file(file_path,fileName,content_to_print):
    # 打开文件并写入内容
    create_directory_if_not_exists(file_path)
    with open(file_path+"/"+fileName, 'a') as file:
        file.write(content_to_print)
# 示例用法
file_path = "example.txt"
lines = read_file_by_lines(file_path)

if lines:
    for line in lines:
        print(line.strip())  # 使用strip()方法去除每行末尾的换行符