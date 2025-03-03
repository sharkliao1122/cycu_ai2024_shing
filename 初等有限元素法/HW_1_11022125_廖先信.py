# 第一題
# a =  1*3*5*.....*(m-2)*m
# b = 1+3+5+...+(m-2)+m
# c = 1/1 + 1/3 + 1/5 + ..... + 1/m 
a = 1
b = 0
c = 0
m = 101

for i in range(0,(m+1)//2):
    a = a * (2*i+1)
    b = b + (2*i+1)
    c = c + 1/(2*i+1)
print(a)
print(b)
print(c)

# 第二題
for x in [0.1,0.25,0.66,0.99]:
    for m in [3,10,50,200,400]:
        d = 0
        for i in range(0,m):
            d = d + x**i
        print(d)      
for j in [0.10,0.25,0.66,0.99]:
    print(1/(1-j))

# 第三題

for n in [  5, 30, 100, 1000, 10000]:
    x = 0
    y = 0
    delta_x = 3/n
    for i in range(1,n+1):
        x = delta_x*0.5*i
        y = y + (x**2)*((x**3+1)**0.5)*delta_x
    print(y)

# 第四題
# 4-1
# 此程式碼為 一個 猜數字遊戲 
# 使用者有三次機會
# 數字範圍 1-10
import random

ans = random.randint(1,10) # 取亂數 1 - 10
i = 0 # 計算猜錯次數
while i!=3:
    guess = int(input("請輸入1-10的數字:"))  # 輸入數字
    # 利用 if else 判斷是否猜對
    # while 迴圈來判斷是否猜錯三次，若猜錯三次則印出答案並結束程式
    if guess == ans:
            print("恭喜你答對了") 
            break
    else:
        print("答錯了")
        i += 1
        if i == 3:
            print("答錯三次了")
            print("答案是",ans)
            

# 4-2
for i in range(1,101):
    if i % 2 !=0 and i % 3 != 0 and i % 5 != 0 and i % 7 != 0  and i % 7 != 0:
        print(i)

# 4-3
# 繪製圖表
import matplotlib.pyplot as plt
import numpy as np
# y = x  (紅色實線)
# y = x^2 (藍色虛線)
# y = x^3 (綠色點狀線)
# x軸範圍為0~20
x = np.arange(0, 20 )
y1 = x
y2 = x**2
y3 = x**3
plt.plot(x, y1, 'r-', x, y2, 'b--', x, y3, 'g.')
plt.show()


