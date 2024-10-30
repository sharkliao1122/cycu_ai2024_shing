import pandas as pd
import matplotlib.pyplot as plt

# 讀取 CSV 檔案，並將第二列作為欄位名稱
df_雙向 = pd.read_excel("C:\專題EXCEL\TCU052\TCU052 三向主樑內力.xlsx", header=1)
df_三向 = pd.read_excel("C:\專題EXCEL\TCU052\TCU052水平雙向全樑內力.xlsx", header=1)

# 保留指定的欄位
columns_to_keep = ["Frame", "Station", "StepType", "P", "V2", "V3", "M2", "M3"]
df_雙向 = df_雙向[columns_to_keep]
df_三向 = df_三向[columns_to_keep]

# 移除無法轉換為浮點數的值
df_雙向 = df_雙向[pd.to_numeric(df_雙向["Frame"], errors='coerce').notnull()]
df_三向 = df_三向[pd.to_numeric(df_三向["Frame"], errors='coerce').notnull()]

# 將 FRAME 欄位的值轉換成 FLOAT
df_雙向["Frame"] = df_雙向["Frame"].astype(float)
df_三向["Frame"] = df_三向["Frame"].astype(float)

# 篩選 Station 為 5 的資料並依照 StepType 排序，再以 FRAME 排序
df_雙向 = df_雙向[df_雙向["Station"] == 5].sort_values(["StepType", "Frame"])
df_三向 = df_三向[df_三向["Station"] == 5].sort_values(["StepType", "Frame"])
# 建立 4 個 DF df_雙向_Max、df_雙向_Min、df_三向_Max、df_三向_Min
df_雙向_Max = df_雙向[df_雙向["StepType"] == "Max"]
df_雙向_Min = df_雙向[df_雙向["StepType"] == "Min"]

df_三向_Max = df_三向[df_三向["StepType"] == "Max"]
df_三向_Min = df_三向[df_三向["StepType"] == "Min"]
