import os
import geopandas as gpd
import matplotlib.pyplot as plt

taiwan = gpd.read_file('20240402/county/county_moi_1090820.shp')

print(taiwan.shape)
print(taiwan)

# 輸出台灣地圖的時候 圖面顯示的範圍 緯度最低為21.5度 緯度最高為25.5度 經度最低為119度 經度最高為122度
taiwan.plot()
plt.xlim(119,122)
plt.ylim(21.5,25.5)

# save to png file before showing the plot
plt.savefig('20240402/taiwan_map.png')

plt.show()