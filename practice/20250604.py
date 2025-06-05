# 繪製網格
def plot_mesh(nodes, elements, title, filename):
    plt.figure(figsize=(8, 8))
    plt.title(title, fontsize=14)
    
    # 繪製元素
    for i, (n1, n2, n3) in enumerate(elements):
        x = [nodes[n1][0], nodes[n2][0], nodes[n3][0], nodes[n1][0]]
        y = [nodes[n1][1], nodes[n2][1], nodes[n3][1], nodes[n1][1]]
        plt.fill(x, y, alpha=0.3)
        plt.plot(x, y, 'b-')
        
        # 標記元素中心
        cx = sum(x[:3])/3
        cy = sum(y[:3])/3
        plt.text(cx, cy, f'E{i+1}', fontsize=12, ha='center', va='center')
    
    # 繪製節點並標記
    for i, (x, y) in enumerate(nodes):
        plt.plot(x, y, 'ro', markersize=8)
        plt.text(x+0.03, y+0.03, f'N{i}', fontsize=12)
    
    # 繪製圓弧
    theta = np.linspace(0, pi/2, 100)
    x_circle = np.cos(theta)
    y_circle = np.sin(theta)
    plt.plot(x_circle, y_circle, 'k-')
    
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 1.1)
    plt.xlabel('X', fontsize=12)
    plt.ylabel('Y', fontsize=12)
    plt.grid(True)
    plt.axis('equal')
    plt.savefig(f'output/{filename}.png', dpi=300)
    plt.close()
