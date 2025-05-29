import numpy as np
from math import cos, sin, pi, sqrt

# 材料參數
G_theta = 5  # 2Gθ = 10
a = b = 1    # 圓的半徑

# 精確解
def exact_solution(x, y):
    return (G_theta/2) * (1 - x**2 - y**2)

# 線性三角形元素的形狀函數導數
def shape_function_derivatives(x1, y1, x2, y2, x3, y3):
    """計算形狀函數導數和元素面積"""
    A = np.array([[1, x1, y1],
                  [1, x2, y2],
                  [1, x3, y3]])
    area = 0.5 * np.linalg.det(A)
    
    a1 = x2*y3 - x3*y2
    a2 = x3*y1 - x1*y3
    a3 = x1*y2 - x2*y1
    
    b1 = y2 - y3
    b2 = y3 - y1
    b3 = y1 - y2
    
    c1 = x3 - x2
    c2 = x1 - x3
    c3 = x2 - x1
    
    dN1dx = b1 / (2*area)
    dN2dx = b2 / (2*area)
    dN3dx = b3 / (2*area)
    
    dN1dy = c1 / (2*area)
    dN2dy = c2 / (2*area)
    dN3dy = c3 / (2*area)
    
    B = np.array([[dN1dx, dN2dx, dN3dx],
                  [dN1dy, dN2dy, dN3dy]])
    
    return B, area

# 計算元素剛性矩陣
def element_stiffness_matrix(x1, y1, x2, y2, x3, y3):
    B, area = shape_function_derivatives(x1, y1, x2, y2, x3, y3)
    ke = np.dot(B.T, B) * area
    return ke

# 計算元素力向量
def element_force_vector(x1, y1, x2, y2, x3, y3):
    _, area = shape_function_derivatives(x1, y1, x2, y2, x3, y3)
    fe = (10 * area / 3) * np.ones(3)  # 10 = 2Gθ
    return fe

# 1. 4個相同扇形元素 (22.5度)
def case1():
    print("\nCase 1: 4個相同扇形元素 (22.5度)\n")
    # 創建節點 (圓心和5個圓周點)
    nodes = [(0, 0)]  # 圓心
    angles = [0, 22.5, 45, 67.5, 90]
    for angle in angles:
        theta = angle * pi / 180
        nodes.append((cos(theta), sin(theta)))
    elements = [(0, 1, 2), 
                (0, 2, 3), 
                (0, 3, 4), 
                (0, 4, 5)]
    num_nodes = len(nodes)
    K = np.zeros((num_nodes, num_nodes))
    for i, (n1, n2, n3) in enumerate(elements):
        x1, y1 = nodes[n1]
        x2, y2 = nodes[n2]
        x3, y3 = nodes[n3]
        ke = element_stiffness_matrix(x1, y1, x2, y2, x3, y3)
        print(f"元素 {i+1} 的剛性矩陣:")
        print(ke)
        print()
        K[np.ix_([n1, n2, n3], [n1, n2, n3])] += ke
    print("全局剛性矩陣:")
    print(K)

# 2. 三邊中點連線 (4個元素)
def case2():
    print("\nCase 2: 三邊中點連線 (4個元素)\n")
    
    # 創建節點 (圓心、軸端點、中點和45度點)
    nodes = [(0, 0),          # 0 - 圓心
             (1, 0),          # 1 - x軸端點
             (0, 1),          # 2 - y軸端點
             (0.5, 0),        # 3 - 邊0-1中點
             (0.5, 0.5),      # 4 - 邊0-2中點
             (0, 0.5),        # 5 - 邊1-2中點
             (sqrt(2)/2, sqrt(2)/2)]  # 6 - 45度圓周點
    
    # 元素連接性
    elements = [(0, 3, 4),    # 元素1
                (3, 1, 6),    # 元素2
                (4, 6, 2),    # 元素3
                (3, 4, 6)]    # 元素4
    
    # 初始化全局剛性矩陣和力向量
    num_nodes = len(nodes)
    K = np.zeros((num_nodes, num_nodes))
    
    # 計算每個元素的貢獻
    for i, (n1, n2, n3) in enumerate(elements):
        x1, y1 = nodes[n1]
        x2, y2 = nodes[n2]
        x3, y3 = nodes[n3]
        
        # 計算元素剛性矩陣
        ke = element_stiffness_matrix(x1, y1, x2, y2, x3, y3)
        print(f"元素 {i+1} 的剛性矩陣:")
        print(ke)
        print()
        
        # 組裝到全局矩陣
        K[np.ix_([n1, n2, n3], [n1, n2, n3])] += ke
    
    # 輸出結果
    print("全局剛性矩陣:")
    print(K)

# 3. 5個相同扇形元素 (18度)
def case3():
    print("\nCase 3: 5個相同扇形元素 (18度)\n")
    # 創建節點 (圓心和6個圓周點)
    nodes = [(0, 0)]  # 圓心
    angles = [0, 18, 36, 54, 72, 90]
    for angle in angles:
        theta = angle * pi / 180
        nodes.append((cos(theta), sin(theta)))
    elements = [(0, 1, 2), 
                (0, 2, 3), 
                (0, 3, 4), 
                (0, 4, 5),
                (0, 5, 6)]
    num_nodes = len(nodes)
    K = np.zeros((num_nodes, num_nodes))
    for i, (n1, n2, n3) in enumerate(elements):
        x1, y1 = nodes[n1]
        x2, y2 = nodes[n2]
        x3, y3 = nodes[n3]
        ke = element_stiffness_matrix(x1, y1, x2, y2, x3, y3)
        print(f"元素 {i+1} 的剛性矩陣:")
        print(ke)
        print()
        K[np.ix_([n1, n2, n3], [n1, n2, n3])] += ke
    print("全局剛性矩陣:")
    print(K)
   

