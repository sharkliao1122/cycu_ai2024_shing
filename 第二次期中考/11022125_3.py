# 讀取 CSV 檔案 "C:\Users\User\OneDrive\M05A\M05A_整理\M05A_20240429.csv"
# 轉換成 Dataframe，整理 Dataframe
# 若資料中有 TimeInterval GantryFrom GantryTo 皆相同的資料合併成同一行，並保留 v31, v32, v41, v5 ，SpaceMeanSpeed 的第一個出現的值

# M05A_0429_INFOR 整理
# 只保留 "編號" "緯度(北緯)" "經度(東經)" 三個欄位，將 經度(東經) 改名為 "經度" 緯度(北緯) 改名為 "緯度"
# 將 編號 欄位的值調整如下
# 01F-000.5S 改為 01F0005S
# 05F-R14.3N 改為 05FR143N 依此類推
# 只保留 "編號" "緯度(北緯)" "經度(東經)" 三個欄位
# 將 '經度(東經)' 改名為 '經度'，'緯度(北緯)' 改名為 '緯度'

# M05A_0429 整理
# 於 M05A_0429 新增 4 個欄位 "GantryFrom_緯度" "GantryFrom_經度" "GantryTo_緯度" "GantryTo_精度"，移除原本的 GantryFrom GantryTo 欄位
# "GantryFrom_緯度" 的值應為 M05A_0429_INFOR 中 "編號" 等於 M05A_0429 中 "GantryFrom" 的 "緯度" 值
# "GantryFrom_經度" 的值應為 M05A_0429_INFOR 中 "編號" 等於 M05A_0429 中 "GantryFrom" 的 "經度" 值
# "GantryTo_緯度" 的值應為 M05A_0429_INFOR 中 "編號" 等於 M05A_0429 中 "GantryTo" 的 "緯度" 值
# "GantryTo_經度" 的值應為 M05A_0429_INFOR 中 "編號" 等於 M05A_0429 中 "GantryTo" 的 "經度" 值

import pandas as pd
import webbrowser
import folium
from folium.plugins import TimestampedGeoJson
import geopandas as gpd
from shapely.geometry import LineString

# 讀取 CSV 檔案並轉換成 Dataframe
M05A_0429 = pd.read_csv(r'C:\Users\User\OneDrive\M05A\M05A_整理\M05A_20240429.csv')
M05A_0429_INFOR = pd.read_csv(r"C:\Users\User\OneDrive\M05A\M05A_0429\國道計費門架座標及里程牌價表104.09.04版.csv")

# 整理 M05A_0429
M05A_0429 = M05A_0429.groupby(["TimeInterval", "GantryFrom", "GantryTo"]).agg({'v31': 'first', 'v32': 'first', 'v41': 'first', 'v5': 'first', 'SpaceMeanSpeed': 'first'}).reset_index()

# 整理 M05A_0429_INFOR
M05A_0429_INFOR = M05A_0429_INFOR[['編號', '緯度(北緯)', '經度(東經)']].rename(columns={'經度(東經)': '經度', '緯度(北緯)': '緯度'})
M05A_0429_INFOR['編號'] = M05A_0429_INFOR['編號'].str.replace('-', '').str.replace('.', '')

# 新增欄位並移除原本的 GantryFrom 和 GantryTo 欄位
for direction in ['From', 'To']:
    M05A_0429 = M05A_0429.merge(M05A_0429_INFOR, left_on=f'Gantry{direction}', right_on='編號', how='left').rename(columns={'緯度': f'Gantry{direction}_緯度', '經度': f'Gantry{direction}_經度'}).drop(['編號'], axis=1)

# 顯示數據框
print(M05A_0429)


# 用 folium  創建台灣地圖
# 圖的內容為 2024 04 29 的 交通量 與車速 隨時間與高速公路里程的變化
# 要有可拖動的時間軸 (M05_0429 內的 TimeInterval 當做時間 )
# 需要用兩條線段連結 一條為北向另一條為南向 條件如下
# GantryFrom_緯度 GantryFrom_經度  GantryTo_緯度  GantryTo_經度 來畫線段 
# GantryFrom 最後一個字元分辨南北向 N:北向 S:南向
# 線段顏色依據 SpaceMeanSpeed 來決定(白色:為無資料 紫色:0-20 紅色:20-40 橘色:40-60 黃色:60-80 綠色:大於80)
# 點須能夠分行顯示 時間( 根據 TimeInterval) 車速( 根據 SpaceMeanSpeed) 車流量 (根據 v31 ) 的資料


# 定義一個函數來根據 SpaceMeanSpeed 決定顏色
def get_color(speed):
    if pd.isna(speed):
        return 'white'
    elif speed <= 20:
        return 'purple'
    elif speed <= 40:
        return 'red'
    elif speed <= 60:
        return 'orange'
    elif speed <= 80:
        return 'yellow'
    else:
        return 'green'

# 讀取數據
df = M05A_0429


# 創建 GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=[LineString([(row['GantryFrom_經度'], row['GantryFrom_緯度']), (row['GantryTo_經度'], row['GantryTo_緯度'])]) for idx, row in df.iterrows()])

# 創建 GeoJSON 物件
def create_feature(row):
    return {
        'type': 'Feature',
        'geometry': row['geometry'].__geo_interface__,
        'properties': {
            'time': row['TimeInterval'],
            'style': {'color': get_color(row['SpaceMeanSpeed'])},
            'icon': 'circle',
            'iconstyle': {
                'fillColor': get_color(row['SpaceMeanSpeed']),
                'fillOpacity': 0.8,
                'stroke': 'true',
                'radius': 7
            },
            'popup': f"TimeInterval: {row['TimeInterval']}<br>SpaceMeanSpeed: {row['SpaceMeanSpeed']}<br>V31: {row['v31']}"
        }
    }

features = gdf.apply(create_feature, axis=1).tolist()
geo_json = {'type': 'FeatureCollection', 'features': features}

# 創建地圖
m = folium.Map(location=[23.5, 121], zoom_start=7)

# 創建 TimestampedGeoJson 物件並加入到地圖
TimestampedGeoJson(
    geo_json,
    period='PT1H',
    add_last_point=True,
    auto_play=False,
    loop=False,
    max_speed=1,
    loop_button=True,
    date_options='YYYY/MM/DD HH:mm',
    time_slider_drag_update=True
).add_to(m)

# 保存並打開地圖
m.save('map.html')
webbrowser.open('file://' + os.path.realpath('map.html'))



