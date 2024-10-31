import  pandas as pd
import os
import matplotlib.pyplot as plt

# 讀取 CSV 檔案，並將第二列作為欄位名稱
df_雙向_位移= pd.read_excel("C:\專題EXCEL新版\專題EXCEL\EYUL\EYUL 水平雙向主樑中點位移.xlsx", header=1)
df_三向_位移 = pd.read_excel("C:\專題EXCEL新版\專題EXCEL\EYUL\EYUL 三向主樑中點位移.xlsx", header=1)
df_雙向_加速度= pd.read_excel("C:\專題EXCEL新版\專題EXCEL\EYUL\EYUL 水平雙向主樑中點加速度.xlsx", header=1)
df_三向_加速度 = pd.read_excel("C:\專題EXCEL新版\專題EXCEL\EYUL\EYUL 三向主樑中點加速度.xlsx", header=1)

# 保留 	StepNum	U1	U2	U3	
df_雙向_位移 = df_雙向_位移[['StepNum','U1','U2','U3']]
df_三向_位移 = df_三向_位移[['StepNum','U1','U2','U3']]
df_雙向_加速度 = df_雙向_加速度[['StepNum','U1','U2','U3']] 
df_三向_加速度 = df_三向_加速度[['StepNum','U1','U2','U3']]
# 將 StepNum 型別改為 FLOAT，並移除非數字值
df_雙向_位移['StepNum'] = pd.to_numeric(df_雙向_位移['StepNum'], errors='coerce')
df_三向_位移['StepNum'] = pd.to_numeric(df_三向_位移['StepNum'], errors='coerce')
df_雙向_加速度['StepNum'] = pd.to_numeric(df_雙向_加速度['StepNum'], errors='coerce')
df_三向_加速度['StepNum'] = pd.to_numeric(df_三向_加速度['StepNum'], errors='coerce')

df_雙向_位移 = df_雙向_位移.dropna(subset=['StepNum'])
df_三向_位移 = df_三向_位移.dropna(subset=['StepNum'])
df_雙向_加速度 = df_雙向_加速度.dropna(subset=['StepNum'])
df_三向_加速度 = df_三向_加速度.dropna(subset=['StepNum'])

# 繪製12 張圖表 分別 為 
# df_雙向_位移    U1對StepNum  ,U2對StepNum , U3對StepNum  的 折線圖 共三張圖 'U1','U2','U3' 單位為 M
# df_三向_位移    U1對StepNum  ,U2對StepNum , U3對StepNum  的 折線圖 共三張圖 'U1','U2','U3' 單位為 M
# df_雙向_加速度  U1對StepNum  ,U2對StepNum , U3對StepNum  的 折線圖 共三張圖 'U1','U2','U3' 單位為 M/S^2
# df_三向_加速度  U1對StepNum  ,U2對StepNum , U3對StepNum  的 折線圖 共三張圖 'U1','U2','U3' 單位為 M/S^2
# X 軸為  StepNum 
# 將圖片存於 輸入之 EXCEL 檔案相同資料夾，並依照  EXCEL 名稱將圖片命名 
# 命名規則 
# 1.若為 df_雙向_位移  中  U1對StepNum  ,U2對StepNum , U3對StepNum 命名為  EYUL 水平雙向主樑中點位移U1  EYUL 水平雙向主樑中點位移U2 EYUL 水平雙向主樑中點位移U3
# 2.df_三向_位移    U1對StepNum  ,U2對StepNum , U3對StepNum 同理 但將檔名中的 "雙向" 改為 "三向" 
# 3.若為 df_雙向_加速度 中 U1對StepNum  ,U2對StepNum , U3對StepNum  的 折線圖 命名為 EYUL 水平雙向主樑中點加速度U1 , EYUL 水平雙向主樑中點加速度U2
# 4.df_三向_加速度  U1對StepNum  ,U2對StepNum , U3對StepNum  的 折線圖 同理 將檔名中的 "雙向" 改為 "三向"
# 5.以上檔案皆須跟據 輸入的 EXCEL 之檔名做更改