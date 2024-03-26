#幫我寫一個爬csv 檔的爬蟲
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

# 目標網址
url = 'https://tisvcloud.freeway.gov.tw/history/TDCS/M04A/20240325/'

# 發送 GET 請求
response = requests.get(url)

# 解析 HTML
soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有的 <a> 標籤（連結）
links = soup.find_all('a')

# 遍歷每一個連結
for link in links:
    # 如果連結的 href 屬性以 .csv 結尾
    if link['href'].endswith('.csv'):
        # 組合完整的檔案 URL
        file_url = url + link['href']
        # 發送 GET 請求來下載 CSV 檔案
        file_response = requests.get(file_url)
        # 將下載的 CSV 檔案內容寫入檔案
        with open(link['href'], 'w') as f:
            f.write(file_response.text)

#將所有的csv 檔合併成一個dataframe
files = os.listdir()
dfs = []
for file in files:
    if file.endswith('.csv'):
        dfs.append(pd.read_csv(file))
df = pd.concat(dfs)
print(df)

            