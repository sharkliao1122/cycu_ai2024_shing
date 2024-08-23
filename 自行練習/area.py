def area(shape,n):
    if shape == 'circle':
        return 3.14*n**2
    elif shape == 'square':
        return n**2
    else:
        return '無法計算'