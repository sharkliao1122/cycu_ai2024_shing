import pandas as pd

# 讀取第一個 CSV 檔案
df_volume = pd.read_csv(r"C:\Users\User\OneDrive\桌面\資料庫應用期末報告\filtered_volume_01F1389S.csv")

# 讀取第二個 CSV 檔案
df_speed = pd.read_csv(r"C:\Users\User\OneDrive\桌面\資料庫應用期末報告\filtered_speed_01F1389S.csv")

# 讀取第三個 CSV 檔案
df_trip = pd.read_csv(r"C:\Users\User\OneDrive\桌面\資料庫應用期末報告\filtered_trip_01F1389S.csv")

# 將 TimeInterval 和 DetectionTime_D 欄位轉換為 datetime 類型
df_volume['TimeInterval'] = pd.to_datetime(df_volume['TimeInterval'])
df_speed['TimeInterval'] = pd.to_datetime(df_speed['TimeInterval'])
df_trip['DetectionTime_D'] = pd.to_datetime(df_trip['DetectionTime_D'])

# 選出指定日期範圍的資料
def filter_date_range(df, start_date, end_date, time_column='TimeInterval'):
    return df[(df[time_column] >= start_date) & (df[time_column] <= end_date)]

df_volume0101 = filter_date_range(df_volume, '2025-01-01 00:00:00', '2025-01-01 23:55:00')
df_volume1218 = filter_date_range(df_volume, '2025-12-18 00:00:00', '2025-12-18 23:55:00')
df_volume1225 = filter_date_range(df_volume, '2025-12-25 00:00:00', '2025-12-25 23:55:00')

df_speed0101 = filter_date_range(df_speed, '2025-01-01 00:00:00', '2025-01-01 23:55:00')
df_speed1218 = filter_date_range(df_speed, '2025-12-18 00:00:00', '2025-12-18 23:55:00')
df_speed1225 = filter_date_range(df_speed, '2025-12-25 00:00:00', '2025-12-25 23:55:00')

df_trip0101 = filter_date_range(df_trip, '2025-01-01 00:00:00', '2025-01-01 23:59:59', time_column='DetectionTime_D')
df_trip1218 = filter_date_range(df_trip, '2025-12-18 00:00:00', '2025-12-18 23:59:59', time_column='DetectionTime_D')
df_trip1225 = filter_date_range(df_trip, '2025-12-25 00:00:00', '2025-12-25 23:59:59', time_column='DetectionTime_D')

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

# 建立 df_analysis DataFrame
def create_df_analysis(df_volume_hourly, df_speed_hourly, df_trip_hourly):
    df_analysis = pd.DataFrame()
    df_analysis['TimeStamp'] = df_volume_hourly['TimeInterval'].dt.hour
    df_analysis['GantryID'] = '01F1389S'
    df_analysis['Volume'] = df_volume_hourly['Volume']
    df_analysis['Speed'] = df_speed_hourly['SpaceMeanSpeed'].round(2)
    
    # 處理 Gantry0 和 Gantry0_count
    df_trip_grouped = df_trip_hourly.groupby('DetectionTime_D').agg({
        'GantryID_O': lambda x: ','.join(x),
        'Count': lambda x: ','.join(map(str, x))
    }).reset_index()
    
    df_analysis = pd.merge(df_analysis, df_trip_grouped, left_on='TimeStamp', right_on='DetectionTime_D', how='left')
    df_analysis = df_analysis[['TimeStamp', 'GantryID', 'Volume', 'Speed', 'GantryID_O', 'Count']]
    df_analysis.columns = ['TimeStamp', 'GantryID', 'Volume', 'Speed', 'Gantry0', 'Gantry0_count']
    
    return df_analysis

df_analysis0101 = create_df_analysis(df_volume0101_hourly, df_speed0101_hourly, df_trip0101_hourly)
df_analysis1218 = create_df_analysis(df_volume1218_hourly, df_speed1218_hourly, df_trip1218_hourly)
df_analysis1225 = create_df_analysis(df_volume1225_hourly, df_speed1225_hourly, df_trip1225_hourly)

# 將 df_analysis 變為 CSV 檔案存於指定路徑
df_analysis0101.to_csv(r"C:\Users\User\OneDrive\桌面\資料庫應用期末報告\df_analysis_0101.csv", index=False)
df_analysis1218.to_csv(r"C:\Users\User\OneDrive\桌面\資料庫應用期末報告\df_analysis1218.csv", index=False)
df_analysis1225.to_csv(r"C:\Users\User\OneDrive\桌面\資料庫應用期末報告\df_analysis1225.csv", index=False)

