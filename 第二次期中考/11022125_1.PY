import os
import requests
import pandas as pd
from datetime import datetime, timedelta
import tarfile
import time
from pathlib import Path

# 建立日期範圍
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 4, 30)
date_range = [start_date + timedelta(days=x) for x in range((end_date-start_date).days + 1)]

# 建立資料夾
os.makedirs('C:\\Users\\User\\Documents\\GitHub\\cycu_ai2024_shing\\20240521', exist_ok=True)
os.makedirs('C:\\Users\\User\\OneDrive\\M05A', exist_ok=True)

df_all = pd.DataFrame()

for date in date_range:
    date_str = date.strftime('%Y%m%d')
    
    # 檢查是否存在壓縮檔
    tar_url = f'https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/M05A_{date_str}.tar.gz'
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.head(tar_url)
            break
        except requests.exceptions.ConnectionError:
            if i < max_retries - 1:
                time.sleep(2 ** i)
                continue
            else:
                raise

    if response.status_code == 200:
        # 下載壓縮檔，並儲存於"C:\Users\User\OneDrive\M05A"
        r = requests.get(tar_url)
        tar_path = Path(f'C:\\Users\\User\\OneDrive\\M05A\\M05A_{date_str}.tar.gz')
        tar_path.parent.mkdir(parents=True, exist_ok=True)  # 確保目錄存在
        tar_path.write_bytes(r.content)
    else:
        print(f'{date_str} 沒有壓縮檔。')
            

    # 如果沒有壓縮檔，則下載每五分鐘的 csv 檔案，並儲存於"C:\Users\User\OneDrive\M05A"
    for hour in range(24):
        for minute in range(0, 60, 5):
            csv_url = f'https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/{date_str}/{hour:02d}/TDCS_M05A_{date_str}_{hour:02d}{minute:02d}00.csv'
            max_retries = 5
            for i in range(max_retries):
                try:
                    response = requests.head(csv_url)
                    break
                except requests.exceptions.ConnectionError:
                    if i < max_retries - 1:
                        time.sleep(2 ** i)
                        continue
                    else:
                        raise

            if response.status_code == 200:
                # 下載 csv 檔案
                   r = requests.get(csv_url)
                   csv_path = Path(f'C:\\Users\\User\\OneDrive\\M05A\\{date_str}_{hour:02d}{minute:02d}.csv')
                   csv_path.parent.mkdir(parents=True, exist_ok=True)  # 確保目錄存在
                   csv_path.write_bytes(r.content)
            else:
                print(f'{date_str}_{hour:02d}{minute:02d} 沒有 csv 檔案。')



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
# 合併檔案
# 這段程式碼會根據日期來選擇合併方式。如果日期小於或等於 2024-04-19，則使用第一種方式合併；否則，使用第二種方式合併。
# 建立日期範圍
dates = pd.date_range(start='2024-01-01', end='2024-04-30')

for date in dates:
    date_str = date.strftime('%Y%m%d')
    dfs = []
    for i in range(24):
        for j in range(0, 60, 5):
            if date <= pd.Timestamp('2024-04-19'):
                csv_path = Path(f"C:\\Users\\User\\OneDrive\\M05A\\解壓縮\\{date_str}\\{i:02d}\\TDCS_M05A_{date_str}_{i:02d}{j:02d}00.csv")
            else:
                csv_path = Path(f"C:\\Users\\User\\OneDrive\\M05A\\TDCS_M05A_{date_str}_{i:02d}{j:02d}00.csv")
            
            if csv_path.exists():
                df = pd.read_csv(csv_path, names=["TimeInterval", "GantryFrom", "GantryTo", "VehicleType", "SpaceMeanSpeed", "交通量"])
                df['SpaceMeanSpeed'] = df.loc[df['VehicleType'] == 31, 'SpaceMeanSpeed']
                df['v31'] = df.loc[df['VehicleType'] == 31, '交通量']
                df['v32'] = df.loc[df['VehicleType'] == 32, '交通量']
                df['v41'] = df.loc[df['VehicleType'] == 41, '交通量']
                df['v42'] = df.loc[df['VehicleType'] == 42, '交通量']
                df['v5'] = df.loc[df['VehicleType'] == 5, '交通量']
                df = df.drop(columns=["VehicleType", "交通量"])
                dfs.append(df)
                df.to_csv(f"C:\\Users\\User\\OneDrive\\M05A\\整理過後的M05A\\M05A_{date_str}.csv", index=False)
               
    if dfs:
        df = pd.concat(dfs, ignore_index=True)
        df.to_csv(f"C:\\Users\\User\\OneDrive\\M05A\\整理過後的M05A\\M05A_{date_str}.csv", index=False)
    print("已合併", date_str)