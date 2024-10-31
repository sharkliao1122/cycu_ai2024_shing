import pandas as pd
import os
import matplotlib.pyplot as plt

# 利用 FOR 迴圈 讀取資夾中的 EXCEL 檔案，並將第二列作為欄位名稱 
# 保留欄位 Time M3 R3Pl R3State
# 留下 R3State 為 B to <=C 的資料 
# C:\專題EXCEL新版\專題EXCEL\EYUL\EYUL三向塑鉸

input_folder = "C:\專題EXCEL新版\專題EXCEL\HWA009(除了塑鉸其他已整理)\HWA009水平雙向塑鉸"

output_folder = "C:\專題EXCEL新版\專題EXCEL\塑鉸M3VSR3PI"
os.makedirs(output_folder, exist_ok=True)

total_files = len([file for file in os.listdir(input_folder) if file.endswith(".xlsx")])
processed_files = 0

for file in os.listdir(input_folder):
    if file.endswith(".xlsx"):
        df = pd.read_excel(os.path.join(input_folder, file), header=1)
        df = df[["Time", "M3", "R3Pl", "R3State"]]
        df = df[df["R3State"].str.contains("B to <=C")]
        
        print()
        
        # 繪製折線圖
        plt.figure()
        plt.plot(df["M3"], df["R3Pl"])
        plt.xlabel("M3")
        plt.ylabel("R3Pl")
        title = os.path.splitext(file)[0] + " M3 VS R3PI"
        plt.title(title)
        plt.savefig(os.path.join(output_folder, title + ".png"))
        plt.close()
        
        processed_files += 1
        print(f"Processed {processed_files}/{total_files} files")

# "C:\\專題EXCEL新版\\專題EXCEL\\EYUL\\EYUL三向塑鉸\\EYUL 三向74H1塑鉸.xlsx"


