import os
import folium
import pandas as pd
import webbrowser  # Import the missing module
from folium.plugins import TimestampedGeoJson  # Import the missing module

# 讀取此檔案 "C:\Users\User\OneDrive\M05A\M05A_整理\M05A_20240429.csv"，並且將其存於一個 DataFrame 中
# 讀取此檔案 "C:\Users\User\OneDrive\M05A\M05A_0429\國道計費門架座標及里程牌價表1130327.csv"，並且將其存於一個 DataFrame 中
# 在 df 中新增 4 個 欄位 GantryFrom_緯度  GantryFrom_經度  GantryTo_緯度  GantryTo_經度
# 將 df_information 中的 設定收費區代碼 更名為 GantryID
# GantryFrom_緯度 的值為 df 中 GantryFrom 欄位的值對應到 df_information 中的 GantryID 所對應的 緯度
# GantryFrom_經度 的值為 df 中 GantryFrom 欄位的值對應到 df_information 中的 GantryID 所對應的 經度
# GantryTo_緯度 的值為 df 中 GantryTo 欄位的值對應到 df_information 中的 GantryID 所對應的 緯度
# GantryTo_經度 的值為 df 中 GantryTo 欄位的值對應到 df_information 中的 GantryID 所對應的 經度




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

print(df)

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
