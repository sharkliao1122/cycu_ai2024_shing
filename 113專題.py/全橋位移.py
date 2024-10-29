import pandas as pd
import matplotlib.pyplot as plt

file_path = r"C:\EYUL\EYUL\EYUL水平雙向全橋位移.xlsx"

# 讀取 Excel 檔案，指定第二列為欄位名稱，第三列為單位，第四列之後為資料
df = pd.read_excel(file_path, header=1)

# 選出第 78, 79, 88, 89, 98, 99 列的資料
df_filtered = df.iloc[[77, 78, 87, 88, 97, 98]]

# 刪除 U3, R1, R2, R3 欄位
df_filtered = df_filtered.drop(columns=['U3', 'R1', 'R2', 'R3'])

# 以 U1 和 U2 新建兩個 DataFrame
df_u1 = df_filtered[['Joint', 'U1']]
df_u2 = df_filtered[['Joint', 'U2']]

# 新增欄位 THETA，定義為相鄰兩列 U1, U2 (77 78 為一組, 87 88 為一組, 97 98 為一組) 的絕對值較大者 / 10 的值
def calculate_theta(df, col):
    theta_values = []
    for i in range(0, len(df), 2):
        if i + 1 < len(df):
            max_val = max(abs(df.iloc[i][col]), abs(df.iloc[i + 1][col]))
            theta = max_val / 10
            theta_values.append(theta)
            theta_values.append(theta)  # 對應兩列相同的 THETA 值
    return theta_values

df_u1['THETA'] = calculate_theta(df_u1, 'U1')
df_u2['THETA'] = calculate_theta(df_u2, 'U2')

# 繪製柱狀圖
fig, ax = plt.subplots()
bar_width = 0.35
index = [45, 51, 57]

# 由於 df_u1 和 df_u2 中每個 Joint 有兩列資料，取平均值來繪製柱狀圖
df_u1_grouped = df_u1.groupby('Joint').mean()
df_u2_grouped = df_u2.groupby('Joint').mean()

bar1 = ax.bar([i - bar_width/2 for i in index], df_u1_grouped['THETA'], bar_width, label='U1 THETA')
bar2 = ax.bar([i + bar_width/2 for i in index], df_u2_grouped['THETA'], bar_width, label='U2 THETA')

ax.set_xlabel('Joint')
ax.set_ylabel('THETA')
ax.set_title('THETA by Joint (U1 and U2)')
ax.set_xticks(index)
ax.set_xticklabels(index)
ax.legend()

# 加上數值標籤
for bar in bar1:
    height = bar.get_height()
    ax.annotate(f'{height:.4f}',  # 使用四位小數顯示完整的 THETA 值
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

for bar in bar2:
    height = bar.get_height()
    ax.annotate(f'{height:.4f}',  # 使用四位小數顯示完整的 THETA 值
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

# 顯示圖表
plt.show()

# 將圖片儲存為圖片檔存於指定路徑 "C:\EYUL\水平雙向全橋位移" 中
output_path = r"C:\EYUL\水平雙向全橋位移\THETA_by_Joint.png"
fig.savefig(output_path)

# 列出 THETA 值
print("U1 THETA values:")
print(df_u1_grouped['THETA'])
print("\nU2 THETA values:")
print(df_u2_grouped['THETA'])