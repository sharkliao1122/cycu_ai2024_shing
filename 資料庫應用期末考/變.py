import pandas as pd

# 讀取csv檔案
df = pd.read_csv(r"C:\資料庫應用期末報告\df_analysis_0101.csv")
df1 = pd.read_csv(r"C:\資料庫應用期末報告\df_analysis_1218.csv")
df2 = pd.read_csv(r"C:\資料庫應用期末報告\df_analysis_1225.csv")

# 繪製折線圖 以時間為x軸，Volume為y軸
# 標題為 01F1389S + "日期" 交通量
# 標籤為 "時間" 和 "交通量"
# 將三組數據合併為一張圖表 紅色為0101，綠色為1218，藍色為1225 (需再加上圖例)

import matplotlib.pyplot as plt

plt.plot(df['TimeStamp'], df['Volume'], color='red', label='0101')
plt.plot(df1['TimeStamp'], df1['Volume'], color='green', label='1218')
plt.plot(df2['TimeStamp'], df2['Volume'], color='blue', label='1225')
plt.title('20250101 Volume(01F1389S)')
plt.xlabel('Time')
plt.ylabel('Volume')
plt.legend()
#存於指定路徑 C:\資料庫應用期末報告\01F1389S 0101交通量.png
plt.savefig(r"C:\資料庫應用期末報告\01F1389S 0101交通量.png")
plt.show()

# 繪製折線圖 以時間為x軸，Speed為y軸
# 標題為 01F1389S + "日期" Speed
# 標籤為 "Time" 和 "Speed"
# 折線圖 需依照 speed 變化作圖 規則如下 0-20為黑色，20-40為紅色，40-60為橘色，60-80為黃色，80-100為藍色，100以上為綠色 (需再加上圖例)
# 請將三組數據分開作圖
# 將顏色的意義標示出來

def plot_speed(df, date, color_map, save_path):
    plt.figure()
    for i in range(len(df) - 1):
        speed = df['Speed'][i]
        for range_, color in color_map.items():
            if range_[0] <= speed < range_[1]:
                plt.plot(df['TimeStamp'][i:i+2], df['Speed'][i:i+2], color=color)
                break
    plt.title(f'2025{date} Speed(01F1389S)')
    plt.xlabel('Time')
    plt.ylabel('Speed')
    plt.legend(handles=[plt.Line2D([0], [0], color=color, lw=2, label=f'{range_[0]}-{range_[1]}') for range_, color in color_map.items()])
    plt.savefig(save_path)
    plt.show()

color_map = {
    (0, 20): 'black',
    (20, 40): 'red',
    (40, 60): 'orange',
    (60, 80): 'yellow',
    (80, 100): 'blue',
    (100, float('inf')): 'green'
}

plot_speed(df, '0101', color_map, r"C:\資料庫應用期末報告\01F1389S 0101 Speed.png")
plot_speed(df1, '1218', color_map, r"C:\資料庫應用期末報告\01F1389S 1218 Speed.png")
plot_speed(df2, '1225', color_map, r"C:\資料庫應用期末報告\01F1389S 1225 Speed.png")

#繪製柱狀圖 以Gantry0為x軸(選擇Gantry0-count 前七多)，Gantry0-count為y軸
#紅色表示 0101，，藍色表示 1225
#標題為 20250101 GANTRY VOLUME
#標籤為 "Gantry" 和 "Volume"
#將x 軸間距擴大

def plot_gantry(df, date, save_path):
    plt.figure()
    plt.bar(df['Gantry0'][:7], df['Gantry0-count'][:7], color='red' if date == '0101' else 'blue')
    plt.title(f'2025{date} GANTRY VOLUME')
    plt.xlabel('Gantry')
    plt.ylabel('Volume')
    plt.xticks(rotation=45)
    plt.savefig(save_path)
    plt.show()
    
plot_gantry(df, '0101', r"C:\資料庫應用期末報告\20250101 GANTRY VOLUME.png")
plot_gantry(df2, '1225', r"C:\資料庫應用期末報告\20250101 GANTRY VOLUME.png")