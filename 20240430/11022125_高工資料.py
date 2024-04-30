

# 設定 CSV 檔案的 URL
# 以迴圈方式幫我從 https://tisvcloud.freeway.gov.tw/history/TDCS/M03A/20240429/00/TDCS_M03A_20240429_000000.csv  https://tisvcloud.freeway.gov.tw/history/TDCS/M03A/20240429/00/TDCS_M03A_20240429_000500.csv 到 https://tisvcloud.freeway.gov.tw/history/TDCS/M03A/20240429/23/TDCS_M03A_20240429_235500.csv 這個網址下載所有的檔案
import os
import pandas as pd
import requests
import io

for i in range(0, 24):
    for j in range(0, 60, 5):
        # 設定 URL
        url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M03A/20240429/{i:02d}/TDCS_M03A_20240429_{i:02d}{j:02d}00.csv"
        # 下載檔案
        response = requests.get(url)
        # 讀取 CSV 檔案，並設定欄位名稱
        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')), names=['時間', '里程', '南北向', '車種', '數量'])
        # 將處理後的資料寫存入  "C:\\Users\\User\\OneDrive\\桌面\\AI與土木應用\\HW03A"
        df.to_csv(f"C:\\Users\\User\\OneDrive\\桌面\\AI與土木應用\\HW03A\\{i:02d}{j:02d}.csv", index=False)
        print(f"{i:02d}{j:02d}.csv 下載並處理成功")

# 設定目錄路徑 "C:\\Users\\User\\OneDrive\\桌面\\AI與土木應用\\HW03A"
directory = "C:\\Users\\User\\OneDrive\\桌面\\AI與土木應用\\HW03A"

# 獲取目錄下的所有檔案名稱
filenames = os.listdir(directory)

# 讀取每個 CSV 檔案，並將它們存儲在一個列表中
dfs = [pd.read_csv(f"{directory}\\{filename}") for filename in filenames if filename.endswith('.csv')]

# 檢查 dfs 是否為空
if dfs:
    # 合併所有的 DataFrame
    df = pd.concat(dfs, ignore_index=True)

    # 將合併後的 DataFrame 寫入到一個新的 CSV 檔案並存於此位置C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240430
    df.to_csv(r"C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240430\M03A.csv", index=False)
    print("所有 CSV 檔案已成功合併並存儲在 C:\\Users\\User\\OneDrive\\桌面\\AI與土木應用\\GitHub\\cycu_ai2024_shing\\20240430\\M03A\\HW03A.csv")     
else:
    print("在指定的目錄下沒有找到任何 CSV 檔案。")



# 處理 M04A
# 設定 CSV 檔案的 URL
for i in range(0, 24):
    for j in range(0, 60, 5):
        # 設定 URL
        url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M04A/20240429/{i:02d}/TDCS_M04A_20240429_{i:02d}{j:02d}00.csv"
        # 下載檔案
        response = requests.get(url)
        # 讀取 CSV 檔案，並設定欄位名稱
        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')), names=['時間', '上游', '下游', '車種', '車速', '車流量'])
        # 將處理後的資料寫存入 C:\Users\User\OneDrive\桌面\AI與土木應用\HW04A
        df.to_csv(f"C:\\Users\\User\\OneDrive\\桌面\\AI與土木應用\\HW04A\\{i:02d}{j:02d}.csv", index=False)
        print(f"{i:02d}{j:02d}.csv 下載並處理成功")


# 設定目錄路徑C:\Users\User\OneDrive\桌面\AI與土木應用\HW04A
directory = "C:\\Users\\User\\OneDrive\\桌面\\AI與土木應用\\HW04A"   

# 獲取目錄下的所有檔案名稱
filenames = os.listdir(directory)

# 讀取每個 CSV 檔案，並將它們存儲在一個列表中
dfs = [pd.read_csv(f"{directory}\\{filename}") for filename in filenames if filename.endswith('.csv')]

# 檢查 dfs 是否為空
if dfs:
    # 合併所有的 DataFrame
    df = pd.concat(dfs, ignore_index=True)

    # 將合併後的 DataFrame 寫入到一個新的 CSV 檔案並存於此位置C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240430\M04A
    df.to_csv(r"C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240430\M04A.csv", index=False)
    print("所有 CSV 檔案已成功合併並存儲在 C:\\Users\\User\\OneDrive\\桌面\\AI與土木應用\\GitHub\\cycu_ai2024_shing\\20240430\\M04A\\HW04A.csv")     
else:
    print("在指定的目錄下沒有找到任何 CSV 檔案。")
