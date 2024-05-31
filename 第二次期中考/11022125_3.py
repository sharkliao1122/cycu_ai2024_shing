# 讀取 CSV 檔案 "C:\Users\User\OneDrive\M05A\M05A_整理\M05A_20240429.csv"
# 轉換成 Dataframe，整理 Dataframe
# 若資料中有 TimeInterval GantryFrom GantryTo 皆相同的資料合併成同一行，並保留 v31, v32, v41, v5 ，SpaceMeanSpeed 的第一個出現的值

# M05A_0429_INFOR 整理
# 只保留 "編號" "緯度(北緯)" "經度(東經)" 三個欄位，將 經度(東經) 改名為 "經度" 緯度(北緯) 改名為 "緯度"
# 將 編號 欄位的值調整如下
# 01F-000.5S 改為 01F0005S
# 05F-R14.3N 改為 05FR143N 依此類推
# 只保留 "編號" "緯度(北緯)" "經度(東經)" 三個欄位
# 將 '經度(東經)' 改名為 '經度'，'緯度(北緯)' 改名為 '緯度'

# M05A_0429 整理
# 於 M05A_0429 新增 4 個欄位 "GantryFrom_緯度" "GantryFrom_經度" "GantryTo_緯度" "GantryTo_精度"，移除原本的 GantryFrom GantryTo 欄位
# "GantryFrom_緯度" 的值應為 M05A_0429_INFOR 中 "編號" 等於 M05A_0429 中 "GantryFrom" 的 "緯度" 值
# "GantryFrom_經度" 的值應為 M05A_0429_INFOR 中 "編號" 等於 M05A_0429 中 "GantryFrom" 的 "經度" 值
# "GantryTo_緯度" 的值應為 M05A_0429_INFOR 中 "編號" 等於 M05A_0429 中 "GantryTo" 的 "緯度" 值
# "GantryTo_經度" 的值應為 M05A_0429_INFOR 中 "編號" 等於 M05A_0429 中 "GantryTo" 的 "經度" 值

import pandas as pd

# 讀取 CSV 檔案並轉換成 Dataframe
M05A_0429 = pd.read_csv(r'C:\Users\User\OneDrive\M05A\M05A_整理\M05A_20240429.csv')
M05A_0429_INFOR = pd.read_csv(r"C:\Users\User\OneDrive\M05A\M05A_0429\國道計費門架座標及里程牌價表104.09.04版.csv")

# 整理 M05A_0429
M05A_0429 = M05A_0429.groupby(["TimeInterval", "GantryFrom", "GantryTo"]).agg({'v31': 'first', 'v32': 'first', 'v41': 'first', 'v5': 'first', 'SpaceMeanSpeed': 'first'}).reset_index()

# 整理 M05A_0429_INFOR
M05A_0429_INFOR = M05A_0429_INFOR[['編號', '緯度(北緯)', '經度(東經)']].rename(columns={'經度(東經)': '經度', '緯度(北緯)': '緯度'})
M05A_0429_INFOR['編號'] = M05A_0429_INFOR['編號'].str.replace('-', '').str.replace('.', '')

# 新增欄位並移除原本的 GantryFrom 和 GantryTo 欄位
for direction in ['From', 'To']:
    M05A_0429 = M05A_0429.merge(M05A_0429_INFOR, left_on=f'Gantry{direction}', right_on='編號', how='left').rename(columns={'緯度': f'Gantry{direction}_緯度', '經度': f'Gantry{direction}_經度'}).drop(['編號', f'Gantry{direction}'], axis=1)

# 顯示數據框
print(M05A_0429)








