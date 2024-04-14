import openpyxl
import folium

from folium.plugins import HeatMapWithTime
import pandas as pd

from folium.plugins import TimestampedGeoJson

# 從此位置讀取 C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240409\地震活動彙整_638487222151058655.csv
#將此 csv 檔案 C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240409\地震活動彙整_638487222151058655.csv 傳換成傳換成 excel 檔案
df = pd.read_csv(r'C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240409\地震活動彙整_638487222151058655.csv', encoding='ISO-8859-1')
df.to_excel(r'C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240409\地震.xlsx', index=False)


# 讀取上面的 excel 檔案
wb = openpyxl.load_workbook(r'C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240409\地震.xlsx')
sheet = wb.active
#將 excel 轉換成 dataframe
df = pd.DataFrame(sheet.values)


# 並將第917列以後的資料刪除
df = df.drop(df.index[916:])
#將 df 中的時間、經度、緯度和規模轉換為列表
time_index = pd.to_datetime(df[0], format='%Y/%m/%d %H:%M').astype(str).tolist()
lat = df[2].astype(float).tolist()  # 從第二行開始轉換
lon = df[1].astype(float).tolist()  # 從第二行開始轉換
magnitude = df[3].astype(float).tolist()  # 從第二行開始
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
                    "radius": 10 if magnitude[i] >= 5 else 5  # Adjust the size of the marker based on the magnitude
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







