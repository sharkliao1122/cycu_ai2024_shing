# 讀取此檔案"C:\Users\User\OneDrive\M05A\M05A_0429\M05A_20240429.csv"並轉換成 Dataframe

import pandas as pd
import os
import folium
import pandas as pd


# 讀取檔案
file_path = "C:\\Users\\User\\OneDrive\\M05A\\M05A_0429\\M05A_20240429.csv"
df = pd.read_csv(file_path)

from folium.plugins import TimestampedGeoJson  # Import the missing module

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
                "style": {"color": get_color(row['SpaceMeanSpeed']) if row['GantryFrom'][-1] == 'N' else 'blue'},
                "popup": f"TimeInterval: {row['TimeInterval']}, SpaceMeanSpeed: {row['SpaceMeanSpeed']}, v31: {row['v31']}",
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
    max_speed=3,
    loop_button=True,
    date_options='YYYY/MM/DD HH:mm:ss',
    time_slider_drag_update=True,
).add_to(m)

# 將地圖保存為 html 文件，並存於 C:\Users\User\OneDrive\M05A\M05A_0429
m.save(r"C:\Users\User\OneDrive\M05A\M05A_0429\map.html")

# 在瀏覽器中打開地圖
webbrowser.open(r"C:\Users\User\OneDrive\M05A\M05A_0429\map.html")