import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, pi, sqrt
import os

# 創建輸出目錄
if not os.path.exists('output'):
    os.makedirs('output')

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

# 將矩陣轉換為LaTeX格式
def matrix_to_latex(matrix, name, precision=4):
    rows = []
    for row in matrix:
        if len(row.shape) > 0:  # 處理2D矩陣
            row_str = " & ".join([f"{x:.{precision}f}" for x in row])
        else:  # 處理1D向量
            row_str = f"{row:.{precision}f}"
        rows.append(row_str)
    
    if len(rows) > 1:
        content = " \\\\\n".join(rows)
        return f"\\mathbf{{{name}}} = \\begin{{bmatrix}}\n{content}\n\\end{{bmatrix}}"
    else:
        return f"\\mathbf{{{name}}} = \\begin{{bmatrix}}\n{rows[0]}\n\\end{{bmatrix}}"

def rel_error(fem, exact):
    fem = np.asarray(fem)
    exact = np.asarray(exact)
    # 避免除以零
    denom = np.where(np.abs(exact) > 1e-12, np.abs(exact), 1)
    return np.linalg.norm(fem - exact) / np.linalg.norm(denom)

def area_formula_latex(x1, y1, x2, y2, x3, y3, area):
    return (
        "\\[\n"
        "A = \\frac{1}{2} \\left|"
        f"({x1:.4f}({y2:.4f}-{y3:.4f}) + {x2:.4f}({y3:.4f}-{y1:.4f}) + {x3:.4f}({y1:.4f}-{y2:.4f}))"
        f"\\right| = {area:.4f}\n"
        "\\]"
    )

