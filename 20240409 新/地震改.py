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
    start_date = datetime(2024, 8, 1, 15, 0, 0)
    end_date = datetime(2024, 8, 1, 16, 0, 0)
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