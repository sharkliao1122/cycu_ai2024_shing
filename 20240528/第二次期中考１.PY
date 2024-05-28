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

# 讀取 CSV 檔案 依照日期一天一天將CSV檔案合併
# 從"C:\Users\User\OneDrive\M05A\解壓縮\20240101\00\TDCS_M05A_20240101_000000.csv" 到"C:\Users\User\OneDrive\M05A\解壓縮\20240101\23\TDCS_M05A_20240101_235500.csv" 將其合併為一個檔案 叫做 "MO5A_20240101.csv"
# 從"C:\Users\User\OneDrive\M05A\解壓縮\20240102\00\TDCS_M05A_20240102_000000.csv" 到"C:\Users\User\OneDrive\M05A\解壓縮\20240102\23\TDCS_M05A_20240102_235500.csv" 將其合併為一個檔案 叫做 "MO5A_20240102.csv"
# 建立日期範圍
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 1, 2)
date_range = [start_date + timedelta(days=x) for x in range((end_date-start_date).days + 1)]

df_all = pd.DataFrame()
for date in date_range:
    date_str = date.strftime('%Y%m%d')
    df_date = pd.DataFrame()
    for hour in range(24):
        for minute in range(0, 60, 5):
            csv_path = Path(f'C:\\Users\\User\\OneDrive\\M05A\\解壓縮\\{date_str}\\{hour:02d}\\TDCS_M05A_{date_str}_{hour:02d}{minute:02d}00.csv')
            if csv_path.exists():
                df = pd.read_csv(csv_path)
                df_date = pd.concat([df_date, df], ignore_index=True)
    if not df_date.empty:
        df_date.to_csv(f'C:\\Users\\User\\OneDrive\\M05A\\M05A_{date_str}.csv', index=False)
        df_all = pd.concat([df_all, df_date], ignore_index=True)
    else:
        print(f'{date_str} 沒有 CSV 檔案。')



