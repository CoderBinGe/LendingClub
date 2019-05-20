import os
import zipfile
import pandas as pd

from data_process_tool import analyze_data

dataset_path = './dataset'
zip_file_path = './dataset/loan.zip'
file_path = './dataset/loan.csv'


def run_main():
    # 如果不存在csv文件，就解压zip文件
    if not os.path.exists(file_path):
        with zipfile.ZipFile(zip_file_path) as zf:
            zf.extractall(dataset_path)

    # 读取数据
    data = pd.read_csv(file_path, low_memory=False)
    # print(data.info())
    # print(data.head())
    # print(data.describe())

    # 对数据进行分析
    analyze_data(data)

    if os.path.exists(file_path):
        # 如果存在csv文件，删除csv文件，释放空间
        os.remove(file_path)


if __name__ == '__main__':
    run_main()
