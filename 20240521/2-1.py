import os
import pandas as pd
import requests
import io

# 讀取此檔案 C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240521\M05A.csv\
# 並將其存入 DataFrame 1
# 讀取 CSV 檔案，並設定欄位名稱
df = pd.read_csv(r"C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240521\M05A.csv", names=["TimeInterval", "GantryFrom", "GantryTo", "VehicleType", "SpaceMeanSpeed", "TrafficVolume"])

# 將 df 1 中 VehicleType 欄位中為 31 的資料篩選出來，其餘的資料則不要
# Filter the rows where "VehicleType" is 31
df = df[df["VehicleType"] == 31]
print(df)
# 讀取 csv 檔案並匯入成 df2
df2 = pd.read_csv(
    r"C:\Users\User\OneDrive\桌面\AI與土木應用\GitHub\cycu_ai2024_shing\20240521\國道計費門架座標及里程牌價表104.09.04版_373038.csv", 
    encoding="cp950", 
    usecols=["編號", "緯度(北緯)", "經度(東經)"],
   
   )
df2 = df2.rename(columns={"緯度(北緯)": "緯度", "經度(東經)": "經度"})
df2["編號"] = df2["編號"].str.replace("-", "").str.replace(".", "")
print(df2)

# 將 df2 編號欄位作為索引值，
# Set the "編號" column as the index
df2.set_index("編號", inplace=True)