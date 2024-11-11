import pandas as pd
import os
import matplotlib.pyplot as plt

# 利用 FOR 迴圈 讀取 2 個資夾中的 EXCEL 檔案，並將第二列作為欄位名稱，建立 2 個 DataFrame dF_雙向 和 dF_三向
# 保留欄位 Time M3 R3Pl R3State
# 留下 R3State 為 B to <=C 的資料
#"C:\專題EXCEL新版\專題EXCEL\EYUL\EYUL水平雙向塑鉸"
# C:\專題EXCEL新版\專題EXCEL\EYUL\EYUL三向塑鉸

input_folder1 = "C:\專題EXCEL新版\專題EXCEL\TCU052設計\TCU052設計 EXCEL\TCU052設計水平雙向塑鉸"
input_folder2 = "C:\專題EXCEL新版\專題EXCEL\TCU052設計\TCU052設計 EXCEL\TCU052設計三向塑鉸"
files1 = [file for file in os.listdir(input_folder1) if file.endswith(".xlsx")]
files2 = [file for file in os.listdir(input_folder2) if file.endswith(".xlsx")]

total_files = len(files1) + len(files2)
processed_files = 0

df_雙向 = pd.DataFrame()
df_三向 = pd.DataFrame()

output_folder = "C:\專題EXCEL新版\專題EXCEL\素餃雙向 + 三項"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for file1, file2 in zip(files1, files2):
    df_temp_雙向 = pd.read_excel(os.path.join(input_folder1, file1), header=1)
    df_temp_三向 = pd.read_excel(os.path.join(input_folder2, file2), header=1)
    if file1.endswith(".xlsx"):
        df_temp_雙向 = df_temp_雙向[df_temp_雙向["R3State"].str.contains("C to <=D", na=False)]
        df_temp_雙向 = df_temp_雙向[["Time", "M3", "R3Pl", "R3State"]]
        df_temp_雙向 = df_temp_雙向[df_temp_雙向["R3State"].str.contains("C to <=D")]
        df_雙向 = pd.concat([df_雙向, df_temp_雙向], ignore_index=True)
        
        processed_files += 1
        print(f"Processed {processed_files}/{total_files} files in Biaxial")
        
    if file2.endswith(".xlsx"):
        df_temp_三向 = df_temp_三向[df_temp_三向["R3State"].str.contains("C to <=D", na=False)]
        df_temp_三向 = df_temp_三向[["Time", "M3", "R3Pl", "R3State"]]
        df_temp_三向 = df_temp_三向[df_temp_三向["R3State"].str.contains("C to <=D")]
        df_三向 = pd.concat([df_三向, df_temp_三向], ignore_index=True)
        
        processed_files += 1
        print(f"Processed {processed_files}/{total_files} files in Triaxial")
    
    # 生成圖片標題和檔案名稱
    base_name_雙向 = os.path.basename(file1).replace("水平雙向", "").replace(".xlsx", "").strip()
    base_name_三向 = os.path.basename(file2).replace("三向", "").replace(".xlsx", "").strip()
    a = f"{base_name_雙向} Biaxial + Triaxial"
    
    title_m3 = f"Time vs M3 ({a})"
    title_r3pl = f"Time vs R3Pl ({a})"
    
    output_file_m3 = os.path.join(output_folder, f"{a} (M3).png")
    output_file_r3pl = os.path.join(output_folder, f"{a} (R3Pl).png")
    
    # 繪製折線圖
    plt.figure()
    plt.plot(df_雙向["Time"], df_雙向["M3"], 'orange', label='Biaxial M3')
    plt.plot(df_三向["Time"], df_三向["M3"], 'b--', label='Triaxial M3')
    plt.xlabel('Time')
    plt.ylabel('M3')
    plt.xlim(0, 120)  # 設定 X 軸範圍
    plt.ylim(-37500, 37500)  # 設定 Y 軸範圍
    plt.legend()
    plt.title(title_m3)
    plt.savefig(output_file_m3)
    print(f"Saved plot: {output_file_m3}")
    
    plt.figure()
    plt.plot(df_雙向["Time"], df_雙向["R3Pl"], 'orange', label='Biaxial R3Pl')
    plt.plot(df_三向["Time"], df_三向["R3Pl"], 'b--', label='Triaxial R3Pl')
    plt.xlabel('Time')
    plt.ylabel('R3Pl')
    plt.xlim(0, 120)  # 設定 X 軸範圍
    plt.ylim(-0.03, 0.03)  # 設定 Y 軸範圍
    plt.legend()
    plt.title(title_r3pl)
    plt.savefig(output_file_r3pl)
    df_三向 = pd.DataFrame()
    df_雙向 = pd.DataFrame()
    
 
    
# 圖片標題為 根據檔案名稱生成 及 Y 軸 標題 ，舉例如下
#"C:\專題EXCEL新版\專題EXCEL\EYUL\EYUL水平雙向塑鉸\EYUL水平雙向74H1塑鉸.xlsx"
#"C:\專題EXCEL新版\專題EXCEL\EYUL\EYUL三向塑鉸\EYUL 三向74H1塑鉸.xlsx"
# Y 軸 標題為 M3 
# 則標題 為 EYUL 74H1 水平雙向 + 三向塑鉸 M3 並存檔於 C:\專題EXCEL新版\專題EXCEL\素餃雙向 + 三項
# "C:\專題EXCEL新版\專題EXCEL\TCU052\TCU052水平雙向塑鉸\TCU052水平雙向74H10塑鉸.xlsx"
# "C:\專題EXCEL新版\專題EXCEL\TCU052\TCU052三向塑鉸\TCU052 三向74H10塑鉸.xlsx"
# Y 軸 標題為 R3Pl
# 則標題 為 TCU052 74H10 水平雙向 + 三向塑鉸 R3Pl 並存檔於 C:\專題EXCEL新版\專題EXCEL\雙向 + 三項 塑鉸
# 以上標題 用英文顯示 檔案名稱則可用中文顯示