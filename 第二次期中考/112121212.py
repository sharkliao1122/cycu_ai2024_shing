import folium
from folium.plugins import TimestampedGeoJson
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
import webbrowser
import os

import os
import folium
import pandas as pd
import webbrowser  # Import the missing module
from folium.plugins import TimestampedGeoJson  # Import the missing module

# 利用 folium 創建台灣地圖
# 並且依據 SpaceMeanSpeed 的數值來設定線條的顏色(白色: 無資料, 紫色: 低於 20, 紅色: 20-40, 橘色: 40-60, 黃色: 60-80, 綠色: 80 以上)
# 設置一個可拖動的時間軸，依照 TimeInterval 來顯示不同時間的交通狀況
# 並且將 TimeInterval, SpaceMeanSpeed, 流量, 方向 顯示在 popup 中
# 並且將地圖存檔於 C:\Users\User\OneDrive\M05A\M05A_0429\map.html 

# 創建地圖
m = folium.Map(location=[23.5, 121], zoom_start=7)

# 定義顏色函數
def get_color(speed):
    if pd.isnull(speed):
        return 'white'
    elif speed < 20:
        return 'purple'
    elif speed < 40:
        return 'red'
    elif speed < 60:
        return 'orange'
    elif speed < 80:
        return 'yellow'
    else:
        return 'green'

# 創建包含所有數據的列表
data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [[row['GantryFrom_經度'], row['GantryFrom_緯度']], [row['GantryTo_經度'], row['GantryTo_緯度']]],
            },
            "properties": {
                "times": [row['TimeInterval'], row['TimeInterval']],
                "style": {"color": get_color(row['SpaceMeanSpeed']), "weight":20},  # 增加 weight 參數
                "popup": f"TimeInterval: {row['TimeInterval']}<br>SpaceMeanSpeed: {row['SpaceMeanSpeed']}<br>TrafficVolume: {row['v31']}<br>Direction: {'North' if row['GantryFrom'][-1] == 'N' else 'South'}",
            },
        }
        for _, row in df.iterrows()
    ],
}

# 添加 TimestampedGeoJson 到地圖
TimestampedGeoJson(
    data,
    period='PT1H',
    add_last_point=True,
    auto_play=False,
    loop=False,
    max_speed=10,
    loop_button=True,
    date_options='YYYY/MM/DD HH:mm:ss',
    time_slider_drag_update=True,
).add_to(m)

# 將地圖保存為 html 文件，並存於 C:\Users\User\OneDrive\M05A\M05A_0429
m.save(r"C:\Users\User\OneDrive\M05A\M05A_0429\map.html")

# 在瀏覽器中打開地圖
webbrowser.open(r"C:\Users\User\OneDrive\M05A\M05A_0429\map.html")        
