import requests
from bs4 import BeautifulSoup
import os

# 目標網址
url = 'https://tisvcloud.freeway.gov.tw/history/TDCS/M04A/20240325/00/'
#以迴圈方式依'https://tisvcloud.freeway.gov.tw/history/TDCS/M04A/20240325/00/' 'https://tisvcloud.freeway.gov.tw/history/TDCS/M04A/20240325/01/' 直至'https://tisvcloud.freeway.gov.tw/history/TDCS/M04A/20240325/23/'
for i in range(0,24):
    url = 'https://tisvcloud.freeway.gov.tw/history/TDCS/M04A/20240325/'+str(i).zfill(2)+'/'
    # 如果目錄不存在，則建立目錄
    if not os.path.exists(str(i).zfill(2)):
        os.makedirs(str(i).zfill(2))
    # 目標網址
    url = 'https://tisvcloud.freeway.gov.tw/history/TDCS/M04A/20240325/'+str(i).zfill(2)+'/'
    # 發送 GET 請求
    response = requests.get(url)
    # 如果回應的狀態碼不是 200，則印出錯誤訊息並結束程式
    if response.status_code != 200:
        print(f'Error: Unable to access {url}')
        exit()
    # 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    # 找到所有的 <a> 標籤（連結）
    links = soup.find_all('a')
    # 遍歷每一個連結，並下載 CSV 檔案至 /workspaces/cycu_ai2024_shing/20240326
    import pandas as pd

    csv_files = []  # 儲存所有 CSV 檔案的路徑

    import os

    # 建立資料夾
    folder_name = "/workspaces/cycu_ai2024_shing/20240326/高工數據"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for link in links:
        href = link.get('href')
        if href.endswith('.csv'):
            filename = href.split('/')[-1]
            file_path = os.path.join(folder_name, filename)  # CSV 檔案的路徑
            csv_files.append(file_path)  # 將路徑加入列表
            response = requests.get(url + href)
            with open(file_path, 'wb') as f:
                f.write(response.content)
                print(f'Download {filename} to {file_path}')
    
import pandas as pd
import glob

# 獲取資料夾中所有 CSV 檔案的路徑
csv_files = glob.glob("/workspaces/cycu_ai2024_shing/20240326/高工數據/*.csv")

# 讀取並合併所有 CSV 檔案
df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)

# 顯示 DataFrame
print(df)
                

                
                
                
                
                

