def i(b,h):
    i = ((10**3*b/12) + b*10*(0.5*h + 5)**2 ) + 10*(h-20)**3
    return i


def I_H(a, b):
    # 各部分尺寸
    bf = a  # 翼緣寬度
    tf = 16   # 翼緣厚度
    hw = b   # 腹板高度（不含翼緣）
    tw = 10  # 腹板寬度（沿水平方向）

    # 全高（包含上下翼緣）
    H = 2 * tf + hw

    # 中性軸位置：以底部為基準
    y_centroid = tf + hw / 2

    # 翼緣慣性矩（平行軸定理）
    A_flange = bf * tf
    d_flange = abs(y_centroid - tf / 2)  # 上翼緣
    I_flange = 2 * ((1/12) * bf * tf**3 + A_flange * d_flange**2)

    # 腹板慣性矩（在中性軸上）
    I_web = (1/12) * tw * hw**3

    # 總慣性矩
    return I_flange + I_web
print(I_H(200, 468))
print(I_H(200, 218))
print(I_H(100, 468))
print(I_H(200, 268))
print(I_H(200, 968))