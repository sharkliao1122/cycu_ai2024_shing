import pandas as pd
import os
import matplotlib.pyplot as plt

# 讀取 4 個 Excel 檔案
df_雙向人造 = pd.read_excel("C:\專題EXCEL新版\專題excel_NEW\專題excel\TCU052人造\TCU052人造水平雙向梁中點加速度.xlsx", header=1)
df_雙向設計 = pd.read_excel("C:\專題EXCEL新版\專題excel_NEW\專題excel\TCU052設計\TCU052設計水平雙向樑中點加速度.xlsx", header=1)
df_三向人造 = pd.read_excel("C:\專題EXCEL新版\專題excel_NEW\專題excel\TCU052人造\TCU052人造 三向主樑中點加速度.xlsx", header=1)
df_三向設計 = pd.read_excel("C:\專題EXCEL新版\專題excel_NEW\專題excel\TCU052設計\TCU052設計 三向主樑中點加速度.xlsx", header=1)

# 保留指定的欄位 StepNum, U1, U2, U3
df_雙向人造 = df_雙向人造[["StepNum", "U1", "U2", "U3"]]
df_雙向設計 = df_雙向設計[["StepNum", "U1", "U2", "U3"]]
df_三向人造 = df_三向人造[["StepNum", "U1", "U2", "U3"]]
df_三向設計 = df_三向設計[["StepNum", "U1", "U2", "U3"]]

# 移除無法轉換為浮點數的值
df_雙向人造 = df_雙向人造[pd.to_numeric(df_雙向人造["StepNum"], errors='coerce').notnull()]
df_雙向設計 = df_雙向設計[pd.to_numeric(df_雙向設計["StepNum"], errors='coerce').notnull()]
df_三向人造 = df_三向人造[pd.to_numeric(df_三向人造["StepNum"], errors='coerce').notnull()]
df_三向設計 = df_三向設計[pd.to_numeric(df_三向設計["StepNum"], errors='coerce').notnull()]

# 將 StepNum 欄位的值轉換成 FLOAT
df_雙向人造["StepNum"] = df_雙向人造["StepNum"].astype(float)
df_雙向設計["StepNum"] = df_雙向設計["StepNum"].astype(float)
df_三向人造["StepNum"] = df_三向人造["StepNum"].astype(float)
df_三向設計["StepNum"] = df_三向設計["StepNum"].astype(float)

# 獲取輸入文件的資料夾路徑
input_folder = "C:\專題EXCEL新版\專題excel_NEW\專題excel\圖表\人造+設計\TCU052\全梁加速度"

# 繪製圖表
for col in ["U1", "U2", "U3"]:
    # 第一張圖：df_雙向人造 + df_雙向設計
    plt.figure()
    plt.plot(df_雙向人造["StepNum"], df_雙向人造[col], label="Biaxial Artificial", color="red")
    plt.plot(df_雙向設計["StepNum"], df_雙向設計[col], label="Biaxial Design", color="green", linestyle='--')
    title = f"{col} X Midpoint Acceleration (Biaxial Artificial + Biaxial Design)"
    plt.title(title)
    plt.xlabel("StepNum")
    plt.ylabel("Acceleration (m/s^2)")
    plt.ylim(-30, 30)  # 設定 Y 軸範圍
    plt.legend()
    plt.savefig(os.path.join(input_folder, f"{title}.png"))

    # 第二張圖：df_三向人造 + df_三向設計
    plt.figure()
    plt.plot(df_三向人造["StepNum"], df_三向人造[col], label="Triaxial Artificial", color="red")
    plt.plot(df_三向設計["StepNum"], df_三向設計[col], label="Triaxial Design", color="green", linestyle='--')
    title = f"{col} X Midpoint Acceleration (Triaxial Artificial + Triaxial Design)"
    plt.title(title)
    plt.xlabel("StepNum")
    plt.ylabel("Acceleration (m/s^2)")
    plt.ylim(-30, 30)  # 設定 Y 軸範圍
    plt.legend()
    plt.savefig(os.path.join(input_folder, f"{title}.png"))




