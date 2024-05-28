import os
import requests
import pandas as pd
from datetime import datetime, timedelta
import tarfile
import time
from pathlib import Path

# 用迴圈方式解壓縮 
# 檔案格式如下 "C:\Users\User\OneDrive\M05A\M05A_20240101.tar.gz" 到 "C:\Users\User\OneDrive\M05A\M05A_20240419.tar.gz" (2024/01/01 ~ 2024/04/19)
# 刪除原本的壓縮檔，將解壓縮後的檔案存於""C:\Users\User\OneDrive\M05A\解壓縮""
# 建立日期範圍

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 4, 19)
date_range = [start_date + timedelta(days=x) for x in range((end_date-start_date).days + 1)]

os.makedirs('C:\\Users\\User\\OneDrive\\M05A', exist_ok=True)   
for date in date_range:
    date_str = date.strftime('%Y%m%d')
    tar_path = Path(f'C:\\Users\\User\\OneDrive\\M05A\\M05A_{date_str}.tar.gz')
    if tar_path.exists():
        with tarfile.open(tar_path, 'r:gz') as tar:
            tar.extractall('C:\\Users\\User\\OneDrive\\M05A')
        tar_path.unlink()  # 刪除原本的壓縮檔
    else:   
        print(f'{date_str} 沒有壓縮檔。')

# 讀取 CSV 檔案 依照日期一天一天將CSV檔案依照欄位(TimeInterval、GantryFrom、GantryTo、VehicleType、SpaceMeanSpeed、交通量)合併
# 從"C:\Users\User\OneDrive\M05A\解壓縮\20240101\00\TDCS_M05A_20240101_000000.csv" 到"C:\Users\User\OneDrive\M05A\解壓縮\20240101\23\TDCS_M05A_20240101_235500.csv" 將其合併為一個檔案 叫做 "MO5A_20240101.csv"
# 從"C:\Users\User\OneDrive\M05A\解壓縮\20240102\00\TDCS_M05A_20240102_000000.csv" 到"C:\Users\User\OneDrive\M05A\解壓縮\20240102\23\TDCS_M05A_20240102_235500.csv" 將其合併為一個檔案 叫做 "MO5A_20240102.csv"
# 建立日期範圍


# 建立日期範圍
dates = pd.date_range(start='2024-01-01', end='2024-01-02')

for date in dates:
    date_str = date.strftime('%Y%m%d')
    dfs = []
    for i in range(24):
        for j in range(0, 60, 5):
            csv_path = Path(f"C:\\Users\\User\\OneDrive\\M05A\\解壓縮\\{date_str}\\{i:02d}\\TDCS_M05A_{date_str}_{i:02d}{j:02d}00.csv")
            if csv_path.exists():
                df = pd.read_csv(csv_path, names=["TimeInterval", "GantryFrom", "GantryTo", "VehicleType", "SpaceMeanSpeed", "交通量"])
                 # 將　df　中的欄位名稱改為下列9個欄位名稱
                # "TimeInterval"
                # "GantryFrom"
                # "GantryTo"
                # "SpaceMeanSpeed" (改為只要 "VehicleType" 為 31，所對應之 "SpaceMeanSpeed" 的值)
                # "v31" (改為只要 "VehicleType" 為 31，所對應之 "交通量" 的值)
                # "v32" (改為只要 "VehicleType" 為 32，所對應之 "交通量" 的值)
                # "v41" (改為只要 "VehicleType" 為 41，所對應之 "交通量" 的值)
                # "v42" (改為只要 "VehicleType" 為 42，所對應之 "交通量" 的值)
                # "v5"  (改為只要 "VehicleType" 為  5，所對應之 "交通量" 的值)
                # 刪除  "VehicleType" "交通量" 欄位
    
                df['SpaceMeanSpeed'] = df.loc[df['VehicleType'] == 31, 'SpaceMeanSpeed']
                df['v31'] = df.loc[df['VehicleType'] == 31, '交通量']
                df['v32'] = df.loc[df['VehicleType'] == 32, '交通量']
                df['v41'] = df.loc[df['VehicleType'] == 41, '交通量']
                df['v42'] = df.loc[df['VehicleType'] == 42, '交通量']
                df['v5'] = df.loc[df['VehicleType'] == 5, '交通量']
                df = df[["TimeInterval", "GantryFrom", "GantryTo", "SpaceMeanSpeed", "v31", "v32", "v41", "v42", "v5"]]
               
                
                dfs.append(df)
    if dfs:
        df = pd.concat(dfs, ignore_index=True)
        df.to_csv(f"C:\\Users\\User\\OneDrive\\M05A\\解壓縮\\MO5A_{date_str}.csv", index=False)
    else:
        print(f"在指定的目錄下沒有找到 {date_str} 的 CSV 檔案。")