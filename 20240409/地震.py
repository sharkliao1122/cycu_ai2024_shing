import openpyxl
import folium
from folium.plugins import HeatMapWithTime
import pandas as pd

from folium.plugins import TimestampedGeoJson

# 讀取Excel檔案
book = openpyxl.load_workbook(r'C:\Users\User\Documents\GitHub\cycu_ai2024_shing\地震.xlsx')

# 選擇活動工作表
sheet = book.active

# 將工作表轉換為DataFrame
# 並將第818列以後的資料刪除
df = pd.DataFrame(sheet.values)
df = df.drop(df.index[817:])
df.columns = df.iloc[0]
df = df.drop(df.index[0])

# 將時間、緯度、經度和規模轉換為列表
time_index = pd.to_datetime(df.iloc[1:, 0]).astype(str).tolist()  # 將時間轉換為str類型
lat = df.iloc[1:, 2].astype(float).tolist()  # 從第二行開始轉換
lon = df.iloc[1:, 1].astype(float).tolist()  # 從第二行開始轉換
magnitude = df.iloc[1:, 3].astype(float).tolist()  # 從第二行開始轉換

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
                    "radius": 7
                },
                "popup": f"規模: {magnitude[i]}, 經度: {lon[i]}, 緯度: {lat[i]}, 時間: {time_index[i]}",
            },
        }
        for i in range(len(lat))
    ],
}

m = folium.Map(location=[23.5, 121], zoom_start=7)

TimestampedGeoJson(
    data,
    period="PT1H",
    add_last_point=True,
    auto_play=False,
    loop=False,
    max_speed=1,
    loop_button=True,
    date_options="YYYY/MM/DD HH:mm:ss",
    time_slider_drag_update=True,
).add_to(m)

m.save('earthquake.html')

# 在瀏覽器中打開地圖
import webbrowser
webbrowser.open('earthquake.html')