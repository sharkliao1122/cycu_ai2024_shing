import pandas as pd




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








