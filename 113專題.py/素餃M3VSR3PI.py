import pandas as pd
import os
import matplotlib.pyplot as plt

# 利用 FOR 迴圈 讀取資夾中的 EXCEL 檔案，並將第二列作為欄位名稱 
# 保留欄位 Time M3 R3Pl R3State
# 留下 R3State 為 B to <=C 的資料 
# C:\專題EXCEL新版\專題EXCEL\EYUL\EYUL三向塑鉸
input_folder = "C:\專題EXCEL新版\專題excel_NEW\專題excel\EYUL\EYUL三向塑鉸"


files1 = [file for file in os.listdir(input_folder) if file.endswith(".xlsx")]
output_folder = "C:\專題EXCEL新版\專題excel_NEW\專題excel\圖表\塑鉸M3與R3PI\EYUL塑鉸"
processed_files = 0

for file in files1:
    if file.endswith(".xlsx"):
        df = pd.read_excel(os.path.join(input_folder, file), header=1)
        df = df[["Time", "M3", "R3Pl", "R3State"]]
        
        # 繪製 R3State 為 B to <=C 的圖
        df_B_to_C = df[df["R3State"].str.contains("B to <=C")]
        if not df_B_to_C.empty:
            title = "R3Pl VS M3 (B to <=C)"
            file_name = os.path.splitext(os.path.basename(file))[0] + "_B_to_C"
            output_file = os.path.join(output_folder, f"{file_name}.png")
            
            plt.figure()
            plt.plot(df_B_to_C["R3Pl"], df_B_to_C["M3"])
            plt.xlabel("R3Pl")
            plt.ylabel("M3")
            plt.xlim(-0.003, 0.003)  # 設定 X 軸範圍
            plt.ylim(-37500,37500)  # 設定 Y 軸範圍
            plt.title(title)
            plt.savefig(output_file)
            plt.close()
        
        # 繪製 R3State 為 C to <=D 的圖
        df_C_to_D = df[df["R3State"].str.contains("C to <=D")]
        if not df_C_to_D.empty:
            title = "R3Pl VS M3 (C to <=D)"
            file_name = os.path.splitext(os.path.basename(file))[0] + "_C_to_D"
            output_file = os.path.join(output_folder, f"{file_name}.png")
            
            plt.figure()
            plt.plot(df_C_to_D["R3Pl"], df_C_to_D["M3"])
            plt.xlabel("R3Pl")
            plt.ylabel("M3")
            plt.xlim(-0.003, 0.003)  # 設定 X 軸範圍
            plt.ylim(-37500,37500)  # 設定 Y 軸範圍
            plt.title(title)
            plt.savefig(output_file)
            plt.close()
        
        processed_files += 1
        print(f"Processed {processed_files}/{len(files1)} files")
        
        # 重置 df
        df = pd.DataFrame()








