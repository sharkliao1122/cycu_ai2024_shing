import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame as  df 
from pandas import read_csv
from scipy.interpolate import CubicSpline
from mpl_toolkits.mplot3d import Axes3D

#read ('TDCS_M05A_20240429_cub.csv', index=False) as df
# the first line is column names

# 讀取此位置 C:\Users\User\Documents\GitHub\cycu_ai2024_shing\20240507\M05A_31.csv 的檔案
df = read_csv(r'C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240507\M05A_31.csv', index_col=False)
# 將 timeInterval 欄位轉換為如下格式，每 5 分鐘為一個區間，總共 288 個區間
# 例如 00:00:00 轉換為 0 ， 00:15:00 轉換為 3 ， 01:00:00 轉換為 12

df['TimeInterval'] = pd.to_datetime(df['TimeInterval']).apply(lambda x: x.hour * 12 + x.minute // 5)


# 選取 df 中 GantryFrom 欄位中最後一個字元為 N 的資料且在 GantryTo 欄位中含有 01F 及 GantryTo 欄位中含有 N，將其存為 df2
df2 = df[(df['GantryFrom'].str[-1] == 'N') & (df['GantryTo'].str.contains('01F'))] 

# GantryFrom 和 GantryTo 欄位中的資料保留 第4個字元 到 第7個字元 ，將其轉換為整數
# 並且將轉換後的 GantryFrom *10000 + GantryTo 存入 miles 欄位
df2['GantryFrom'] = df2['GantryFrom'].str[3:7].astype(int)
df2['GantryTo'] = df2['GantryTo'].str[3:7].astype(int)


# df2依照 GantryFrom 欄位由小至大進行排序
df2 = df2.sort_values(by='GantryFrom') 
print(df2) 

# 將 df2 存為 csv 檔案於C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240514,並命名為 'M05A_31N.csv'
df2.to_csv(r'C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240514\M05A_31N.csv', index=False)

