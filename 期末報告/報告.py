import pandas as pd
import matplotlib.pyplot as plt

# 讀取 CSV 檔案並轉換成 DataFrame
df = pd.read_csv("C:\\Users\\User\\Downloads\\ObsTempAvg_桃園市.csv")

# 刪除 'CityName' 欄位
df = df.drop(columns=['CityName'])

# 只保留 MM 為 6、7、8、9 的資料
df = df[df['MM'].isin([6, 7, 8, 9])]

# 將 'YY' 和 'MM' 合併為 '日期'
df['日期'] = pd.to_datetime(df['YY'].astype(str) + '-' + df['MM'].astype(str))

# 繪製圖表
# 依照 6 7 8 9月 繪製 AvgTemp (依序為紅、橘、黃、綠)
colors = ['red', 'orange', 'yellow', 'green']
for i, month in enumerate([6, 7, 8, 9]):
    plt.plot(df[df['MM'] == month]['日期'], df[df['MM'] == month]['TempValue'], color=colors[i], label=f'{month}月')
    
plt.legend()
plt.show()