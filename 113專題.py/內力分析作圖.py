# 請幫我建立一個 讀取 excel 檔案的程式
# "C:\Users\User\OneDrive\桌面\學業\專題\EYUL\EYUL\EYUL 三向主樑內力.xlsx"
# 此 excel 第二列為欄位名稱，請幫我依據欄位名稱建立 df (留下 Station	CaseType	StepType	P	V2	V3	M2	M3 欄位)  


import pandas as pd
import matplotlib.pyplot as plt
import os

file_path = r"C:\Users\User\OneDrive\桌面\EYUL\EYUL\EYUL水平雙向全樑內力.xlsx" # 更改檔案路徑
output_dir = r"C:\Users\User\OneDrive\桌面\EYUL\水平雙向全樑內力" # 更改輸出目錄
# 確認輸出目錄存在，若不存在則創建
os.makedirs(output_dir, exist_ok=True)

try:
    # 讀取 Excel 檔案，指定第二列為欄位名稱
    df = pd.read_excel(file_path, header=1)

    # 選取指定的欄位
    columns_to_keep = ['Station', 'CaseType', 'StepType', 'P', 'V2', 'V3', 'M2', 'M3']
    df = df[columns_to_keep]

    # 顯示前幾列資料以確認
    print(df.head())
except (PermissionError, FileNotFoundError) as e:
    print(f"Error: {e}")
    exit()

# 繪製圖表
variables = ['P', 'V2', 'V3', 'M2', 'M3']
for var in variables:
    plt.figure()
    
    # 選取 StepType 為 Max 和 Min 的資料
    df_max = df[df['StepType'] == 'Max']
    df_min = df[df['StepType'] == 'Min']
    
    plt.plot(df_max['Station'], df_max[var], label='Max')
    plt.plot(df_min['Station'], df_min[var], label='Min')
    
    plt.xlabel('Station')
    plt.ylabel(var)
    plt.title(f'Horizontal internal force of beam- {var}') # 更改標題
    plt.legend()
    plt.grid(True)
    
    # 儲存圖表
    output_path = os.path.join(output_dir, f'水平雙向全樑內力_{var}.png')  # 更改檔名
    plt.savefig(output_path)
    plt.close()