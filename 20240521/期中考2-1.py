import os
import requests
import pandas as pd
from datetime import datetime, timedelta
import tarfile
import time

# 建立日期範圍
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 4, 30)
date_range = [start_date + timedelta(days=x) for x in range((end_date-start_date).days + 1)]

# 建立資料夾
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
        # 下載壓縮檔
        r = requests.get(tar_url)
        tar_path = f'C:\\Users\\User\\OneDrive\\M05A\\M05A_{date_str}.tar.gz'
        os.makedirs(os.path.dirname(tar_path), exist_ok=True)  # 確保目錄存在
        with open(tar_path, 'wb') as f:
            f.write(r.content)
            

    # 如果沒有壓縮檔，則下載每五分鐘的 csv 檔案
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
                csv_path = f'C:\\Users\\User\\OneDrive\\M05A\\TDCS_M05A_{date_str}_{hour:02d}{minute:02d}00.csv'
                os.makedirs(os.path.dirname(csv_path), exist_ok=True)  # 確保目錄存在
                with open(csv_path, 'wb') as f:
                    f.write(r.content)