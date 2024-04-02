import pandas as pd

# 讀取Excel文件
df = pd.read_excel('C:\\Users\\User\\OneDrive\\桌面\\AI與土木應用\\GitHub\\cycu_ai2024_shing\\20240312\\112年1-10月交通事故簡訊通報資料.xlsx', engine='openpyxl')

#篩選欄位為"國道名稱 '的資料，將 國道一號  國道二號 國道三號 國道四號 的資料分別存到df1 df2 df3 df4
df1 = df[df['國道名稱'] == '國道1號']
df2 = df[df['國道名稱'] == '國道2號']
df3 = df[df['國道名稱'] == '國道3號']
df4 = df[df['國道名稱'] == '國道4號']

#國道一號的資料
#把 欄位 '年' '月' '日' '時' '分'
#合併成一個欄位 '日期' , 並且轉換成日期格式
df1['事件開始'] = df1['年'].astype(str) + '-' + df1['月'].astype(str) + '-' + df1['日'].astype(str) + ' ' + df1['時'].astype(str) + ':' + df1['分'].astype(str)
df1['事件開始'] = pd.to_datetime(df1['事件開始'])

#把 欄位 '年' '月' '日' '事件排除'  合併成一個欄位 '事件排除' , 並且轉換成日期格式
df1['事件排除'] = df1['年'].astype(str) + '-' + df1['月'].astype(str) + '-' + df1['日'].astype(str) + ' ' + df1['事件排除'].astype(str)
df1['事件排除'] = pd.to_datetime(df1['事件排除'])

#drop 欄位 '年' '月' '日' '時' '分'
df1 = df1.drop(columns=['年', '月', '日', '時', '分'])

#國道二號的資料
#把 欄位 '年' '月' '日' '時' '分'
#合併成一個欄位 '日期' , 並且轉換成日期格式
df2['事件開始'] = df2['年'].astype(str) + '-' + df2['月'].astype(str) + '-' + df2['日'].astype(str) + ' ' + df2['時'].astype(str) + ':' + df2['分'].astype(str)
df2['事件開始'] = pd.to_datetime(df2['事件開始'])

#把 欄位 '年' '月' '日' '事件排除'  合併成一個欄位 '事件排除' , 並且轉換成日期格式
df2['事件排除'] = df2['年'].astype(str) + '-' + df2['月'].astype(str) + '-' + df2['日'].astype(str) + ' ' + df2['事件排除'].astype(str)
df2['事件排除'] = pd.to_datetime(df2['事件排除'])

#drop 欄位 '年' '月' '日' '時' '分'
df2 = df2.drop(columns=['年', '月', '日', '時', '分'])

#國道三號的資料
#把 欄位 '年' '月' '日' '時' '分'
#合併成一個欄位 '日期' , 並且轉換成日期格式
df3['事件開始'] = df3['年'].astype(str) + '-' + df3['月'].astype(str) + '-' + df3['日'].astype(str) + ' ' + df3['時'].astype(str) + ':' + df3['分'].astype(str)
df3['事件開始'] = pd.to_datetime(df3['事件開始'])

#把 欄位 '年' '月' '日' '事件排除'  合併成一個欄位 '事件排除' , 並且轉換成日期格式
df3['事件排除'] = df3['年'].astype(str) + '-' + df3['月'].astype(str) + '-' + df3['日'].astype(str) + ' ' + df3['事件排除'].astype(str)
df3['事件排除'] = pd.to_datetime(df3['事件排除'])

#drop 欄位 '年' '月' '日' '時' '分'
df3 = df3.drop(columns=['年', '月', '日', '時', '分'])

#國道四號的資料
#把 欄位 '年' '月' '日' '時' '分'
#合併成一個欄位 '日期' , 並且轉換成日期格式
df4['事件開始'] = df4['年'].astype(str) + '-' + df4['月'].astype(str) + '-' + df4['日'].astype(str) + ' ' + df4['時'].astype(str) + ':' + df4['分'].astype(str)
df4['事件開始'] = pd.to_datetime(df4['事件開始'])

#把 欄位 '年' '月' '日' '事件排除'  合併成一個欄位 '事件排除' , 並且轉換成日期格式
df4['事件排除'] = df4['年'].astype(str) + '-' + df4['月'].astype(str) + '-' + df4['日'].astype(str) + ' ' + df4['事件排除'].astype(str)
df4['事件排除'] = pd.to_datetime(df4['事件排除'])

#drop 欄位 '年' '月' '日' '時' '分'
df4 = df4.drop(columns=['年', '月', '日', '時', '分'])

print(df1)
print(df2)
print(df3)
print(df4)


import matplotlib.pyplot as plt


#繪圖
def plot_dataframe(df, title):
    df['事件開始1'] = df['事件開始'].apply(lambda x: int(x.timestamp()))
    df['事件排除1'] = df['事件排除'].apply(lambda x: int(x.timestamp()))

    print(df[['事件開始', '事件排除', '國道名稱','里程','事件開始1','事件排除1']])

    for index, row in df.iterrows():
        plt.plot([row['事件開始1'], row['事件排除1']], [row['里程'], row['里程']])

    plt.xlabel('事件時間')
    plt.ylabel('里程')

    plt.title(title)
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus'] = False

    #plt.savefig(title + '.png')  # 保存圖形為PNG文件
    plt.show()

# 假設 df2, df3, df4 是您的 DataFrame
#plot_dataframe(df1, '國道1號交通事故')  
#plot_dataframe(df2, '國道2號交通事故')
#plot_dataframe(df3, '國道3號交通事故')
#plot_dataframe(df4, '國道4號交通事故')
