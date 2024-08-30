# 請幫我建立一之爬蟲程式，爬取中央氣象局的地震資訊，並且將資訊寫入到一個檔案中。
# 請注意，這個程式必須要能夠在每次執行時，都能夠將最新的地震資訊寫入到檔案中。
# 網址格式如下 https://scweb.cwa.gov.tw/zh-tw/earthquake/details/2024080115224438 需將數字部分從08/01 00:00:00 至 08/31 23:59:59 逐一爬取
# 所需爬取內容關鍵字格式如下：
# 發震時間： 113年8月1日 15時22分44秒
# 震央位置： 北緯 23.97 ° 東經 121.71 °
# 地震深度： 26.7 公里
# 芮氏規模： 3.8

# 將內容依照欄位分配如下，並以 Df 形式呈現
# 發震時間, 震央位置, 地震深度, 芮氏規模

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

# 生成所有可能的網址
def generate_urls(start_date, end_date):
    urls = []
    current_date = start_date
    while current_date <= end_date:
        url = f"https://scweb.cwa.gov.tw/zh-tw/earthquake/details/{current_date.strftime('%Y%m%d%H%M%S')}"
        urls.append(url)
        current_date += timedelta(seconds=1)
    return urls

# 爬取單個網址的地震資訊
def fetch_earthquake_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        info = {}
        info['發震時間'] = soup.find(text="發震時間：").find_next().text.strip()
        info['震央位置'] = soup.find(text="震央位置：").find_next().text.strip()
        info['地震深度'] = soup.find(text="地震深度：").find_next().text.strip()
        info['芮氏規模'] = soup.find(text="芮氏規模：").find_next().text.strip()
        return info
    return None

# 主函數
def main():
    start_date = datetime(2024, 8, 1, 0, 0, 0)
    end_date = datetime(2024, 8, 31, 23, 59, 59)
    urls = generate_urls(start_date, end_date)
    
    data = []
    total_urls = len(urls)
    for i, url in enumerate(urls):
        info = fetch_earthquake_info(url)
        if info:
            data.append(info)
        # 顯示進度
        current_time = start_date + timedelta(seconds=i)
        print(f"Progress: {i+1}/{total_urls} - Current Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    df = pd.DataFrame(data)
    df.to_csv('earthquake_data.csv', index=False)
    print(df)

if __name__ == "__main__":
    main()