# 執行所有案例
case1()
case2()
case3()

# 將所有矩陣輸出成 pdf 檔案
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def matrix_to_str(mat):
    return '\n'.join(['\t'.join([f"{v:10.4f}" for v in row]) for row in mat])

def export_matrices_to_pdf():
    pdf_path = r'C:\Users\User\OneDrive\桌面\學業\matrices_output.pdf'
    with PdfPages(pdf_path) as pdf:
        # Case 1
        fig, ax = plt.subplots(figsize=(12, 16))
        ax.axis('off')
        ax.set_title('Case 1: Global Stiffness Matrix', fontsize=14, loc='left')
        nodes = [(0, 0)]
        angles = [0, 22.5, 45, 67.5, 90]
        for angle in angles:
            theta = angle * pi / 180
            nodes.append((cos(theta), sin(theta)))
        elements = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 5)]
        num_nodes = len(nodes)
        K1 = np.zeros((num_nodes, num_nodes))
        y = 0.98
        for idx, (n1, n2, n3) in enumerate(elements):
            x1, y1_ = nodes[n1]
            x2, y2_ = nodes[n2]
            x3, y3_ = nodes[n3]
            ke = element_stiffness_matrix(x1, y1_, x2, y2_, x3, y3_)
            ax.text(0.01, y, f"Element {idx+1}:\n{matrix_to_str(ke)}", fontsize=9, family='monospace', va='top', ha='left', wrap=True, transform=ax.transAxes)
            y -= 0.13
            K1[np.ix_([n1, n2, n3], [n1, n2, n3])] += ke
        ax.text(0.01, y-0.08, "Global stiffness matrix:\n" + matrix_to_str(K1), fontsize=9, family='monospace', va='top', ha='left', wrap=True, transform=ax.transAxes)
        pdf.savefig(fig)
        plt.close(fig)

        # Case 2
        fig, ax = plt.subplots(figsize=(12, 16))
        ax.axis('off')
        ax.set_title('Case 2: Global Stiffness Matrix', fontsize=14, loc='left')
        nodes = [(0, 0), (1, 0), (0, 1), (0.5, 0), (0.5, 0.5), (0, 0.5), (sqrt(2)/2, sqrt(2)/2)]
        elements = [(0, 3, 4), (3, 1, 6), (4, 6, 2), (3, 4, 6)]
        num_nodes = len(nodes)
        K2 = np.zeros((num_nodes, num_nodes))
        y = 0.98
        for idx, (n1, n2, n3) in enumerate(elements):
            x1, y1_ = nodes[n1]
            x2, y2_ = nodes[n2]
            x3, y3_ = nodes[n3]
            ke = element_stiffness_matrix(x1, y1_, x2, y2_, x3, y3_)
            ax.text(0.01, y, f"Element {idx+1}:\n{matrix_to_str(ke)}", fontsize=9, family='monospace', va='top', ha='left', wrap=True, transform=ax.transAxes)
            y -= 0.13
            K2[np.ix_([n1, n2, n3], [n1, n2, n3])] += ke
        ax.text(0.01, y-0.08, "Global stiffness matrix:\n" + matrix_to_str(K2), fontsize=9, family='monospace', va='top', ha='left', wrap=True, transform=ax.transAxes)
        pdf.savefig(fig)
        plt.close(fig)

        # Case 3
        fig, ax = plt.subplots(figsize=(12, 16))
        ax.axis('off')
        ax.set_title('Case 3: Global Stiffness Matrix', fontsize=14, loc='left')
        nodes = [(0, 0)]
        angles = [0, 18, 36, 54, 72, 90]
        for angle in angles:
            theta = angle * pi / 180
            nodes.append((cos(theta), sin(theta)))
        elements = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 5), (0, 5, 6)]
        num_nodes = len(nodes)
        K3 = np.zeros((num_nodes, num_nodes))
        y = 0.98
        for idx, (n1, n2, n3) in enumerate(elements):
            x1, y1_ = nodes[n1]
            x2, y2_ = nodes[n2]
            x3, y3_ = nodes[n3]
            ke = element_stiffness_matrix(x1, y1_, x2, y2_, x3, y3_)
            ax.text(0.01, y, f"Element {idx+1}:\n{matrix_to_str(ke)}", fontsize=9, family='monospace', va='top', ha='left', wrap=True, transform=ax.transAxes)
            y -= 0.13
            K3[np.ix_([n1, n2, n3], [n1, n2, n3])] += ke
        ax.text(0.01, y-0.08, "Global stiffness matrix:\n" + matrix_to_str(K3), fontsize=9, family='monospace', va='top', ha='left', wrap=True, transform=ax.transAxes)
        pdf.savefig(fig)
        plt.close(fig)

export_matrices_to_pdf()