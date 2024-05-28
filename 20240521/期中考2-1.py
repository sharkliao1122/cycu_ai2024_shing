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


# 解壓縮所有 此位置"C:\Users\User\OneDrive\M05A"的所有 tar.gz 檔案 
# 將解壓縮後的檔案存至 "C:\Users\User\OneDrive\M05A\解壓縮M05A"
tar_files = list(Path('C:\\Users\\User\\OneDrive\\M05A').glob('M05A_*.tar.gz'))
os.makedirs('C:\\Users\\User\\OneDrive\\M05A\\解壓縮M05A', exist_ok=True)
for tar_file in tar_files:
    with tarfile.open(tar_file, 'r:gz') as tar:
        tar.extractall('C:\\Users\\User\\OneDrive\\M05A\\解壓縮M05A')

        




# 讀取所有 csv 檔案，將其合併成一個 DataFrame
dfs = []
for i in range(24):
    for j in range(0, 60, 5):
        csv_path = Path(f"C:\\Users\\User\\OneDrive\\M05A\\M05A_20240101\\M05A\\20240101\\{i:02d}\\TDCS_M05A_20240101_{i:02d}{j:02d}00.csv")
        if csv_path.exists():
            df = pd.read_csv(csv_path, names=["TimeInterval", "GantryFrom", "GantryTo", "VehicleType", "SpaceMeanSpeed", "TrafficVolume"])
            dfs.append(df)

df = pd.concat(dfs, ignore_index=True) if dfs else print("在指定的目錄下沒有找到任何 CSV 檔案。")

# 將 DataFrame 進行處理
df = df.pivot(index=["TimeInterval", "GantryFrom", "GantryTo", "SpaceMeanSpeed"], columns="VehicleType", values="TrafficVolume")
df.columns = [f"V{col}" for col in df.columns]
df = df.reset_index()

# 儲存處理後的 DataFrame
os.makedirs('C:\\Users\\User\\OneDrive\\M05A\\整理過後的M05A', exist_ok=True)
df.to_csv('C:\\Users\\User\\OneDrive\\M05A\\整理過後的M05A\\整理過後的M05A.csv', index=False)




