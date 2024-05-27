import os
import pandas as pd
import requests
import io
import folium
from folium import plugins

# 建立資料夾
os.makedirs('C:\\Users\\User\\OneDrive\\M05A0429', exist_ok=True)

# 下載和處理 CSV 檔案
for i in range(24):
    for j in range(0, 60, 5):
        url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/20240429/{i:02d}/TDCS_M05A_20240429_{i:02d}{j:02d}00.csv"
        response = requests.get(url)
        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')), names=["TimeInterval", "GantryFrom", "GantryTo", "VehicleType", "SpaceMeanSpeed", "TrafficVolume"])
        # 留下VehicleType 為31的資料
        df = df[df["VehicleType"] == 31]
        # 儲存 CSV 檔案
        df.to_csv(f"C:\\Users\\User\\OneDrive\\M05A0429\\{i:02d}{j:02d}.csv", index=False)
        # 列印進度
        print(f"{i:02d}:{j:02d}")


# 合併所有 CSV 檔案
dfs = [pd.read_csv(f"C:\\Users\\User\\OneDrive\\M05A0429\\{filename}") for filename in os.listdir("C:\\Users\\User\\OneDrive\\M05A0429") if filename.endswith('.csv')]
df = pd.concat(dfs, ignore_index=True) if dfs else print("在指定的目錄下沒有找到任何 CSV 檔案。")

# 讀取和處理其他 CSV 檔案
df2 = pd.read_csv(r"C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240521\國道計費門架座標及里程牌價表104.09.04版_373038.csv", encoding="cp950", usecols=["編號", "緯度(北緯)", "經度(東經)"])
df2 = df2.rename(columns={"緯度(北緯)": "緯度", "經度(東經)": "經度", "編號": "Gantry"})
df2["Gantry"] = df2["Gantry"].str.replace("-", "").str.replace(".", "")

# 合併 df 和 df2
df = df.merge(df2, left_on="GantryFrom", right_on="Gantry", how="left").rename(columns={"緯度": "緯度(GantryFrom)", "經度": "經度(GantryFrom)"}).drop(columns=["Gantry"])
df = df.merge(df2, left_on="GantryTo", right_on="Gantry", how="left").rename(columns={"緯度": "緯度(GantryTo)", "經度": "經度(GantryTo)"}).drop(columns=["Gantry"])
print(df)

# 畫地圖以台灣為中心
# PolyLine 以 TimeInterval 為準繪圖
# 時間軸以 TimeInterval 為準
# 依速度大小改變顏色如下
# 白色:無資料 紫色:0-20 紅色:20-40 橘色:40-60 黃色:60-80 綠色:80以上
# 將 html 存檔於 C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240521\2-1.py
# 並開啟該 html 檔案

# 建立地圖
map = folium.Map(location=[23.69781, 120.960515], zoom_start=8)

# 繪製 PolyLine
for i in range(len(df)):
    if df["SpaceMeanSpeed"][i] == 0:
        color = "purple"
    elif 0 < df["SpaceMeanSpeed"][i] <= 20:
        color = "purple"
    elif 20 < df["SpaceMeanSpeed"][i] <= 40:
        color = "red"
    elif 40 < df["SpaceMeanSpeed"][i] <= 60:
        color = "orange"
    elif 60 < df["SpaceMeanSpeed"][i] <= 80:
        color = "yellow"
    elif 80 < df["SpaceMeanSpeed"][i]:
        color = "green"
    if pd.notnull(df["緯度(GantryFrom)"][i]) and pd.notnull(df["經度(GantryFrom)"][i]) and pd.notnull(df["緯度(GantryTo)"][i]) and pd.notnull(df["經度(GantryTo)"][i]):
        folium.PolyLine([(df["緯度(GantryFrom)"][i], df["經度(GantryFrom)"][i]), (df["緯度(GantryTo)"][i], df["經度(GantryTo)"][i])], color=color, weight=2, opacity=0.8).add_to(map).add_to(map)
    
# 繪製時間軸
time_index = df["TimeInterval"].unique().tolist()
time_index.sort()
time_index = [str(time) for time in time_index]

plugins.TimestampedGeoJson({
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [df["緯度(GantryFrom)"][i], df["經度(GantryFrom)"][i]]
            },
            "properties": {
                "time": time_index[i] if i < len(time_index) else None,
                "style": {
                    "color": "black"
                }
            }
        }
        for i in range(len(df))
    ]
}).add_to(map)

# 存檔並開啟
map.save(r"C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240521\2-2.html")
os.system(r"C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240521\2-2.html")