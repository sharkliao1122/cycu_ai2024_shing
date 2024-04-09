import geopandas as gpd
import pandas as pd


#請幫我在此位置C:\Users\User\Documents\GitHub\cycu_ai2024_shing\20240402 尋找fiona支援的格式並raed shape file
import os
import geopandas as gpd

os.environ['SHAPE_RESTORE_SHX'] = 'YES'
df_taiwan = gpd.read_file("C:\\Users\\User\\OneDrive\\桌面\\AI與土木應用\\GitHub\\cycu_ai2024_shing")
                
##################################################
##################################################
# crawler from rss of central weather agency

import requests
import feedparser

county_list = []
for num in range(1, 23):
    #string format with prefix 0 if num < 10
    url = 'https://www.cwa.gov.tw/rss/forecast/36_' + str(num).zfill(2) + '.xml'
    print(url)
    #get xml from url
    response = requests.get(url)
    #parse rss feed
    feed = feedparser.parse(response.content)

    tempdict = {}

    for entry in feed.entries:
        # entry.title includes '溫度'
        if '溫度' in entry.title:
        # 資料的格式 如下:
        # 金門縣04/02 今晚明晨 晴時多雲 溫度: 22 ~ 24 降雨機率: 10% (04/02 17:00發布)
            print(entry.title)
        #取出縣市名稱(前三個字)
            tempdict['county'] = entry.title[:3]

        #取出溫度的部分 使用空格切割後 取出 -7 與 -5 的部分
            tempdict['min'] = entry.title.split(' ')[-7]
            tempdict['max'] = entry.title.split(' ')[-5]
            print(tempdict['county'], tempdict['min'], tempdict['max'])
    
            county_list.append(tempdict)
        print("=======================================")

df_weather = pd.DataFrame(county_list)


##################################################
##################################################
#plot taiwan using matplotlib
import matplotlib.pyplot as plt
geo_taiwan = pd.merge(df_taiwan, df_weather, left_on='geometry', right_on='county')

print (geo_taiwan)


geo_taiwan.plot()
plt.xlim(118,122)
plt.ylim(21.5,25.5)

#output countyname at centroid of each polygon
for x, y, label in zip(geo_taiwan.geometry.centroid.x, geo_taiwan.geometry.centroid.y, geo_taiwan['min']):
    plt.text(x, y, label, fontsize=8, ha='center')

for x, y, label in zip(geo_taiwan.geometry.centroid.x, geo_taiwan.geometry.centroid.y, geo_taiwan['max']):
    plt.text(x+ 0.2 , y, label, fontsize=8, ha='center')
plt.show()

