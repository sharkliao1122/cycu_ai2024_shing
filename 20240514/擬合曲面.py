import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame as  df 
from pandas import read_csv
from scipy.interpolate import CubicSpline
from mpl_toolkits.mplot3d import Axes3D


# 讀取此位置 C:\Users\User\Documents\GitHub\cycu_ai2024_shing\20240514\M05A_31N.csv 的檔案
df = read_csv(r'C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240514\M05A_31N.csv', index_col=False)

data = np.array([df['GantryFrom'], df['TimeInterval'].astype(int), df['TrafficVolume']]).T

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

# 顯示圖形
plt.show()

#將圖片存於 C:\Users\User\Documents\GitHub\cycu_ai2024_shing\20240514
plt.savefig(r'C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240514\擬合曲面11022125.png')

