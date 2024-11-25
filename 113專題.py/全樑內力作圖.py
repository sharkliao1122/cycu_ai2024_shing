import pandas as pd
import matplotlib.pyplot as plt

# 讀取 CSV 檔案，並將第二列作為欄位名稱
df_雙向 = pd.read_excel("C:\專題EXCEL新版\專題excel_NEW\專題excel\TCU052人造\TCU052人造 三向柱底內力.xlsx",header=1)
df_三向 = pd.read_excel("C:\專題EXCEL新版\專題excel_NEW\專題excel\TCU052設計\TCU052設計 三向主樑內力.xlsx", header=1)

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

print(df_雙向_Max)
print(df_雙向_Min)
print(df_三向_Max)
print(df_三向_Min)


# 依照  df_雙向_Max、df_雙向_Min、df_三向_Max、df_三向_Min 繪製4條折線於同一張圖
# 其中 df_雙向_Max、df_雙向_Min 顏色為紅色，df_三向_Max、df_三向_Min 顏色為藍色
# X 軸 為 staion (M) 其值為 frame * 10 + 5 ，Y 軸為 P (KN)   括弧中為單位
# 標題為 "EYUL 全梁雙向三向內力圖"(請用英文標題)
# 存於 "C:\EYUL\全梁雙向三項內力\EYUL 全梁雙向三向內力圖.png"

def plot_graph(y_label, column, title, file_name, y_lim):
    plt.figure(figsize=(10, 6))
    plt.plot([0] + (df_雙向_Max["Frame"] * 10 + 5).tolist(), [0] + df_雙向_Max[column].tolist(), color='red', label='artifical earthquake Max')
    plt.plot([0] + (df_雙向_Min["Frame"] * 10 + 5).tolist(), [0] + df_雙向_Min[column].tolist(), color='red', linestyle='--', label='artifical earthquake Min')
    plt.plot([0] + (df_三向_Max["Frame"] * 10 + 5).tolist(), [0] + df_三向_Max[column].tolist(), color='blue', label='design Max')
    plt.plot([0] + (df_三向_Min["Frame"] * 10 + 5).tolist(), [0] + df_三向_Min[column].tolist(), color='blue', linestyle='--', label='design Min')
    plt.axhline(0, color='black', linewidth=0.5)  # 在 Y 軸上添加水平線
    plt.ylim(y_lim)  # 設置 Y 軸的最大最小值
    plt.title(title)
    plt.xlabel("Station (m)")
    plt.ylabel(y_label)
    plt.legend()
    plt.savefig(file_name)
    
    
# 繪製 P 圖
plot_graph("P (KN)", "P", "TCU052 Full Beam Force Diagram","C:\專題EXCEL新版\專題excel_NEW\專題excel\圖表\人造+設計\TCU052\全梁\設計+人造全梁三向P圖.png",(-15000, 15000))

# 繪製 V2 圖
plot_graph("V2 (KN)", "V2", "TCU052 Full Beam V2 Diagram","C:\專題EXCEL新版\專題excel_NEW\專題excel\圖表\人造+設計\TCU052\全梁\設計+人造全梁三向V2圖.png",(-15000, 15000))

# 繪製 V3 圖
plot_graph("V3 (KN)", "V3","TCU052 Full Beam V3 Diagram", "C:\專題EXCEL新版\專題excel_NEW\專題excel\圖表\人造+設計\TCU052\全梁\設計+人造全梁三向V3圖.png",(-15000, 15000))

# 繪製 M2 圖向三向M2圖.png", (-
plot_graph("M2 (KN-m)", "M2", "TCU052 Full Beam M2 Diagram", "C:\專題EXCEL新版\專題excel_NEW\專題excel\圖表\人造+設計\TCU052\全梁\設計+人造全梁三向M2圖.png",(-75000, 75000))

# 繪製 M3 圖
plot_graph("M3 (KN-m)", "M3", "TCU052 Full Beam M3 Diagram", "C:\專題EXCEL新版\專題excel_NEW\專題excel\圖表\人造+設計\TCU052\全梁\設計+人造全梁三向M3圖.png",(-75000, 75000))