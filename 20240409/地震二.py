import openpyxl
import folium

from folium.plugins import HeatMapWithTime
import pandas as pd

from folium.plugins import TimestampedGeoJson

# 從此位置讀取 csv 檔案
df = pd.read_csv(r'C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240409\地震活動彙整_638487195244966260.csv', encoding='ISO-8859-1')
#此 csv 檔案傳換成 excel 檔案
df.to_excel(r'C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240409\地震.xlsx', index=False)
#將 df 中的時間、緯度、經度和規模轉換為列表
#將 918 列以後的資料刪除
df = df.drop(df.index[917:])
print(df.columns)
time_index = pd.to_datetime(df['Unnamed: 1'], format='%Y/%m/%d %H:%M:%S').astype(str).tolist()
lat = df['Unnamed: 3'].astype(float).tolist()  # 從第二行開始轉換
lon = df['Unnamed: 2'].astype(float).tolist()  # 從第二行開始轉換
magnitude = df['Unnamed: 4'].astype(float).tolist()  # 從第二行開始

import folium
#設為台灣地圖
m = folium.Map(location=[23.69781, 120.960515], zoom_start=7)

# 創建一個包含所有地震數據的列表
# 創建一個包含所有地震數據的列表
data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon[i], lat[i]],
            },
            "properties": {
                "time": time_index[i],
                "style": {"color" : "red" if magnitude[i] >= 5 else "blue"},
                "icon": "circle",
                "iconstyle": {
                    "fillColor": "red" if magnitude[i] >= 5 else "blue",
                    "fillOpacity": 0.8,
                    "stroke": "true",
                    "radius": 10 if magnitude[i] >= 5 else 5  # 根據規模大小調整標示點的大小
                },
                "popup": f"規模: {magnitude[i]}, 經度: {lon[i]}, 緯度: {lat[i]}, 時間: {time_index[i]}",
            },
        }
        for i in range(len(lat))
    ],
}
TimestampedGeoJson(
    data,
    period="PT1H",
    add_last_point=True,
    auto_play=False,
    loop=False,
    max_speed=4,
    loop_button=True,
    date_options="YYYY/MM/DD HH:mm:ss",
    time_slider_drag_update=True,
).add_to(m)

# 將地圖保存為html文件
m.save('earthquake.html')

# 在瀏覽器中打開地圖
import webbrowser
webbrowser.open('earthquake.html')




