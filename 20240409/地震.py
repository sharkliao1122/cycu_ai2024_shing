import openpyxl
import folium
import pandas as pd

# 讀取Excel檔案
book = openpyxl.load_workbook(r'C:\Users\User\Documents\GitHub\cycu_ai2024_shing\地震.xlsx')

# 選擇活動工作表
sheet = book.active

# 將工作表轉換為DataFrame
# 並將第818列以後的資料刪除
df = pd.DataFrame(sheet.values)
df = df.drop(df.index[817:])
df.columns = df.iloc[0]
df = df.drop(df.index[0])

# 使用 folium 將df中的所有地震標示在地圖上
m = folium.Map(location=[23.5, 121], zoom_start=7)
for i in range(1, len(df)):  # 從第二行開始迭代
    color = 'red' if float(df.iloc[i, 3]) >= 5 else 'blue'  # 如果規模大於或等於5，則顏色為紅色；否則，顏色為藍色
    popup_text = f"規模: {df.iloc[i, 3]}, 經度: {df.iloc[i, 1]}, 緯度: {df.iloc[i, 2]}, 時間: {df.iloc[i, 0]}"  # 創建彈出視窗的文字
    folium.Circle(location=[float(df.iloc[i, 2]), float(df.iloc[i, 1])], radius=float(df.iloc[i, 3]), color=color, fill=True, fill_color=color, popup=popup_text).add_to(m)
m.save('earthquake.html')
# 在瀏覽器中打開地圖
import webbrowser
webbrowser.open('earthquake.html')