import pandas as pd
import os
import matplotlib.pyplot as plt

# 讀取 4 個 Excel 檔案
df_雙向人造 = pd.read_excel("C:\專題EXCEL新版\專題excel_NEW\專題excel\TCU052人造\TCU052人造水平雙向柱底內力.xlsx", header=1)
df_雙向設計 = pd.read_excel("C:\專題EXCEL新版\專題excel_NEW\專題excel\TCU052設計\TCU052設計水平雙向柱底內力.xlsx", header=1)
df_三向人造 = pd.read_excel("C:\專題EXCEL新版\專題excel_NEW\專題excel\TCU052人造\TCU052人造 三向柱底內力.xlsx", header=1)
df_三向設計 = pd.read_excel("C:\專題EXCEL新版\專題excel_NEW\專題excel\TCU052設計\TCU052設計 三向柱底內力.xlsx", header=1)

# 保留指定的欄位
columns_to_keep = ["Frame", "Station", "StepType", "P", "V2", "V3", "M2", "M3"]
df_雙向人造 = df_雙向人造[columns_to_keep]
df_雙向設計 = df_雙向設計[columns_to_keep]
df_三向人造 = df_三向人造[columns_to_keep]
df_三向設計 = df_三向設計[columns_to_keep]

# 移除無法轉換為浮點數的值
df_雙向人造 = df_雙向人造[pd.to_numeric(df_雙向人造["Frame"], errors='coerce').notnull()]
df_雙向設計 = df_雙向設計[pd.to_numeric(df_雙向設計["Frame"], errors='coerce').notnull()]
df_三向人造 = df_三向人造[pd.to_numeric(df_三向人造["Frame"], errors='coerce').notnull()]
df_三向設計 = df_三向設計[pd.to_numeric(df_三向設計["Frame"], errors='coerce').notnull()]

# 將 FRAME 欄位的值轉換成 FLOAT
df_雙向人造["Frame"] = df_雙向人造["Frame"].astype(float)
df_雙向設計["Frame"] = df_雙向設計["Frame"].astype(float)
df_三向人造["Frame"] = df_三向人造["Frame"].astype(float)
df_三向設計["Frame"] = df_三向設計["Frame"].astype(float)

# 篩選 Station 為 5 的資料
df_雙向人造 = df_雙向人造[df_雙向人造["Station"] == 0]
df_雙向設計 = df_雙向設計[df_雙向設計["Station"] == 0]
df_三向人造 = df_三向人造[df_三向人造["Station"] == 0]
df_三向設計 = df_三向設計[df_三向設計["Station"] == 0]

print(df_雙向人造)
print(df_雙向設計)
print(df_三向人造)
print(df_三向設計)

# 取得輸入 EXCEL 檔案的路徑題
output_dir = "C:\專題EXCEL新版\專題excel_NEW\專題excel\圖表\人造+設計\TCU052\住底內壢"

def plot_graph(y_label, column, title, file_name, df_人造, df_設計):
    plt.figure(figsize=(12, 8))
    bar_width = 0.2  # 設定柱狀圖的寬度
    frames = df_人造["Frame"].unique()
    index = range(len(frames))

    bars1 = plt.bar(index, df_人造[df_人造["StepType"] == "Max"][column], bar_width, color='red', label='BI Max')
    bars2 = plt.bar([i + bar_width for i in index], df_設計[df_設計["StepType"] == "Max"][column], bar_width, color='green', linestyle='--', label='Design Max')
    bars3 = plt.bar([i + 2 * bar_width for i in index], df_人造[df_人造["StepType"] == "Min"][column], bar_width, color='red', hatch='//', label='BI Min')
    bars4 = plt.bar([i + 3 * bar_width for i in index], df_設計[df_設計["StepType"] == "Min"][column], bar_width, color='green', linestyle='--', hatch='//', label='Design Min')

    plt.xlabel("Frame")
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks([i + 1.5 * bar_width for i in index], frames)
    plt.legend()
    
    # 設定 Y 軸範圍
    if column in ["P", "V2", "V3"]:
        plt.ylim(-13000, 13000)
    elif column in ["M2", "M3"]:
        plt.ylim(-130000, 130000)
    
    # 顯示每個柱狀圖的數值
    for bars in [bars1, bars2, bars3, bars4]:
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(file_name)

# 繪製雙向圖
plot_graph("P (KN)", "P", "TCU052 Column Bottom Force Diagram (雙向)", os.path.join(output_dir, "TCU052雙向 柱底P內力圖(雙向).png"), df_雙向人造, df_雙向設計)
plot_graph("V2 (KN)", "V2", "TCU052 Column Bottom V2 Diagram (雙向)", os.path.join(output_dir, "TCU052雙向 柱底V2內力圖(雙向).png"), df_雙向人造, df_雙向設計)
plot_graph("V3 (KN)", "V3", "TCU052 Column Bottom V3 Diagram (雙向)", os.path.join(output_dir, "TCU052雙向 柱底V3內力圖(雙向).png"), df_雙向人造, df_雙向設計)
plot_graph("M2 (KN-m)", "M2", "TCU052 Column Bottom M2 Diagram (雙向)", os.path.join(output_dir, "TCU052雙向 柱底M2內力圖(雙向).png"), df_雙向人造, df_雙向設計)
plot_graph("M3 (KN-m)", "M3", "TCU052 Column Bottom M3 Diagram (雙向)", os.path.join(output_dir, "TCU052雙向 柱底M3內力圖(雙向).png"), df_雙向人造, df_雙向設計)

# 繪製三向圖
plot_graph("P (KN)", "P", "TCU052 Column Bottom Force Diagram (三向)", os.path.join(output_dir, "TCU052三向 柱底P內力圖(三向).png"), df_三向人造, df_三向設計)
plot_graph("V2 (KN)", "V2", "TCU052 Column Bottom V2 Diagram (三向)", os.path.join(output_dir, "TCU052三向 柱底V2內力圖(三向).png"), df_三向人造, df_三向設計)
plot_graph("V3 (KN)", "V3", "TCU052 Column Bottom V3 Diagram (三向)", os.path.join(output_dir, "TCU052三向 柱底V3內力圖(三向).png"), df_三向人造, df_三向設計)
plot_graph("M2 (KN-m)", "M2", "TCU052 Column Bottom M2 Diagram (三向)", os.path.join(output_dir, "TCU052三向 柱底M2內力圖(三向).png"), df_三向人造, df_三向設計)
plot_graph("M3 (KN-m)", "M3", "TCU052 Column Bottom M3 Diagram (三向)", os.path.join(output_dir, "TCU052三向 柱底M3內力圖(三向).png"), df_三向人造, df_三向設計)
