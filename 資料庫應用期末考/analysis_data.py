# 讀取 3 個 csv 檔案
# 第一個 資料第一列為欄位 欄位名稱如下 TimeInterval、GantryID、Direction、VehicleType、Volume
# 第二個 資料第一列為欄位 欄位名稱如下 TimeInterval、GantryFrom、GantryTo、VehicleType、SpaceMeanSpeed、Volume
# 第三個 資料第一列為欄位 欄位名稱如下 TimeInterval、GantryID、VehicleType、VolumeVehicleType、DetectionTime_O、GantryID_O、DetectionTime_D、GantryID_D 、TripLength、TripEnd、TripInformation 
# 分別建立 3 個 DataFrame df_volume、df_speed、df_trip 分別存放讀取的資料


# 建立一個新的 df_analysis DataFrame
# 欄位名稱和定義如下
# TimeStamp: 時間戳記 為 00 到 23 共 24 小時  
# GantryID: 為 01F1389S
# Volume: 當小時的車流量 為 df_volume 中 該時段內所有 Volume 的總和
# Speed: 當小時的平均速度 為 df_speed 中 該時段內所有 SpaceMeanSpeed 的平均值
# Gantry0: 起始交流道 為 df_trip 中 該時段內所有 GantryID_O 的值

import pandas as pd

# 讀取第一個 CSV 檔案
df_volume = pd.read_csv(r"C:\資料庫應用期末報告\filtered_volume_01F1389S.csv")

# 讀取第二個 CSV 檔案
df_speed = pd.read_csv(r"C:\資料庫應用期末報告\filtered_speed_01F1389S.csv")

# 讀取第三個 CSV 檔案
df_trip = pd.read_csv(r"C:\資料庫應用期末報告\filtered_trip_01F1389S.csv")

# 將 TimeInterval 和 DetectionTime_D 欄位轉換為 datetime 類型
df_volume['TimeInterval'] = pd.to_datetime(df_volume['TimeInterval'])
df_speed['TimeInterval'] = pd.to_datetime(df_speed['TimeInterval'])
df_trip['DetectionTime_D'] = pd.to_datetime(df_trip['DetectionTime_D'])

# 選出指定日期範圍的資料
def filter_date_range(df, start_date, end_date, time_column='TimeInterval'):
    return df[(df[time_column] >= start_date) & (df[time_column] <= end_date)]

df_volume0101 = filter_date_range(df_volume, '2025/01/01 00:00:00', '2025/01/01 23:55:00')
df_volume1218 = filter_date_range(df_volume, '2024/12/18 00:00:00', '2024/12/18 23:55:00')
df_volume1225 = filter_date_range(df_volume, '2024/12/25 00:00:00', '2024/12/25 23:55:00')

df_speed0101 = filter_date_range(df_speed, '2025/01/01 00:00:00', '2025/01/01 23:55:00')
df_speed1218 = filter_date_range(df_speed, '2024/12/18 00:00:00', '2024/12/18 23:55:00')
df_speed1225 = filter_date_range(df_speed, '2024/12/25 00:00:00', '2024/12/25 23:55:00')

df_trip0101 = filter_date_range(df_trip, '2025/01/01 00:00:00', '2025/01/01 23:59:59', time_column='DetectionTime_D')
df_trip1218 = filter_date_range(df_trip, '2024/12/18 00:00:00', '2024/12/18 23:59:59', time_column='DetectionTime_D')
df_trip1225 = filter_date_range(df_trip, '2024/12/25 00:00:00', '2024/12/25 23:59:59', time_column='DetectionTime_D')

# 定義合併函數
def aggregate_hourly_volume(df):
    df['TimeInterval'] = df['TimeInterval'].dt.floor('H')
    df_agg = df.groupby(['TimeInterval', 'GantryID', 'Direction', 'VehicleType']).agg({'Volume': 'sum'}).reset_index()
    return df_agg

