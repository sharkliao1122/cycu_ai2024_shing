# 幫我讀取 兩分 CSV 檔案 並分別 建立 兩個 DataFrame 一個叫做 df_雙向 另一個叫做 df_三向
# CSV 檔案中第二列為欄位名稱 幫我留下 這些欄位 	Station	 StepType	P	V2	V3	M2	M3 ，且留下的 資料 只有 Station	為5 的資料
# df_雙向  "C:\Users\User\OneDrive\桌面\EYUL\EYUL水平雙向全樑內力.xlsx"
# df_三向  "C:\Users\User\OneDrive\桌面\EYUL\EYUL 三向主樑內力.xlsx"

import pandas as pd

# 讀取 CSV 檔案，並將第二列作為欄位名稱
df_雙向 = pd.read_excel("C:\\Users\\User\\OneDrive\\桌面\\EYUL\\EYUL水平雙向全樑內力.xlsx", header=1)
df_三向 = pd.read_excel("C:\\Users\\User\\OneDrive\\桌面\\EYUL\\EYUL 三向主樑內力.xlsx", header=1)

# 保留指定的欄位
columns_to_keep = ['Station', 'StepType', 'P', 'V2', 'V3', 'M2', 'M3']
df_雙向 = df_雙向[columns_to_keep]
df_三向 = df_三向[columns_to_keep]

# 篩選 Station 為 5 的資料
df_雙向 = df_雙向[df_雙向['Station'] == 5]
df_三向 = df_三向[df_三向['Station'] == 5]

# 顯示結果
print(df_雙向)
print(df_三向)