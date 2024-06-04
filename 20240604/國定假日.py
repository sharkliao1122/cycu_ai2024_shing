import csv
import os

data = [
    ["日期", "星期", "節日"],
    ["1月1日", "星期一", "元旦"],
    ["1月1日", "星期一", "中華民國開國紀念日"],
    ["2月8日 ～ 2月14日", "星期四 ～ 星期三", "春節"],
    ["2月28日", "星期三", "228 紀念日"],
    ["4月4日", "星期四", "兒童節"],
    ["4月4日", "星期四", "清明節"],
    ["4月5日", "星期五", "兒童節 (放假日)"],
    ["5月1日", "星期三", "勞動節 *"],
    ["6月10日", "星期一", "端午節"],
    ["9月17日", "星期二", "中秋節"],
    ["10月10日", "星期四", "中華民國國慶日"]
]

# 指定檔案路徑為桌面
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
file_path = os.path.join(desktop_path, 'holidays.csv')

with open(file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("CSV檔案已存入桌面，檔名為'holidays.csv'")
print("檔案路徑:", file_path)