def aggregate_hourly_speed(df):
    df['TimeInterval'] = df['TimeInterval'].dt.floor('H')
    df['GantryID'] = df['GantryFrom']  # 假設 GantryFrom 是我們需要的 GantryID
    df_agg = df.groupby(['TimeInterval', 'GantryID', 'VehicleType']).agg({'SpaceMeanSpeed': 'mean'}).reset_index()
    return df_agg

def aggregate_hourly_trip(df):
    df['DetectionTime_D'] = df['DetectionTime_D'].dt.floor('H')
    df_agg = df.groupby(['DetectionTime_D', 'GantryID_O']).size().reset_index(name='Count')
    return df_agg

# 將資料改為每小時為一組
df_volume0101_hourly = aggregate_hourly_volume(df_volume0101)
df_volume1218_hourly = aggregate_hourly_volume(df_volume1218)
df_volume1225_hourly = aggregate_hourly_volume(df_volume1225)

df_speed0101_hourly = aggregate_hourly_speed(df_speed0101)
df_speed1218_hourly = aggregate_hourly_speed(df_speed1218)
df_speed1225_hourly = aggregate_hourly_speed(df_speed1225)

df_trip0101_hourly = aggregate_hourly_trip(df_trip0101)
df_trip1218_hourly = aggregate_hourly_trip(df_trip1218)
df_trip1225_hourly = aggregate_hourly_trip(df_trip1225)

# 建立分析 DataFrame
def create_analysis_df(df_volume_hourly, df_speed_hourly, df_trip_hourly):
    df_analysis = pd.DataFrame()
    df_analysis['TimeStamp'] = df_volume_hourly['TimeInterval'].dt.hour
    df_analysis['GantryID'] = '01F1389S'
    df_analysis['Volume'] = df_volume_hourly['Volume']
    df_analysis['Speed'] = df_speed_hourly['SpaceMeanSpeed'].round(2)
    
    # 展開 GantryID_O
    expanded_rows = []
    for _, row in df_analysis.iterrows():
        gantry_ids = df_trip_hourly[df_trip_hourly['DetectionTime_D'].dt.hour == row['TimeStamp']]['GantryID_O'].values
        counts = df_trip_hourly[df_trip_hourly['DetectionTime_D'].dt.hour == row['TimeStamp']]['Count'].values
        for gantry_id, count in zip(gantry_ids, counts):
            new_row = row.copy()
            new_row['Gantry0'] = gantry_id
            new_row['Gantry0-count'] = count
            expanded_rows.append(new_row)
    
    df_analysis = pd.DataFrame(expanded_rows)
    return df_analysis

# 建立3組新的 df_analysis DataFrame
df_analysis_0101 = create_analysis_df(df_volume0101_hourly, df_speed0101_hourly, df_trip0101_hourly)
df_analysis_1218 = create_analysis_df(df_volume1218_hourly, df_speed1218_hourly, df_trip1218_hourly)
df_analysis_1225 = create_analysis_df(df_volume1225_hourly, df_speed1225_hourly, df_trip1225_hourly)

#將上述df 檔案儲存為 csv 檔案於指定路徑 C:\Users\User\OneDrive\桌面\學業\AI與土木應用\GitHub\cycu_ai2024_shing\資料庫應用期末考
df_analysis_0101.to_csv(r"C:\Users\User\OneDrive\桌面\學業\AI與土木應用\GitHub\cycu_ai2024_shing\資料庫應用期末考\df_analysis_0101.csv", index=False)
df_analysis_1218.to_csv(r"C:\Users\User\OneDrive\桌面\學業\AI與土木應用\GitHub\cycu_ai2024_shing\資料庫應用期末考\df_analysis_1218.csv", index=False)
df_analysis_1225.to_csv(r"C:\Users\User\OneDrive\桌面\學業\AI與土木應用\GitHub\cycu_ai2024_shing\資料庫應用期末考\df_analysis_1225.csv", index=False)
