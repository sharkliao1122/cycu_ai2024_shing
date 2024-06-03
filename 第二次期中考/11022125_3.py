# 讀取此檔案 "C:\Users\User\OneDrive\M05A\M05A_整理\M05A_20240429.csv"，並且將其存於一個 DataFrame 中
# 讀取此檔案 "C:\Users\User\OneDrive\M05A\M05A_0429\國道計費門架座標及里程牌價表1130327.csv"，並且將其存於一個 DataFrame 中
# 在 df 中新增 4 個 欄位 GantryFrom_緯度  GantryFrom_經度  GantryTo_緯度  GantryTo_經度
# 將 df_information 中的 設定收費區代碼 更名為 GantryID
# GantryFrom_緯度 的值為 df 中 GantryFrom 欄位的值對應到 df_information 中的 GantryID 所對應的 緯度
# GantryFrom_經度 的值為 df 中 GantryFrom 欄位的值對應到 df_information 中的 GantryID 所對應的 經度
# GantryTo_緯度 的值為 df 中 GantryTo 欄位的值對應到 df_information 中的 GantryID 所對應的 緯度
# GantryTo_經度 的值為 df 中 GantryTo 欄位的值對應到 df_information 中的 GantryID 所對應的 經度


import os
import folium
import pandas as pd
import webbrowser  # Import the missing module
from folium.plugins import TimestampedGeoJson  # Import the missing module

# 讀取檔案
file_path_1 = r"C:\Users\User\OneDrive\M05A\M05A_整理\M05A_20240429.csv"
file_path_2 = r"C:\Users\User\OneDrive\M05A\M05A_0429\國道計費門架座標及里程牌價表1130327.csv"
df = pd.read_csv(file_path_1)
df_information = pd.read_csv(file_path_2)

# 在 df 中新增 4 個欄位
df['GantryFrom_緯度'] = None
df['GantryFrom_經度'] = None
df['GantryTo_緯度'] = None
df['GantryTo_經度'] = None



# 將 df_information 中的設定收費區代碼更名為 GantryID
df_information = df_information.rename(columns={"設定收費區代碼": "GantryID"})

# 只保留 GantryID, 緯度, 經度 三列
df_information = df_information[['GantryID', '緯度', '經度']]

# 建立映射字典
latitude_dict = df_information.set_index('GantryID')['緯度'].to_dict()
longitude_dict = df_information.set_index('GantryID')['經度'].to_dict()

# 映射 GantryFrom 和 GantryTo 列的值
df['GantryFrom_緯度'] = df['GantryFrom'].map(latitude_dict)
df['GantryFrom_經度'] = df['GantryFrom'].map(longitude_dict)
df['GantryTo_緯度'] = df['GantryTo'].map(latitude_dict)
df['GantryTo_經度'] = df['GantryTo'].map(longitude_dict)

# 合併 TimeInterval, GantryFrom, GantryTo 相同的列
df = df.groupby(['TimeInterval', 'GantryFrom', 'GantryTo'], as_index=False).first()


print (df)
print (df_information)

