#第一題
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

#第二題
for x in [0.1,0.25,0.66,0.99]:
    for m in [3,10,50,200,400]:
        d = 0
        for i in range(0,m):
            d = d + x**i
        print(d)      
for j in [0.10,0.25,0.66,0.99]:
    print(1/(1-j))

#第三題

for n in [  5, 30, 100, 1000, 10000]:
    x = 0
    y = 0
    delta_x = 3/n
    for i in range(1,n+1):
        x = delta_x*0.5*i
        y = y + (x**2)*((x**3+1)**0.5)*delta_x
    print(y)
