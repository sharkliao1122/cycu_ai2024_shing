import pandas as pd
import os
import matplotlib.pyplot as plt

# 讀取 CSV 檔案，並將第二列作為欄位名稱
df_雙向 = pd.read_excel("C:\專題EXCEL新版\專題EXCEL\TCU052設計\TCU052設計水平雙向柱底內力.xlsx", header=1)
df_三向 = pd.read_excel("C:\專題EXCEL新版\專題EXCEL\TCU052設計\TCU052設計 三向柱底內力.xlsx", header=1)

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

# 篩選 Station 為 5 的資料
df_雙向 = df_雙向[df_雙向["Station"] == 0]
df_三向 = df_三向[df_三向["Station"] == 0]

print(df_雙向)
print(df_三向)


# 依照  df_雙向(紅色)、df_三向(藍色) 繪製4個柱狀(順序 雙向且為Max , 三向且為Max , 雙向且為Min ,  三向且為Min)於同一張圖
# X 軸 為 Frame ，Y 軸為 P (KN)   括弧中為單位
# 標題為 "EYUL 柱底內力圖"(請用英文標題)
# 存於 "C:\EYUL\柱底內力\EYUL 柱底內力圖.png"

# 取得輸入 EXCEL 檔案的路徑
input_path = "C:\專題EXCEL新版\專題EXCEL\TCU052設計"
output_dir = input_path

def plot_graph(y_label, column, title, file_name):
    plt.figure(figsize=(12, 8))
    bar_width = 0.2  # 設定柱狀圖的寬度
    frames = df_雙向["Frame"].unique()
    index = range(len(frames))

    bars1 = plt.bar(index, df_雙向[df_雙向["StepType"] == "Max"][column], bar_width, color='red', label='BI Max')
    bars2 = plt.bar([i + bar_width for i in index], df_三向[df_三向["StepType"] == "Max"][column], bar_width, color='blue', label='TRI Max')
    bars3 = plt.bar([i + 2 * bar_width for i in index], df_雙向[df_雙向["StepType"] == "Min"][column], bar_width, color='red', hatch='//', label='BI Min')
    bars4 = plt.bar([i + 3 * bar_width for i in index], df_三向[df_三向["StepType"] == "Min"][column], bar_width, color='blue', hatch='//', label='TRI Min')

    plt.xlabel("Frame")
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks([i + 1.5 * bar_width for i in index], frames)
    plt.legend()
    
    # 顯示每個柱狀圖的數值
    for bars in [bars1, bars2, bars3, bars4]:
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(file_name)
    plt.show()

# 繪製 P 圖
plot_graph("P (KN)", "P", "EYUL Column Bottom Force Diagram", os.path.join(output_dir, "TCU052設計 柱底內力圖.png"))

# 繪製 V2 圖
plot_graph("V2 (KN)", "V2", "EYUL Column Bottom V2 Diagram", os.path.join(output_dir, "TCU052設計 柱底V2內力圖.png"))

# 繪製 V3 圖
plot_graph("V3 (KN)", "V3", "EYUL Column Bottom V3 Diagram", os.path.join(output_dir, "TCU052設計 柱底V3內力圖.png"))

# 繪製 M2 圖
plot_graph("M2 (KN-m)", "M2", "EYUL Column Bottom M2 Diagram", os.path.join(output_dir, "TCU052設計 柱底M2內力圖.png"))

# 繪製 M3 圖
plot_graph("M3 (KN-m)", "M3", "EYUL Column Bottom M3 Diagram", os.path.join(output_dir,"TCU052設計 柱底M3內力圖.png"))
