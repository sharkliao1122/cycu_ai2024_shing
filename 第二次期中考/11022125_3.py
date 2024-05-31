import pandas as pd


# 讀取 CSV 檔案 "C:\Users\User\OneDrive\M05A\M05A_整理\M05A_20240429.csv"
# 轉換成 Dataframe，整理 Dataframe
# 若資料中有 TimeInterval GantryFrom GantryTo 皆相同的資料合併成同一行，並保留 v31, v32, v41, v5 ，SpaceMeanSpeed 的第一個出現的值

M05A_0429 = pd.read_csv(r'C:\Users\User\OneDrive\M05A\M05A_整理\M05A_20240429.csv')
M05A_0429_INFOR = pd.read_csv(r"C:\Users\User\OneDrive\M05A\M05A_0429\國道計費門架座標及里程牌價表104.09.04版.csv")
M05A_0429 = M05A_0429.groupby(["TimeInterval", "GantryFrom", "GantryTo"]).agg({'v31': 'first', 'v32': 'first', 'v41': 'first', 'v5': 'first', 'SpaceMeanSpeed': 'first'}).reset_index()




# 在 M05A_0429 中新增 兩個 欄位 "緯度_GANTRYFROM" "經度GANTRYFROM" "緯度_GANTRYTO" "經度GANTRYTO"，
# 並根據 GantryFrom   的值 將 M05A_0429_INFOR 中的 "緯度" "經度" 的值對應到 M05A_0429 "緯度_GANTRYFROM" "經度GANTRYFROM" 中
# 並根據 GantryTo     的值 將 M05A_0429_INFOR 中的 "緯度" "經度" 的值對應到 M05A_0429 "緯度_GANTRYTO" "經度GANTRYTO"     中

M05A_0429 = M05A_0429.merge(M05A_0429_INFOR, left_on='GantryFrom', right_on='編號', how='left')
M05A_0429 = M05A_0429.merge(M05A_0429_INFOR, left_on='GantryTo', right_on='編號', how='left', suffixes=('_GANTRYFROM', '_GANTRYTO'))
M05A_0429 = M05A_0429.drop(columns=['GantryID_GANTRYFROM', 'GantryID_GANTRYTO'])
M05A_0429 = M05A_0429.rename(columns={'緯度_GANTRYFROM': '緯度', '經度GANTRYFROM': '經度', '緯度_GANTRYTO': '緯度', '經度GANTRYTO': '經度'})


# 顯示數據框
print(M05A_0429)







