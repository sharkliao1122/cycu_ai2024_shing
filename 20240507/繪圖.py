import os
import pandas as pd
import requests
import io

# 設定目錄路徑C:\Users\User\Documents\GitHub\cycu_ai2024_shing\20240507
# 幫我將 保留 vehicleType 為 31 和 GantryFrom 開頭前三碼為01F，並將資料存入 C:\Users\User\Documents\GitHub\cycu_ai2024_shing\20240507\M05A_31.csv
# 讀取 CSV 檔案
df = pd.read_csv(r"C:\Users\User\Documents\GitHub\cycu_ai2024_shing\20240507\M05A.csv")

# 保留 vehicleType 為 31 和 GantryFrom 開頭前三碼為01F 的所有資料
df = df[(df["VehicleType"] == 31) & (df["GantryFrom"].str.startswith("01F"))]

# 將處理後的資料寫存入 C:\Users\User\Documents\GitHub\cycu_ai2024_shing\20240507\M05A_31.csv
df.to_csv(r"C:\Users\User\Documents\GitHub\cycu_ai2024_shing\20240507\M05A_31.csv", index=False)

# 因為我們要做機器學習，所以必須對資料做特徵化工程，將資料轉換成機器學習模型可以理解的形式
# 請幫我將 TimeInterval 欄位轉換成數值型態,數值每日的第幾個五分鐘(0~287)，如 00:00 為第0個五分鐘 00:05 為 第一個 5分鐘
# 命名為 TimeIndex，其餘資料不必轉換
# 讀取 CSV 檔案
df = pd.read_csv(r"C:\Users\User\Documents\GitHub\cycu_ai2024_shing\20240507\M05A_31.csv")

# 將 TimeInterval 欄位轉換成數值型態 ( x軸 )
df['TimeInterval'] = pd.to_datetime(df['TimeInterval']).apply(lambda x: x.hour * 12 + x.minute // 5)
print(df['TimeInterval'])

# 將 GantryFrom、GantryFrom 欄位轉換成數值型態 ( y軸 )如 01F0017N 為 170， 01F0018N 為 180 ， 01F0019S 為 191，01F0017S 為 171, 01F0018S 為 181 (里程FROM)
def gantry_to_numeric(gantry):
    if gantry[-1] == 'N':
        return int(gantry[3:7])*10 
    elif gantry[-1] == 'S':
        return int(gantry[3:7])*10 + 1

df['GantryFrom'] = df['GantryFrom'].apply(gantry_to_numeric)

df['GantryTo'] = df['GantryTo'].apply(gantry_to_numeric)

# 將兩個欄位合併成一個欄位(將gantryfrom * 100000 與 gantryto 相加)，命名為 GantryFromTo  (y軸)
df['GantryFromTo'] = df['GantryFrom'] * 100000 + df['GantryTo']
print(df['GantryFromTo'])

#列印TrafficVolume
print(df['TrafficVolume'])

# 將速度轉換成類別型態，分為 0~20、21~39、40~59、60~79、80 以上，命名為 SpaceMeanSpeed ( 顏色 )
def speed_to_category(speed):
    if pd.isnull(speed):
        return 0
    elif speed <= 20:
        return 1
    elif speed <= 39:
        return 2
    elif speed <= 59:
        return 3
    elif speed <= 79:
        return 4
    else:
        return 5

import matplotlib.pyplot as plt

df['SpaceMeanSpeed'] = df['SpaceMeanSpeed'].apply(speed_to_category)
print(df['SpaceMeanSpeed'])

# 假設你的 DataFrame 叫做 df
fig = plt.figure(figsize=(20, 12))  # 改變這裡的數值以放大或縮小圖形
ax = fig.add_subplot(111, projection='3d')

# 創建一個顏色映射
color_map = {0: 'white', 1: 'purple', 2: 'red', 3: 'orange', 4: 'yellow', 5: 'green'}
df['color'] = df['SpaceMeanSpeed'].map(color_map)

# 繪製散點圖
scatter = ax.scatter(df['TimeInterval'], df['GantryFromTo'], df['TrafficVolume'], c=df['color'])

# 設置圖表標題和軸標籤
ax.set_title('里程、交通量、速度、時間')
ax.set_xlabel('TimeInterval')
ax.set_ylabel('GantryFromTo')
ax.set_zlabel('TrafficVolume')

# 顯示圖表
plt.show()