#https://www.cwa.gov.tw/V8/C/S/eservice/rss.html
import requests
from bs4 import BeautifulSoup
import feedparser
import urllib.parse
import geopandas as gpd
import matplotlib.pyplot as plt
import re
# Read shp data of Taiwan county 
# 縣市界
file_path = "C:\\Users\\User\\OneDrive\\桌面\\AI與土木應用\\GitHub\\cycu_ai2024_shing"
County_data = gpd.read_file(file_path)
base_url = 'https://www.cwa.gov.tw/V8/C/S/eservice/rss.html'
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

rss_links = [urllib.parse.urljoin(base_url, a['href']) for a in soup.find_all('a', href=True) if 'rss' in a['href']]
temp_dict = {}
# 遍歷所有的RSS鏈接

#搜尋County_data 的所有欄位並列印
print(County_data.columns)

for link in rss_links:
    feed = feedparser.parse(link)

    for entry in feed.entries:
        city_match = re.search(r'(\w+市|\w+縣)', entry.title)
        temp_match = re.search(r'溫度: (\d+ ~ \d+)', entry.title)
        if city_match and temp_match:
            temp_dict[city_match.group(1)] = temp_match.group(1)
print(temp_dict)
County_data['Temperature'] = County_data['City'].map(temp_dict)

# 讀取你的地理資訊
gdf = gpd.GeoDataFrame(County_data)

# 建立一個新的圖片，並設定大小
fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# 繪製地圖
gdf.plot(column='Temperature', legend=True, ax=ax)

# 設定 x 軸和 y 軸的範圍
ax.set_xlim(118, 124)
ax.set_ylim(20, 28 )

# 在每個區域的中心點添加文字
for x, y, label in zip(gdf.geometry.centroid.x, gdf.geometry.centroid.y, gdf['Temperature']):
    ax.text(x, y, label, fontsize=10)



plt.title('11022125shing')
# 顯示地圖
plt.show()

# 存檔
plt.savefig('map.png')


