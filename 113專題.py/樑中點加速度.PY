import pandas as pd
import os
import matplotlib.pyplot as plt

# 讀取 CSV 檔案，並將第二列作為欄位名稱
df_雙向 = pd.read_excel("C:\專題EXCEL新版\專題EXCEL\TCU052設計\TCU052設計水平雙向樑中點加速度.xlsx", header=1)
df_三向 = pd.read_excel("C:\專題EXCEL新版\專題EXCEL\TCU052設計\TCU052設計 三向主樑中點加速度.xlsx",header=1)

# 保留指定的欄位 StepNum, U1, U2, U3
df_雙向 = df_雙向[["StepNum", "U1", "U2", "U3"]]
df_三向 = df_三向[["StepNum", "U1", "U2", "U3"]]

# 移除無法轉換為浮點數的值
df_雙向 = df_雙向[pd.to_numeric(df_雙向["StepNum"], errors='coerce').notnull()]
df_三向 = df_三向[pd.to_numeric(df_三向["StepNum"], errors='coerce').notnull()]

# 將 StepNum 欄位的值轉換成 FLOAT
df_雙向["StepNum"] = df_雙向["StepNum"].astype(float)
df_三向["StepNum"] = df_三向["StepNum"].astype(float)

# 獲取輸入文件的資料夾路徑
input_folder = "C:\專題EXCEL新版\專題EXCEL\TCU052設計"

# 根據檔名設定顏色
if "設計" in input_folder:
    color_雙向 = "green"
    color_三向 = "orange"
else:
    color_雙向 = "red"
    color_三向 = "blue"

# 繪製雙向折線圖 3張折線圖 (U1, U2, U3)
for col in ["U1", "U2", "U3"]:
    plt.figure()
    plt.plot(df_雙向["StepNum"], df_雙向[col], label="Biaxial", color=color_雙向)
    title = f"{col} X Midpoint Acceleration (Biaxial)"
    plt.title(title)
    plt.xlabel("StepNum")
    plt.ylabel("Acceleration (m/s^2)")
    plt.ylim(-11, 11)  # 設定 Y 軸範圍
    plt.legend()
    plt.savefig(os.path.join(input_folder, f"{title}.png"))

# 繪製三向折線圖 3張折線圖 (U1, U2, U3)
for col in ["U1", "U2", "U3"]:
    plt.figure()
    plt.plot(df_三向["StepNum"], df_三向[col], label="Triaxial", color=color_三向)
    title = f"{col} X Midpoint Acceleration (Triaxial)"
    plt.title(title)
    plt.xlabel("StepNum")
    plt.ylabel("Acceleration (m/s^2)")
    plt.ylim(-11, 11)  # 設定 Y 軸範圍
    plt.legend()
    plt.savefig(os.path.join(input_folder, f"{title}.png"))



