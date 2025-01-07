import os
import requests
import pandas as pd
from datetime import datetime, timedelta

def download_csv(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)

def generate_urls(date):
    base_url = "https://tisvcloud.freeway.gov.tw/history/TDCS/M06A/"
    urls = []
    for hour in range(24):
        timestamp = datetime.strptime(date, "%Y%m%d") + timedelta(hours=hour)
        url = f"{base_url}{date}/{timestamp.strftime('%H')}/TDCS_M06A_{timestamp.strftime('%Y%m%d_%H%M%S')}.csv"
        urls.append(url)
    return urls

def main():
    dates = ["20241218", "20241225", "20250101"]
    save_dir = "C:\\資料庫應用 期末考"
    os.makedirs(save_dir, exist_ok=True)
    
    data_frames = {}
    for date in dates:
        all_data = []
        urls = generate_urls(date)
        total_files = len(urls)
        for i, url in enumerate(urls):
            file_name = url.split('/')[-1]
            save_path = os.path.join(save_dir, file_name)
            download_csv(url, save_path)
            data = pd.read_csv(save_path)
            # 設定下載的 CSV 檔案的欄位名稱
            data.columns = ['VehicleType', 'DetectionTime_O', 'GantryID_O', 'DetectionTime_D', 'GantryID_D', 'TripLength', 'TripEnd', 'TripInformation']
            all_data.append(data)
            print(f"Downloading data for {date}: {i + 1}/{total_files} files downloaded")
        
        combined_data = pd.concat(all_data)
        combined_data = combined_data[['VehicleType', 'DetectionTime_O', 'GantryID_O', 'DetectionTime_D', 'GantryID_D', 'TripLength', 'TripEnd', 'TripInformation']]
        data_frames[date] = combined_data
        combined_save_path = os.path.join(save_dir, f"M06A_{date[4:]}.csv")
        combined_data.to_csv(combined_save_path, index=False)
        
        # 刪除下載的 CSV 檔案
        for url in urls:
            file_name = url.split('/')[-1]
            save_path = os.path.join(save_dir, file_name)
            if os.path.exists(save_path):
                os.remove(save_path)
    
    df_1218 = data_frames["20241218"]
    df_1225 = data_frames["20241225"]
    df_0101 = data_frames["20250101"]

if __name__ == "__main__":
    main()