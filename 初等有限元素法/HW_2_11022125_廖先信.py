import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, diff, lambdify, sin, pi

# --- 基本參數 ---
L, EI, q0 = 1, 1, 1
M0 = q0 * L**2 / pi**2
x = symbols('x')
x_plot = np.linspace(0, L, 300)

# --- 試函數與導數 ---
phi_syms = [x**2, x**3, x**4]
phi_derivatives = [[diff(p, x, n) for n in range(4)] for p in phi_syms]
phi_funcs_all = [[lambdify(x, d) for d in ds] for ds in phi_derivatives]

# --- 理論解 ---
w_exact = (q0 / (EI * pi**4)) * (np.sin(pi * x_plot) + pi * x_plot - pi * x_plot**3 / 6)

# --- 繪圖 ---
plt.figure(figsize=(14, 8))

for N in [1, 2, 3]:
    phi_funcs = phi_funcs_all[:N]

    # 剛性矩陣 K 和荷載向量 F
    K = np.zeros((N, N))
    F = np.zeros(N)

    for i in range(N):
        for j in range(N):
            integrand = phi_funcs[i][2](x_plot) * phi_funcs[j][2](x_plot)
            K[i, j] = EI * np.trapz(integrand, x_plot)

        qphi = q0 * np.sin(pi * x_plot / L) * phi_funcs[i][0](x_plot)
        F[i] = np.trapz(qphi, x_plot) + M0 * phi_funcs[i][1](L)

    a = np.linalg.solve(K, F)

    # 解出 w, θ, M, V
    w = sum(a[i] * phi_funcs[i][0](x_plot) for i in range(N))
    θ = sum(a[i] * phi_funcs[i][1](x_plot) for i in range(N))
    M = -EI * sum(a[i] * phi_funcs[i][2](x_plot) for i in range(N))
    V = -EI * sum(a[i] * phi_funcs[i][3](x_plot) for i in range(N))

    # 畫圖
    plt.subplot(2, 2, 1); plt.plot(x_plot, w, label=f"N={N}")
    plt.subplot(2, 2, 2); plt.plot(x_plot, θ, label=f"N={N}")
    plt.subplot(2, 2, 3); plt.plot(x_plot, M, label=f"N={N}")
    plt.subplot(2, 2, 4); plt.plot(x_plot, V, label=f"N={N}")

# 理論解 w(x)
plt.subplot(2, 2, 1)
plt.plot(x_plot, w_exact, 'k--', label="理論解")
plt.title("w(x) 位移"), plt.xlabel("x"), plt.ylabel("w(x)")
plt.legend()

# 子圖標題與圖例
titles = ["θ(x) 旋轉角", "M(x) 彎矩", "V(x) 剪力"]
ylabels = ["dw/dx", "M(x)", "V(x)"]

for i, title in enumerate(titles, start=2):
    plt.subplot(2, 2, i)
    plt.title(title)
    plt.xlabel("x"), plt.ylabel(ylabels[i - 2])
    plt.legend()

plt.tight_layout()
plt.show()
