import os
import pandas as pd
import requests
import io

# 建立資料夾
os.makedirs('C:\\Users\\User\\OneDrive\\M05A0429', exist_ok=True)

for i in range(0, 24):
    for j in range(0, 60, 5):
       
        # 設定 URL
        url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/20240429/{i:02d}/TDCS_M05A_20240429_{i:02d}{j:02d}00.csv"
       
        # 下載檔案
        response = requests.get(url)
       
        # 讀取 CSV 檔案，並設定欄位名稱
        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')), names=["TimeInterval", "GantryFrom", "GantryTo", "VehicleType", "SpaceMeanSpeed", "TrafficVolume"])
       
        # 將處理後的資料寫存入 C:\Users\User\OneDrive\M05A0429
        df.to_csv(f"C:\\Users\\User\\OneDrive\\M05A0429\\{i:02d}{j:02d}.csv", index=False)
        print(f"{i:02d}{j:02d}.csv 下載並處理成功")

# 設定目錄路徑C:\Users\User\OneDrive\M05A0429
directory = r"C:\Users\User\OneDrive\M05A0429"

# 獲取目錄下的所有檔案名稱
filenames = os.listdir(directory)

# 讀取每個 CSV 檔案，並將它們存儲在一個列表中
dfs = [pd.read_csv(f"{directory}\\{filename}") for filename in filenames if filename.endswith('.csv')]

# 檢查 dfs 是否為空
if dfs:
    
    # 依照欄位名稱合併所有的 DataFrame，欄位名稱如下 TimeInterval、GantryFrom、GantryTo、VehicleType、SpaceMeanSpeed、交通量
    df = pd.concat(dfs, ignore_index=True)

    # 將合併後的 DataFrame 寫入到一個新的 CSV 檔案並存於此位置C:\Users\User\OneDrive\M05A0429
    df.to_csv(r"C:\Users\User\OneDrive\M05A0429\M05A.csv", index=False)
else:
    print("在指定的目錄下沒有找到任何 CSV 檔案。")

