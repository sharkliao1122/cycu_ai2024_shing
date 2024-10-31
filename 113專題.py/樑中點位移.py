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

# 繪製6張圖表 分別 為 df_雙向  和 df_三向 中 'U1','U2','U3' 對 'StepNum'  的 折線圖
# 將同張圖 要有 時間與位移 以及 時間與加速度
# X 軸為  StepNum  Y 軸為 U1(M)
# 雙向
plt.figure(figsize=(15, 15))
plt.subplot(3, 2, 1)

plt.plot(df_雙向_位移['StepNum'], pd.to_numeric(df_雙向_位移['U1'], errors='coerce'), label='U1(M)')
plt.plot(df_雙向_加速度['StepNum'], pd.to_numeric(df_雙向_加速度['U1'], errors='coerce'), label='U1(M/s^2)')
plt.title('U1(M) AND U1(M/s^2) vs StepNum')
plt.xlabel('StepNum')
plt.ylabel('U1(M)')
plt.legend()

# Show all plots at the end
plt.show()
