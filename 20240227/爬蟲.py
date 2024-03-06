import requests
import feedparser

# RSS feed URL
url = "https://news.pts.org.tw/xml/newsfeed.xml"

# 發送 GET 請求
response = requests.get(url)

# 解析 RSS feed
feed = feedparser.parse(response.content)

# 提取並列印所有的標題和summary，並將 標題 和 summary 含有中國或美國以紅色顯示，其他以綠色顯示，每個新聞間已經藍色粗分隔線分隔
for entry in feed.entries:
    title = entry.title
    summary = entry.summary
    if "中國" in title or "美國" in title:
        print("\033[31m" + title + "\033[0m")
        print("\033[31m" + summary + "\033[0m")
    else:
        print("\033[32m" + title + "\033[0m")
        print("\033[32m" + summary + "\033[0m")
    print("\033[34m" + "======================" + "\033[0m")