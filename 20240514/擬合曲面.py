import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame as  df 
from pandas import read_csv
from scipy.interpolate import CubicSpline
from mpl_toolkits.mplot3d import Axes3D

#read ('TDCS_M05A_20240429_cub.csv', index=False) as df
# the first line is column names

#讀取此位置 C:\Users\User\Documents\GitHub\cycu_ai2024_shing\20240507\M05A_31.csv 的檔案
df = read_csv('C:\\Users\\User\\Documents\\GitHub\\cycu_ai2024_shing\\20240507\\M05A_31.csv', index_col=False)

# 函數定義
def gantry_to_numeric(gantry):
    #去掉 01F
    gantry = gantry[4:]
    if gantry[-1] == 'N':
        return int(gantry[0:3])*10 
    elif gantry[-1] == 'S':
        return int(gantry[0:3])*10 + 1  

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
# 將 TimeInterval 欄位轉換成數值型態 ( x軸 )
df['TimeInterval'] = pd.to_datetime(df['TimeInterval']).apply(lambda x: x.hour * 12 + x.minute // 5)

# 將 GantryFrom、GantryFrom 欄位轉換成數值型態 ( y軸 )
df['GantryFrom'] = df['GantryFrom'].apply(gantry_to_numeric)
df['GantryTo'] = df['GantryTo'].apply(gantry_to_numeric)
print(df['GantryFrom'])
print(df['GantryTo'])


# 將兩個欄位合併成一個欄位(將gantryfrom * 100000 與 gantryto 相加)，命名為 GantryFromTo  (y軸)
df['GantryFromTo'] = df['GantryFrom'] * 100000 + df['GantryTo']

# 將速度轉換成類別型態，命名為 SpaceMeanSpeed ( 顏色 )
df['SpaceMeanSpeed'] = df['SpaceMeanSpeed'].apply(speed_to_category)



data = np.array([df['GantryFromTo'], df['TimeInterval'].astype(int), df['TrafficVolume']]).T

print (data)
# 創建一個新的圖形 
# 畫出多視角圖形  重 111, 110, 101, 100
# add four subplots to the figure
# subplot(111) is subplot(111,portjection='3d')

# 對時間和里程數據進行網格化
# 假設 x (時間) 和 y (里程) 已經是規則的網格數據
x = np.linspace(data[:, 0].min(), data[:, 0].max(), num=50)  # 調整 num 以匹配數據點的密度
y = np.linspace(data[:, 1].min(), data[:, 1].max(), num=50)
x, y = np.meshgrid(x, y)

# 插值找到每個 (x, y) 點對應的 z (車流量)
from scipy.interpolate import griddata
z = griddata((data[:, 0], data[:, 1]), data[:, 2], (x, y), method='cubic')


fig = plt.figure()
ax = fig.add_subplot(121, projection='3d')
# 繪製曲面圖
surf = ax.plot_surface(x, y, z, cmap='viridis')

# 添加顏色條
#fig.colorbar(surf)

# 設置坐標軸標籤
ax.set_xlabel('Time')
ax.set_ylabel('Mileage')
ax.set_zlabel('Traffic Volume')
#設置標題 11022125
ax.set_title('11022125 Traffic Volume')

ax1 = fig.add_subplot(122, projection='3d')
# 繪製曲面圖
surf = ax1.plot_surface(x, y, z, cmap='viridis')
# 設置坐標軸標籤
ax1.set_xlabel('Time')
ax1.set_ylabel('Mileage')
ax1.set_zlabel('Traffic Volume')
ax1.view_init(elev=45, azim=60)
ax1.set_title('11022125 Traffic Volume')

plt.tight_layout()

#將圖片存於 C:\Users\User\Documents\GitHub\cycu_ai2024_shing\20240514
plt.savefig('C:\\Users\\User\\Documents\\GitHub\\cycu_ai2024_shing\\20240514\\擬合曲面11022125.png')

# 顯示圖形
plt.show()
