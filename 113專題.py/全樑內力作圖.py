import pandas as pd
import matplotlib.pyplot as plt

# 讀取 CSV 檔案，並將第二列作為欄位名稱
df_雙向 = pd.read_excel("C:\專題EXCEL新版\專題EXCEL\TCU052設計\TCU052設計水平雙向全樑內力.xlsx", header=1)
df_三向 = pd.read_excel("C:\專題EXCEL新版\專題EXCEL\TCU052設計\TCU052設計 三向主樑內力.xlsx", header=1)

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

def plot_graph(y_label, column, title, file_name):
    plt.figure(figsize=(10, 6))
    plt.plot([0] + (df_雙向_Max["Frame"] * 10 + 5).tolist(), [0] + df_雙向_Max[column].tolist(), color='red', label='BI Max')
    plt.plot([0] + (df_雙向_Min["Frame"] * 10 + 5).tolist(), [0] + df_雙向_Min[column].tolist(), color='red', linestyle='--', label='BI Min')
    plt.plot([0] + (df_三向_Max["Frame"] * 10 + 5).tolist(), [0] + df_三向_Max[column].tolist(), color='blue', label='TRI Max')
    plt.plot([0] + (df_三向_Min["Frame"] * 10 + 5).tolist(), [0] + df_三向_Min[column].tolist(), color='blue', linestyle='--', label='TRI Min')
    plt.axhline(0, color='black', linewidth=0.5)  # 在 Y 軸上添加水平線
    plt.title(title)
    plt.xlabel("Station (m)")
    plt.ylabel(y_label)
    plt.legend()
    plt.savefig(file_name)
    plt.show()
# 繪製 P 圖
plot_graph("P (KN)", "P", "EYUL Full Beam Biaxial Triaxial Force Diagram","C:\專題EXCEL新版\專題EXCEL\TCU052設計\TCU052設計全梁雙向三向P圖.png")

# 繪製 V2 圖
plot_graph("V2 (KN)", "V2", "EYUL Full Beam Biaxial Triaxial V2 Diagram", "C:\專題EXCEL新版\專題EXCEL\TCU052設計\TCU052設計全梁雙向三向V2圖.png")

# 繪製 V3 圖
plot_graph("V3 (KN)", "V3", "EYUL Full Beam Biaxial Triaxial V3 Diagram", "C:\專題EXCEL新版\專題EXCEL\TCU052設計\TCU052設計全梁雙向三向V3圖.png")

# 繪製 M2 圖
plot_graph("M2 (KN-m)", "M2", "EYUL Full Beam Biaxial Triaxial M2 Diagram", "C:\專題EXCEL新版\專題EXCEL\TCU052設計\TCU052設計全梁雙向三向M2圖.png")

# 繪製 M3 圖
plot_graph("M3 (KN-m)", "M3", "EYUL Full Beam Biaxial Triaxial M3 Diagram", "C:\專題EXCEL新版\專題EXCEL\TCU052設計\TCU052設計全梁雙向三向M3圖.png")