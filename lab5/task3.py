import math
import numpy as np 
import sympy
import matplotlib.pyplot as plt

def main():
    N = int(input("Введите N: "))
    if N < 2:
        print("Некорректное число точек.")
        return
    xstep = 1 / N
    ystep = 2 / N
    vars = []
    equations = []
    initvals = []
    x = []
    for i in range(N + 1):
        vars.append(f"y{i}")
        if i == 0:
            equations.append("y0 - 1.0")
            initvals.append(1.0)
            x.append(0.0)
        elif i == N:
            equations.append(f"y{i} - 3.0")
            initvals.append(3.0)
            x.append(1.0)
        else:
            equations.append(f"y{i-1} - 2 * y{i} + y{i+1} - {xstep ** 2} * (y{i} ** 3) - {xstep ** 2} * {(xstep * i) ** 2}")
            initvals.append(1.0 + ystep * i)
            x.append(xstep * i)
    y = newton(vars, equations, initvals)
    plt.grid()
    plt.plot(x, initvals, label = "Init values")
    plt.plot(x, y, label = "Result values")
    plt.legend()
    plt.show()

def newton(vrs, eqs, initvals):
    f = sympy.Matrix(eqs)
    f = sympy.lambdify(sympy.symbols(vrs), f)
    W = sympy.Matrix(eqs).jacobian(vrs)
    W = sympy.lambdify(sympy.symbols(vrs), W)
    xp = initvals.copy()
    kmax = 100
    k = 0
    while True:
        xc = np.linalg.solve(W(*xp), f(*xp)).reshape([len(vrs),]).tolist()
        k += 1
        if k >= kmax:
            break
        for i in range(len(xp)):
            xp[i] -= xc[i]
        if np.linalg.norm(xc) > 1e-7:
            pass
        else:
            break
    return xp

if __name__ == "__main__":
    main()