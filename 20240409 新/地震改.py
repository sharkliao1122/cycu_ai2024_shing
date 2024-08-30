# 讀取此 csv 檔案
# 檔案位置如下 C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240409 新\地震活動彙整_638606530177607117.csv 
# 依照下列欄位分類 地震時間、緯度、經度、深度、規模

import requests
from bs4 import BeautifulSoup
import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson
from datetime import datetime, timedelta
import webbrowser

# 讀取 CSV 檔案，嘗試使用不同的編碼格式
file_path = r"C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240409 新\地震活動彙整_638606530177607117.csv"

# 嘗試使用 'big5' 編碼
try:
    df = pd.read_csv(file_path, encoding='big5')
except UnicodeDecodeError:
    # 如果 'big5' 編碼失敗，嘗試使用 'latin1' 編碼
    df = pd.read_csv(file_path, encoding='latin1')

# 選擇需要的欄位
selected_columns = ['地震時間', '緯度', '經度', '深度', '規模']
df_selected = df[selected_columns]

# 將 '地震時間' 轉換為 datetime 格式
df_selected['地震時間'] = pd.to_datetime(df_selected['地震時間'])

# 創建地圖
m = folium.Map(location=[df_selected['緯度'].mean(), df_selected['經度'].mean()], zoom_start=5)

# 定義顏色對應規模
def get_color(magnitude):
    if magnitude < 1:
        return 'white'
    elif magnitude < 2:
        return 'green'
    elif magnitude < 3:
        return 'blue'
    elif magnitude < 4:
        return 'yellow'
    elif magnitude < 5:
        return 'orange'
    else:
        return 'red'

# 構建 GeoJson 格式的數據
features = []
for _, row in df_selected.iterrows():
    magnitude = row['規模']
    color = get_color(magnitude)
    feature = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [row['經度'], row['緯度']],
        },
        'properties': {
            'time': row['地震時間'].strftime('%Y-%m-%dT%H:%M:%S'),
            'popup': (
                f"地震時間: {row['地震時間']}<br>"
                f"緯度: {row['緯度']}<br>"
                f"經度: {row['經度']}<br>"
                f"深度: {row['深度']} 公里<br>"
                f"規模: {magnitude}"
            ),
            'icon': 'circle',
            'iconstyle': {
                'fillColor': color,
                'fillOpacity': 0.6,
                'stroke': 'true',
                'radius': magnitude * 2  # 根據地震規模調整點的大小
            }
        }
    }
    features.append(feature)

# 添加時間軸
TimestampedGeoJson(
    {'type': 'FeatureCollection', 'features': features},
    period='PT1H',  # 每小時一個時間點
    add_last_point=True,
    auto_play=False,
    loop=False,
    max_speed=10,
    loop_button=True,
    date_options='YYYY/MM/DD HH:mm:ss',
    time_slider_drag_update=True
).add_to(m)


# 打開地圖
m.save('earthquake.html')
webbrowser.open('earthquake.html')
# 顯示 DataFrame
print(df_selected)