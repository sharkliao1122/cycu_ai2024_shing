import pandas as pd
import os
import matplotlib.pyplot as plt

# 利用 FOR 迴圈 讀取資夾中的 EXCEL 檔案，並將第二列作為欄位名稱 
# 保留欄位 Time M3 R3Pl R3State
# 留下 R3State 為 B to <=C 的資料 
# C:\專題EXCEL新版\專題EXCEL\EYUL\EYUL三向塑鉸
input_folder = "C:\專題EXCEL新版\專題EXCEL\TCU052設計\TCU052設計水平雙向塑鉸"
files1 = [file for file in os.listdir(input_folder) if file.endswith(".xlsx")]
output_folder = "C:\\專題EXCEL新版\\專題EXCEL\\塑鉸M3VSR3PI"
processed_files = 0

for file in files1:
    if file.endswith(".xlsx"):
        df = pd.read_excel(os.path.join(input_folder, file), header=1)
        df = df[["Time", "M3", "R3Pl", "R3State"]]
        df = df[df["R3State"].str.contains("B to <=C")]
        print(df)
        print()
        
        processed_files += 1
        print(f"Processed {processed_files}/{len(files1)} files")
        
        # 生成圖片標題和檔案名稱
        title = "R3Pl VS M3"
        file_name = os.path.splitext(os.path.basename(file))[0]
        output_file = os.path.join(output_folder, f"{file_name}.png")
        
        # 繪製折線圖
        plt.figure()
        plt.plot(df["R3Pl"], df["M3"])
        plt.xlabel("R3Pl")
        plt.ylabel("M3")
        plt.title(title)
        plt.savefig(output_file)
        plt.close()
        
        # 重置 df
        df = pd.DataFrame()