def main():
    all_latex = []
    all_errors = []
    all_element_errors = []  # 新增：儲存每個元素的相對誤差
    print("開始計算案例1...")
    def case1_capture():
        latex_output = []
        element_errors = []
        latex_output.append("\\section{Case 1: 4 identical sector elements (22.5 degrees)}")
        nodes = [(0, 0)]
        angles = [0, 22.5, 45, 67.5, 90]
        for angle in angles:
            theta = angle * pi / 180
            nodes.append((cos(theta), sin(theta)))
        elements = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 5)]
        plot_mesh(nodes, elements, "Case 1: 4 identical sector elements (22.5 degrees)", "case1_mesh")
        num_nodes = len(nodes)
        K = np.zeros((num_nodes, num_nodes))
        F = np.zeros(num_nodes)
        latex_output.append("\\subsection{Element stiffness matrices}")
        for i, (n1, n2, n3) in enumerate(elements):
            x1, y1 = nodes[n1]
            x2, y2 = nodes[n2]
            x3, y3 = nodes[n3]
            # 輸出元素面積公式與結果
            _, area = shape_function_derivatives(x1, y1, x2, y2, x3, y3)
            latex_output.append(f"Element {i+1} area formula and value:")
            latex_output.append(area_formula_latex(x1, y1, x2, y2, x3, y3, area))
            ke = element_stiffness_matrix(x1, y1, x2, y2, x3, y3)
            latex_output.append(f"Element {i+1} (nodes {n1}, {n2}, {n3}):")
            latex_output.append(matrix_to_latex(ke, f"k^{i+1}"))
            K[np.ix_([n1, n2, n3], [n1, n2, n3])] += ke
            fe = element_force_vector(x1, y1, x2, y2, x3, y3)
            F[[n1, n2, n3]] += fe
            # 計算元素中心的精確解與FEM解相對誤差
            cx = (x1 + x2 + x3) / 3
            cy = (y1 + y2 + y3) / 3
            exact = exact_solution(cx, cy)
            # FEM元素解用三個節點平均
            fem = 0
            try:
                fem = (U[n1] + U[n2] + U[n3]) / 3
            except:
                fem = 0
            relerr = abs(fem - exact) / (abs(exact) + 1e-12)
            element_errors.append(relerr)
        latex_output.append("\\subsection{Global stiffness matrix}")
        latex_output.append(matrix_to_latex(K, "K"))
        latex_output.append("\\subsection{Force vector}")
        latex_output.append(matrix_to_latex(F, "F"))
        boundary_nodes = [1, 2, 3, 4, 5]
        for node in boundary_nodes:
            K[node, :] = 0
            K[:, node] = 0
            K[node, node] = 1
            F[node] = 0
        latex_output.append("\\subsection{Global matrix after boundary conditions}")
        latex_output.append(matrix_to_latex(K, "K_{boundary}"))
        latex_output.append("\\subsection{Force vector after boundary conditions}")
        latex_output.append(matrix_to_latex(F, "F_{boundary}"))
        U = np.linalg.solve(K, F)
        latex_output.append("\\subsection{Nodal displacement solution}")
        latex_output.append("\\begin{tabular}{|c|c|c|c|c|c|c|}")
        latex_output.append("\\hline")
        latex_output.append("Node & x & y & FEM solution & Exact solution & Abs Rel Error & Percent Error (\\%) \\\\")
        latex_output.append("\\hline")
        exacts = []
        for i, (x, y) in enumerate(nodes):
            exact = exact_solution(x, y) if i != 0 else G_theta/2
            exacts.append(exact)
        errors = np.abs(U - np.array(exacts)) / (np.abs(exacts) + 1e-12)
        percent_errors = [(exact - fem) / (exact + 1e-12) * 100 if abs(exact) > 1e-12 else 0.0 for fem, exact in zip(U, exacts)]
        for i, (x, y) in enumerate(nodes):
            exact = exacts[i]
            abs_rel_error = errors[i]
            percent_error = percent_errors[i]
            latex_output.append(f"{i} & {x:.4f} & {y:.4f} & {U[i]:.6f} & {exact:.6f} & {abs_rel_error:.2e} & {percent_error:.2f} \\\\")
        latex_output.append("\\hline")
        latex_output.append("\\end{tabular}")
        l2err = rel_error(U, exacts)
        latex_output.append(f"\\textbf{{Relative $L^2$ error:}} {l2err:.4e}")
        return latex_output, l2err, element_errors
    case1_latex, case1_err, case1_elem_err = case1_capture()
    all_latex.extend(case1_latex)
    all_errors.append(case1_err)
    all_element_errors.append(case1_elem_err)
    print("案例1計算完成，圖片和LaTeX文件已保存")

    print("開始計算案例2...")
    def case2_capture():
        latex_output = []
        element_errors = []
        latex_output.append("\\section{Case 2: Midpoint connection of three sides (4 elements)}")
        nodes = [
            (0, 0),
            (1, 0),
            (0, 1),
            (0.5, 0),
            (0, 0.5),
            (sqrt(2)/2, sqrt(2)/2)
        ]
        elements = [
            (3, 4, 5),
            (0, 3, 4),
            (2, 4, 5),
            (3, 1, 5)
        ]
        plot_mesh(nodes, elements, "Case 2: Midpoint connection of three sides (4 elements)", "case2_mesh")
        num_nodes = len(nodes)
        K = np.zeros((num_nodes, num_nodes))
        F = np.zeros(num_nodes)
        latex_output.append("\\subsection{Element stiffness matrices}")
        for i, (n1, n2, n3) in enumerate(elements):
            x1, y1 = nodes[n1]
            x2, y2 = nodes[n2]
            x3, y3 = nodes[n3]
            _, area = shape_function_derivatives(x1, y1, x2, y2, x3, y3)
            latex_output.append(f"Element {i+1} area formula and value:")
            latex_output.append(area_formula_latex(x1, y1, x2, y2, x3, y3, area))
            ke = element_stiffness_matrix(x1, y1, x2, y2, x3, y3)
            latex_output.append(f"Element {i+1} (nodes {n1}, {n2}, {n3}):")
            latex_output.append(matrix_to_latex(ke, f"k^{i+1}"))
            K[np.ix_([n1, n2, n3], [n1, n2, n3])] += ke
            fe = element_force_vector(x1, y1, x2, y2, x3, y3)
            F[[n1, n2, n3]] += fe
        latex_output.append("\\subsection{Global stiffness matrix}")
        latex_output.append(matrix_to_latex(K, "K"))
        latex_output.append("\\subsection{Force vector}")
        latex_output.append(matrix_to_latex(F, "F"))
        boundary_nodes = [1, 2, 5]
        for node in boundary_nodes:
            K[node, :] = 0
            K[:, node] = 0
            K[node, node] = 1
            F[node] = 0
        latex_output.append("\\subsection{Global matrix after boundary conditions}")
        latex_output.append(matrix_to_latex(K, "K_{boundary}"))
        latex_output.append("\\subsection{Force vector after boundary conditions}")
        latex_output.append(matrix_to_latex(F, "F_{boundary}"))
        try:
            U = np.linalg.solve(K, F)
            latex_output.append("\\subsection{Nodal displacement solution}")
            latex_output.append("\\begin{tabular}{|c|c|c|c|c|c|c|}")
            latex_output.append("\\hline")
            latex_output.append("Node & x & y & FEM solution & Exact solution & Abs Rel Error & Percent Error (\\%) \\\\")
            latex_output.append("\\hline")
            exacts = []
            for i, (x, y) in enumerate(nodes):
                exact = exact_solution(x, y) if i != 0 else G_theta/2
                exacts.append(exact)
            errors = np.abs(U - np.array(exacts)) / (np.abs(exacts) + 1e-12)
            percent_errors = [(exact - fem) / (exact + 1e-12) * 100 if abs(exact) > 1e-12 else 0.0 for fem, exact in zip(U, exacts)]
            for i, (x, y) in enumerate(nodes):
                exact = exacts[i]
                abs_rel_error = errors[i]
                percent_error = percent_errors[i]
                latex_output.append(f"{i} & {x:.4f} & {y:.4f} & {U[i]:.6f} & {exact:.6f} & {abs_rel_error:.2e} & {percent_error:.2f} \\\\")
            latex_output.append("\\hline")
            latex_output.append("\\end{tabular}")
            l2err = rel_error(U, exacts)
            latex_output.append(f"\\textbf{{Relative $L^2$ error:}} {l2err:.4e}")
            return latex_output, l2err, element_errors
        except np.linalg.LinAlgError:
            latex_output.append("\\textbf{Error: Singular matrix, cannot solve for nodal displacements.}")
            return latex_output, None, []
    case2_latex, case2_err, case2_elem_err = case2_capture()
    all_latex.extend(case2_latex)
    all_errors.append(case2_err)
    all_element_errors.append(case2_elem_err)
    print("案例2計算完成，圖片和LaTeX文件已保存")

    print("開始計算案例3...")
    def case3_capture():
        latex_output = []
        element_errors = []
        latex_output.append("\\section{Case 3: 5 identical sector elements (18 degrees)}")
        nodes = [(0, 0)]
        angles = [0, 18, 36, 54, 72, 90]
        for angle in angles:
            theta = angle * pi / 180
            nodes.append((cos(theta), sin(theta)))
        elements = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 5), (0, 5, 6)]
        plot_mesh(nodes, elements, "Case 3: 5 identical sector elements (18 degrees)", "case3_mesh")
        num_nodes = len(nodes)
        K = np.zeros((num_nodes, num_nodes))
        F = np.zeros(num_nodes)
        latex_output.append("\\subsection{Element stiffness matrices}")
        for i, (n1, n2, n3) in enumerate(elements):
            x1, y1 = nodes[n1]
            x2, y2 = nodes[n2]
            x3, y3 = nodes[n3]
            _, area = shape_function_derivatives(x1, y1, x2, y2, x3, y3)
            latex_output.append(f"Element {i+1} area formula and value:")
            latex_output.append(area_formula_latex(x1, y1, x2, y2, x3, y3, area))
            ke = element_stiffness_matrix(x1, y1, x2, y2, x3, y3)
            latex_output.append(f"Element {i+1} (nodes {n1}, {n2}, {n3}):")
            latex_output.append(matrix_to_latex(ke, f"k^{i+1}"))
            K[np.ix_([n1, n2, n3], [n1, n2, n3])] += ke
            fe = element_force_vector(x1, y1, x2, y2, x3, y3)
            F[[n1, n2, n3]] += fe
        latex_output.append("\\subsection{Global stiffness matrix}")
        latex_output.append(matrix_to_latex(K, "K"))
        latex_output.append("\\subsection{Force vector}")
        latex_output.append(matrix_to_latex(F, "F"))
        boundary_nodes = list(range(1, 7))
        for node in boundary_nodes:
            K[node, :] = 0
            K[:, node] = 0
            K[node, node] = 1
            F[node] = 0
        latex_output.append("\\subsection{Global matrix after boundary conditions}")
        latex_output.append(matrix_to_latex(K, "K_{boundary}"))
        latex_output.append("\\subsection{Force vector after boundary conditions}")
        latex_output.append(matrix_to_latex(F, "F_{boundary}"))
        U = np.linalg.solve(K, F)
        latex_output.append("\\subsection{Nodal displacement solution}")
        latex_output.append("\\begin{tabular}{|c|c|c|c|c|c|c|}")
        latex_output.append("\\hline")
        latex_output.append("Node & x & y & FEM solution & Exact solution & Abs Rel Error & Percent Error (\\%) \\\\")
        latex_output.append("\\hline")
        exacts = []
        for i, (x, y) in enumerate(nodes):
            exact = exact_solution(x, y) if i != 0 else G_theta/2
            exacts.append(exact)
        errors = np.abs(U - np.array(exacts)) / (np.abs(exacts) + 1e-12)
        percent_errors = [(exact - fem) / (exact + 1e-12) * 100 if abs(exact) > 1e-12 else 0.0 for fem, exact in zip(U, exacts)]
        for i, (x, y) in enumerate(nodes):
            exact = exacts[i]
            abs_rel_error = errors[i]
            percent_error = percent_errors[i]
            latex_output.append(f"{i} & {x:.4f} & {y:.4f} & {U[i]:.6f} & {exact:.6f} & {abs_rel_error:.2e} & {percent_error:.2f} \\\\")
        latex_output.append("\\hline")
        latex_output.append("\\end{tabular}")
        l2err = rel_error(U, exacts)
        latex_output.append(f"\\textbf{{Relative $L^2$ error:}} {l2err:.4e}")
        return latex_output, l2err, element_errors
    case3_latex, case3_err, case3_elem_err = case3_capture()
    all_latex.extend(case3_latex)
    all_errors.append(case3_err)
    all_element_errors.append(case3_elem_err)
    print("案例3計算完成，圖片和LaTeX文件已保存")

    # 輸出精確解與三個CASE的相對誤差（表格方式）
    all_latex.append("\\section{Summary of Relative $L^2$ Errors}")
    all_latex.append("\\begin{table}[h!]")
    all_latex.append("\\centering")
    all_latex.append("\\begin{tabular}{|c|c|}")
    all_latex.append("\\hline")
    all_latex.append("Case & Relative $L^2$ Error \\\\")
    all_latex.append("\\hline")
    all_latex.append(f"Case 1 & {all_errors[0]:.4e} \\\\")
    all_latex.append(f"Case 2 & {all_errors[1] if all_errors[1] is not None else 'N/A'} \\\\")
    all_latex.append(f"Case 3 & {all_errors[2]:.4e} \\\\")
    all_latex.append("\\hline")
    all_latex.append("\\end{tabular}")
    all_latex.append("\\caption{Relative $L^2$ error for each case compared to the exact solution.}")
    all_latex.append("\\end{table}")

    # 輸出每個元素的相對誤差表格
    all_latex.append("\\section{Element-wise Relative Errors}")
    all_latex.append("\\begin{table}[h!]")
    all_latex.append("\\centering")
    all_latex.append("\\begin{tabular}{|c|c|c|}")
    all_latex.append("\\hline")
    all_latex.append("Case & Element & Relative Error \\\\")
    all_latex.append("\\hline")
    for case_idx, elem_errs in enumerate(all_element_errors, 1):
        for elem_idx, err in enumerate(elem_errs, 1):
            all_latex.append(f"Case {case_idx} & {elem_idx} & {err:.4e} \\\\")
            print(f"Case {case_idx} Element {elem_idx} Relative Error: {err:.4e}")  # 已有CASE 1
    # 額外列印CASE 2與CASE 3所有元素誤差
    print("\n--- CASE 2 Element Relative Errors ---")
    for elem_idx, err in enumerate(all_element_errors[1], 1):
        print(f"Case 2 Element {elem_idx} Relative Error: {err:.4e}")
    print("\n--- CASE 3 Element Relative Errors ---")
    for elem_idx, err in enumerate(all_element_errors[2], 1):
        print(f"Case 3 Element {elem_idx} Relative Error: {err:.4e}")
    all_latex.append("\\hline")
    all_latex.append("\\end{tabular}")
    all_latex.append("\\caption{Element-wise relative error (center value) for each case.}")
    all_latex.append("\\end{table}")

    with open('output/all_cases.tex', 'w') as f:
        f.write('\n'.join(all_latex))

    print("所有案例計算完成，LaTeX文件已保存")
    print("所有計算完成！結果保存在output目錄中")

if __name__ == "__main__":
    main()
